import json
import parse_pdf as parse

W = 595
H = 842


if __name__ == "__main__":

    parser = parse.ParsePdf("../isa_m16c60.pdf")

    print(json.dumps(parser.parse_range(158, 160), default=lambda x: x.__dict__, indent=2, sort_keys=True))




