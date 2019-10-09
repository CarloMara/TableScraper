class InstructionBox:

    def __init__(self, y0, y1, title, elements, mnemonics):
        self.y0 = y0
        self.y1 = y1
        self.yc = (y1 + y0)/2
        self.title = title
        self.elements = self.add_elements(elements)
        self.mnemonic = self.add_mnemonic(mnemonics)

    def add_elements(self, elements):
        # checks if element is inside instruction and adds it to the elements list
        instruction_elements = []
        for element in elements:
            if self.is_container(element):
                instruction_elements.append(element)

        return instruction_elements

    def add_mnemonic(self, mnemonics):
        # checks if a mnemonic is inside instruction and adds it to the mnemonics list
        instruction_mnemonics = []
        for mnemonic in mnemonics:
            if self.is_container(mnemonic):
                instruction_mnemonics.append(mnemonic)

        return instruction_mnemonics

    def is_container(self, chunk, y_tolerance=2):
        if (self.y0 - y_tolerance) <= chunk.yc <= (self.y1 + y_tolerance) and \
                (self.y0 - y_tolerance) <= chunk.yc <= (self.y1 - y_tolerance):
            return True
        else:
            return False
