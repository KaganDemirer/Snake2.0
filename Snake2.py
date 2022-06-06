import pygame
import math
import random

# window size 600x600
WIDTH = 600
HEIGHT = 600

pygame.init()
pygame.display.set_caption("Snake 2.0")
screen = pygame.display.set_mode((WIDTH, HEIGHT))

players = []
foods = []


class Snake:
    def __init__(self, x, y, team, color):
        self.x = x
        self.y = y
        self.team = team
        self.color = color
        self.direction = 0
        self.body = [[x, y]]
        self.add = 30

    def draw(self):
        for i in self.body:
            pygame.draw.circle(screen, self.color, (int(i[0]), int(i[1])), 5)

    def move(self):
        self.x += math.sin(math.radians(self.direction))
        self.y += math.cos(math.radians(self.direction))
        if self.add == 0:
            self.body.pop()
        else:
            self.add -= 1
        if self.x < 0:
            self.x = WIDTH
        if self.x > WIDTH:
            self.x = 0
        if self.y < 0:
            self.y = HEIGHT
        if self.y > HEIGHT:
            self.y = 0
        self.body.insert(0, [self.x, self.y])
        for food in foods:
            if self.x >= food.x-6 and self.x <= food.x+6 and self.y >= food.y-6 and self.y <= food.y+6:
                self.eat(food)
        if self.check_collision():
            players.remove(self)
            players.append(Snake(random.randint(0, WIDTH), random.randint(0, HEIGHT), self.team, self.color))
            
    def eat(self, food):
        self.add += random.randint(1,7)
        food.x = random.randint(0, WIDTH)
        food.y = random.randint(0, HEIGHT)

    def check_collision(self):
        for player in players:
            if player.team != self.team:
                for i in range(len(player.body)):
                    if self.x >= player.body[i][0]-3 and self.x <= player.body[i][0]+3 and self.y >= player.body[i][1]-3 and self.y <= player.body[i][1]+3:
                        return True
        return False

class Food:
    def __init__(self, x, y, color):
        self.x = x
        self.y = y
        self.color = color

    def draw(self):
        pygame.draw.circle(screen, self.color, (int(self.x), int(self.y)), 3)


def spawn_snakes():
    global players
    players.append(Snake(100, 300, 1, (255, 0, 0)))
    players.append(Snake(500, 300, 2, (0, 255, 0)))

def spawn_food():
    global foods
    foods.append(Food(random.randint(0, WIDTH), random.randint(0, HEIGHT), (random.randint(0, 255), random.randint(0, 255), random.randint(0, 255))))

spawn_snakes()


running = True
stop = False
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
    keys=pygame.key.get_pressed()
    if stop == False:
        for player in players:
            if keys[pygame.K_RIGHT]:
                if player.team == 1:
                    player.direction -= 2
            if keys[pygame.K_LEFT]:
                if player.team == 1:
                    player.direction += 2
            if keys[pygame.K_d]:
                if player.team == 2:
                    player.direction -= 2
            if keys[pygame.K_a]:
                if player.team == 2:
                    player.direction += 2
        screen.fill((255,255,255))
        if len(foods) <= 500:
            spawn_food()
        for i in foods:
            i.draw()
        for i in players:
            i.move()
            i.draw()
            
    pygame.display.update()