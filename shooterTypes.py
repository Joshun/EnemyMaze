import pygame

COL_WHITE = (255, 255, 255)
COL_BLACK = (0, 0, 0)
COL_RED = (255, 0, 0)
COL_GREEN = (0, 255, 0)
COL_BLUE = (0, 0, 255)
COL_YELLOW = (255, 149, 0)

def in_x_range(point, x1, x4):
    test_x1 = point.x
    test_x4 = point.x + point.width

    return test_x4 >= x1 and test_x1 <= x4

def in_y_range(point, y1, y4):
    test_y1 = point.y
    test_y4 = point.y + point.height

    return test_y4 >= y1 and test_y1 <= y4

class BaseObject:

    def __init__(self, x, y, width, height, screen, name='unlabelled'):
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.name = name
        self.screen = screen
        self.colour = COL_WHITE

    def getCoordinates(self):
        x1 = self.x
        x2 = self.x + self.width
        y1 = self.y
        y2 = self.y + self.height
        return x1, x2, y1, y2

    def setName(self, name):
        self.name = name

    def setColour(self, colour):
        self.colour = colour

    def draw(self):
        pygame.draw.rect(self.screen, self.colour, (self.x, self.y, self.width, self.height))


    def checkCollision(self, colObject):
        test_x1 = colObject.x
        test_x4 = colObject.x + colObject.width
        test_y1 = colObject.y
        test_y4 = colObject.y + colObject.height

        its_x1 = self.x
        its_x4 = self.x + self.width
        its_y1 = self.y
        its_y4 = self.y + self.height

        #collidedSides = { 'L': False, 'R': False, 'T':False, 'B':False }

        if in_x_range(colObject, its_x1, its_x4):
            if test_y4 >= its_y1 and test_y1 < its_y1:
                return True
            if test_y1 <= its_y4 and test_y4 > its_y4:
                return True
        if in_y_range(colObject, its_y1, its_y4):
            if test_x4 >= its_x1 and test_x1 < its_x1:
                return True
            elif test_x1 <= its_x4 and test_x4 > its_x4:
                return True

        return False


class Wall(BaseObject):

    def __init__(self, x, y, width, height, screen, isSolid=True, isExit=False):
        super(Wall, self).__init__(x, y, width, height, screen)
        self.isSolid = isSolid
        self.isExit = isExit

class Player(BaseObject):

    def __init__(self, x, y, width, height, screen):
        super(Player, self).__init__(x, y, width, height, screen, name='Player 1')
        self.setColour(COL_BLUE)
        self.speed = 1
        self.health = 100
    def setSpeed(self, speed):
        self.speed = speed
    def goLeft(self):
        self.x -= self.speed
    def goRight(self):
        self.x += self.speed
    def goUp(self):
        self.y -= self.speed
    def goDown(self):
        self.y += self.speed
    def loseHealth(self, amount):
        self.health -= amount

class Enemy(BaseObject):

    def __init__(self, x, y, width, height, screen):
        super(Enemy, self).__init__(x, y, width, height, screen, name='unlabelled')
        self.setColour(COL_RED)
        self.speed = 2
        self.direction = 0
    def setSpeed(self, speed):
        self.speed = speed
    def changeDirection(self):
        if self.direction == 0:
            self.direction = 1
            self.y -= self.speed
            print('Enemy direction: upwards')
        else:
            self.direction = 0
            self.y += self.speed
            print('Enemy direction: downwards')
    def processMovement(self, mapObject):
        testCoords = BaseObject(self.x, self.y + self.speed, self.width, self.height, self.screen)
        if not mapObject.checkCollisions(testCoords):
            if self.direction == 0:
                self.y += self.speed
            else:
                self.y -= self.speed
        else:
            self.changeDirection()
