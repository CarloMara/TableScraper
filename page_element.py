import itertools


class PageElement():
    # Page element contains all text boxes inside a heat zone

    def __init__(self, container, children):
        self.container = container  # heat box
        self.children = children    # array of textboxes
        self.sorted_children = self.sort_children()

    def sort_children(self):
        tmp = sorted(self.children, key=lambda text_box: text_box.yc)
        y_group = itertools.groupby(tmp, lambda text_box: text_box.yc)

        sorted_chunk = []
        for key, group in y_group:
            sorted_x = sorted(group, key=lambda text_box: text_box.xc)
            for box in sorted_x:
                sorted_chunk.append(box)
        return sorted_chunk
