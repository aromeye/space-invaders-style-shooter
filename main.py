from pygame import *
#from time import time
from random import randint
init()
WIDTH, HEIGHT = 1000, 850
FPS = 120
BACKGROUND = transform.scale(image.load('alpes.png'), (WIDTH, HEIGHT))
ROCKET_IMG = "use_bullet.png"
ENEMY_IMG = "NAVE_TRANSPARENTE.png"
PLAYER_IMG = 'NAVE_2_TRANSPARENTE.png'

#imagenes por si acaso
CAT = 'gato.png'
STONE = 'stone.png'
WOOD = 'tf2_wood_texture'
WIN_SCREEN = transform.scale(image.load('gato.png'), (WIDTH, HEIGHT))

VICTORY_CONDITION = 20
VICTORY_COLOR = 0, 0, 0
score = 0
MAX_SPEED = 15
SPEED = 5
TIME = (SPEED*2)
finish = False
EXPLOSION_SIZE = 90
Ammo_type = 'normal'


#font.init()
#font = pygame.font.Font(None, 36)
#text_surface = font.render("FUCK YOU (not realy lol)", True, (255, 255, 255))
#text_rect = text_surface.get_rect(center=(45, 45))

run = True

window = display.set_mode((WIDTH, HEIGHT))
display.set_caption('shooter')

class GameSprite(sprite.Sprite):

    def __init__(self, player_image, size_x, size_y, player_x, player_y, player_speed, player_HP):
        sprite.Sprite.__init__(self)

        self.image = transform.scale(image.load(player_image), (size_x, size_y))
        self.speed = player_speed
        self.size_y = size_y
        self.size_x = size_x
        self.HP = player_HP

        self.rect = self.image.get_rect()
        self.rect.x = player_x
        self.rect.y = player_y

    def reset(self):
        window.blit(self.image, (self.rect.x, self.rect.y))


class Player(GameSprite):
    def move(self):
        keys = key.get_pressed()
        if keys[K_a] and self.rect.x > 5:
            self.rect.x -= self.speed
        if keys[K_d] and self.rect.x < WIDTH:
            self.rect.x += self.speed
        if keys[K_s] and self.rect.y < (HEIGHT - self.size_y):
            self.rect.y += self.speed
        if keys[K_w] and self.rect.y > (HEIGHT/2):
            self.rect.y -= self.speed

    def shoot(self):
        bullet = Boolet(ROCKET_IMG, 15, 60, self.rect.centerx, self.rect.top, (SPEED*2), 1)
        bullets.add(bullet)
            

class Enemy(GameSprite):
    def update(self):
        self.rect.y += self.speed

        if self.rect.y >= HEIGHT:
            if self.speed <= MAX_SPEED:
                self.speed += 1
            self.rect.y = 0
            self.speed = randint(1, 5 + SPEED)
            self.rect.x = randint(0, WIDTH - 65)

class Ammo(GameSprite):
    def update(self):
        self.rect.y += randint(-5, self.speed)

class Bombs(GameSprite): #basicamente un temporizador xddddddddddddd
    def update(self):
        if self.speed >= 0.5:
            self.speed -= 0.5
        else:
            self.kill()


class Boolet(GameSprite):

    def update(self):
        if self.rect.y <= 0:
            self.kill()

        if Ammo_type != 'afterburn':
            self.rect.y -= self.speed
            if self.speed >= 0:
                self.speed -= (SPEED/40)
            
        if Ammo_type == 'normal' and self.speed <= 0:
            bomb = Bombs('explosion.png', EXPLOSION_SIZE,EXPLOSION_SIZE, (self.rect.centerx - EXPLOSION_SIZE/2), (self.rect.y - self.size_y), 5, -1)
            explosions.add(bomb)
            self.kill()
        elif self.speed <= 0:
            self.kill()

player = Player(PLAYER_IMG, 90, 90, 350, 435, (SPEED*2), -1)
enemies = sprite.Group()
bullets = sprite.Group()
explosions = sprite.Group()

for i in range(1, 6):
    enemy = Enemy(ENEMY_IMG, 65, 80, randint(0, WIDTH - 65), 0, randint(1, 5), 1)
    enemies.add(enemy)

run = True
clock = time.Clock()
while run:
    for e in event.get():
        if e.type == QUIT:
            run = False
        if e.type == KEYDOWN:
            if e.key == K_SPACE:
                player.shoot()

    if not finish:
        #window.blit(text_surface, text_rect)
        #pygame.display.flip()
        window.blit(BACKGROUND, (0, 0))
        explosions.update()
        explosions.draw(window)
        enemies.draw(window)
        enemies.update()
        player.reset()
        player.move()
        bullets.draw(window)
        bullets.update()
        colitions = sprite.groupcollide(enemies, bullets, True, True)
        colitions_2 = sprite.groupcollide(enemies, explosions, True, True)
        for c in colitions:
            enemy = Enemy(ENEMY_IMG, 65, 80, randint(0, WIDTH - 65), 0, randint(1, 5), 1)
            enemies.add(enemy)
            score += 1
            print(score)
        for c in colitions_2:
            enemy = Enemy(ENEMY_IMG, 65, 80, randint(0, WIDTH - 65), 0, randint(1, 5), 1)
            enemies.add(enemy)
            score += 1
            print(score)
        if score == VICTORY_CONDITION:
            finish = True
            window.blit(WIN_SCREEN, (0, 0))
    #window.blit(text_surface, text_rect)
    #pygame.display.flip()
    display.update()
    clock.tick(FPS)
quit()


#