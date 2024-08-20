import turtle

# Create a new turtle screen and set its background color
screen = turtle.Screen()
screen.bgcolor("black")

# Create a new turtle object
smiley = turtle.Turtle()
# Set the turtle color and width
smiley.color("green")
smiley.width(3)
# Draw the face
"""
Lifts the pen up, so that the turtle does not leave a trail when it moves.
"""
smiley.penup()
smiley.goto(0, -100)  # Center the face on the screen
smiley.pendown()
smiley.circle(100)

# Draw the eyes
smiley.penup()
smiley.goto(-40, 50)  # Position for the left eye
smiley.pendown()
smiley.dot(25)
smiley.penup()
smiley.goto(40, 50)  # Position for the right eye
smiley.pendown()
smiley.dot(25)

# Draw the mouth
smiley.penup()
smiley.goto(57, 10)  # Position for the mouth
smiley.pendown()
smiley.right(90)
for i in range(60):
    smiley.forward(3.4)
    smiley.right(3)

smiley.penup()
smiley.goto(0, -100)  # Center the face on the screen
smiley.pendown()
smiley.forward(10)

# Draw the body
smiley.penup()
smiley.goto(0, -100)  # body on the bottom on the screen
smiley.pendown()
smiley.left(100)
smiley.left(80)
smiley.forward(100)

#kaka
smiley.circle(100)
smiley.penup()
smiley.goto(-100, 25)  # Position for the left eye
smiley.pendown()
smiley.dot(25)
smiley.penup()
smiley.goto(15, 50)  # Position for the right eye
smiley.pendown()
smiley.dot(25)
smiley.penup()
smiley.goto(-36, 27)  # Position for the left eye
smiley.pendown()
smiley.dot(25)
smiley.penup()
smiley.goto(46, 19)  # Position for the right eye
smiley.pendown()
smiley.dot(25)
smiley.goto(-19, 28)  # Position for the left eye
smiley.pendown()
smiley.dot(25)
smiley.penup()
smiley.goto(87, 57)  # Position for the right eye
smiley.pendown()
smiley.dot(25)
# Keep the window open
turtle.done()
