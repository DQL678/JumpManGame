import pygame
import sys

# --- Constants ---
SCREEN_WIDTH = 1000
SCREEN_HEIGHT = 650
FPS = 60

GRAVITY = 0.8

PLAYER_SIZE = 150
PLAYER_SPEED = 15
WHITE = (255, 255, 255)

# --- Player class ---
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

        # Jump and gravity
        self.velocity_y = 0
        self.jump_strength = -20
        self.on_ground = False

    def update(self, pressed_keys):
        # Horizontal movement
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

        # Jump
        if pressed_keys[self.controls["up"]] and self.on_ground:
            self.velocity_y = self.jump_strength
            self.on_ground = False

        # Apply gravity
        self.velocity_y += GRAVITY
        self.rect.y += self.velocity_y

        # Ground collision
        if self.rect.bottom >= SCREEN_HEIGHT:
            self.rect.bottom = SCREEN_HEIGHT
            self.velocity_y = 0
            self.on_ground = True

        # Keep inside screen bounds horizontally
        self.rect.x = max(0, min(self.rect.x, SCREEN_WIDTH - PLAYER_SIZE))


# --- Main game function ---
def main():
    pygame.init()
    screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
    pygame.display.set_caption("Jump man")
    clock = pygame.time.Clock()

    # Define controls for players
    controls_p1 = {"up": pygame.K_w, "down": pygame.K_s,
                   "left": pygame.K_a, "right": pygame.K_d}
    controls_p2 = {"up": pygame.K_UP, "down": pygame.K_DOWN,
                   "left": pygame.K_LEFT, "right": pygame.K_RIGHT}

    # Create players using PNG image
    player1 = Player(200, 300, "Boneca Ambalabu.png", controls_p1)
    player2 = Player(600, 300, "Boneca Ambalabu.png", controls_p2)

    all_sprites = pygame.sprite.Group(player1, player2)

    # Game loop
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

        pressed_keys = pygame.key.get_pressed()
        all_sprites.update(pressed_keys)

        # Example collision check
        if player1.rect.colliderect(player2.rect):
            print("Collision!")

        screen.fill(WHITE)
        all_sprites.draw(screen)

        pygame.display.flip()
        clock.tick(FPS)


if __name__ == "__main__":
    main()
