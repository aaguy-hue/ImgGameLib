import ImgGameLib as igl

canvas = igl.Canvas(800, 800, bg_color="#99CDDE", gif=True)

ground = igl.Rectangle(0, 700, 800, 100, fill="green", rigidbody=True)
ground.draw(canvas)

player = igl.Sprite(100, 100, "examples\\images\\firewizard.png", width=68, height=200)
player.draw(canvas)

player.apply_gravity()

canvas.save("game.gif", duration=20)
