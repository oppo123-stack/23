#製作一個python程式，turtle可以用wasd操控的簡單角色移動
#角色碰到果實會加分，碰到障礙物會扣分
import turtle
import random

# --- Setup ---
screen = turtle.Screen()
screen.title("WASD 控制 - 收集果實 / 避開障礙")
screen.setup(width=600, height=600)
screen.tracer(0)

player = turtle.Turtle()
player.shape("turtle")
player.color("blue")
player.penup()
player.speed(0)

move_distance = 20

# --- Score display ---
score = 0
score_writer = turtle.Turtle()
score_writer.hideturtle()
score_writer.penup()
score_writer.goto(0, 260)

def update_score():
    score_writer.clear()
    score_writer.write(f"Score: {score}", align="center", font=("Arial", 16, "normal"))

# --- Utility: place object at random position within bounds ---
def place_random(obj):
    x = random.randint(-260, 260)
    y = random.randint(-220, 260)
    obj.goto(x, y)

# --- Fruit ---
fruit = turtle.Turtle()
fruit.shape("circle")
fruit.color("green")
fruit.penup()
fruit.speed(0)

# --- Obstacles ---
obstacles = []
NUM_OBSTACLES = 3
for _ in range(NUM_OBSTACLES):
    o = turtle.Turtle()
    o.shape("square")
    o.color("red")
    o.penup()
    o.speed(0)
    place_random(o)
    obstacles.append(o)

# ensure fruit doesn't spawn on top of obstacles or player
def place_fruit():
    while True:
        place_random(fruit)
        if all(fruit.distance(o) > 40 for o in obstacles) and fruit.distance(player) > 60:
            break

# --- Collision handling ---
def check_collisions():
    global score
    # fruit collision
    if player.distance(fruit) < 20:
        score += 10
        update_score()
        place_fruit()
    # obstacle collisions
    for obs in obstacles:
        if player.distance(obs) < 20:
            score -= 5
            update_score()
            # simple penalty: move player back to center
            player.goto(0, 0)
            break

# --- Movement functions ---
def move_up():
    if player.ycor() + move_distance <= 290:
        player.sety(player.ycor() + move_distance)
    check_collisions()
    screen.update()

def move_down():
    if player.ycor() - move_distance >= -290:
        player.sety(player.ycor() - move_distance)
    check_collisions()
    screen.update()

def move_left():
    if player.xcor() - move_distance >= -290:
        player.setx(player.xcor() - move_distance)
    check_collisions()
    screen.update()

def move_right():
    if player.xcor() + move_distance <= 290:
        player.setx(player.xcor() + move_distance)
    check_collisions()
    screen.update()

# --- Continuous movement using press/release handlers ---
# movement state flags
moving = {"up": False, "down": False, "left": False, "right": False}

# start/stop handlers (call move once for immediate response)
def start_up():
    move_up()
    moving["up"] = True

def stop_up():
    moving["up"] = False

def start_down():
    move_down()
    moving["down"] = True

def stop_down():
    moving["down"] = False

def start_left():
    move_left()
    moving["left"] = True

def stop_left():
    moving["left"] = False

def start_right():
    move_right()
    moving["right"] = True

def stop_right():
    moving["right"] = False

# bind keys using onkeypress (press) and onkeyrelease (if available) for release
screen.listen()
# lowercase
screen.onkeypress(start_up, "w")
screen.onkeypress(start_down, "s")
screen.onkeypress(start_left, "a")
screen.onkeypress(start_right, "d")
# uppercase
screen.onkeypress(start_up, "W")
screen.onkeypress(start_down, "S")
screen.onkeypress(start_left, "A")
screen.onkeypress(start_right, "D")

# stop bindings (try onkeyrelease if available, fall back to onkey)
if hasattr(screen, "onkeyrelease"):
    screen.onkeyrelease(stop_up, "w")
    screen.onkeyrelease(stop_down, "s")
    screen.onkeyrelease(stop_left, "a")
    screen.onkeyrelease(stop_right, "d")
    screen.onkeyrelease(stop_up, "W")
    screen.onkeyrelease(stop_down, "S")
    screen.onkeyrelease(stop_left, "A")
    screen.onkeyrelease(stop_right, "D")
else:
    # some turtle versions don't expose onkeyrelease; use onkey as a fallback
    screen.onkey(stop_up, "w")
    screen.onkey(stop_down, "s")
    screen.onkey(stop_left, "a")
    screen.onkey(stop_right, "d")
    screen.onkey(stop_up, "W")
    screen.onkey(stop_down, "S")
    screen.onkey(stop_left, "A")
    screen.onkey(stop_right, "D")

# periodic loop to apply continuous movement when keys are held
def game_loop():
    moved = False
    if moving["up"]:
        if player.ycor() + move_distance <= 290:
            player.sety(player.ycor() + move_distance)
        moved = True
    if moving["down"]:
        if player.ycor() - move_distance >= -290:
            player.sety(player.ycor() - move_distance)
        moved = True
    if moving["left"]:
        if player.xcor() - move_distance >= -290:
            player.setx(player.xcor() - move_distance)
        moved = True
    if moving["right"]:
        if player.xcor() + move_distance <= 290:
            player.setx(player.xcor() + move_distance)
        moved = True

    if moved:
        check_collisions()
        screen.update()

    # repeat
    screen.ontimer(game_loop, 60)  # approximately 60ms per tick (~16 FPS)

# Initialize game
place_fruit()
update_score()
# start continuous movement loop
game_loop()

# Start game
screen.mainloop()
