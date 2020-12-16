from .shared import PanelPainter


def calculate(text: str) -> int:
    painter = PanelPainter(text)
    painter.run()
    return len(painter.panels)
