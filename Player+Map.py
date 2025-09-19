import pygame
import sys

# constants
SCREEN_WIDTH = 1000
SCREEN_HEIGHT = 650
FPS = 60

GRAVITY = 0.8

PLAYER_SIZE = 50
PLAYER_SPEED = 7
WHITE = (255, 255, 255)

# Farver
PLATFORM_COLOR = (100, 100, 255)  # blå platforme
GROUND_COLOR = (200, 50, 50)      # rød bund
BG_COLOR = (30, 30, 30)           # baggrund

LEVEL_MAP = [
    "................................................................................",
    "................................................................................",
    "......................XXXXX..........................XXXXX......................",
    "......XXXX............................................................XXXX......",
    "...........................XXXXX...............XXXXX............................",
    "XXX..........................................................................XXX",
    ".................XXXX.....................................XXXX..................",
    "..................................XXXXXXXXXXXX..................................",
    "XXXXX......................................................................XXXXX",
    "..........XXXXXX................................................XXXXXX..........",
    ".........................XXXXXX..................XXXXXX.........................",
    "....................................XXXXXXXX....................................",
    ".................XXXX.....................................XXXX..................",
    "XXXXX..................................XX..................................XXXXX",
    "................................................................................",
    ".....XXXXXXX.........XX........XXXXX........XXXXX.......XX..........XXXXXXX.....",
    "................................................................................",
    "...............XXX...........XX....................XX.........XXX...............",
    "..................................XXXXXXXXXXXX..................................",
    "................................................................................"
]

# Dynamisk beregning af rækker/kolonner ud fra LEVEL_MAP
ROWS = len(LEVEL_MAP)
COLUMNS = len(LEVEL_MAP[0])
TILE_WIDTH = SCREEN_WIDTH / COLUMNS
TILE_HEIGHT = SCREEN_HEIGHT / ROWS

# map class
class Map:
    def __init__(self):
        self.platforms = []
        self.ground = None
        self.load_map()

    def load_map(self):
        """Laver platformene ud fra LEVEL_MAP + en rød bund."""
        self.platforms.clear()

        # Byg de blå platforme
        for row_index, row in enumerate(LEVEL_MAP):
            for col_index, tile in enumerate(row):
                if tile == "X":
                    rect = pygame.Rect(col_index * TILE_WIDTH, row_index * TILE_HEIGHT, TILE_WIDTH, TILE_HEIGHT)
                    self.platforms.append(rect)

        # Lav rød bund-platform (hele bunden af skærmen)
        self.ground = pygame.Rect(0, SCREEN_HEIGHT - TILE_HEIGHT, SCREEN_WIDTH, TILE_HEIGHT)

    def draw(self, screen):
        """Tegner platforme og bund på skærmen."""
        pygame.draw.rect(screen, GROUND_COLOR, self.ground)
        for platform in self.platforms:
            pygame.draw.rect(screen, PLATFORM_COLOR, platform)

# player class
class Player(pygame.sprite.Sprite):
    def __init__(self, x, y, image_path, controls):
        super().__init__()
        self.original_image = pygame.image.load(image_path).convert_alpha()
        self.original_image = pygame.transform.scale(self.original_image, (PLAYER_SIZE, PLAYER_SIZE))
        self.image = self.original_image.copy()
        self.rect = self.image.get_rect(center=(x, y))

        self.controls = controls
        self.speed = PLAYER_SPEED
        self.facing_right = True

        # jump and gravity
        self.velocity_y = 0
        self.jump_strength = -15
        self.on_ground = False

    def update(self, pressed_keys, platforms):
        # horizontal movement
        if pressed_keys[self.controls["left"]]:
            self.rect.x -= self.speed
            if self.facing_right:
                self.image = pygame.transform.flip(self.original_image, True, False)
                self.facing_right = False

        if pressed_keys[self.controls["right"]]:
            self.rect.x += self.speed
            if not self.facing_right:
                self.image = self.original_image.copy()
                self.facing_right = True

        # jump
        if pressed_keys[self.controls["up"]] and self.on_ground:
            self.velocity_y = self.jump_strength
            self.on_ground = False

        # gravity
        self.velocity_y += GRAVITY
        self.rect.y += self.velocity_y

        # platform collision
        self.on_ground = False
        for platform in platforms:
            if self.rect.colliderect(platform) and self.velocity_y >=0:
                self.rect.bottom = platform.top
                self.velocity_y = 0
                self.on_ground = True

        # ground collision
        if self.rect.bottom >= SCREEN_HEIGHT:
            self.rect.bottom = SCREEN_HEIGHT
            self.velocity_y = 0
            self.on_ground = True

        # keep inside screen bounds horizontally
        self.rect.x = max(0, min(self.rect.x, SCREEN_WIDTH - PLAYER_SIZE))


# main game function
def main():
    pygame.init()
    screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
    pygame.display.set_caption("Jump man")
    clock = pygame.time.Clock()

    # controls for players
    controls_p1 = {"up": pygame.K_w, "down": pygame.K_s,
                   "left": pygame.K_a, "right": pygame.K_d}
    controls_p2 = {"up": pygame.K_UP, "down": pygame.K_DOWN,
                   "left": pygame.K_LEFT, "right": pygame.K_RIGHT}

    game_map = Map()

    # players with png
    player1 = Player(200, 100, "Boneca Ambalabu.png", controls_p1)
    player2 = Player(600, 100, "Boneca Ambalabu.png", controls_p2)

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
