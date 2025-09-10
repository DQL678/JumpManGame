import pygame
import pymunk

# Initialize Pygame and Pymunk
pygame.init()

# Constants
WIDTH, HEIGHT = 800, 600
WINDOW = pygame.display.set_mode((WIDTH, HEIGHT))
CLOCK = pygame.time.Clock()
SPACE = pymunk.Space()
SPACE.gravity = (0, 1000)  # Set gravity

# Create a Ball
BALL_RADIUS = 20
ball_body = pymunk.Body(1, pymunk.moment_for_circle(1, 0, BALL_RADIUS))
ball_body.position = (400, 100)
ball_shape = pymunk.Circle(ball_body, BALL_RADIUS)
SPACE.add(ball_body, ball_shape)

# Main Loop
run = True
while run:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run = False

    # Physics Step
    SPACE.step(1 / 60.0)

    # Draw Everything
    WINDOW.fill((0, 0, 0))
    pygame.draw.circle(WINDOW, (0, 255, 0), (int(ball_body.position.x), int(ball_body.position.y)), BALL_RADIUS)

    pygame.display.update()
    CLOCK.tick(60)

pygame.quit()