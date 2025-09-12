import pygame
import sys

# Skærmstørrelse
SCREEN_WIDTH = 1000
SCREEN_HEIGHT = 800

# Farver
PLATFORM_COLOR = (100, 100, 255)  # blå platforme
GROUND_COLOR = (200, 50, 50)      # rød bund
BG_COLOR = (30, 30, 30)           # baggrund

# Map layout (2D array)
# X = platform, . = tomt rum
LEVEL_MAP = [
    "................................................................................",
    "XX................................XXXXXXXXXXXX................................XX",
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


# Test
if __name__ == "__main__":
    pygame.init()
    screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
    pygame.display.set_caption("Map Generator Test")
    clock = pygame.time.Clock()

    game_map = Map()

    while True:
        screen.fill(BG_COLOR)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

        game_map.draw(screen)
        pygame.display.flip()
        clock.tick(60)
