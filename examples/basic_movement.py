import ImgGameLib as igl

def goLeft(canvas, player):
    print("Moving left...")
    player.move(x=-10, transition=True)
    canvas.save("game.gif", duration=20)
    # canvas.discard()
def goRight(canvas, player):
    print("Moving right...")
    player.move(x=10, transition=True)
    canvas.save("game.gif", duration=20)
    # canvas.discard()
def jump(canvas, player):
    print("Jumping...")
    player.move(y=-50, transition=True)
    player.apply_gravity()
    canvas.save("game.gif", duration=40)

canvas = igl.Canvas(800, 800, bg_color="#99CDDE", gif=True)

ground = igl.Rectangle(0, 700, 800, 100, fill="green", rigidbody=True)
ground.draw(canvas)

player = igl.Rectangle(400, 620, 30, 80, fill="red")
player.draw(canvas)

canvas.save("game.gif")

action = " "
while action[0].lower() != "q":
    action = input("What action would you like to take? Left, right, jump, or quit? ")
    if action[0].lower() == "l":
        goLeft(canvas, player)
    elif action[0].lower() == "r":
        goRight(canvas, player)
    elif action[0].lower() == "j":
        jump(canvas, player)
