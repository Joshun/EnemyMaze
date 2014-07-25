import pygame, copy

COL_WHITE = (255, 255, 255)
COL_BLACK = (0, 0, 0)
COL_GREY = (122, 122, 122)
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


    def checkCollision_old(self, colObject):
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

    def checkCollision(self, colObject):
        rect1 = pygame.Rect(self.x, self.y, self.width, self.height)
        rect2 = pygame.Rect(colObject.x, colObject.y, colObject.width, colObject.height)
        return rect1.colliderect(rect2)


class Wall(BaseObject):

    def __init__(self, x, y, width, height, screen, isSolid=True, isExit=False):
        super(Wall, self).__init__(x, y, width, height, screen)
        if isExit is True:
            self.setColour(COL_WHITE)
            isSolid = False
        else:
            self.setColour(COL_GREY)
        self.isExit = isExit
        self.isSolid = isSolid

class Bullet(BaseObject):

    def __init__(self, x, y, width, height, screen, speed, screenWidth):
        super(Bullet, self).__init__(x, y, width, height, screen)
        self.speed = speed
        self.screenWidth = screenWidth
    def processMovement(self):
        if self.x > self.screenWidth:
            return True  # Return True if bullet is 'spent'
        else:
            self.x += self.speed


class Player(BaseObject):

    def __init__(self, x, y, width, height, screen):
        super(Player, self).__init__(x, y, width, height, screen, name='Player 1')
        self.setColour(COL_BLUE)
        self.speed = 1
        self.health = 100
        self.bullets = []
    def setSpeed(self, speed):
        self.speed = speed
    def setMaxBullets(self, nBullets):
        self.maxBullets = nBullets
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
    def fireBullet(self):
        newBullet = Bullet(self.x + 10, self.y, 8, 4, self.screen, 8, 640)
        self.bullets.append(newBullet)
    def drawBullets(self):
        for item in self.bullets:
            item.draw()
    def processBullets(self):
        for item in self.bullets:
            if item.processMovement():
                self.bullets.remove(item)  # Remove 'spent' bullets
    def getNumBullets(self):
        return len(self.bullets)


class Enemy(BaseObject):

    def __init__(self, x, y, width, height, screen, etype='vertical'):
        super(Enemy, self).__init__(x, y, width, height, screen, name='unlabelled')
        if etype == 'vertical':
            self.setColour(COL_RED)
        elif etype == 'horizontal':
            self.setColour(COL_YELLOW)
        self.speed = 2
        self.direction = 0
        self.etype = etype
    def setSpeed(self, speed):
        self.speed = speed
    def changeDirection(self):
        if self.direction == 0:
            self.direction = 1
            if self.etype == 'vertical':
                self.y -= self.speed
            elif self.etype == 'horizontal':
                self.x -= self.speed
            #print('Enemy direction: upwards')
        else:
            self.direction = 0
            if self.etype == 'vertical':
                self.y += self.speed
            elif self.etype == 'horizontal':
                self.x += self.speed
           # print('Enemy direction: downwards')
    def processMovement(self, mapObject):
        testCoords = BaseObject(self.x, self.y + self.speed, self.width, self.height, self.screen)
        if not mapObject.checkCollisions(testCoords):
            if self.direction == 0:
                if self.etype == 'vertical':
                    self.y += self.speed
                elif self.etype == 'horizontal':
                    self.x += self.speed
            else:
                if self.etype == 'vertical':
                    self.y -= self.speed
                elif self.etype == 'horizontal':
                    self.x -= self.speed
        else:
            self.changeDirection()

class ExploderEnemy(BaseObject):

    def __init__(self, x, y, width, height, screen):
        super(ExploderEnemy, self).__init__(x, y, width, height, screen)
        self.speed = 1
        self.ticks = 0
        subObjectBase = BaseObject(self.x, self.y, self.width // 4, self.height // 4, self.screen)
        self.subObjects = [ copy.copy(subObjectBase), copy.copy(subObjectBase), copy.copy(subObjectBase), copy.copy(subObjectBase) ]
    def setSpeed(self, speed):
        self.speed = speed
    def processMovement(self, mapObject):
        self.subObjects[0].x -= self.speed
        self.subObjects[0].y -= self.speed

        self.subObjects[1].x += self.speed
        self.subObjects[1].y -= self.speed

        self.subObjects[2].x -= self.speed
        self.subObjects[2].y += self.speed

        self.subObjects[3].x += self.speed
        self.subObjects[3].x += self.speed

        self.ticks += 1
        if self.ticks < 80:
            return False
        else:
            self.ticks = 0
            for item in self.subObjects:
                item.x = self.x
                item.y = self.y
            return True
    def draw(self):
        enemyNum = 1
        for item in self.subObjects:
            #print('Drawing exploder enemy #{0}({1},{2})'.format(enemyNum, item.x, item.y))
            item.draw()
            enemyNum += 1
    def checkCollision(self, colObject):
        for item in self.subObjects:
            if item.checkCollision(colObject):
                return True
        return False


