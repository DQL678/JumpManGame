import pygame
import sys
from Player import Player
from Map import Map

# constants
SCREEN_WIDTH = 1000
SCREEN_HEIGHT = 650
FPS = 60
BG_COLOR = (30, 30, 30)


def main():
    pygame.init()
    screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
    pygame.display.set_caption("Jump man")
    clock = pygame.time.Clock()

    # controls
    controls_p1 = {"up": pygame.K_w, "down": pygame.K_s,
                   "left": pygame.K_a, "right": pygame.K_d}
    controls_p2 = {"up": pygame.K_UP, "down": pygame.K_DOWN,
                   "left": pygame.K_LEFT, "right": pygame.K_RIGHT}

    # map
    game_map = Map(SCREEN_WIDTH, SCREEN_HEIGHT)

    # players
    player1 = Player(200, 100, "Boneca Ambalabu.png", controls_p1, SCREEN_WIDTH, SCREEN_HEIGHT)
    player2 = Player(600, 100, "Boneca Ambalabu.png", controls_p2, SCREEN_WIDTH, SCREEN_HEIGHT)

    all_sprites = pygame.sprite.Group(player1, player2)

    # game loop
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

        pressed_keys = pygame.key.get_pressed()

        platforms = game_map.platforms + [game_map.ground]
        player1.update(pressed_keys, platforms)
        player2.update(pressed_keys, platforms)

        screen.fill(BG_COLOR)
        game_map.draw(screen)
        all_sprites.draw(screen)

        pygame.display.flip()
        clock.tick(FPS)


if __name__ == "__main__":
    main()
