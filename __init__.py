#!/usr/bin/env python3

import pygame
from map import *

def main():
    done = False
    keystates = { 'LEFT':False, 'RIGHT':False, 'UP':False, 'DOWN':False}
    scr_width = 640
    scr_height = 480
    scr_tile = 16
    print('Starting game...')
    pygame.init()
    pygame.font.init()
    if not pygame.font.get_init():
        print('Error: pygame must have font support to run this game')
        done = True
    else:
        mainFont = pygame.font.SysFont(None, 24)
        mainFontX = 0
        mainFontY = 0
    screen = pygame.display.set_mode((scr_width, scr_height))
    clock = pygame.time.Clock()
    pygame.key.set_repeat(1, 10)
    map1 = Map(scr_width, scr_height, scr_tile, screen, "map1.map")
    player1 = map1.getPlayer()
    player1.setSpeed(4)
    enemies = map1.getEnemies()


    while not done:

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                done = True
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    done = True
                if event.key == pygame.K_LEFT:
                    print('Left key pressed!')
                    keystates['LEFT'] = True
                if event.key == pygame.K_RIGHT:
                    print('Right key pressed!')
                    keystates['RIGHT'] = True
                if event.key == pygame.K_UP:
                    print('Up key pressed!')
                    keystates['UP'] = True
                if event.key == pygame.K_DOWN:
                    print('Down key pressed!')
                    keystates['DOWN'] = True
            elif event.type == pygame.KEYUP:
                if event.key == pygame.K_LEFT:
                    print('Left key released!')
                    keystates['LEFT'] = False
                if event.key == pygame.K_RIGHT:
                    print('Right key released!')
                    keystates['RIGHT'] = False
                if event.key == pygame.K_UP:
                    print('Up key released')
                    keystates['UP'] = False
                if event.key == pygame.K_DOWN:
                    print('Down key released')
                    keystates['DOWN'] = False

        # Test object to see if player will collide if it moves in the direction directed to by the user
        testCoords = BaseObject(player1.x, player1.y, player1.width, player1.height, screen)
        if keystates['LEFT']:
            testCoords.x -= player1.speed
        if keystates['RIGHT']:
            testCoords.x += player1.speed
        if keystates['UP']:
            testCoords.y -= player1.speed
        if keystates['DOWN']:
            testCoords.y += player1.speed

        if not map1.checkCollisions(testCoords):
            if keystates['LEFT']:
                player1.goLeft()
            if keystates['RIGHT']:
                player1.goRight()
            if keystates['UP']:
                player1.goUp()
            if keystates['DOWN']:
                player1.goDown()

        for item in enemies:
            if item.checkCollision(player1):
                print('Enemy hit player!!!')
                player1.loseHealth(2)
            item.processMovement(map1)

        if player1.health <= 0:
            print('You died, game over!')
            done = True

        screen.fill(COL_BLACK)
        map1.draw()
        drawHealth(screen, mainFont, player1.health)
        pygame.display.flip()
        clock.tick(60)

def drawHealth(screen, font, health):
    textInput = "Health: {0}".format(health)
    if health > 40:
        textColour = COL_GREEN
    elif health <= 40 and health > 20:
        textColour = COL_YELLOW
    else:
        textColour = COL_RED
    text = font.render(textInput, True, textColour)
    textRect = text.get_rect()
    textRect.topleft = (0, 0)
    screen.blit(text, textRect)

if __name__ == '__main__': main()