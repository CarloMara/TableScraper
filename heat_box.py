class HeatBox:

    def __init__(self, x0, x1, y0, y1):
        self.x0 = x0
        self.x1 = x1
        self.y0 = y0
        self.y1 = y1
        self.xc = (x1 + x0)/2
        self.yx = (y1 + y0)/2

    def is_container(self, chunk, x_tolerance=1, y_tolerance=2):
        if (self.x0 - x_tolerance) <= chunk.x0 <= (self.x1 + x_tolerance) and \
                (self.x0 - x_tolerance) <= chunk.x1 <= (self.x1 + x_tolerance) and \
                (self.y0 - y_tolerance) <= chunk.y0 <= (self.y1 + y_tolerance) and \
                (self.y0 - y_tolerance) <= chunk.y1 <= (self.y1 - y_tolerance):
            return True
        else:
            return False
