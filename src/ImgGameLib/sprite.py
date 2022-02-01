from typing import Tuple, Union
from PIL import Image
from . import constants
from .rectangle import Rectangle
from .drawable import Drawable

class Sprite(Drawable):
    collider = constants.RECT_COLLIDER
    drawable_type = "rect"
    
    def __init__(self, x: int, y: int, sprite: Union[str, Image.Image], width: int=None, height: int=None):
        """Creates a new sprite.
        
        Required Parameters:
            - x: int - the left x of the image
            - y: int - the top y of the image
            - sprite: str | PIL.Image.Image - a PIL Image object for the image or a string for the path to the image
        
        Optional Parameters:
            - width: int - the width of the image
            - height: int - the height of the image
        """
        self.x1 = x
        self.y1 = y
        if isinstance(sprite, Image.Image):
            self.sprite = sprite
        else:
            self.sprite = Image.open(sprite)
        self.sprite.convert("RGBA")
        self.width, self.height = self.sprite.size
        if width is not None:
            self.sprite = self.sprite.resize((width, self.height))
            self.width = width
        if height is not None:
            self.sprite = self.sprite.resize((self.width, height))
            self.height = height
        self.x2 = x+self.width
        self.y2 = y+self.height
        self.drawn = False
    
    def move(self, x: int=0, y: int=0, transition: bool=False):
        """Move the sprite by some x and y.
        
        Parameters:
            - x: int - the amount by which to increment the x
            - y: int - the amount by which to increment the y
            - transition: bool - whether to generate an automatic transition, only applicable for gifs (not recommended for complex animations)
        """
        if not self.drawn:
            raise ValueError("The rectangle must be drawn before being moved.")
        if transition and not self.canvas.gif:
            raise ValueError("You can only generate transitions for gifs.")

        x = round(x)
        y = round(y)

        if transition:
            add_num_x = 1 if abs(x) == x else -1
            add_num_y = 1 if abs(y) == y else -1
            for _ in range(abs(x)):
                self.canvas.erase(self.x1, self.y1, self.x2, self.y2)
                self.x1 += add_num_x
                self.x2 += add_num_x
                self.canvas._draw_sprite(self)
            for _ in range(abs(y)):
                self.canvas.erase(self.x1, self.y1, self.x2, self.y2)
                self.y1 += add_num_y
                self.y2 += add_num_y
                self.canvas._draw_sprite(self)
        else:
            self.canvas.erase(self.x1, self.y1, self.x2, self.y2)
            self.x1 += x
            self.x2 += x
            self.y1 += y
            self.y2 += y
            self.canvas._draw_sprite(self)
    
    def coords(self) -> Tuple[int, int, int, int]:
        return self.x1, self.y1, self.x2, self.y2

    def center(self) -> Tuple[int, int]:
        return ((self.x1 + self.x2)/2, (self.y1 + self.y2)/2)

    def apply_gravity(self) -> None:
        """Applies gravity to an image. Only recommended for simple scenarios. In more complex cases, make a loop and use Canvas.check_collision(sprite.coords(), Sprite.collider) to check for collision with rigidbodies."""
        if not self.drawn:
            raise ValueError("You must first draw the rectangle before applying gravity to it.")
        
        velocity_y = 0
        acceleration_y = 0.6
        
        while not self.canvas.check_outofbounds(self) and not self.canvas.check_collision(self.coords(), Rectangle.collider):
            velocity_y += acceleration_y
            self.move(y=velocity_y)
    
    def draw(self, canvas: "Canvas"):
        """Draw the sprite to the canvas.
        
        Parameters:
            canvas: Canvas - the canvas to draw the sprite to
        """
        self.drawn = True
        self.canvas = canvas
        self.canvas._draw_sprite(self)
