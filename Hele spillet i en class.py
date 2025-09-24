import pygame
import sys

# =========================
# constants
# =========================
SCREEN_WIDTH = 1000
SCREEN_HEIGHT = 650
FPS = 60

GRAVITY = 0.8

PLAYER_SIZE = 50
PLAYER_SPEED = 7

# Farver
WHITE = (255, 255, 255)
PLATFORM_COLOR = (100, 100, 255)  # blå platforme
GROUND_COLOR = (200, 50, 50)      # rød bund
BG_COLOR = (30, 30, 30)           # baggrund
BTN_BG = (60, 60, 60)
BTN_BG_HOVER = (90, 90, 90)

# =========================
# LEVEL MAP
# =========================
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


# =========================
# Map class
# =========================
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
                    rect = pygame.Rect(
                        col_index * TILE_WIDTH,
                        row_index * TILE_HEIGHT,
                        TILE_WIDTH,
                        TILE_HEIGHT
                    )
                    self.platforms.append(rect)

        # Lav rød bund-platform (hele bunden af skærmen)
        self.ground = pygame.Rect(0, SCREEN_HEIGHT - TILE_HEIGHT, SCREEN_WIDTH, TILE_HEIGHT)

    def draw(self, screen):
        """Tegner platforme og bund på skærmen."""
        pygame.draw.rect(screen, GROUND_COLOR, self.ground)
        for platform in self.platforms:
            pygame.draw.rect(screen, PLATFORM_COLOR, platform)


# =========================
# Player class
# =========================
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
            if self.rect.colliderect(platform) and self.velocity_y >= 0:
                self.rect.bottom = platform.top
                self.velocity_y = 0
                self.on_ground = True

        # ground collision (failsafe hvis ingen platforme under)
        if self.rect.bottom >= SCREEN_HEIGHT:
            self.rect.bottom = SCREEN_HEIGHT
            self.velocity_y = 0
            self.on_ground = True

        # keep inside screen bounds horizontally
        self.rect.x = max(0, min(self.rect.x, SCREEN_WIDTH - PLAYER_SIZE))


# =========================
# Start screen
# =========================
def show_start_screen(screen, clock):
    pygame.font.init()
    title_font = pygame.font.SysFont(None, 72)
    text_font = pygame.font.SysFont(None, 28)
    btn_font = pygame.font.SysFont(None, 36)

    title_surf = title_font.render("Bomber Jumper", True, WHITE)

    instructions = [
        "Instruktioner:",
        "Spiller 1: A/D for at gå, W for at hoppe",
        "Spiller 2: Venstre/Højre for at gå, Pil op for at hoppe",
        "",
        "Mål: Spræng platforme (senere) og få modstanderen til at falde!",
        "Første spiller til at vinde 3 runder vinder kampen.",
        "",
        "Tryk ENTER eller SPACE for at starte",
        "eller klik på knappen nedenfor."
    ]

    # Beregn hvor teksten ender
    start_y = SCREEN_HEIGHT // 2 - 60
    line_height = 28
    end_y = start_y + len(instructions) * line_height

    # Start-knap under teksten
    btn_width, btn_height = 220, 60
    btn_rect = pygame.Rect(0, 0, btn_width, btn_height)
    btn_rect.center = (SCREEN_WIDTH // 2, end_y + 50)  # 50 px under teksten

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit(); sys.exit()
            elif event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                if btn_rect.collidepoint(event.pos):
                    return
            elif event.type == pygame.KEYDOWN:
                if event.key in (pygame.K_RETURN, pygame.K_SPACE):
                    return

        # Baggrund
        screen.fill(BG_COLOR)

        # Titel
        title_pos = title_surf.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2 - 120))
        screen.blit(title_surf, title_pos)

        # Instruktions-tekst
        y = start_y
        for line in instructions:
            surf = text_font.render(line, True, WHITE)
            rect = surf.get_rect(center=(SCREEN_WIDTH // 2, y))
            screen.blit(surf, rect)
            y += line_height

        # Knappen (hover)
        mouse_pos = pygame.mouse.get_pos()
        hovered = btn_rect.collidepoint(mouse_pos)
        pygame.draw.rect(screen, BTN_BG_HOVER if hovered else BTN_BG, btn_rect, border_radius=12)
        btn_text = btn_font.render("START", True, WHITE)
        btn_text_rect = btn_text.get_rect(center=btn_rect.center)
        screen.blit(btn_text, btn_text_rect)

        pygame.display.flip()
        clock.tick(FPS)

# =========================
# main game function
# =========================
def main():
    pygame.init()
    screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
    pygame.display.set_caption("Bomber Jumper")
    clock = pygame.time.Clock()

    # 1) Vis startskærm
    show_start_screen(screen, clock)

    # 2) Init spillet
    controls_p1 = {"up": pygame.K_w, "down": pygame.K_s, "left": pygame.K_a, "right": pygame.K_d}
    controls_p2 = {"up": pygame.K_UP, "down": pygame.K_DOWN, "left": pygame.K_LEFT, "right": pygame.K_RIGHT}

    game_map = Map()

    # Husk at pege på faktiske billedfiler
    player1 = Player(200, 100, "Boneca Ambalabu.png", controls_p1)
    player2 = Player(800, 100, "Boneca Ambalabu.png", controls_p2)

    all_sprites = pygame.sprite.Group(player1, player2)

    # 3) Game loop
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit(); sys.exit()

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
