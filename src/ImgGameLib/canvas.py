from typing import IO, Optional, Union
from PIL import Image, ImageColor, ImageDraw

class Canvas:
    """A simple canvas you can draw stuff upon.

    Methods:
        - show - display the image
        - get_imagedraw - return the PIL ImageDraw object

    Parameters:
        - width - the width of the canvas
        - height - the height of the canvas
        - bg_color - the background color of the canvas
    """
    # This is based upon the tkinter canvas
    def __init__(self, width, height, bg_color: str="white") -> None:
        self.bg_color = bg_color
        self.width = width
        self.height = height

        self._im: Image = Image.new(
            mode="RGBA",
            size=(self.width, self.height),
            color=ImageColor.getrgb(self.bg_color)
        )
        self._draw: ImageDraw.ImageDraw = ImageDraw.Draw(self._im)
    
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
        self._im.show()
    
    def get_imagedraw(self) -> ImageDraw.ImageDraw:
        """Returns the PIL Image being drawn upon."""
        return self._draw
    
    def save(self, save_file: Union[str, IO], filetype: Optional[str]=None) -> None:
        """Saves the image to a file.
        
        Parameters:
            - save_file: Union[str, IO] - either a string (or pathlib.Path object) with the file name/path to save to, or a file object to save to
            - filetype: Optional[str] - the type of file
        """
        self._im.save(save_file, format=filetype)
