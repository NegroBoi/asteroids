from random import *
from pygame import *

w, h = 700, 500
window = display.set_mode((w, h))

display.set_caption("Астероидс")

clock = time.Clock()
game = True
finish = False

class GameSprite(sprite.Sprite):
    def __init__(self, pImage, pX, pY, sizeX, sizeY, pSpeed):
        sprite.Sprite.__init__(self)
        self.image = transform.scale(image.load(pImage), (sizeX, sizeY))
        self.speed = pSpeed
        self.rect = self.image.get_rect()
        self.rect.x = pX
        self.rect.y = pY
    
    def draw(self):
        window.blit(self.image, (self.rect.x, self.rect.y))

class Player(GameSprite):
    def update(self):
        keys = key.get_pressed()
        if keys[K_LEFT]:
            self.rect.x -= self.speed
        if keys[K_RIGHT]:
            self.rect.x += self.speed
    def fire(self):
        bullet = Bullet('bullet.png', self.rect.centerx-20, self.rect.top, 40, 80, -15)
        bullets.add(bullet)

bullets = sprite.Group()

class Bullet(GameSprite):
    def update(self):
        self.rect.y += self.speed
        if self.rect.y < 0:
            self.kill()

mixer.init()
mixer.music.load("space.ogg")

lost = 0
class Enemy(GameSprite):
    def update(self):
        self.rect.y += self.speed
        global lost
        global hearts
        if self.rect.y > h:
            try:
                hearts.pop(0)
            except:
                ...
            self.rect.x = randint(0, w-80)
            self.rect.y = 0
            lost += 1

bg = transform.scale(image.load("fon.jpg"), (w, h))

ship = Player("da.png", 10, h-100, 70, 130, 4)

asteroids = sprite.Group()
for i in range(6):
    randpic = randint(1,2)
    if randpic == 1:
        pic = "net.png"
    if randpic == 2:
        pic = "ga.png"
    asteroid = Enemy(pic, randint(10, w-50), -40, 50, 50, 
                     randint(1, 2))
    asteroids.add(asteroid)

score = 0
font.init()
mainfont = font.SysFont("Arial", 40)

reload_time = False
num_fire = 0
from time import time as timer

lives = 10
hearts = []
hX = 300

for i in range(lives):
    heart = GameSprite("serce.png", hX, 10, 30, 30, 0)
    hearts.append(heart)
    hX += 40

restart = GameSprite("puk.png", 200, 200, 200, 120, 0)

def gameloop():
    global game, finish, score, reload_time, num_fire, lost, hearts
    while game:
        for e in event.get():
            if e.type == QUIT:
                game = False
            if e.type == KEYDOWN:
                if e.key == K_SPACE:
                    if num_fire < 5 and reload_time == False:
                        ship.fire()
                        num_fire += 1
                    if num_fire >= 5 and reload_time == False:
                        reload_start = timer()
                        reload_time = True
            if e.type == MOUSEBUTTONDOWN and e.button == 1:
                x, y = e.pos
                if restart.rect.collidepoint(x, y):
                    for a in asteroids:
                        a.rect.y = -100
                        a.rect.x = randint(0, w-100)
                    finish, lost, score = 0, 0, 0
                    lives = 10
                    hearts = []
                    hX = 300
                    for i in range(lives):
                        heart = GameSprite("serce.png", hX, 10, 40 ,38, 0)
                        hearts.append(heart)
                        hX += 30
                    

        if not finish:
            window.blit(bg, (0, 0))
            score_text = mainfont.render("killed: " + str(score), True, (50, 205, 200))
            lost_text = mainfont.render("missing: " + str(lost), True, (50, 205, 200))
            window.blit(score_text, (5, 10))
            window.blit(lost_text, (5, 50))
            ship.draw()
            ship.update()
            asteroids.draw(window)
            asteroids.update()
            bullets.draw(window)
            bullets.update()

            collides = sprite.groupcollide(bullets, asteroids, True, True)
            for c in collides:
                score += 1
                randpic = randint(1,2)
                if randpic == 1:
                    pic = "net.png"
                if randpic == 2:
                    pic = "ga.png"
                asteroid = Enemy(pic, randint(10, w-50), -40, 50, 50, 
                                 randint(1, 5))
                asteroids.add(asteroid)

            if reload_time:
                reload_end = timer()
                if reload_end - reload_start < 3:
                    reload = mainfont.render("RELOADING", True, (50, 205, 200))
                    window.blit(reload, (250, 200))
                else:
                    num_fire = 0
                    reload_time = False

            if sprite.spritecollide(ship, asteroids, False):
                reload = mainfont.render("TI PROIGRAL NEMOSH", True, (50, 205, 200))
                window.blit(reload, (180, 150))
                finish = True

            for heart in hearts:
                heart.draw()

            if len(hearts) <= 0:
                restart.draw()
                reload = mainfont.render("TI PROIGRAL NEMOSH", True, (50, 205, 200))
                window.blit(reload, (180, 150))
                finish = True

        display.update()
        clock.tick(60)

gameloop()