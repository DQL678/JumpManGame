import pygame
import sys

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

        # horizontal collision
        for platform in platforms:
            if self.rect.colliderect(platform):
                if dx > 0:
                    self.rect.right = platform.left
                elif dx < 0:
                    self.rect.left = platform.right

        # jump
        if pressed_keys[self.controls["up"]] and self.on_ground:
            self.velocity_y = self.jump_strength
            self.on_ground = False

        # vertical movement
        self.velocity_y += GRAVITY
        self.rect.y += self.velocity_y

        # vertical collision
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

        # ground collision
        if self.rect.bottom >= SCREEN_HEIGHT:
            self.rect.bottom = SCREEN_HEIGHT
            self.velocity_y = 0
            self.on_ground = True

        # keep inside screen bounds
        self.rect.x = max(0, min(self.rect.x, SCREEN_WIDTH - PLAYER_SIZE))
