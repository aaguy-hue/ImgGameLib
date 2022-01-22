from .canvas import Canvas
from .drawable import Drawable

from typing import Tuple
from PIL import ImageDraw, ImageColor

class Rectangle(Drawable):
    def __init__(self, x1: int, y1: int, width: int, height: int, border="black", fill=None):
        self.x1 = x1
        self.y1 = y1
        self.x2 = x1+width
        self.y2 = y1+height
        self.border = ImageColor.getrgb(border)
        self.fill = ImageColor.getrgb(fill)
        self.drawn = False
    
    def move(self, x: int=0, y: int=0):
        """Move the rectangle by some x and y.
        
        Parameters:
            - x: int - the amount by which to increment the x
            - y: int - the amount by which to increment the y
        """
        if self.drawn:
            self.canvas.erase(self.x1, self.y1, self.x2, self.y2)
        self.x1 += x
        self.x2 += x
        self.y1 += y
        self.y2 += y
        self.draw_object.rectangle(
            (self.x1, self.y1, self.x2, self.y2),
            outline=self.border,
            fill=self.fill
        )
    
    def draw(self, canvas: Canvas):
        """Draw the rectangle to the canvas.
        
        Parameters:
            canvas: Canvas - the canvas to draw the rectangle to"""
        self.drawn = True
        self.canvas = canvas
        self.draw_object: ImageDraw.ImageDraw = self.canvas.get_imagedraw()
        self.draw_object.rectangle(
            (self.x1, self.y1, self.x2, self.y2),
            outline=self.border,
            fill=self.fill
        )
    
    def coords(self) -> Tuple[int, int, int, int]:
        return self.x1, self.y1, self.x2, self.y2

    def center(self) -> Tuple[int, int]:
        return ((self.x1 + self.x2)/2, (self.y1 + self.y2)/2)
