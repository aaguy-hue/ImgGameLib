# ImgGameLib
A light wrapper around [pillow](https://pillow.readthedocs.io/en/stable/) designed for the making of games through generating images.

This is useful in several scenarios in which you are very limited, such as with discord bots.

## Example
```py
# Import the module
import ImgGameLib as igl

# Create a canvas
canvas = igl.Canvas(
    100,
    100,
    bg_color="#99CDDE"
)

# Create a 100x100 rectangle at (50,50) and draw it
rect = igl.Rectangle(
    50,
    50,
    100,
    100
)
rect.draw(canvas)

# Save the first frame to frame_1.png
canvas.save("frame_1.png")

# Move the rectangle by 10 pixels on the x axis
rect.move(x=10)

# Save the second frame to frame_2.png
canvas.save("frame_2.png")
```
See the examples folder for more examples.
