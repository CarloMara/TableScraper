import cv2
from .projection_sampling import horizontal_projection, hysteresis_thresholding, vertical_projection
from .util import draw_dots_for_list_horizontal, draw_dots_from_list, rgb_to_bgr, draw_chunk_line, draw_chunk_box
from .heat_box import HeatBox


def draw_dots(cimg, img, height_threshold):
    (H, W) = img.shape[:2]
    edges = cv2.Canny(cimg, 275, 500, apertureSize=3)
    y_projection = horizontal_projection(edges, 0, W, 0, H)
    draw_dots_for_list_horizontal(img, y_projection, H, color=rgb_to_bgr((144, 89, 47)))
    # find vertical chunks
    y_chunks = hysteresis_thresholding(y_projection)
    for y_tuple in y_chunks:
        if y_tuple[1]-y_tuple[0] > height_threshold:
            x_projection = vertical_projection(edges, y_tuple[0], y_tuple[1])
            draw_dots_from_list(img, x_projection, y_tuple[1] - y_tuple[0], y_tuple[0],
                                     color=rgb_to_bgr((150, 139, 116)))


def draw_chunks_line(cimg, img, height_threshold):
    (H, W) = img.shape[:2]
    edges = cv2.Canny(cimg, 275, 500, apertureSize=3)
    y_projection = horizontal_projection(edges, 0, W, 0, H)
    y_chunks = hysteresis_thresholding(y_projection)
    for y_tuple in y_chunks:
        if y_tuple[1] - y_tuple[0] > height_threshold:
            draw_chunk_line(img, y_tuple, W)


def draw_chunks_box(cimg, img, height_threshold, width_threshold):
    (H, W) = img.shape[:2]
    edges = cv2.Canny(cimg, 275, 500, apertureSize=3)
    y_projection = horizontal_projection(edges, 0, W, 0, H)
    y_chunks = hysteresis_thresholding(y_projection)
    for y_tuple in y_chunks:
        if y_tuple[1]-y_tuple[0] > height_threshold:
            x_projection = vertical_projection(edges, y_tuple[0], y_tuple[1])
            x_chunks = hysteresis_thresholding(x_projection)
            for x_tuple in x_chunks:
                if x_tuple[1] - x_tuple[0] > width_threshold:
                    draw_chunk_box(img, x_tuple, y_tuple, color=rgb_to_bgr((255,181,22)))


def boxes_from_img(img, height_threshold, width_threshold):
    (H, W) = img.shape[:2]
    edges = cv2.Canny(img, 275, 500, apertureSize=3)

    y_projection = horizontal_projection(edges, 0, W, 0, H)

    box_coordinates = []

    # find vertical chunks
    y_chunks = hysteresis_thresholding(y_projection)

    for y_tuple in y_chunks:

        # analyze only big chunks
        if y_tuple[1]-y_tuple[0] > height_threshold:
            x_projection = vertical_projection(edges, y_tuple[0], y_tuple[1])

            # find horizontal chunks
            x_chunks = hysteresis_thresholding(x_projection)

            for x_tuple in x_chunks:
                if x_tuple[1] - x_tuple[0] > width_threshold:
                    box_coordinates.append(HeatBox(x_tuple[0], x_tuple[1], y_tuple[0], y_tuple[1]))

    return box_coordinates
