class PageElement():
    # Page element contains all text boxes inside a heat zone

    def __init__(self, container, children):
        self.container = container  #heat box
        self.children = children    #array of textboxes
        self.grouped_chunks = self.consolidate_children()

    def consolidate_children(self):
        tmp = self.children

        # group by same Y
        grouped_chunks = []
        done_x = []
        done_y = []
        for i in tmp:
            tmp_list = []
            for k in tmp:
                if int(i.yc) == int(k.yc):
                    tmp_list.append(k)
                    done_y.append(int(k.yc))

            if not (int(i.yc) in done_x):
                grouped_chunks.append(tmp_list)
                done_x.append(int(i.yc))

        return grouped_chunks
