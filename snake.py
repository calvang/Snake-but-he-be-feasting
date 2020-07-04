import pygame
import sys
import random

class snake(object):
    def __init__(self):
        self.length = 1
        self.width = 1
        self.positions = [((SCREEN_WIDTH / 2), (SCREEN_HEIGHT / 2))]
        self.direction = random.choice([UP, DOWN, LEFT, RIGHT])
        self.color = (93, 216, 228)

    def get_head_pos(self):
        return self.positions[0]

    def turn(self,point):
        if self.length > 1 and (point[0]*-1, point[1]*-1) == self.direction:
            return
        else:
            self.direction = point
        
    def move(self, score):
        current = self.get_head_pos()
        x,y = self.direction
        new = (((current[0] + x*GRID_SIZE) % SCREEN_WIDTH), (current[1] + y*GRID_SIZE) % SCREEN_HEIGHT)
        if len(self.positions) > 2 and new in self.positions[2:]:
            self.reset()
            return 0
        else:
            self.positions.insert(0, new)
            if len(self.positions) > self.length:
                self.positions.pop()
            return score

    def reset(self):
        self.length = 1
        self.positions = [((SCREEN_WIDTH / 2), (SCREEN_HEIGHT / 2))]
        self.direction = random.choice([UP, DOWN, LEFT, RIGHT])
    
    def draw(self, surface):
        for p in self.positions:
            r = pygame.Rect((p[0], p[1]), (GRID_SIZE, GRID_SIZE))
            pygame.draw.rect(surface, self.color, r)
            pygame.draw.rect(surface, (17, 24, 47), r, 1)

    def handle_keys(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_UP:
                    self.turn(UP)
                if event.key == pygame.K_DOWN:
                    self.turn(DOWN)
                if event.key == pygame.K_LEFT:
                    self.turn(LEFT)
                if event.key == pygame.K_RIGHT:
                    self.turn(RIGHT)

class food(object):
    def __init__(self):
        self.position = (0,0)
        self.color = (223, 163, 49)
        self.randomize_pos()

    def randomize_pos(self):
        self.position = (random.randint(0, GRID_WIDTH-1) * GRID_SIZE, random.randint(0, GRID_HEIGHT-1) * GRID_SIZE)

    def draw(self,surface):
        r = pygame.Rect((self.position[0], self.position[1]), (GRID_SIZE, GRID_SIZE)) 
        pygame.draw.rect(surface, self.color, r)
        pygame.draw.rect(surface, (17, 24, 47), r, 1)

def drawGrid(surface):
    for y in range(0, int(GRID_HEIGHT)):
        for x in range(0, int(GRID_WIDTH)):
            if (x + y) % 2 == 0:
                r = pygame.Rect((x*GRID_SIZE, y*GRID_SIZE), (GRID_SIZE,
                    GRID_SIZE))
                pygame.draw.rect(surface, (17, 24, 47), r)
            else:
                rr = pygame.Rect((x*GRID_SIZE, y*GRID_SIZE), (GRID_SIZE, GRID_SIZE))
                pygame.draw.rect(surface, (23, 35, 58), rr)

SCREEN_WIDTH = 1600
SCREEN_HEIGHT = 1600

GRID_SIZE = 80
GRID_WIDTH = SCREEN_HEIGHT / GRID_SIZE
GRID_HEIGHT = SCREEN_WIDTH / GRID_SIZE

UP = (0, -1)
DOWN = (0, 1)
LEFT = (-1, 0)
RIGHT = (1, 0)

def main():
    pygame.init()

    clock = pygame.time.Clock()
    screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT), 0 ,32)

    surface = pygame.Surface(screen.get_size())
    surface = surface.convert()
    drawGrid(surface)

    snek = snake()
    snaks = []
    for i in range(20):
        snack = food()
        snaks.append(snack)
    myfont = pygame.font.SysFont('arial', 64)
    
    score = 0
    while(True):
        clock.tick(10)
        snek.handle_keys()

        drawGrid(surface)
        score = snek.move(score)
        if score == 0 and len(snaks) > 20:
            del snaks[20:]
        for snack in snaks:
            if snek.get_head_pos() == snack.position:
                snek.length += 1
                score += 1
                snack.randomize_pos()
                if len(snaks) < snek.length**2:
                    for i in range(int(snek.length%5)):
                        snak = food()
                        snaks.append(snak)
            snek.draw(surface)
            snack.draw(surface)
            screen.blit(surface, (0, 0))
        text = myfont.render("Score {0}".format(score), 1, (255, 255, 255))
        screen.blit(text, (5, 10))
        pygame.display.update()

main()
