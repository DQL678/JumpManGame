# Import essential libraries
import pygame
import sys
from pygame.locals import *

# Initialize the Pygame framework
pygame.init()

# Set up the clock for precise frame rate control
clock = pygame.time.Clock()

# Create the game window
screen = pygame.display.set_mode((400, 400))

# Define a visually appealing light green color
lightgreen = (144, 238, 144)

# Set initial values for the sprite's position and jump parameters
x = 50
y = 300
m = 1
v = 15
jump = 0

# Load the sprite image for a captivating visual element
# sprite = pygame.image.load('data/wheel/1.png')

# Flag to control the game loop
game_running = True

# Unraveling the Jumping Logic
while game_running:
    # Maintain an optimal frame rate
    clock.tick(60)

    # Handle events, ensuring smooth execution
    pygame.time.delay(20)
    for event in pygame.event.get():
        if event.type == QUIT:
            pygame.quit()
            sys.exit()

    # Detect key presses, a crucial element for user interaction
    keys = pygame.key.get_pressed()

    # Initiate a jump when the sprite is not in mid-air and the space key is pressed
    if jump == 0:
        if keys[pygame.K_SPACE]:
            jump = 1  # Set the jump flag to initiate a dynamic leap

    # Execute the calculated jump when the jump flag is active
    if jump == 1:
        k = 0.5 * m * v ** 2  # Calculate the vertical displacement
        y -= k  # Update the sprite's vertical position
        v -= 1  # Simulate gravity by gradually decreasing velocity
        if v < 0:
            m = -1  # Change the direction of displacement for a realistic jump feel
        if v == -11:
            m = 1  # Reset parameters for subsequent jumps
            v = 10
            jump = 0  # Reset the jump flag upon completion

    # Rendering the Dynamic Sprite
    # Enhance the visual appeal with a light green background
    screen.fill(lightgreen)

    # Draw the dynamically jumping sprite on the screen
    # screen.blit(sprite, (x, y))
    pygame.draw.rect(screen, ('#1CA61C'), (x, y, 90, 90), 5)

    # Update the display
    pygame.display.update()