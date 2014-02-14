__author__ = 'Vin Breau'

# VERSION 1.0, completed on Feb. 12th, 2014
# Project started on Feb. 10th, 2014

import pygame
import sys
import random
from pygame.locals import *

# Window Settings
WINDOWWIDTH = 640
WINDOWHEIGHT = 480

# Colors
TEXTCOLOR1 = (0, 175, 0)
TEXTCOLOR2 = (100, 255, 100)
BACKGROUNDCOLOR = (0, 0, 0)
PADDLECOLOR = (0, 175, 0)
BOUNDRYCOLOR = (0, 100, 0)
BALLCOLOR = (100, 255, 100)
DIVIDINGLINECOLOR = (0, 25, 0)

# Game object settings
PADDLEWIDTH = 15
PADDLEHEIGHT = 50
BALLSIZE = 15
PLAYERMOVERATE = 10
UPPERLIMIT = 75
TOPWALL = pygame.Rect(0, UPPERLIMIT, WINDOWWIDTH, 10)
BOTTOMWALL = pygame.Rect(0, WINDOWHEIGHT - 10, WINDOWWIDTH, 10)
DIVIDEINGLINE = pygame.Rect((WINDOWWIDTH / 2) - 10, UPPERLIMIT, 10, WINDOWHEIGHT - UPPERLIMIT)
BALL = pygame.Rect((WINDOWWIDTH / 2) - BALLSIZE, (WINDOWHEIGHT / 2), BALLSIZE, BALLSIZE)
WALLBUFFER = 15
FPS = 40
WINNINGSCORE = 6


def terminate():
    pygame.quit()
    sys.exit()


def waitForPlayerToPressKey():
    while True:
        for event in pygame.event.get():
            if event.type == QUIT:
                terminate()
            if event.type == KEYDOWN:
                if event.type == K_ESCAPE:
                    terminate()
                return


def drawText(text, font, surface, textColor, x, y):
    # render(text, antialias, color, background=None)
    textobj = font.render(text, 1, textColor)
    textrect = textobj.get_rect()
    textrect.topleft = (x, y)
    surface.blit(textobj, textrect)


def startBallMoving():
    hSpeed = 0
    vSpeed = 0
    while hSpeed == 0:
        hSpeed = random.randint(-2, 2)
        hSpeed = hSpeed * 2
    while vSpeed == 0:
        vSpeed = random.randint(-2, 2)
        vSpeed = vSpeed * 2
    return hSpeed, vSpeed

def winGame(winner):
    gameSurface.fill(BACKGROUNDCOLOR)
    drawText('GAME OVER', scoreFont, gameSurface, TEXTCOLOR2, (WINDOWWIDTH / 3) - 50, (WINDOWHEIGHT / 3))
    drawText('%s WINS!' % (winner), scoreFont, gameSurface, TEXTCOLOR1, (WINDOWWIDTH / 3) - 85, (WINDOWHEIGHT / 3) + 80)
    drawText('Press a key to start.', bodyFont, gameSurface, TEXTCOLOR1, (WINDOWWIDTH / 3) + 25, WINDOWHEIGHT - 100)
    pygame.display.update()
    waitForPlayerToPressKey()


# Initialize pygame and window surface
pygame.init()
mainClock = pygame.time.Clock()
gameSurface = pygame.display.set_mode((WINDOWWIDTH, WINDOWHEIGHT))  # Add ", pygame.FULLSCREEN" before final ) for FS
pygame.display.set_caption('PONG')
pygame.mouse.set_visible(False)

# ball settings
ballMoving = False
ballDirection = None
ballMaxSpeed = 6
ballMinSpeed = 3
ballMovPosX = 0
ballMovPosY = 0

#Text font settings
titleFont = pygame.font.Font('alex.ttf', 100)
scoreFont = pygame.font.Font('alexb.ttf', 60)
bodyFont = pygame.font.SysFont(None, 25)
subFont = pygame.font.SysFont(None, 18)

# Sound settings
ballOutOfBounds = pygame.mixer.Sound('outOfBounds.wav')
ballHitWallSound = pygame.mixer.Sound('wallHit.wav')
ballHitPlayerSound = pygame.mixer.Sound('paddleHit.wav')

# Player paddle settings
playerOne = pygame.Rect(20, (WINDOWHEIGHT / 2) - (PADDLEHEIGHT / 2), PADDLEWIDTH, PADDLEHEIGHT)
playerTwo = pygame.Rect((WINDOWWIDTH - 40), (WINDOWHEIGHT / 2) - (PADDLEHEIGHT / 2), PADDLEWIDTH, PADDLEHEIGHT)

