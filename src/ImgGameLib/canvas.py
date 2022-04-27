from typing import IO, Optional, Union
from PIL import Image, ImageColor, ImageDraw

from ImgGameLib import constants

class Canvas:
    """A simple canvas you can draw stuff upon.

    Methods:
        - erase
        - show
        - discard
        - copy
        - register_rigidbody
        - check_collision
        - check_outofbounds
        - save
    """
    # This is based upon the tkinter canvas
    def __init__(self, width, height, bg_color: Union[tuple, str]="white", gif: bool=False) -> None:
        """Initializes a canvas.
        
        Parameters:
            - width: int - the width of the canvas
            - height: int - the height of the canvas
            - bg_color: Union[tuple, str] - the background color of the canvas
            - gif: bool - whether a gif should be saved instead of a normal image
        """
        self.bg_color = bg_color
        self.width = width
        self.height = height
        self.gif = gif

        self._im: Image = Image.new(
            mode="RGBA",
            size=(self.width, self.height),
            color=ImageColor.getrgb(self.bg_color)
        )
        self._draw: ImageDraw.ImageDraw = ImageDraw.Draw(self._im)

        if self.gif:
            self.gif_frames = [self._im.copy()]
        
        self.rigidbodies = {
            "rect": [],
        }
    
    def erase(self, x1, y1, x2, y2) -> None:
        """Erases a selection of the image, with the selection being a rectangle.
        
        Parameters:
            - x1 - the top left x of the rectangular selection
            - y1 - the top left y of the rectangular selection
            - x2 - the bottom right x of the rectangular selection
            - y2 - the bottom right y of the rectangular selection
        """
        self._draw.rectangle((x1, y1, x2, y2), outline=None, fill=self.bg_color)

    def show(self) -> None:
        """Displays the image."""
        if self.gif:
            raise ValueError("Displaying gifs is not supported yet.")
        self._im.show()
    
    def _append_frame(self) -> None:
        self.gif_frames.append(self._im.copy())

    def _draw_rectangle(self, rect: "Rectangle") -> None:
        self._draw.rectangle(
            (rect.x1, rect.y1, rect.x2, rect.y2),
            outline=rect.border,
            fill=rect.fill,
            width=rect.border_thickness
        )
        if self.gif:
            self._append_frame()
    
    def _draw_sprite(self, sprite: "Sprite") -> None:
        if sprite.sprite.mode == "RGBA":
            the_sprite = Image.new(
                mode="RGBA",
                size=(self.width, self.height),
                color=(0, 0, 0, 0)
            )
            the_sprite.paste(sprite.sprite, (sprite.x1, sprite.y1, sprite.x2, sprite.y2))
            self._im = Image.alpha_composite(self._im, the_sprite)
            self._draw: ImageDraw.ImageDraw = ImageDraw.Draw(self._im)
        else:
            self._im.paste(
                sprite.sprite,
                (
                    sprite.x1,
                    sprite.y1,
                    sprite.x2,
                    sprite.y2
                )
            )

        if self.gif:
            self._append_frame()
    
    def copy(self):
        cp = Canvas(width=self.width, height=self.height, bg_color=self.bg_color, gif=self.gif)
        cp._im = self._im.copy()
        cp._draw = ImageDraw.Draw(cp._im)

        if self.gif:
            cp.gif_frames = [self.gif_frames[i].copy() for i in range(len(self.gif_frames))]
        return cp
    
    @property
    def is_gif(self) -> bool:
        return self.gif
    
    def discard_frames(self) -> None:
        """Gets rid of all previous frames of the animation."""
        if not self.gif:
            raise ValueError("This function is not applicable for images.")
        self._im = self.gif_frames[-1]
        self._draw: ImageDraw.ImageDraw = ImageDraw.Draw(self._im)
        self.gif_frames = [self._im.copy()]
    
    def register_rigidbody(self, collider_type: int, drawable: "Drawable") -> None:
        """Registers an item as a rigidbody item.
        
        Required Parameters:
            collider_type: int - the type of collider (import constants for these)
            drawable: Drawable - a drawable for the rigidbody
        """
        if collider_type == constants.RECT_COLLIDER:
            self.rigidbodies["rect"].append(drawable)
        else:
            raise ValueError("Invalid collider type.")
    
    def check_collision(self, coords: Union[list, tuple], collider_type: int) -> bool:
        """Checks if there is collision between some object and a rigidbody.
        
        Required Parameters:
            coords: Union[list, tuple] - a drawable object's coordinates to check if it has collided with something
            collider_type: int - the type of collider
        """
        if collider_type == constants.RECT_COLLIDER:
            for rect_rigidbody in self.rigidbodies["rect"]:
                a_left, a_top, a_right, a_bottom = coords
                b_left, b_top, b_right, b_bottom = rect_rigidbody.coords()

                if not (a_left > b_right or a_right < b_left
                        or a_bottom < b_top or a_top > b_bottom):
                    return True
        else:
            raise ValueError("Collisions are currently unsupported for this drawable.")
        return False
    
    def check_outofbounds(self, drawable: "Drawable") -> bool:
        """Checks if an object is no longer visible in the image.
        
        Required Parameters:
            drawable: Drawable - a drawable object to check if is out of the image
        """
        if drawable.drawable_type == "rect":
            if drawable.x1 < 0 or drawable.y1 < 0 or drawable.x2 > self.width or drawable.y2 > self.height:
                return True
        else:
            raise ValueError("This function is currently unsupported for this drawable.")
        
        return False
    
    def save(self, save_file: Union[str, IO], filetype: Optional[str]=None, *, optimize_gif: bool=False, loop: bool=False, duration: int=0, no_gif: bool=False) -> None:
        """Saves the image to a file.
        
        Required Parameters:
            - save_file: Union[str, IO] - either a string (or pathlib.Path object) with the file name/path to save to, or a file object to save to
        
        Optional Parameters:
            - filetype: Optional[str] - the type of file
        
        Optional GIF Parameters:
            - no_gif: bool - if true, only the current frame will be saved
            - optimize_gif: bool - whether to optimize the gif
            - loop: bool - whether the gif should loop
            - duration: int - the duration of the gif in milliseconds
        """
        if self.gif and not no_gif:
            params = {
                "fp":save_file,
                "format":filetype,
                "save_all":True,
                "append_images":self.gif_frames[1:],
                "optimize":optimize_gif,
                "duration":duration
            }
            if loop: params["loop"] = 0
            self.gif_frames[0].save(**params)
        else:
            if optimize_gif:
                raise ValueError("You cannot optimize an image which isn't a gif.")
            if loop:
                raise ValueError("Images that aren't gifs cannot loop.")
            if duration:
                raise ValueError("Images that aren't gifs cannot have a set duration.")
            self._im.save(save_file, format=filetype)
