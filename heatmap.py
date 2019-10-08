import numpy as np
import cv2
import projection_sampling as sample
import util
import heat_box as hb
import text_box as box
from IPython import embed


def heat_map(img, height_threshold, draw_dots=False, draw_boxes=False, draw_chunks=False):
    # this function does a shit ton of things, and needs braking down
    # analysis need to be separated from visualization
    # most analysis are already separated
    (H, W) = img.shape[:2]
    edges = cv2.Canny(img, 275, 500, apertureSize=3)

    y_projection = sample.horizontal_projection(edges, 0, W, 0, H)

    box_coordinates = []

    if draw_dots:
        util.draw_dots_for_list_horizontal(img, y_projection, H)

    # find vertical chunks
    y_chunks = sample.hysteresis_thresholding(y_projection)

    for y_tuple in y_chunks:
        if draw_chunks:
            util.draw_chunk_line(img, y_tuple, W)

        # analyze only big chunks
        if y_tuple[1]-y_tuple[0] > height_threshold:
            x_projection = sample.vertical_projection(edges, y_tuple[0], y_tuple[1])

            if draw_dots:
                util.draw_dots_from_list_vertical(img, x_projection, y_tuple[1] - y_tuple[0], y_tuple[0])

            # find horizontal chunks
            x_chunks = sample.hysteresis_thresholding(x_projection)

            for x_tuple in x_chunks:
                # FIXME: add second thresholding step to futher reduce the size of vertical chunks
                if draw_boxes:
                    util.draw_chunk_box(img, x_tuple, y_tuple)
                # x0, x1, y0, y1
                box_coordinates.append((x_tuple[0], x_tuple[1], y_tuple[0], y_tuple[1]))
    return img, box_coordinates


def draw_dots(cimg, img, height_threshold):
    (H, W) = img.shape[:2]
    edges = cv2.Canny(cimg, 275, 500, apertureSize=3)
    y_projection = sample.horizontal_projection(edges, 0, W, 0, H)
    util.draw_dots_for_list_horizontal(img, y_projection, H, color=util.rgb_to_bgr((144, 89, 47)))
    # find vertical chunks
    y_chunks = sample.hysteresis_thresholding(y_projection)
    for y_tuple in y_chunks:
        if y_tuple[1]-y_tuple[0] > height_threshold:
            x_projection = sample.vertical_projection(edges, y_tuple[0], y_tuple[1])
            util.draw_dots_from_list(img, x_projection, y_tuple[1] - y_tuple[0], y_tuple[0],
                                     color=util.rgb_to_bgr((150, 139, 116)))


def draw_chunks_line(cimg, img, height_threshold):
    (H, W) = img.shape[:2]
    edges = cv2.Canny(cimg, 275, 500, apertureSize=3)
    y_projection = sample.horizontal_projection(edges, 0, W, 0, H)
    y_chunks = sample.hysteresis_thresholding(y_projection)
    for y_tuple in y_chunks:
        if y_tuple[1] - y_tuple[0] > height_threshold:
            util.draw_chunk_line(img, y_tuple, W)


def draw_chunks_box(cimg, img, height_threshold, width_threshold):
    (H, W) = img.shape[:2]
    edges = cv2.Canny(cimg, 275, 500, apertureSize=3)
    y_projection = sample.horizontal_projection(edges, 0, W, 0, H)
    y_chunks = sample.hysteresis_thresholding(y_projection)
    for y_tuple in y_chunks:
        if y_tuple[1]-y_tuple[0] > height_threshold:
            x_projection = sample.vertical_projection(edges, y_tuple[0], y_tuple[1])
            x_chunks = sample.hysteresis_thresholding(x_projection)
            for x_tuple in x_chunks:
                if x_tuple[1] - x_tuple[0] > width_threshold:
                    util.draw_chunk_box(img, x_tuple, y_tuple, color=util.rgb_to_bgr((255,181,22)))


def boxes_from_img(img, height_threshold, width_threshold):
    (H, W) = img.shape[:2]
    edges = cv2.Canny(img, 275, 500, apertureSize=3)

    y_projection = sample.horizontal_projection(edges, 0, W, 0, H)

    box_coordinates = []

    # find vertical chunks
    y_chunks = sample.hysteresis_thresholding(y_projection)

    for y_tuple in y_chunks:

        # analyze only big chunks
        if y_tuple[1]-y_tuple[0] > height_threshold:
            x_projection = sample.vertical_projection(edges, y_tuple[0], y_tuple[1])

            # find horizontal chunks
            x_chunks = sample.hysteresis_thresholding(x_projection)

            for x_tuple in x_chunks:
                if x_tuple[1] - x_tuple[0] > width_threshold:
                    box_coordinates.append(hb.HeatBox(x_tuple[0], x_tuple[1], y_tuple[0], y_tuple[1]))

    return box_coordinates
