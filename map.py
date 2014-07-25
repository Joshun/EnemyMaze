import pygame
from shooterTypes import *

class Map:

    def __init__(self, width, height, tileSize, screen, mapFile):
        self.width = width
        self.height = height
        self.tileSize = tileSize
        self.screen = screen
        self.numXTiles = self.width / self.tileSize
        self.numYTiles = self.height / self.tileSize
        self.sprites = []
        self.player = False
        self.loadMapFile(mapFile)
    def loadMapFile(self, mapFile):
        numLines = 0
        xPos = 0
        yPos = 0
        currentLineLength = 0
        playerDeclared = False
        with open(mapFile, "r") as mFile:
            for line in mFile:
                line = line.rstrip('\n')
                currentLineLength = len(line)
                print('Line {} has width {}'.format(numLines + 1, currentLineLength))
                if currentLineLength != self.numXTiles:
                    print('Error: incorrect width at line {} ( should be {})'.format(numLines + 1, self.numXTiles))
                    return
                else:
                    for element in line:
                        if element == '=':  # Wall object
                            #print('Drawing sprite at ({},{})'.format(xPos, yPos))
                            spriteElement = Wall(xPos, yPos, self.tileSize, self.tileSize, self.screen)
                            self.sprites.append(spriteElement)
                        elif element == 'P':  # Player object (can only be one)
                            if playerDeclared is False:
                                spriteElement = Player(xPos, yPos, 8, 8, self.screen)
                                self.player = spriteElement
                                playerDeclared = True
                            else:
                                print('Error: player declared multiple times in mapfile')
                        elif element == 'V':  # Enemy object
                            spriteElement = Enemy(xPos, yPos, self.tileSize, self.tileSize, self.screen)
                            self.sprites.append(spriteElement)
                        elif element == 'H':  # Horizontal enemy object
                            spriteElement = Enemy(xPos, yPos, self.tileSize, self.tileSize, self.screen, etype='horizontal')
                            self.sprites.append(spriteElement)
                        elif element == 'X':  # Exit wall object
                            spriteElement = Wall(xPos, yPos, self.tileSize, self.tileSize, self.screen, isExit=True)
                            self.sprites.append(spriteElement)
                        elif element == 'E':  # Exploder enemy object
                            spriteElement = ExploderEnemy(xPos, yPos, self.tileSize, self.tileSize, self.screen)
                            self.sprites.append(spriteElement)
                        xPos += self.tileSize
                    xPos = 0
                    yPos += self.tileSize
                    numLines += 1
            if numLines != self.numYTiles:
                print('Warning: lines in file to not fill screen (should be {})'.format(self.numYTiles))
    def draw(self):
        for item in self.sprites:
            item.draw()
        self.player.draw()
    def getPlayer(self):
        return self.player
    def getEnemies(self):
        enemyArr = []
        for item in self.sprites:
            if item.__class__.__name__ == 'Enemy' or item.__class__.__name__ == 'ExploderEnemy':
                enemyArr.append(item)
        return enemyArr
    def removeItem(self, item):
        self.sprites.remove(item)
    def checkCollisions(self, testObject):
        testObjectType = testObject.__class__.__name__
        for item in self.sprites:
            collisionOccurred = testObject.checkCollision(item)
            if collisionOccurred == True:
                itemType = item.__class__.__name__
                if itemType == 'Wall':
                    if item.isExit == True:
                        print('You have reached the exit, well done!')
                    if item.isSolid == False:
                        return False
                    else:
                        return True

        return 0
