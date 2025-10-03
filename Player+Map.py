import pygame
import sys

# konstanter
SCREEN_WIDTH = 1000
SCREEN_HEIGHT = 650
FPS = 60
GRAVITY = 0.9
PLAYER_SIZE = 50
PLAYER_SPEED = 4

# farver
WHITE = (255, 255, 255)
PLATFORM_COLOR = (100, 100, 255)
GROUND_COLOR = (200, 50, 50)
BG_COLOR = (30, 30, 30)

LEVEL_MAP = [
    "................................................................................",
    "................................................................................",
    "........................XXX................................XXXXX................",
    ".........XXXX........XXXXXX................XXXXX......................XXX.......",
    "........XXXXX...................................................................",
    "......XXX.....................................................................XX",
    ".................XXXXX....................................XXXX..................",
    "..................................XXXXXXXXXXXX..................................",
    "XXXXX.......................................................................XXXX",
    "..................................................XXXXXXX........XXXXXX.........",
    "...........XXXXXX........XXXXXX.................................................",
    "....................................XXXXXXXX....................................",
    "...................................XXXXXXXXX..............XXXX............XXXXXX",
    "XXXXX............XXXX............XXXXX..........................................",
    "................................................................................",
    "............................................XXXXX...................XXXXXXX.....",
    ".....XXXXXXX..............XXXX..................................................",
    "......................................................XXXXXXXX..................",
    ".................XXXX.............XXXXXXXXXXXX..................................",
    "................................................................................"
]

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
        self.platforms.clear()
        for row_index, row in enumerate(LEVEL_MAP):
            for col_index, tile in enumerate(row):
                if tile == "X":
                    rect = pygame.Rect(col_index * TILE_WIDTH, row_index * TILE_HEIGHT, TILE_WIDTH, TILE_HEIGHT)
                    self.platforms.append(rect)
        self.ground = pygame.Rect(0, SCREEN_HEIGHT - TILE_HEIGHT, SCREEN_WIDTH, TILE_HEIGHT)

    def draw(self, screen):
        pygame.draw.rect(screen, GROUND_COLOR, self.ground)
        for platform in self.platforms:
            pygame.draw.rect(screen, PLATFORM_COLOR, platform)

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

        self.velocity_y = 0
        self.jump_strength = -15
        self.on_ground = False

        self.score = 0
        self.start_x = x
        self.start_y = y

    def update(self, pressed_keys, platforms, ground, opponent):
        dx = 0
        if pressed_keys[self.controls["left"]]:
            dx = -self.speed
            if self.facing_right:
                self.image = pygame.transform.flip(self.original_image, True, False)
                self.facing_right = False
        if pressed_keys[self.controls["right"]]:
            dx = self.speed
            if not self.facing_right:
                self.image = self.original_image.copy()
                self.facing_right = True

        self.rect.x += dx

        for platform in platforms:
            if self.rect.colliderect(platform):
                if dx > 0:
                    self.rect.right = platform.left
                elif dx < 0:
                    self.rect.left = platform.right

        if pressed_keys[self.controls["up"]] and self.on_ground:
            self.velocity_y = self.jump_strength
            self.on_ground = False

        self.velocity_y += GRAVITY
        self.rect.y += self.velocity_y

        self.on_ground = False
        for platform in platforms:
            if self.rect.colliderect(platform):
                if self.velocity_y > 0:
                    self.rect.bottom = platform.top
                    self.velocity_y = 0
                    self.on_ground = True
                elif self.velocity_y < 0:
                    self.rect.top = platform.bottom
                    self.velocity_y = 0

        # modstanderen får point ved bund kollision
        if self.rect.colliderect(ground):
            opponent.score += 1
            self.respawn()

        self.rect.x = max(0, min(self.rect.x, SCREEN_WIDTH - PLAYER_SIZE))

    def respawn(self):
        self.rect.center = (self.start_x, self.start_y)
        self.velocity_y = 0

def main():
    pygame.init()
    screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
    pygame.display.set_caption("Jump man")
    clock = pygame.time.Clock()

    controls_p1 = {"up": pygame.K_w, "down": pygame.K_s,
                   "left": pygame.K_a, "right": pygame.K_d}
    controls_p2 = {"up": pygame.K_UP, "down": pygame.K_DOWN,
                   "left": pygame.K_LEFT, "right": pygame.K_RIGHT}

    game_map = Map()

    player1 = Player(200, 100, "Boneca Ambalabu.png", controls_p1)
    player2 = Player(600, 100, "Frigo Camelo.png", controls_p2)

    all_sprites = pygame.sprite.Group(player1, player2)
    font = pygame.font.SysFont(None, 36)

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

        pressed_keys = pygame.key.get_pressed()

        platforms = game_map.platforms
        ground = game_map.ground

        player1.update(pressed_keys, platforms, ground, player2)
        player2.update(pressed_keys, platforms, ground, player1)

        screen.fill(BG_COLOR)
        game_map.draw(screen)
        all_sprites.draw(screen)

        score_text_p1 = font.render(f"P1 Score: {player1.score}", True, WHITE)
        score_text_p2 = font.render(f"P2 Score: {player2.score}", True, WHITE)

        screen.blit(score_text_p1, (10, 10))
        screen.blit(score_text_p2, (SCREEN_WIDTH - 200, 10))

        pygame.display.flip()
        clock.tick(FPS)

if __name__ == "__main__":
    main()
