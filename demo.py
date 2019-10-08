import cv2
import pdf_extractor as pe
import heatmap as hm
import sdl_view as sdl
import aggregator as aggr
import util

# W = 1245 // 2
# H = 1754 // 2

W = 595
H = 842


if __name__ == "__main__":

    img = cv2.imread('../p167.png')
    img = cv2.resize(img, (W, H))

    work_img = cv2.imread('../p167.png')
    work_img = cv2.resize(work_img, (W, H))

    edges = cv2.Canny(img, 275, 500, apertureSize=3)
    # hm.draw_dots(img, work_img, 20)
    # hm.draw_chunks_line(img, work_img, 20)
    # hm.draw_chunks_box(img, work_img, 20, 5)

    mine = pe.PdfExtractor(w=W, h=H, file='../isa_m16c60.pdf')

    text_boxes = mine.get_text_chunks(166)

    visual_elements = hm.boxes_from_img(img, 20, 5)

    aggregator = aggr.Aggregator(visual_elements, text_boxes)

    aggregator.draw_stuff(work_img)

    for k in aggregator.page_elements:
        print("IMG Chunk: ")
        for elm in k.grouped_chunks:
            print(elm)
        print("\n")

    for text in text_boxes:
        util.draw_chunk_box(img, (int(text.x0), int(text.x1)),
                            (int(text.y0), int(text.y1)), color=util.rgb_to_bgr((255, 181, 22)))

    #
    # for box in box_headers:
    #     cv2.circle(work_img, (int(box.xc), H - int(box.yc)), 10, (util.rgb_to_bgr((105,87,31))))
    #     print(box.xc)
    #     print(box.yc)
    #     boxes.append(box)
    #
    # for box in boxes_img:
    #     cv2.circle(work_img, (int(box.xc), int(box.yc)), 10, (util.rgb_to_bgr((255,220,142))))
    #     print(box.xc)
    #     print(box.yc)
    #     boxes.append(box)
    #
    # boxes_sort(boxes)

    view = sdl.SdlView((W, H))

    view.handle_sdl((edges, edges), (img, work_img))




