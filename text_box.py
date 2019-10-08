
class TextBox:
    def __init__(self, x0, x1, y0, y1, text):
        self.x0 = x0
        self.x1 = x1
        self.y0 = y0
        self.y1 = y1
        self.xc = (x1 + x0)/2
        self.yc = (y1 + y0)/2
        self.text = text

    def __str__(self):
        return "Text: " + self.text + " xc: " + str(self.xc) + " yc: " + str(self.yc)

    # def __repr__(self):
    #     return "Text: " + self.text + " xc: " + str(self.xc) + " yc: " + str(self.yc)

    def __repr__(self):
        return self.text
