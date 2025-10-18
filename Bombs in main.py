import pygame
import sys

# Konstanter
SCREEN_WIDTH = 1000
SCREEN_HEIGHT = 650
FPS = 60
GRAVITY = 0.9
PLAYER_SIZE = 50
PLAYER_SPEED = 4
BOMB_SIZE = 10
BOMB_SPEED = 3 # Pixels per frame
EXPLOSION_RADIUS = 30
BOMB_TIMER = 3000  # Millisekunder før eksplosion

# Farver
WHITE = (255, 255, 255)
PLATFORM_COLOR = (100, 100, 255)
GROUND_COLOR = (200, 50, 50)
BG_COLOR = (30, 30, 30)
BTN_BG = (60, 60, 60)
BTN_BG_HOVER = (90, 90, 90)
ORANGE = (255, 165, 0)

# LEVEL MAP
LEVEL_MAP = [
    "................................................................................",
    "................XXXX........................................XXXX................",
    "..........................XXXXXXXX............XXXXXXXX..........................",
    ".........XXXX......................................................XXXX.........",
    "XXX..........................................................................XXX",
    ".................XXXXXXXX..............................XXXXXXXX.................",
    "................................................................................",
    "...XXXXXX.........................XXXXXXXXXXXX.........................XXXXXX...",
    "................................................................................",
    ".............XXXXXXXX......................................XXXXXXXX.............",
    "..........XXXX................XXXX............XXXX................XXXX..........",
    "................................XXXX........XXXX................................",
    ".....................XXXXXXXX......................XXXXXXXX.....................",
    "XXXXXXXX................................................................XXXXXXXX",
    "....................................XXXXXXX.....................................",
    "................................................................................",
    "XXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX",
    "................................................................................",
    "XXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX",
    "................................................................................"
]

ROWS = len(LEVEL_MAP)
COLUMNS = len(LEVEL_MAP[0])
TILE_WIDTH = SCREEN_WIDTH / COLUMNS
TILE_HEIGHT = SCREEN_HEIGHT / ROWS


