import pygame
import random

from pygame.locals import (
    #RLEACCEL,
    K_UP,
    K_DOWN,
    K_LEFT,
    K_RIGHT,
    K_w,
    K_a,
    K_s,
    K_d,
    K_ESCAPE,
    KEYDOWN,
    QUIT,
)

SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600

#Custom Events:
ADDENEMY = pygame.USEREVENT + 1
pygame.time.set_timer(ADDENEMY, 250)

class Player(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.surf = pygame.Surface((75, 25))
        self.surf.fill((0, 0, 0))
        self.rect = self.surf.get_rect()

    def update(self, keys):
        if keys[K_UP] or keys[K_w]:
            self.rect.move_ip(0, -8)
        if keys[K_DOWN] or keys[K_s]:
            self.rect.move_ip(0, 8)
        if keys[K_LEFT] or keys[K_a]:
            self.rect.move_ip(-8, 0)
        if keys[K_RIGHT] or keys[K_d]:
            self.rect.move_ip(8, 0)

        # Keep player on the screen
        if self.rect.left < 0:
            self.rect.left = 0
        if self.rect.right > SCREEN_WIDTH:
            self.rect.right = SCREEN_WIDTH
        if self.rect.top <= 0:
            self.rect.top = 0
        if self.rect.bottom >= SCREEN_HEIGHT:
            self.rect.bottom = SCREEN_HEIGHT


class Enemy(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.surf = pygame.Surface((20, 10))
        self.surf.fill((255, 120, 120))
        self.rect = self.surf.get_rect(
            center=(
                random.randint(SCREEN_WIDTH + 20, SCREEN_WIDTH + 100),
                random.randint(0, SCREEN_HEIGHT),
            )
        )
        self.speed = random.randint(5, 20)

    # Move the sprite based on speed
    # Remove the sprite when it passes the left edge of the screen
    def update(self):
        self.rect.move_ip(-self.speed, 0)
        if self.rect.right < 0:
            self.kill()


#############
pygame.init()

screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
#bg_texture = pygame.image.load("bg_texture.bmp").convert()
#bg_texture = pygame.transform.scale(bg_texture, (SCREEN_WIDTH, SCREEN_HEIGHT))
#bg_texture.set_colorkey((0,0,0), RLEACCEL)
#bg_rect = bg_texture.get_rect()

player = Player()

enemies = pygame.sprite.Group()
all_sprites = pygame.sprite.Group()

all_sprites.add(player)

# Event Loop:
clock = pygame.time.Clock()

running = True
while running:
    screen.fill((200, 200, 200))
    #screen.blit(bg_texture, bg_rect)

    for event in pygame.event.get():
        if event.type == KEYDOWN:
            if event.key == K_ESCAPE:
                running = False

        elif event.type == QUIT:
            running = False

        elif event.type == ADDENEMY:
            new_enemy = Enemy()
            enemies.add(new_enemy)
            all_sprites.add(new_enemy)

    pressed_keys = pygame.key.get_pressed()
    player.update(pressed_keys)
    enemies.update()

    for entity in all_sprites:
        screen.blit(entity.surf, entity.rect)

    if pygame.sprite.spritecollideany(player, enemies):
        player.kill()
        running = False
        print("You Died.")

    pygame.display.flip()

    clock.tick(60)