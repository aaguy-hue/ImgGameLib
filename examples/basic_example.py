import ImgGameLib as igl

canvas = igl.Canvas(800, 800, bg_color="#99CDDE")

# Note: The border goes inwards, it does not take any extra space
rect = igl.Rectangle(10, 10, 100, 100, border="yellow", fill="red", border_thickness=5)
rect.draw(canvas)

canvas.show()

input("Press enter to continue...")

canvas.erase(10, 10, 110, 110)
canvas.show()
