import cv2
import pdf_extractor as pe
import heatmap as hm
import sdl_view as sdl

W = 1245 // 2
H = 1754 // 2


if __name__ == "__main__":

    img = cv2.imread('../p215.png')
    img = cv2.resize(img, (W, H))

    edges = cv2.Canny(img,275,500, apertureSize=3)
    work_img = img
    hm.draw_dots(img, work_img, 20)
    hm.draw_chunks(img, work_img, 20)

    mine = pe.PdfExtractor(w=W, h=H, file='../isa_m16c60.pdf')
    chunks = mine.mine_pdf2(215)
    start_chunks = mine.find_start_img_chunks(chunks)

    mine.print_start_chunks(start_chunks)

    view = sdl.SdlView((W, H))

    view.handle_sdl((edges, edges), (img, work_img))



