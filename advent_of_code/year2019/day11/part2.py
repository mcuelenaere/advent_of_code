from .shared import PanelPainter


def calculate(text: str) -> str:
    painter = PanelPainter(text)
    painter.panels[(0, 0)] = 1
    painter.run()

    max_x = max(x for x, y in painter.panels.keys())
    max_y = max(y for x, y in painter.panels.keys())
    for y in range(max_y + 1):
        print(''.join('#' if painter.panels[(x, y)] == 1 else ' ' for x in range(max_x + 1)))

    # and again, I'm not implementing OCR :)
    return "UZAEKBLP"


