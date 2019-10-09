import cv2
from .page_element import PageElement
from .util import find_header_and_mnemonic, draw_chunk_box, rgb_to_bgr
import itertools
from .instruction_box import InstructionBox


class Aggregator:
    # Aggregate page elements and text chunks

    def __init__(self, page_elements, text_chunks):
        self.page_elements = self.find_container(page_elements, text_chunks)
        self.titles, self.mnemonics = find_header_and_mnemonic(text_chunks)

    def find_container(self, containers, chunks):
        page_chunks = []
        for container in containers:
            text_children = []
            for chunk in chunks:
                if container.is_container(chunk):
                    text_children.append(chunk)

            page_chunks.append(PageElement(container, text_children))
        return self.sort_children(page_chunks)

    def get_instructions(self):
        instruction_boundaries = self.__get_instructions_boundary()
        instructions = []
        for instruction in instruction_boundaries:
            instructions.append(
                InstructionBox(instruction[0], instruction[1], instruction[2], self.page_elements, self.mnemonics))

        return instructions

    def __get_instructions_boundary(self):
        sorted_titles = sorted(self.titles, key=lambda textbox: textbox.yc)
        if len(sorted_titles)>1:
            split_gen = self.chunks(sorted_titles, 2)
            splitted = []

            for i in split_gen:
                splitted.append(i)

            splitted.append([sorted_titles[len(sorted_titles)-1], ])

            coords_list=[]
            for coords in splitted:
                try:
                    coords_list.append((coords[0].y1, coords[1].y0, coords[0].text))
                except IndexError:
                    coords_list.append((coords[0].y1, 842, coords[0].text))

            return coords_list
        else:
            coords_list = []
            coords_list.append((sorted_titles[0].y1, 842, sorted_titles[0].text))
            return coords_list

    def draw_stuff(self, img):
        for element in self.page_elements:
            draw_chunk_box(img, (element.container.x0, element.container.x1),
                                (element.container.y0, element.container.y1), color=rgb_to_bgr((150, 139, 116)))
            for text in element.children:
                cv2.circle(img, (int(text.xc), int(text.yc)), 3, color=rgb_to_bgr((150, 139, 116)))
                draw_chunk_box(img, (int(text.x0), int(text.x1)),
                                    (int(text.y0), int(text.y1)), color=rgb_to_bgr((255, 181, 22)))
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

    @staticmethod
    def chunks(l, n):
        """Yield successive n-sized chunks from l."""
        for i in range(0, len(l), n):
            yield l[i:i + n]
