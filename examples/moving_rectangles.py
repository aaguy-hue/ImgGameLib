import ImgGameLib as igl

canvas = igl.Canvas(800, 800, bg_color="#99CDDE", gif=True)

rect = igl.Rectangle(10, 10, 100, 100, border="yellow", fill="red", border_thickness=5)
rect.draw(canvas)

for _ in range(100):
    rect.move(x=1,y=2)

canvas.save("test.gif", "gif", optimize_gif=True, duration=50, loop=False)
