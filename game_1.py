import pygame
import random

#billentyűmozgatás importálása
from pygame.locals import (
    RLEACCEL,
    K_DOWN,
    K_ESCAPE,
    KEYDOWN,
    K_LEFT,
    K_RIGHT,
    K_UP,
    K_SPACE,
    QUIT,
)
#pygame könyvtár inicializálása
pygame.init()

#Player osztály deklarálása, méret-szín-alak
class Player(pygame.sprite.Sprite):
    def __init__(self):
        super(Player, self).__init__()
        self.surf = pygame.Surface((50,20))
        self.surf.fill((14,255,124))
        self.rect = self.surf.get_rect()

    #Mozgatás függvény
    def update(self, pressed_keys):
        if(pressed_keys[K_UP]):
            self.rect.move_ip(0,-8)
        if(pressed_keys[K_DOWN]):
            self.rect.move_ip(0,8)
        if(pressed_keys[K_LEFT]):
            self.rect.move_ip(-8,0)
        if(pressed_keys[K_RIGHT]):
            self.rect.move_ip(8,0)

        #Bullet
        if(pressed_keys[K_SPACE]):
            new_bullet = Bullet()
            bullets.add(new_bullet)

        #Képernyőn tartás
        if(self.rect.left < 0):
            self.rect.left = 0
        if(self.rect.right > SCREEN_WIDTH):
            self.rect.right = SCREEN_WIDTH
        if(self.rect.bottom > SCREEN_HEIGHT):
            self.rect.bottom = SCREEN_HEIGHT
        if(self.rect.top < 0):
            self.rect.top = 0;

class Enemy(pygame.sprite.Sprite):
    def __init__(self):
        super(Enemy, self).__init__()
        self.surf = pygame.Surface((20, 10))
        self.surf.fill((255, 50, 50))
        self.rect = self.surf.get_rect(
            center=(
                random.randint(SCREEN_WIDTH + 20, SCREEN_WIDTH + 100),
                random.randint(0, SCREEN_HEIGHT),
            )
        )
        self.speed = random.randint(10, 50)

    def update(self):
        self.rect.move_ip(-self.speed, 0)
        if(self.rect.right < 0):
            self.kill()  

class Bullet(pygame.sprite.Sprite):
    def __init__(self):
        super(Bullet, self).__init__()
        self.surf = pygame.Surface((5,5))
        self.surf.fill((255,255,255))
        self.rect = self.surf.get_rect()  
        self.rect.center = player.rect.center
        self.speed = 10

    def update(self):
        self.rect.move_ip(self.speed, 0)
        if(self.rect.left > SCREEN_WIDTH):
            self.kill()

#képernyő méreteinek delvétele, illetve ablak cím
SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("Gameszkó")

#Ellenség hozzáadás event készítése
ADDENEMY = pygame.USEREVENT + 1
pygame.time.set_timer(ADDENEMY, 1000)

#player objektum Player osztályból
player = Player()


#Sprite group létrehozása
enemies = pygame.sprite.Group()
all_sprites = pygame.sprite.Group()
all_sprites.add(player)


#Lövedék
bullets = pygame.sprite.Group()

#Lövedékevent
ADDBULLET = pygame.USEREVENT + 1
pygame.time.set_timer(ADDBULLET, 250)

clock = pygame.time.Clock()

running = True

while running:
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
        elif event.type == ADDBULLET:
            new_bullet = Bullet()
            bullets.add(new_bullet)





    pressed_keys = pygame.key.get_pressed()

    player.update(pressed_keys)
    enemies.update()
    bullets.update()
    
  
    screen.fill((0, 0, 0))


    for entity in all_sprites:
        screen.blit(entity.surf, entity.rect)

        if pygame.sprite.spritecollideany(player, enemies):
            player.kill()
            running = False


    bullets.draw(screen)


    
    pygame.display.flip()
    clock.tick(30)
    
pygame.quit()