# STARTSKÆRM
def show_start_screen(screen, clock):
    pygame.font.init()
    title_font = pygame.font.SysFont(None, 72)
    text_font = pygame.font.SysFont(None, 28)
    btn_font = pygame.font.SysFont(None, 36)

    title_surf = title_font.render("Bomber Jumper", True, WHITE)

    instructions = [
        "Instruktioner:",
        "Spiller 1: A/D for at gå, W for at hoppe, LSHIFT for at smide bomber",
        "Spiller 2: Venstre/Højre for at gå, Pil op for at hoppe, RCTRL for at smide bomber",
        "",
        "Mål: Ramme modstanderen med bombe eller få dem til at at falde ned fra banen.",
        "Første spiller til at nå 3 point vinder.",
        "",
        "Tryk ENTER eller SPACE for at starte",
        "eller klik på knappen nedenfor."
    ]

    start_y = SCREEN_HEIGHT // 2 - 60
    line_height = 28
    end_y = start_y + len(instructions) * line_height

    btn_width, btn_height = 220, 60
    btn_rect = pygame.Rect(0, 0, btn_width, btn_height)
    btn_rect.center = (SCREEN_WIDTH // 2, end_y + 50)

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

        screen.fill(BG_COLOR)

        title_pos = title_surf.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2 - 120))
        screen.blit(title_surf, title_pos)

        y = start_y
        for line in instructions:
            surf = text_font.render(line, True, WHITE)
            rect = surf.get_rect(center=(SCREEN_WIDTH // 2, y))
            screen.blit(surf, rect)
            y += line_height

        mouse_pos = pygame.mouse.get_pos()
        hovered = btn_rect.collidepoint(mouse_pos)
        pygame.draw.rect(screen, BTN_BG_HOVER if hovered else BTN_BG, btn_rect, border_radius=12)
        btn_text = btn_font.render("START", True, WHITE)
        btn_text_rect = btn_text.get_rect(center=btn_rect.center)
        screen.blit(btn_text, btn_text_rect)

        pygame.display.flip()
        clock.tick(FPS)


# MAP
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


# BOMB
class Bomb(pygame.sprite.Sprite):
    def __init__(self, x, y, image, game_map, players):
        super().__init__()
        self.image = pygame.transform.scale(image, (BOMB_SIZE * 2, BOMB_SIZE * 2))
        self.rect = self.image.get_rect(center=(x, y))
        self.spawn_time = pygame.time.get_ticks()
        self.exploded = False
        self.explosion_time = 0
        self.game_map = game_map
        self.players = players

    def update(self):
        current_time = pygame.time.get_ticks()

        if not self.exploded:
            # Bombe falder
            self.rect.y += BOMB_SPEED

            # Stopper ovenpå platform eller ground
            for platform in self.game_map.platforms + [self.game_map.ground]:
                if self.rect.colliderect(platform):
                    self.rect.bottom = platform.top
                    break
            # Eksploderer bomben hvis timeren er gået
            if current_time - self.spawn_time >= BOMB_TIMER:
                self.explode()
        else:
            # Eksplosion fjernes efter 1 sekund
            if current_time - self.explosion_time >= 1000:
                self.kill()

    def explode(self):
        self.exploded = True
        self.explosion_time = pygame.time.get_ticks()

        # Tegn explosion
        self.image = pygame.Surface((EXPLOSION_RADIUS * 2, EXPLOSION_RADIUS * 2), pygame.SRCALPHA)
        pygame.draw.circle(self.image, ORANGE, (EXPLOSION_RADIUS, EXPLOSION_RADIUS), EXPLOSION_RADIUS)
        self.rect = self.image.get_rect(center=self.rect.center)

        # Updateret platform array
        new_platforms = []
        explosion_area = pygame.Rect(
            self.rect.centerx - EXPLOSION_RADIUS, self.rect.centery - EXPLOSION_RADIUS,
            EXPLOSION_RADIUS * 2, EXPLOSION_RADIUS * 2)

        # Loop gennem alle platforme
        for platform in self.game_map.platforms:
            # Hvis eksplosion kollidere med platform skippes den.
            if platform.colliderect(explosion_area):
                continue
            # Hvis den ikke gør det tilføj den til det nye array
            new_platforms.append(platform)
        # Updateres til det nye platform array
        self.game_map.platforms = new_platforms

        for player in self.players:
            if self.rect.colliderect(player.rect):
                player.opponent.score += 1
                player.respawn()


# PLAYER
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

        self.drop_cooldown = 0

        self.opponent = None

    def update(self, pressed_keys, game_map, ground, opponent, bombs_group, bomb_img, players):
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

        for platform in game_map.platforms:
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
        for platform in game_map.platforms:
            if self.rect.colliderect(platform):
                if self.velocity_y > 0:
                    self.rect.bottom = platform.top
                    self.velocity_y = 0
                    self.on_ground = True
                elif self.velocity_y < 0:
                    self.rect.top = platform.bottom
                    self.velocity_y = 0

        if self.rect.colliderect(ground):
            opponent.score += 1
            self.respawn()

        # Drop bombe
        if "drop" in self.controls and pressed_keys[self.controls["drop"]] and self.drop_cooldown == 0:
            # Bombe oprettes
            bomb = Bomb(self.rect.centerx, self.rect.bottom, bomb_img, game_map, players)
            bombs_group.add(bomb)
            # Vent 100 frames for at kunne droppe en bombe mere (forhindrer bombe spam)
            self.drop_cooldown = 50

        # Cooldown timer
        if self.drop_cooldown > 0:
            self.drop_cooldown -= 1

        # Borders/Vægge
        self.rect.x = max(0, min(self.rect.x, SCREEN_WIDTH - PLAYER_SIZE))

    def respawn(self):
        self.rect.center = (self.start_x, self.start_y)
        self.velocity_y = 0


# MAIN
def main():
    pygame.init()
    screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
    pygame.display.set_caption("Jump Man")
    clock = pygame.time.Clock()

    # Først startskærm
    show_start_screen(screen, clock)

    # Controls
    controls_p1 = {"up": pygame.K_w, "left": pygame.K_a, "right": pygame.K_d, "drop": pygame.K_LSHIFT}
    controls_p2 = {"up": pygame.K_UP, "left": pygame.K_LEFT, "right": pygame.K_RIGHT, "drop": pygame.K_RCTRL}

    game_map = Map()

    # Load images
    bomb_img = pygame.image.load("bombeRealistic.png").convert_alpha()
    player1 = Player(200, 100, "Boneca Ambalabu.png", controls_p1)
    player2 = Player(600, 100, "Frigo Camelo.png", controls_p2)

    player1.opponent = player2
    player2.opponent = player1
    players = [player1, player2]

    all_sprites = pygame.sprite.Group(player1, player2)
    bombs_group = pygame.sprite.Group()
    font = pygame.font.SysFont(None, 36)

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit(); sys.exit()

        pressed_keys = pygame.key.get_pressed()

        ground = game_map.ground
        platforms = game_map.platforms

        player1.update(pressed_keys, game_map, ground, player2, bombs_group, bomb_img, players)
        player2.update(pressed_keys, game_map, ground, player1, bombs_group, bomb_img, players)

        bombs_group.update()

        screen.fill(BG_COLOR)
        game_map.draw(screen)
        all_sprites.draw(screen)
        bombs_group.draw(screen)

        score_text_p1 = font.render(f"P1 Score: {player1.score}", True, WHITE)
        score_text_p2 = font.render(f"P2 Score: {player2.score}", True, WHITE)

        screen.blit(score_text_p1, (10, 10))
        screen.blit(score_text_p2, (SCREEN_WIDTH - 140, 10))

        if player1.score >= 3 or player2.score >= 3:
            winner = "Spiller 1" if player1.score >= 3 else "Spiller 2"
            win_text = font.render(f"{winner} vinder!", True, WHITE)
            screen.blit(win_text, (SCREEN_WIDTH // 2 - 100, SCREEN_HEIGHT - 500))
            pygame.display.flip()
            pygame.time.wait(1500)
            show_start_screen(screen, clock)
            player1.score = 0
            player2.score = 0
            player1.respawn()
            player2.respawn()
            game_map.load_map()
            bombs_group.empty()

        pygame.display.flip()
        clock.tick(FPS)


if __name__ == "__main__":
    main()
