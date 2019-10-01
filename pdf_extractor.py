from pdfminer.pdfparser import PDFParser
from pdfminer.pdfdocument import PDFDocument
from pdfminer.pdfpage import PDFPage
from pdfminer.pdfinterp import PDFResourceManager
from pdfminer.pdfinterp import PDFPageInterpreter
from pdfminer.layout import LAParams, LTTextBox, LTTextLine, LTFigure, LTImage
from pdfminer.converter import PDFPageAggregator


class PdfExtractor:

    def __init__(self, w, h, file):
        self.w = w
        self.h = h
        self.file = file
        self.__layout_pages()

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

    def get_text_box(self, page_number):
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

    def mine_pdf2(self, page_number):
        text_chunks = []
        layout = self.layout_page(page_number)
        for obj in layout:
            if isinstance(obj, LTTextBox):
                text_chunks.append(obj)
        return text_chunks

    def find_start_img_chunks(self, text_chunks, header_size=22, start_index=0):
        """Find instruction in page by searching for text with a given height. Return a list with the name,
        the mnemonic and the operands and the starting location in the page """
        started = False
        last_index = 0
        name = ""
        name_y = ()
        mnemonic = "AAAA"
        operands = "BBBB"
        cursed_recursion = []

        for i in range(start_index, len(text_chunks)):
            if header_size - 1 < (text_chunks[i].y1 - text_chunks[i].y0) < header_size + 1:
                last_index = i
                if started:
                    cursed_recursion.append((name, name_y, mnemonic, operands))
                    cursed_recursion.append(self.find_start_img_chunks(text_chunks, start_index=last_index))
                    return cursed_recursion
                name = text_chunks[i].get_text()
                name_y = (text_chunks[i].y0, text_chunks[i].y1)
                started = True
                continue
                # Should we suppose that the next two elements are always the mnemonic?
            if last_index == i - 1:
                mnemonic = text_chunks[i].get_text()
            if last_index == i - 2:
                operands = text_chunks[i].get_text()
        return name, name_y, mnemonic, operands

    @staticmethod
    def print_start_chunks(chunks):
        for i in chunks:
            print("Name: " + str(i[0]).strip('\n'))
            print("    Y0: " + str(i[1][0]).strip('\n') + "   Y1: " + str(i[1][1]).strip('\n'))
            print("Mnemonic: " + str(i[2]).strip('\n'))
            print("Operands: " + str(i[3]).strip('\n'))
            print("\n")