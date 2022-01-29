from .drawable import Drawable
from . import constants

from typing import Tuple, Union
from PIL import ImageDraw, ImageColor

class Rectangle(Drawable):
    """A simple rectangle that can be drawn to a canvas.
    
    Methods:
        - move
        - draw
        - coords
        - center
        - apply_gravity
    """
    collider = constants.RECT_COLLIDER

    def __init__(self, x1: int, y1: int, width: int, height: int, border: Union[tuple, str]="black", fill: Union[tuple, str]="black", border_thickness: int=1, rigidbody: bool=False):
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
            - rigidbody: bool - whether objects will stop when falling upon colliding with this rectangle
        """
        self.drawable_type = "rect"
        self.x1 = x1
        self.y1 = y1
        self.x2 = x1+width
        self.y2 = y1+height
        self.border_thickness = border_thickness
        self.border = ImageColor.getrgb(border)
        self.fill = ImageColor.getrgb(fill)
        self.rigidbody = rigidbody
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
            add_num_x = 1 if abs(x) == x else -1
            add_num_y = 1 if abs(y) == y else -1
            for _ in range(abs(x)):
                self.canvas.erase(self.x1, self.y1, self.x2, self.y2)
                self.x1 += add_num_x
                self.x2 += add_num_x
                self.canvas._draw_rectangle(self)
            for _ in range(abs(y)):
                self.canvas.erase(self.x1, self.y1, self.x2, self.y2)
                self.y1 += add_num_y
                self.y2 += add_num_y
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
        if self.rigidbody:
            self.canvas.register_rigidbody(
                constants.RECT_COLLIDER,
                [
                    self.x1,
                    self.y1,
                    self.x2,
                    self.y2
                ]
            )
        self.canvas._draw_rectangle(self)
    
    def apply_gravity(self) -> None:
        """Applies gravity to a rectangle. Only recommended for simple scenarios. In more complex cases, make a loop and use Canvas.check_collision(rect.coords(), Rectangle.collider) to check for collision with rigidbodies."""
        velocity_y = 0
        acceleration_y = 0.6
        
        while not self.canvas.check_outofbounds(self) and not self.canvas.check_collision(self.coords(), Rectangle.collider):
            velocity_y += acceleration_y
            coords = list()
            self.move(y=velocity_y)
    
    def coords(self) -> Tuple[int, int, int, int]:
        return self.x1, self.y1, self.x2, self.y2

    def center(self) -> Tuple[int, int]:
        return ((self.x1 + self.x2)/2, (self.y1 + self.y2)/2)
