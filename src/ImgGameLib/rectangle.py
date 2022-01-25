from .drawable import Drawable

from typing import Tuple, Union
from PIL import ImageDraw, ImageColor

class Rectangle(Drawable):
    """A simple rectangle that can be drawn to a canvas.
    
    Methods:
        - move
        - draw
        - coords
        - center
    """
    def __init__(self, x1: int, y1: int, width: int, height: int, border: Union[tuple, str]="black", fill: Union[tuple, str]="black", border_thickness: int=1):
        """Initializes a rectangle.
        
        Required Parameters:
            - x1: int - the first x coordinate
            - y1: int - the first y coordinate
            - width: int - the width of the rectangle
            - height: int - the height of the rectangle
        
        Optional Parameters:
            - border: Union[tuple, str] - the border color of the rectangle
            - fill: Union[tuple, str] - the fill color of the rectangle
            - border_thickness: int - the thickness of the border
        """
        self.x1 = x1
        self.y1 = y1
        self.x2 = x1+width
        self.y2 = y1+height
        self.border_thickness = border_thickness
        self.border = ImageColor.getrgb(border)
        self.fill = ImageColor.getrgb(fill)
        self.drawn = False
    
    def move(self, x: int=0, y: int=0, transition: bool=False):
        """Move the rectangle by some x and y.
        
        Parameters:
            - x: int - the amount by which to increment the x
            - y: int - the amount by which to increment the y
            - transition: bool - whether to generate an automatic transition, only applicable for gifs (not recommended for complex animations)
        """
        if not self.drawn:
            raise ValueError("The rectangle must be drawn before being moved.")
        if transition and not self.canvas.gif:
            raise ValueError("You can only generate transitions for gifs.")

        if transition:
            for _ in range(x):
                self.canvas.erase(self.x1, self.y1, self.x2, self.y2)
                self.x1 += 1
                self.x2 += 1
                self.canvas._draw_rectangle(self)
            for _ in range(y):
                self.canvas.erase(self.x1, self.y1, self.x2, self.y2)
                self.y1 += 1
                self.y2 += 1
                self.canvas._draw_rectangle(self)
        else:
            self.canvas.erase(self.x1, self.y1, self.x2, self.y2)
            self.x1 += x
            self.x2 += x
            self.y1 += y
            self.y2 += y
            self.canvas._draw_rectangle(self)
    
    def draw(self, canvas: "Canvas"):
        """Draw the rectangle to the canvas.
        
        Parameters:
            canvas: Canvas - the canvas to draw the rectangle to"""
        self.drawn = True
        self.canvas = canvas
        self.canvas._draw_rectangle(self)
    
    def coords(self) -> Tuple[int, int, int, int]:
        return self.x1, self.y1, self.x2, self.y2

    def center(self) -> Tuple[int, int]:
        return ((self.x1 + self.x2)/2, (self.y1 + self.y2)/2)
