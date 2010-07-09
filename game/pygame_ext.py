import pygame

def draw_line(surface, (x1, y1), (x2, y2), colormap):
    cols = len(colormap)

    if cols == 0:
        """no color, no drawing..."""
    elif cols == 1:
        """in case of 1 color line use original pygame function"""
        return pygame.draw.line(surface, colormap[0], (x1, y1), (x2, y2), 1)
    else:

        xx = float(x2 - x1)
        yy = float(y2 - y1)

        xxx = min(abs(xx / yy), 1) * (xx / abs(xx))
        yyy = min(abs(yy / xx), 1) * (yy / abs(yy))

        pxarray = pygame.PixelArray(surface)

        x, y = float(x1), float(y1)

        pixel_count = int(max(abs(xx), abs(yy)))

        for i in range(pixel_count):
            pxarray[int(round(x))][int(round(y))] = colormap[i % cols]
            x += xxx
            y += yyy
    rect = pygame.Rect(x1, y1, x2, y2)
    rect.normalize()
    return rect
