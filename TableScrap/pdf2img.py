import os
import cv2


class PdfImageExtractor:

    def __init__(self, path, W, H):
        self.path = path
        self.W = W
        self.H = H

    def get_page(self, pageno):
        # print(pageno)
        cmd = "convert -density 150 -background white -alpha remove \"" + self.path + "[" + str(pageno-1) + "]" + \
              "\" -quality 90 -colorspace RGB page.png"
        os.system(cmd)

        img = cv2.imread('./page.png')
        img = cv2.resize(img, (self.W, self.H))

        return img
