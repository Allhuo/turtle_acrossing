from turtle import Turtle
import random

COLORS = ["red", "orange", "yellow", "green", "blue", "purple"]
STARTING_MOVE_DISTANCE = 5
MOVE_INCREMENT = 10


class CarManager(Turtle):
    def __init__(self, new_ycor):
        super().__init__()
        self.shape("square")
        self.penup()
        self.shapesize(stretch_wid=1, stretch_len=2)
        self.color(random.choice(COLORS))
        self.setheading(180)
        self.move_speed = STARTING_MOVE_DISTANCE
        self.setx(300)
        self.sety(new_ycor)

    def move_left(self):
        self.forward(self.move_speed)

    def speed_up(self):
        self.move_speed += MOVE_INCREMENT

    def reset(self):
        self.move_speed = STARTING_MOVE_DISTANCE


