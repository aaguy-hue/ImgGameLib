from abc import ABC, abstractmethod
from typing import Tuple


class Drawable(ABC):
    @abstractmethod
    def center(self) -> Tuple[int, int]:
        """Returns the coordinates at the center of the object.
        
        It is in the form of (x, y), where x and y are the coordinates at the center of the object."""
        ...
    
    @abstractmethod
    def coords(self) -> Tuple[int, int, int, int]:
        """Returns the coordinates of the object as a tuple.
        
        It is in the form of (x1, y1, x2, y2), where x1 and y1 are the coordinates at the top left, and x2 and y2 are the coordinates at the bottom right."""
        ...
    
    @abstractmethod
    def move(self, x: int, y: int, transition=False) -> None:
        """Moves the object by some x and y."""
        ...
    
    @abstractmethod
    def draw(self, canvas: "Canvas"):
        """Draws the object to a canvas."""
        ...
