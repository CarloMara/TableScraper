from .pdf_extractor import PdfExtractor
from .heatmap import boxes_from_img
from .aggregator import Aggregator
from .pdf2img import PdfImageExtractor


class ParsePdf:

    def __init__(self, path, w=595, h=842):
        self.W = w
        self.H = h
        self.path = path

    def parse_range(self, start, end):
        cv_page_gen = PdfImageExtractor(self.path, self.W, self.H)
        mine = PdfExtractor(w=self.W, h=self.H, file=self.path)
        instructions = []
        for i in range(start, end):
            img = cv_page_gen.get_page(i)
            # hm.draw_dots(img, work_img, 20)
            # hm.draw_chunks_line(img, work_img, 20)
            # hm.draw_chunks_box(img, work_img, 20, 5)
            # view.display_img(img)
            text_boxes = mine.get_text_chunks(i - 1)
            visual_elements = boxes_from_img(img, 20, 5)
            aggregator = Aggregator(visual_elements, text_boxes)
            # aggregator.draw_stuff(img)
            tmp = aggregator.get_instructions()
            for instruction in tmp:
                instructions.append(instruction)
        return instruction

    def parse_page(self, pageno):
        cv_page_gen = PdfImageExtractor(self.path, self.W, self.H)
        mine = PdfExtractor(w=self.W, h=self.H, file=self.path)
        instructions = []
        img = cv_page_gen.get_page(pageno)
        # hm.draw_dots(img, work_img, 20)
        # hm.draw_chunks_line(img, work_img, 20)
        # hm.draw_chunks_box(img, work_img, 20, 5)
        # view.display_img(img)
        text_boxes = mine.get_text_chunks(pageno - 1)
        visual_elements = boxes_from_img(img, 20, 5)
        aggregator = Aggregator(visual_elements, text_boxes)
        # aggregator.draw_stuff(img)
        return aggregator.get_instructions()
