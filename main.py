from tkinter import *
import random

# Constants
GAME_WIDTH = 800
GAME_HEIGHT = 800
SPEED = 100
SPACE_SIZE = 50
BODY_PARTS = 3
SNAKE_COLOR = "#FFA500"
FOOD_COLOR = "#FFFFFF"
BACKGROUND_COLOR = "#1C2951"

class Snake:
    def __init__(self):
        # Initialize snake properties
        self.body_size = BODY_PARTS
        self.coordinates = []
        self.squares = []

        # Create initial coordinates for the snake
        for i in range(0, BODY_PARTS):
            self.coordinates.append([0, 0])

        # Create rectangles representing the snake on the canvas
        for x, y in self.coordinates:
            square = canvas.create_rectangle(x, y, x+SPACE_SIZE, y+SPACE_SIZE, fill=SNAKE_COLOR, tag="snake")
            self.squares.append(square)

class Food:
    def __init__(self):
        # Initialize food properties with random coordinates
        x = random.randint(0, (GAME_WIDTH/SPACE_SIZE) - 1) * SPACE_SIZE
        y = random.randint(0, (GAME_HEIGHT/SPACE_SIZE) - 1) * SPACE_SIZE
        self.coordinates = [x, y]
        
        # Create oval representing the food on the canvas
        canvas.create_oval(x, y, x+SPACE_SIZE, y+SPACE_SIZE, fill=FOOD_COLOR, tag="food")

def next_turn(snake, food):
    # Get the current coordinates of the snake's head
    x, y = snake.coordinates[0]

    # Update coordinates based on the current direction
    if direction == "up":
        y -= SPACE_SIZE
    elif direction == "down":
        y += SPACE_SIZE
    elif direction == "left":
        x -= SPACE_SIZE
    elif direction == "right":
        x += SPACE_SIZE

    # Insert new head coordinates at the beginning of the snake's coordinates list
    snake.coordinates.insert(0, [x, y])

    # Create a new rectangle representing the updated head on the canvas
    square = canvas.create_rectangle(x, y, x+SPACE_SIZE, y+SPACE_SIZE, fill=SNAKE_COLOR)

    # Update the list of squares representing the snake's body
    snake.squares.insert(0, square)

    # Check if the snake has eaten the food
    if x == food.coordinates[0] and y == food.coordinates[1]:
        global score
        score += 1
        label.config(text="Score: {}".format(score))
        # Delete the food on the canvas and create a new one
        canvas.delete("food")
        food = Food()
    else:
        # If the snake hasn't eaten, remove the last element of the snake (tail)
        del snake.coordinates[-1]
        canvas.delete(snake.squares[-1])
        del snake.squares[-1]

    # Check for collisions with the snake's body or game boundaries
    if check_collisions(snake):
        game_over()
        return

    # Schedule the next turn after a delay defined by the SPEED constant
    window.after(SPEED, next_turn, snake, food)   

def change_direction(new_direction):
    global direction
    # Change the direction if it's a valid move (avoid moving directly opposite)
    if new_direction == "up":
        if direction != "down":
            direction = new_direction
    elif new_direction == "down":
        if direction != "up":
            direction = new_direction
    elif new_direction == "left":
        if direction != "right":
            direction = new_direction
    elif new_direction == "right":
        if direction != "left":
            direction = new_direction

def check_collisions(snake):
    x, y = snake.coordinates[0]

    # Check if the head collides with the game boundaries
    if x < 0 or x >= GAME_WIDTH or y < 0 or y >= GAME_HEIGHT:
        return True
    
    # Check if the head collides with the snake's body
    for body_part in snake.coordinates[1:]:
        if x == body_part[0] and y == body_part[1]:
            return True

def game_over():
    # Display the game over message and exit after a delay
    canvas.delete(ALL)
    canvas.create_text(canvas.winfo_width()/2, canvas.winfo_height()/2, font=("Arial", 40), text="Game Over", fill="white", anchor=CENTER)
    window.update()
    window.after(3000)
    window.quit()

# Main application window
window = Tk()
window.title("Snake Game")
window.resizable(False, False)

# Initial setup for score, direction, label, and canvas
score = 0
direction = "down"
label = Label(window, text="Score: {}".format(score), font=("Arial", 40))
label.pack()

canvas = Canvas(window, bg=BACKGROUND_COLOR, height=GAME_HEIGHT, width=GAME_WIDTH)
canvas.pack()

# Adjust window size and position
window.update()
window_width = window.winfo_width()
window_height = window.winfo_height()
screen_width = window.winfo_screenwidth()
screen_height = window.winfo_screenheight()
x = int(screen_width/2 - window_width/2)
y = int(screen_height/2 - window_height/2)
window.geometry(f"{window_width}x{window_height}+{x}+{y}")

# Bind arrow keys to the change_direction function
window.bind("<Up>", lambda event: change_direction("up"))
window.bind("<Down>", lambda event: change_direction("down"))
window.bind("<Left>", lambda event: change_direction("left"))
window.bind("<Right>", lambda event: change_direction("right"))

# Initialize the snake and food
snake = Snake()
food = Food()

# Start the game loop
next_turn(snake, food)

# Start the Tkinter main loop
window.mainloop()
