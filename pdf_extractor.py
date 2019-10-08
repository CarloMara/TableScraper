from pdfminer.pdfparser import PDFParser
from pdfminer.pdfdocument import PDFDocument
from pdfminer.pdfpage import PDFPage
from pdfminer.pdfinterp import PDFResourceManager
from pdfminer.pdfinterp import PDFPageInterpreter
from pdfminer.layout import LAParams, LTTextBox, LTTextLine, LTFigure, LTImage
from pdfminer.converter import PDFPageAggregator
import text_box as tb

class PdfExtractor:

    def __init__(self, w, h, file):
        self.w = w
        self.h = h
        self.file = file
        self.__layout_pages()
        self.layout = []

    def __layout_pages(self):
        # Open a PDF file.
        fp = open(self.file, 'rb')
        # Create a PDF parser object associated with the file object.
        parser = PDFParser(fp)
        # Create a PDF document object that stores the document structure.
        # Supply the password for initialization.
        document = PDFDocument(parser)
        # Create a PDF resource manager object that stores shared resources.
        rsrcmgr = PDFResourceManager()
        # Set parameters for analysis.
        laparams = LAParams(line_margin=0.1)
        # Create a PDF page aggregator object.
        self.device = PDFPageAggregator(rsrcmgr, laparams=laparams)
        # Create a PDF interpreter object.
        self.interpreter = PDFPageInterpreter(rsrcmgr, self.device)
        # Process each page contained in the document.
        self.pages = dict((pageno, page) for (pageno, page) in enumerate(PDFPage.create_pages(document)))

    def layout_page(self, page_number):
        self.interpreter.process_page(self.pages.get(page_number))  # receive the LTPage object for this page
        return self.device.get_result()

    def get_text_box_list(self, page_number):
        text_box = []
        layout = self.layout_page(page_number)
        for obj in layout:
            if isinstance(obj, LTTextBox):
                text_box.append(((obj.x0 / layout.width) * self.w,
                                    (obj.x1 / layout.width) * self.w,
                                    self.h - (obj.y0 / layout.height) * self.h,
                                    self.h - (obj.y1 / layout.height) * self.h))
                print(obj.get_text(), "   ", self.h - (obj.y0 / layout.height) * self.h -
                      (self.h - (obj.y1 / layout.height) * self.h))
        return text_box

    def get_text_box(self, obj):
        if isinstance(obj, LTTextBox):
            text_box =((obj.x0 / self.layout.width) * self.w,
                             (obj.x1 / self.layout.width) * self.w,
                             self.h - (obj.y0 / self.layout.height) * self.h,
                             self.h - (obj.y1 / self.layout.height) * self.h)
            return text_box
        return None

    def get_text_chunks(self, page_number):
        text_chunks = []
        self.layout = self.layout_page(page_number)
        for obj in self.layout:
            if isinstance(obj, LTTextBox):
                text_chunks.append(tb.TextBox(obj.x0, obj.x1, self.h - obj.y0, self.h - obj.y1, obj.get_text().strip("\n")))
        return text_chunks
