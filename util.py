import cv2


def draw_dots_for_list_horizontal(img, list, scale, color=(0,0,0)):
    for i in range(len(list)):
        cv2.circle(img, ((list[i] * scale) // max(list), i), 1, color)


def draw_dots_from_list(img, list, scale, offset, color=(0, 0, 0)):
    for k in range(len(list)):
        cv2.circle(img, (k, (list[k] * scale) // max(list) + offset), 1, color)


def draw_chunk_line(img, i, width):
    cv2.line(img, (0, i[0]), (width, i[0]), (255, 0, 255), 1)
    cv2.line(img, (0, i[1]), (width, i[1]), (255, 0, 255), 1)


def draw_chunk_box(img, x_tuple, y_tuple, color=(255, 0, 255)):
    cv2.line(img, (x_tuple[0], y_tuple[0]), (x_tuple[0], y_tuple[1]), color, 1)
    cv2.line(img, (x_tuple[1], y_tuple[0]), (x_tuple[1], y_tuple[1]), color, 1)
    cv2.line(img, (x_tuple[0], y_tuple[0]), (x_tuple[1], y_tuple[0]), color, 1)
    cv2.line(img, (x_tuple[0], y_tuple[1]), (x_tuple[1], y_tuple[1]), color, 1)


def rgb_to_bgr(colors):
    return colors[2], colors[1], colors[0]


def is_container(container, chunk):
    if container[0] <= chunk[0] <= container[1] and container[0] <= chunk[1] <= container[1] and container[2] <= chunk[2] <= container[3] and container[2] <= chunk[3] <= container[3]:
        return True
    else:
        return False


def find_header_or_title(text_chunks, header_size=28, title_size=21, mnemonics_size=14):
    titles = []
    mnemonics = []
    for i in text_chunks:
        if header_size - 1 < (i.y0 - i.y1) < header_size + 1:
            titles.append(i)
        if title_size - 1 < (i.y0 - i.y1) < title_size + 1:
            titles.append(i)
        if mnemonics_size - 1 < (i.y0 - i.y1) < mnemonics_size + 1:
            mnemonics.append(i)
    return titles, mnemonics


def print_start_chunks(chunks):
    for i in chunks:
        print("Name: " + str(i[0]).strip('\n'))
        print("    Y0: " + str(i[1][0]).strip('\n') + "   Y1: " + str(i[1][1]).strip('\n'))
        print("Mnemonic: " + str(i[2]).strip('\n'))
        print("Operands: " + str(i[3]).strip('\n'))
        print("\n")