topScore = 0
player1Score = 0
player2Score = 0
gameStarted = False

# GAME OVER SCREEN DEBUGGING
# winGame('PLAYER 1')

# Show the Start Screen
drawText('PONG', titleFont, gameSurface, TEXTCOLOR2, (WINDOWWIDTH / 3) - 25, 100)
drawText('Player 1 uses W S keys for movement', bodyFont, gameSurface, TEXTCOLOR1, (WINDOWWIDTH / 4), 200)
drawText('Player 2 uses arrow keys for movement', bodyFont, gameSurface, TEXTCOLOR1, (WINDOWWIDTH / 4) - 6, 220)
drawText('Spacebar serves the ball', bodyFont, gameSurface, TEXTCOLOR1, (WINDOWWIDTH / 4) + 53, 240)
drawText('Press a key to start.', bodyFont, gameSurface, TEXTCOLOR2, (WINDOWWIDTH / 3) + 20, 300)
drawText('This version: Vin Breau, 2014', subFont, gameSurface, TEXTCOLOR1, (WINDOWWIDTH / 3) + 14, WINDOWHEIGHT - 50)
pygame.display.update()
waitForPlayerToPressKey()

while True:
    # Set up the start of the game
    playerOneScore = 0
    playerTwoScore = 0
    p1moveDown = p1moveUp = p2moveDown = p2moveUp = False
    ballMoveUp = ballMoveDown = ballMoveRight = ballMoveLeft = False

    while True:
        for event in pygame.event.get():
            if event.type == QUIT:
                terminate()

            # PLAYER key events
            if event.type == KEYDOWN:
                if event.key == ord('w'):
                    p1moveDown = False
                    p1moveUp = True
                if event.key == ord('s'):
                    p1moveUp = False
                    p1moveDown = True
                if event.key == K_ESCAPE:
                    terminate()
                if event.key == K_UP:
                    p2moveDown = False
                    p2moveUp = True
                if event.key == K_DOWN:
                    p2moveUp = False
                    p2moveDown = True
            if event.type == KEYUP:
                if event.key == ord('w'):
                    p1moveUp = False
                if event.key == ord('s'):
                    p1moveDown = False
                if event.key == K_UP:
                    p2moveUp = False
                if event.key == K_DOWN:
                    p2moveDown = False
                if event.key == K_SPACE and ballMoving == False:
                    ballMovPosX, ballMovPosY = startBallMoving()
                    ballMoving = True
                    gameStarted = True

        # PLAYER 1 move
        if p1moveUp and playerOne.top > UPPERLIMIT + WALLBUFFER:
            playerOne.move_ip(0, -1 * PLAYERMOVERATE)
        if p1moveDown and playerOne.bottom < WINDOWHEIGHT - WALLBUFFER:
            playerOne.move_ip(0, PLAYERMOVERATE)

        # PLAYER 2 move
        if p2moveUp and playerTwo.top > UPPERLIMIT + WALLBUFFER:
            playerTwo.move_ip(0, -1 * PLAYERMOVERATE)
        if p2moveDown and playerTwo.bottom < WINDOWHEIGHT - WALLBUFFER:
            playerTwo.move_ip(0, PLAYERMOVERATE)

        # BALL moving
        # boundary collision detection for BALL
        if BALL.colliderect(TOPWALL) or BALL.colliderect(BOTTOMWALL):
            ballHitWallSound.play()
            ballMovPosY = (ballMovPosY * -1)
            # prevent BALL from getting stuck in boundary walls
            if BALL.top < TOPWALL.bottom:
                BALL.top = TOPWALL.bottom + 1
            if BALL.bottom > BOTTOMWALL.top:
                BALL.bottom = BOTTOMWALL.top - 1
        # Paddle BALL collision checking
        if BALL.colliderect(playerOne) or BALL.colliderect(playerTwo):
            ballHitPlayerSound.play()
            ballMovPosX = (ballMovPosX * -1)

            # Put some spin on the ball depending on where it hits the paddle
            if BALL.centery < playerOne.centery or BALL.centery > playerOne.centery or BALL.centery < playerTwo.centery or BALL.centery > playerTwo.centery:
                if random.randint(0, 1) == 0:
                    ballMovPosX = ballMovPosX * random.randint(1, 5)
                    ballMovPosY = ballMovPosY * random.randint(1, 5)
                else:
                    ballMovPosX = ballMovPosX / random.randint(1, 2)
                    ballMovPosY = ballMovPosY / random.randint(1, 2)
            # If ball hits near center of the paddle, level out the rebound on the X axis
            if (playerOne.centery - 1) <= BALL.centery <= (playerOne.centery + 1):
                if random.randint(0, 1) == 0:
                    ballMovPosY = 0
                else:
                    ballMovPosY = ballMovPosY + 1
            if (playerTwo.centery - 10) <= BALL.centery <= (playerTwo.centery + 10):
                if random.randint(0, 1) == 0:
                    ballMovPosY = 0
                else:
                    ballMovPosY = ballMovPosY + 1

            # Check to see if BALL is hitting top or bottom of paddle
            if (BALL.colliderect(playerOne) and BALL.left < playerOne.right):
                # Prevent the BALL from getting stuck inside the paddle
                if BALL.bottom > playerOne.top or BALL.top < playerOne.bottom:
                    BALL.left = playerOne.right + 1
                ballMovPosY = ballMovPosY * -2
            if (BALL.colliderect(playerTwo) and BALL.right > playerTwo.left):
                # Prevent the BALL from getting stuck inside the paddle
                if BALL.bottom > playerTwo.top or BALL.top < playerTwo.bottom:
                    BALL.right = playerTwo.left - 1
                ballMovPosY = ballMovPosY * -2

        if ballMoving and BALL.left < WINDOWWIDTH and BALL.right > 0 and gameStarted == True:
            # Cap the balls max speed
            if ballMovPosY > ballMaxSpeed:
                ballMovPosY = ballMaxSpeed
            if ballMovPosX < (-1 * ballMaxSpeed):
                ballMovPosX = (-1 * ballMaxSpeed)
            if ballMovPosX > (ballMinSpeed * -1) and ballMovPosX < ballMinSpeed:
                if ballMovPosX > -3:
                    ballMovPosX = -3
                else:
                    ballMovPosX = 3

            # Apply all ball movements now, but first, prevent ball from escaping boundaries
            if BALL.top < TOPWALL.bottom:
                BALL.top = TOPWALL.bottom + 1
            if BALL.bottom > BOTTOMWALL.top:
                BALL.bottom = BOTTOMWALL.top - 1
            BALL.move_ip(ballMovPosX, ballMovPosY)
        elif not ballMoving and gameStarted == False:
            pass
        else:
            ballOutOfBounds.play()
            if BALL.left > WINDOWWIDTH:
                player1Score += 1
                if player1Score == WINNINGSCORE:
                    winGame('PLAYER 1')
                    player1Score = 0
                    player2Score = 0
                    ballMoving = False
                    gameStarted = False
                    BALL.x = (WINDOWWIDTH / 2) - BALLSIZE
                    BALL.y = WINDOWHEIGHT / 2
                    break
            else:
                player2Score += 1
                if player2Score == WINNINGSCORE:
                    winGame('PLAYER 2')
                    player1Score = 0
                    player2Score = 0
                    ballMoving = False
                    gameStarted = False
                    BALL.x = (WINDOWWIDTH / 2) - BALLSIZE
                    BALL.y = WINDOWHEIGHT / 2
                    break
            ballMoving = False
            gameStarted = False
            BALL.x = (WINDOWWIDTH / 2) - BALLSIZE
            BALL.y = WINDOWHEIGHT / 2

        gameSurface.fill(BACKGROUNDCOLOR)

        # Draw score
        drawText(str(player1Score), scoreFont, gameSurface, TEXTCOLOR2, 50, 25)
        drawText(str(player2Score), scoreFont, gameSurface, TEXTCOLOR2, WINDOWWIDTH - 70, 25)

        # draw center, top and bottom walls
        pygame.draw.rect(gameSurface, DIVIDINGLINECOLOR, DIVIDEINGLINE)
        pygame.draw.rect(gameSurface, BOUNDRYCOLOR, TOPWALL)
        pygame.draw.rect(gameSurface, BOUNDRYCOLOR, BOTTOMWALL)

        # Draw the ball
        pygame.draw.rect(gameSurface, BALLCOLOR, BALL)

        # Draw the players
        pygame.draw.rect(gameSurface, PADDLECOLOR, playerOne)
        pygame.draw.rect(gameSurface, PADDLECOLOR, playerTwo)

        pygame.display.update()
        mainClock.tick(40)


