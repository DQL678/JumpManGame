import pygame

pygame.init()
window = pygame.display.set_mode((300, 300))
clock = pygame.time.Clock()

rect = pygame.Rect(135, 220, 30, 30)
vel = 5

run = True
while run:
    clock.tick(100)
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run = False

    keys = pygame.key.get_pressed()
    rect.centerx = (rect.centerx + (keys[pygame.K_RIGHT] - keys[pygame.K_LEFT]) * vel) % 300

    if keys[pygame.K_SPACE]:
        rect.y -= 1
    elif rect.y < 220:
        rect.y += 1

    window.fill((0, 0, 64))
    pygame.draw.rect(window, (64, 64, 64), (0, 250, 300, 100))
    pygame.draw.circle(window, (255, 0, 0), rect.center, 15)
    pygame.display.flip()

pygame.quit()
exit()