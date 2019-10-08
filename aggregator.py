import page_element as pg_chk
import util
import cv2
import itertools



class Aggregator:
    # Aggregate page elements and text chunks

    def __init__(self, page_elements, text_chunks):
        self.page_elements = self.find_container(page_elements, text_chunks)

    def find_container(self, containers, chunks):
        page_chunks = []
        for container in containers:
            text_children = []
            for chunk in chunks:
                if container.is_container(chunk):
                    text_children.append(chunk)

            page_chunks.append(pg_chk.PageElement(container, text_children))
        return self.sort_children(page_chunks)

    def draw_stuff(self, img):
        for element in self.page_elements:
            util.draw_chunk_box(img, (element.container.x0, element.container.x1),
                                (element.container.y0, element.container.y1), color=util.rgb_to_bgr((150, 139, 116)))
            for text in element.children:
                cv2.circle(img, (int(text.xc), int(text.yc)), 3, color=util.rgb_to_bgr((150, 139, 116)))
                util.draw_chunk_box(img, (int(text.x0), int(text.x1)),
                                    (int(text.y0), int(text.y1)), color=util.rgb_to_bgr((255, 181, 22)))
        return img

    @staticmethod
    def sort_children(page_chunks):
        tmp = sorted(page_chunks, key=lambda page_element: page_element.yc)
        y_group = itertools.groupby(tmp, key=lambda page_element: page_element.yc)

        sorted_page_elements = []
        for key, group in y_group:
            sorted_x = sorted(group, key=lambda page_element: page_element.xc)
            for box in sorted_x:
                sorted_page_elements.append(box)
        return sorted_page_elements
