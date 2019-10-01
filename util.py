import cv2


def draw_dots_for_list_horizontal(img, list, scale):
    for i in range(len(list)):
        cv2.circle(img, ((list[i] * scale) // max(list), i), 1, (255, 0, 0))


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
