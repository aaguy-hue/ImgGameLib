import ImgGameLib as igl

def goLeft(canvas, player):
    print("Moving left...")
    velocity = 0
    for _ in range(15):
        # Speed up
        velocity += 0.3
        player.move(x=-velocity)
    for _ in range(25):
        # Slow down
        velocity /= 1.1
        player.move(x=-velocity)
    canvas.save("game.gif", duration=20)
    canvas.discard_frames()
def goRight(canvas, player):
    print("Moving right...")
    velocity = 0
    for _ in range(15):
        # Speed up
        velocity += 0.3
        player.move(x=velocity)
    for _ in range(25):
        # Slow down
        velocity /= 1.1
        player.move(x=velocity)
    canvas.save("game.gif", duration=20)
    canvas.discard_frames()
def jump(canvas, player):
    print("Jumping...")
    velocity = 1
    for _ in range(10):
        # Speed up
        velocity += 0.6
        player.move(y=-velocity)
    for _ in range(5):
        # Slow down
        velocity /= 1.3
        player.move(y=-velocity)
    player.apply_gravity()
    canvas.save("game.gif", duration=40)
    canvas.discard_frames()


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
