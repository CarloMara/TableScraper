import numpy as np
import cv2


def vertical_projection(img, chunkS, chunkE):
    "Return a list containing the sum of the pixels in each column"
    (h, w) = img.shape[:2]
    sum_cols = []
    for j in range(w):
        col = img[chunkS:chunkE, j:j+1] # y1:y2, x1:x2
        # print(col)
        # embed()
        sum_cols.append(np.count_nonzero(col == 255))
    # embed()
    return sum_cols


def horizontal_projection(img, chunkS, chunkE, rowS, rowE):
    "Return a list containing the sum of the pixels in each column"
    (h, w) = img.shape[:2]
    sum_row = []
    for j in range(rowS, rowE):
        # print(j)
        row = img[j:j+1, chunkS:chunkE] # y1:y2, x1:x2
        sum_row.append(np.count_nonzero(row == 255))
    # embed()
    return sum_row


def hysteresis_thresholding(samples):
    # find vertical spaces between text
    chunks = []

    data = [True, 0, 0]
    last = 0

    for i in range(len(samples)):

        # if horz[i] == 0:
        #     cv2.line(img, (0, i), (W, i), (0, 255, 255), 1)
        # chunk detection routine
        if samples[i] != 0 and data[0]:
            data[1] = i
            data[0] = False
        if samples[i] == 0 and (data[0] == False):
            data[2] = i
            data[0] = True
            chunks.append((data[1], data[2]))
    return chunks


