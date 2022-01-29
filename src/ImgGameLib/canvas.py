from typing import IO, Optional, Union
from PIL import Image, ImageColor, ImageDraw

from ImgGameLib import constants

class Canvas:
    """A simple canvas you can draw stuff upon.

    Methods:
        - erase
        - show
        - discard
        - register_rigidbody
        - check_collision
        - check_outofbounds
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
    
    @property
    def is_gif(self) -> bool:
        return self.gif
    
    def discard(self) -> None:
        """Gets rid of all previous frames of the animation."""
        if not self.gif:
            raise ValueError("This function is not applicable for images.")
        self._im = self.gif_frames[-1]
        self.gif_frames = [self._im.copy()]
    
    def register_rigidbody(self, collider_type: int, coords: list) -> None:
        """Registers an item as a rigidbody item.
        
        Required Parameters:
            collider_type: int - the type of collider (import constants for these)
            coords: list - a list of the coordinates of the rigidbody
        """
        if collider_type == constants.RECT_COLLIDER:
            if len(coords) != 4:
                raise ValueError("Rectangle colliders must have exactly 4 coordinates: x1, y1, x2, and y2.")
            self.rigidbodies["rect"].append(coords)
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
                a_left = coords[0]
                a_top = coords[1]
                a_right = coords[2]
                a_bottom = coords[3]
                b_left = rect_rigidbody[0]
                b_top = rect_rigidbody[1]
                b_right = rect_rigidbody[2]
                b_bottom = rect_rigidbody[3]

                if not (a_left >= b_right or a_right <= b_left
                        or a_bottom <= b_top or a_top >= b_bottom):
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
