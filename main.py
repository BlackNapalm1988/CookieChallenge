import pygame
import random
import sys
import time
from dataclasses import dataclass

from settings import *

from pygame.locals import *
from pygame.sprite import *

pygame.init()

#Dimensions
windowWidth = 1000
windowHeight = 900

character = pygame.sprite.Group()
enemySetOne = []
audioOne = pygame.mixer.Sound('audio/floorCreak.wav')
audioTwo = pygame.mixer.Sound('audio/legoAudio.wav')
audioMain = pygame.mixer_music.load('audio/blanket.mp3')
pygame.mixer.init(channels = 2)

#Fonts
fontObjFifty = pygame.font.Font('fonts/CreamPeach.ttf', 50)
fontObjForty = pygame.font.Font('fonts/CreamPeach.ttf', 40)
fontObjThreeNine = pygame.font.Font('fonts/CreamPeach.ttf', 37)
fontObjThirty = pygame.font.Font('fonts/CreamPeach.ttf', 30)
fontObjTwenty = pygame.font.Font('fonts/CreamPeach.ttf', 20)
fontObjThirtyType = pygame.font.Font('fonts/typewriter.ttf', 30)

SCREEN = pygame.display.set_mode((windowWidth, windowHeight))
pygame.display.set_caption('Quiet')

class mainCharacter(pygame.sprite.Sprite):
    def __init__(self):
        self.boardX = 0
        self.boardY = 0
        super().__init__()
        characterImage = pygame.image.load("assets/tempCharacter.png")
        self.image = pygame.Surface((50, 50))
        self.image = pygame.transform.scale(characterImage, (50, 50)).convert_alpha()
        self.rect = self.image.get_rect()

    def update(self, centre):
        self.rect.center = centre

class catEnemy():
    def __init__(self):
        characterImage = pygame.image.load("assets/enemyOne.png")
        self.image = pygame.Surface((50, 50))
        self.image = pygame.transform.scale(characterImage, (50, 50)).convert_alpha()
        self.setXY(0,0)
        self.setDirection(1)
        self.drawing = False
        self.positionX = 0
        self.positionY = 0
        self.change = False

    def setBoardPosition(self, x, y):
        self.boardX = x
        self.boardY = y

    def setXY(self, x, y):
        self.positionX = x
        self.positionY = y

    def setDirection(self, _direction):
        self.direction = _direction

    def setDrawing(self, _drawing):
        self.drawing = _drawing

    def getImage(self):
        return self.image

    def getDrawing(self):
        return self.drawing

    def getDirection(self):
        return self.direction

    def changeDirection(self, _change):
        self.change = _change

    def getChange(self):
        return self.change

    def getPositionX(self):
        return self.positionX

    def getPositionY(self):
        return self.positionY

    def getBoardX(self):
        return self.boardX

    def getBoardY(self):
        return self.boardY

@dataclass
class Item:
    name: str
    filename: str


class Inventory:
    """Track collected items and their images."""

    item_order = [
        Item("redKey", "redKey.png"),
        Item("waterBoot", "toyBox.png"),
        Item("iceSkate", "socks.png"),
        Item("blueKey", "blueKey.png"),
        Item("greenKey", "greenKey.png"),
        Item("socks", "socks.png"),
        Item("flashlight", "flashlight.png"),
    ]

    def __init__(self):
        self.items = {item.name: False for item in self.item_order}
        self.item_indices = {item.name: idx for idx, item in enumerate(self.item_order)}
        self.allInvent = []
        self.inventPics = []
        self.picIndex = []
        self.setImages()

    def setImages(self):
        for item in self.item_order:
            image = pygame.image.load(f"assets/{item.filename}")
            image = pygame.transform.scale(image, (50, 50)).convert_alpha()
            self.inventPics.append(image)

    def add_item(self, name):
        """Collect an item."""
        self.items[name] = True
        self.allInvent.append(name)
        self.picIndex.append(self.item_indices[name])

    def lose_item(self, name):
        """Remove an item from the inventory."""
        self.allInvent.remove(name)
        self.picIndex.remove(self.item_indices[name])
        if name not in self.allInvent:
            self.items[name] = False

    def has_item(self, name):
        return self.items[name]

    # Convenience wrappers used throughout the game
    def getRedKey(self):
        self.add_item("redKey")

    def loseRedKey(self):
        self.lose_item("redKey")

    def returnRedKey(self):
        return self.has_item("redKey")

    def getBlueKey(self):
        self.add_item("blueKey")

    def loseBlueKey(self):
        self.lose_item("blueKey")

    def returnBlueKey(self):
        return self.has_item("blueKey")

    def getGreenKey(self):
        self.add_item("greenKey")

    def loseGreenKey(self):
        self.lose_item("greenKey")

    def returnGreenKey(self):
        return self.has_item("greenKey")

    def returnWaterBoot(self):
        return self.has_item("waterBoot")

    def getWaterBoot(self):
        self.add_item("waterBoot")

    def loseWaterBoot(self):
        self.lose_item("waterBoot")

    def returnSocks(self):
        return self.has_item("socks")

    def getSocks(self):
        self.add_item("socks")

    def loseSocks(self):
        self.lose_item("socks")

    def getFlashlight(self):
        self.add_item("flashlight")

    def loseFlashlight(self):
        self.lose_item("flashlight")

    def returnFlashlight(self):
        return self.has_item("flashlight")

    def getIceSkate(self):
        self.add_item("iceSkate")

    def loseIceSkate(self):
        self.lose_item("iceSkate")

    def returnIceSkate(self):
        return self.has_item("iceSkate")

    def getItem(self, index):
        return self.allInvent[index]

    def returnInventLen(self):
        return len(self.allInvent)

    def returnPic(self, picPosition):
        return self.inventPics[self.picIndex[picPosition]]

def main() :
    global invent, dead, points, enemySetOne, switchesOn, started, won, calculatedTime
    clock = pygame.time.Clock()

    won = False
    paused = False
    dead = False

    newCharacter = mainCharacter()
    newCharacter.rect.x = 50 + (6 * 50)
    newCharacter.rect.y = 100 + (6 * 50)
    character.add(newCharacter)

    enemySetOne.append(catEnemy())

    time_difference = 0

    points = 0
    invent = Inventory()
    readFile(whatLevel)
    setStart(whatLevel)
    drawScreen()
    dead = False
    started = False

    while True:
        #Game over
        if dead == True and won == False:
            for event in pygame.event.get():
                if event.type == MOUSEMOTION :
                    mouseX, mouseY = event.pos
                    if mouseX >= 290 and mouseX <= 370 and mouseY >= 450 and mouseY <= 490:
                        yesDrawing(grey)
                        pygame.display.update()
                    elif mouseX >= 380 and mouseX <= 460 and mouseY >= 450 and mouseY <= 490:
                        noDrawing(grey)
                        pygame.display.update()
                    else :
                        yesDrawing(black)
                        noDrawing(black)
                        pygame.display.update()
                elif event.type == MOUSEBUTTONUP:
                    mouseX, mouseY = event.pos
                    #Checks if the user clicks to play again and then restarts the game
                    if mouseX >= 290 and mouseX <= 370 and mouseY >= 450 and mouseY <= 490:
                        points = 0
                        invent = Inventory()
                        readFile(whatLevel)
                        setStart(whatLevel)
                        started = False
                        drawScreen()
                        dead = False

                    elif mouseX >= 380 and mouseX <= 460 and mouseY >= 450 and mouseY <= 490:
                        pygame.quit()
                        sys.exit()
                elif event.type == QUIT or (event.type == KEYUP and event.key == pygame.K_ESCAPE):
                    pygame.quit()
                    sys.exit()

        elif dead == False and started == False and won == False:
            switchesOn = True
            for event in pygame.event.get() :
                if event.type == KEYUP and event.key == pygame.K_RIGHT and paused != True:
                    now = pygame.time.get_ticks()
                    pygame.mixer_music.play(-1, 0.0)
                    move(1)
                    started = True
                    if hasEnemy :
                        moveEnemy(0)
                if event.type == KEYUP and event.key == pygame.K_LEFT and paused != True :
                    now = pygame.time.get_ticks()
                    pygame.mixer_music.play(-1, 0.0)
                    move(2)
                    started = True
                    if hasEnemy :
                        moveEnemy(0)
                if event.type == KEYUP and event.key == pygame.K_UP and paused != True:
                    now = pygame.time.get_ticks()
                    pygame.mixer_music.play(-1, 0.0)
                    move(3)
                    started = True
                    if hasEnemy :
                        moveEnemy(0)
                if event.type == KEYUP and event.key == pygame.K_DOWN and paused != True:
                    now = pygame.time.get_ticks()
                    pygame.mixer_music.play(-1, 0.0)
                    move(4)
                    started = True
                    if hasEnemy:
                        moveEnemy(0)

                if event.type == QUIT or (event.type == KEYUP and event.key == pygame.K_ESCAPE):
                    pygame.quit()
                    sys.exit()


        #Gameplay
        elif dead == False and started == True and won == False:

            if paused == False:
                time_difference = calculatedTime - (pygame.time.get_ticks() - now)

            for event in pygame.event.get():
                if event.type == KEYUP and event.key == pygame.K_RIGHT and paused != True:
                    move(1)
                if event.type == KEYUP and event.key == pygame.K_LEFT and paused != True :
                    move(2)
                if event.type == KEYUP and event.key == pygame.K_UP and paused != True:
                    move(3)
                if event.type == KEYUP and event.key == pygame.K_DOWN and paused != True:
                    move(4)
                if event.type == KEYUP and event.key == pygame.K_SPACE and paused == True:
                    paused = False
                    clock.tick()
                    addTime = clock.get_time()
                    calculatedTime += addTime
                    for i in range(0, 13, 1):
                        for j in range(0, 13, 1):
                            drawBlock(i, j)
                    drawCharacter()
                    pygame.display.update()
                elif event.type == KEYUP and event.key == pygame.K_SPACE and paused == False:
                    clock.tick()
                    screenTwo = pygame.Surface((650, 650))
                    screenTwo.set_alpha(150)
                    screenTwo.fill((0, 0, 0))

                    SCREEN.blit(screenTwo, (50, 100))

                    spaceText = fontObjFifty.render("Press 'space' to continue", True, text, None)
                    SCREEN.blit(spaceText, ((650 - spaceText.get_width()) / 2 + 50, (650 / 2) + 100))
                    pygame.display.update()

                    paused = True
                if event.type == QUIT or (event.type == KEYUP and event.key == pygame.K_ESCAPE):
                    pygame.quit()
                    sys.exit()
                if event.type == KEYUP and (event.key not in {pygame.K_SPACE, pygame.K_UP, pygame.K_DOWN, pygame.K_RIGHT, pygame.K_LEFT}) :
                    pygame.mixer_music.stop()
                    points = 0
                    invent = Inventory()
                    readFile(whatLevel)
                    setStart(whatLevel)
                    started = False
                    drawScreen()
                    dead = False
                if dead :
                    started = False
            if paused == False:
                timerText = fontObjThirty.render(str(time_difference / 1000), True, text)
                pygame.draw.rect(SCREEN, line, (840, 200, 140, 40))
                SCREEN.blit(timerText, (840, 200))
                if time_difference % 3 == 0 and hasEnemy:
                    moveEnemy(0)
                pygame.display.update()

                if time_difference <= 0 and paused == False:
                    dead = True
                    youDied()
        elif won == True:
            finalLevel()
            for event in pygame.event.get() :
                if event.type == QUIT or (event.type == KEYUP and event.key == pygame.K_ESCAPE):
                    pygame.quit()
                    sys.exit()

def nextLevel():
    global started, points, invent, dead, runBefore
    pygame.mixer_music.stop()
    points = 0
    invent = Inventory()
    readFile(whatLevel)
    setStart(whatLevel)
    drawScreen()
    dead = False
    started = False
    pygame.display.update()

def youDied():
    global dead
    pygame.mixer_music.stop()
    dead = True
    screenTwo = pygame.Surface((650, 650))
    screenTwo.set_alpha(150)
    screenTwo.fill((0, 0, 0))

    SCREEN.blit(screenTwo, (50, 100))

    spaceText = fontObjFifty.render("You were caught. Try again?", True, text, None)
    SCREEN.blit(spaceText, ((650 - spaceText.get_width()) / 2 + 50, (650 / 2) + 50))

    yesDrawing(black)
    noDrawing(black)

    pygame.display.update()

def finalLevel() :
    global goneThroughWin
    goneThroughWin = 0
    if goneThroughWin == 0:
        global won
        won = True
        pygame.mixer_music.stop()
        screenTwo = pygame.Surface((650, 650))
        screenTwo.set_alpha(150)
        screenTwo.fill((0, 0, 0))

        SCREEN.blit(screenTwo, (50, 100))

        spaceText = fontObjFifty.render("You have beat the game!", True, text, None)
        SCREEN.blit(spaceText, ((650 - spaceText.get_width()) / 2 + 50, (650 / 2) + 50))

        spaceText = fontObjFifty.render("Press escape to quit.", True, text, None)
        SCREEN.blit(spaceText, ((650 - spaceText.get_width()) / 2 + 50, (650 / 2) + 100))

        pygame.display.update()
        goneThroughWin += 1

def yesDrawing(buttonColour) :
    # Create a bordered yes and no box
    pygame.draw.rect(SCREEN, grey, (289, 449, 82, 42))
    pygame.draw.rect(SCREEN, buttonColour, (290, 450, 80, 40))

    # Prints out the yes and no
    yesText = fontObjThirty.render('Yes', True, text)
    yesTextSurface = yesText.get_rect()
    yesTextSurface.center = (330, 470)
    SCREEN.blit(yesText, yesTextSurface)

def noDrawing(buttonColour) :
    # Create a bordered yes and no box
    pygame.draw.rect(SCREEN, grey, (379, 449, 82, 42))
    pygame.draw.rect(SCREEN, buttonColour, (380, 450, 80, 40))

    noText = fontObjThirty.render('No', True, text)
    noTextSurface = noText.get_rect()
    noTextSurface.center = (420, 470)
    SCREEN.blit(noText, noTextSurface)

def readFile(levelOn):
    global runBefore, level

    if whatLevel == 1 :
        levelOne = open('levels/LevelOne.txt')

        if runBefore == False :
            for line in levelOne :
                level.append(line.rstrip().split(' '))

            runBefore = True
        else :
            counter = 0
            for line in levelOne :
                level[counter] = line.rstrip().split(' ')
                counter += 1

    if whatLevel == 2 :
        levelTwo = open('levels/LevelTwo.txt')

        counter = 0
        for line in levelTwo :
            if counter < len(level) :
                level[counter] = line.rstrip().split(' ')
            else :
                level.append(line.rstrip().split(' '))
            counter += 1

    if whatLevel == 3 :
        levelThree = open('levels/LevelThree.txt')

        counter = 0
        for line in levelThree :
            if counter < len(level) :
                level[counter] = line.rstrip().split(' ')
            else :
                level.append(line.rstrip().split(' '))
            counter += 1

def setStart(levelNum):
    global savedX, savedY, pointsNeeded, calculatedTime, now

    if levelNum == 1:
        savedX = 9
        savedY = 5
        pointsNeeded = 8
        setEnemy(0)
        now = pygame.time.get_ticks()
        calculatedTime = 600000
    if levelNum == 2:
        savedX = 9
        savedY = 5
        pointsNeeded = 174
        setEnemy(0)
        now = pygame.time.get_ticks()
        calculatedTime = 600000
    if levelNum == 3:
        savedX = 9
        savedY = 5
        pointsNeeded = 175
        setEnemy(0)
        now = pygame.time.get_ticks()
        calculatedTime = 600000

#1 : cat enemy
def setEnemy(enemyNum):
    global originalEnemyX, originalEnemyY, enemySavedX, enemySavedY, hasEnemy
    counter = 0
    if enemyNum == 0 :
        for i in range(0, len(level), 1):
            for j in range(0, len(level[i]), 1):
                if level[i][j] == "E" :
                    counter += 1
                    enemySetOne[enemyNum].setBoardPosition(j, i)
                    #level[i][j] = "G"
                    enemySavedX = j - savedX
                    enemySavedY = i - savedY

        if counter != 0:
            print(str(len(enemySetOne)))
            hasEnemy = True

def drawCharacter() :
    character.draw(SCREEN)
    pygame.display.update()

def moveEnemy(enemyNum) :
    enemyDirection(enemyNum)
    enemyPosition(enemyNum)
    drawEnemy(enemyNum)
    if enemySetOne[enemyNum].getBoardX() == savedX + 6 and enemySetOne[enemyNum].getBoardY() == savedY + 6 :
        youDied()

#1 = right, 2 = left, 3 = up, 4 = down
def drawEnemy(enemyNum) :
    global enemySavedX, enemySavedY
    ###Calculate method
    enemyX = enemySetOne[enemyNum].getBoardX()
    enemyY = enemySetOne[enemyNum].getBoardY()

    tempX = enemyX - savedX
    tempY = enemyY - savedY

    if ((tempX >= 1 and tempX <= 11) and (tempY >= 1 and tempY <= 11)) and enemySetOne[enemyNum].getDrawing() != True :
        enemySetOne[enemyNum].setDrawing(True)
    elif tempX < 0 or tempY < 1 :
        enemySetOne[enemyNum].setDrawing(False)
    elif tempX > 11 or tempY > 11 or ((tempX >= 11 or tempX <= 1) and enemySetOne[enemyNum].getPositionX() > 1) or ((tempY >= 11 or tempY <= 1) and enemySetOne[enemyNum].getPositionY() > 1) :
        enemySetOne[enemyNum].setDrawing(False)
    ###

    direction = enemySetOne[enemyNum].getDirection()

    originalX = enemyX - savedX
    originalY = enemyY - savedY

    if enemySetOne[enemyNum].getDrawing() :
        if direction == 1 :
            drawBlock(originalX, originalY)
            if enemyX != 12 :
                drawBlock(originalX + 1, originalY)
            if enemyX != 0 :
                drawBlock(originalX - 1, originalY)
            SCREEN.blit(enemySetOne[enemyNum].getImage(), (enemySetOne[enemyNum].getPositionX() + 50 + ((enemyX - savedX) * 50), enemySetOne[enemyNum].getPositionY() + 100 + ((enemyY - savedY) * 50)))

        elif direction == 2:
            drawBlock(originalX, originalY)
            if enemyX != 12:
                drawBlock(originalX + 1, originalY)
            if enemyX != 0:
                drawBlock(originalX - 1, originalY)
            SCREEN.blit(enemySetOne[enemyNum].getImage(), (50 - enemySetOne[enemyNum].getPositionX() + ((enemyX - savedX) * 50), enemySetOne[enemyNum].getPositionY() + 100 + ((enemyY - savedY) * 50)))


        elif direction == 3:
            drawBlock(originalX, originalY)
            if enemyY != 12:
                drawBlock(originalX, originalY + 1)
            if enemyY != 0:
                drawBlock(originalX, originalY - 1)
            SCREEN.blit(enemySetOne[enemyNum].getImage(), (50 + enemySetOne[enemyNum].getPositionX() + ((enemyX - savedX) * 50), 100 - enemySetOne[enemyNum].getPositionY() + ((enemyY - savedY) * 50)))

        elif direction == 4:
            drawBlock(originalX, originalY)
            if enemyY != 12:
                drawBlock(originalX, originalY + 1)
            if enemyY != 0:
                drawBlock(originalX, originalY - 1)
            SCREEN.blit(enemySetOne[enemyNum].getImage(), (50 + enemySetOne[enemyNum].getPositionX() + ((enemyX - savedX) * 50), 100 + enemySetOne[enemyNum].getPositionY() + ((enemyY - savedY) * 50)))

        enemySavedX = originalX
        enemySavedY = originalY

        pygame.display.update()

def enemyDirection(enemyNum) :
    if enemySetOne[enemyNum].getChange() == True :
        enemySetOne[enemyNum].changeDirection(False)

        enemyX = enemySetOne[enemyNum].getBoardX()
        enemyY = enemySetOne[enemyNum].getBoardY()


        if savedX + 6 > enemyX :
            if level[enemyY][enemyX + 1] == "G" :
                enemySetOne[enemyNum].setDirection(1)
            elif savedY + 6 < enemyY :
                if level[enemyY - 1][enemyX] == "G" :
                    enemySetOne[enemyNum].setDirection(3)
            elif savedY + 6 < enemyY:
                if level[enemyY + 1][enemyX] == "G" :
                    enemySetOne[enemyNum].setDirection(4)
            elif level[enemyY][enemyX - 1] == "G" :
                enemySetOne[enemyNum].setDirection(2)
        elif savedX + 6 < enemyX :
            if level[enemyY][enemyX - 1] == "G":
                enemySetOne[enemyNum].setDirection(2)
            elif savedY + 6 < enemyY:
                if level[enemyY - 1][enemyX] == "G":
                    enemySetOne[enemyNum].setDirection(3)
            elif savedY + 6 < enemyY:
                if level[enemyY + 1][enemyX] == "G":
                    enemySetOne[enemyNum].setDirection(4)
            elif level[enemyY][enemyX + 1] == "G":
                enemySetOne[enemyNum].setDirection(1)
        elif savedY + 6 < enemyY :
            if level[enemyY - 1][enemyX] == "G":
                enemySetOne[enemyNum].setDirection(3)
            elif level[enemyY][enemyX - 1] == "G":
                enemySetOne[enemyNum].setDirection(2)
            elif level[enemyY][enemyX + 1] == "G":
                enemySetOne[enemyNum].setDirection(1)
            elif level[enemyY + 1][enemyX] == "G":
                enemySetOne[enemyNum].setDirection(4)
        elif savedY + 6 > enemyY :
            if level[enemyY + 1][enemyX] == "G":
                enemySetOne[enemyNum].setDirection(4)
            elif level[enemyY][enemyX - 1] == "G":
                enemySetOne[enemyNum].setDirection(2)
            elif level[enemyY][enemyX + 1] == "G":
                enemySetOne[enemyNum].setDirection(1)
            elif level[enemyY - 1][enemyX] == "G":
                enemySetOne[enemyNum].setDirection(3)

def enemyPosition(enemyNum):
    global dead
    enemyX = enemySetOne[enemyNum].getBoardX()
    enemyY = enemySetOne[enemyNum].getBoardY()

    posX = enemySetOne[enemyNum].getPositionX()
    posY = enemySetOne[enemyNum].getPositionY()


    if enemySetOne[enemyNum].getDirection() == 1 :
        enemySetOne[enemyNum].setXY(posX + 1, posY)

        if enemySetOne[enemyNum].getPositionX() == 50 :
            enemySetOne[enemyNum].setBoardPosition(enemySetOne[enemyNum].getBoardX() + 1, enemySetOne[enemyNum].getBoardY())
            enemySetOne[enemyNum].setXY(0, 0)
            enemySetOne[enemyNum].changeDirection(True)

    elif enemySetOne[enemyNum].getDirection() == 2 :
        enemySetOne[enemyNum].setXY(posX + 1, posY)

        if enemySetOne[enemyNum].getPositionX() == 50 :
            enemySetOne[enemyNum].setBoardPosition(enemySetOne[enemyNum].getBoardX() - 1, enemySetOne[enemyNum].getBoardY())
            enemySetOne[enemyNum].setXY(0, 0)
            enemySetOne[enemyNum].changeDirection(True)

    elif enemySetOne[enemyNum].getDirection() == 3 :
        enemySetOne[enemyNum].setXY(posX, posY + 1)

        if enemySetOne[enemyNum].getPositionY() == 50 :
            enemySetOne[enemyNum].setBoardPosition(enemySetOne[enemyNum].getBoardX(), enemySetOne[enemyNum].getBoardY() - 1)
            enemySetOne[enemyNum].setXY(0, 0)
            enemySetOne[enemyNum].changeDirection(True)

    elif enemySetOne[enemyNum].getDirection() == 4 :
        enemySetOne[enemyNum].setXY(posX, posY + 1)

        if enemySetOne[enemyNum].getPositionY() == 50 :
            enemySetOne[enemyNum].setBoardPosition(enemySetOne[enemyNum].getBoardX(), enemySetOne[enemyNum].getBoardY() + 1)
            enemySetOne[enemyNum].setXY(0, 0)
            enemySetOne[enemyNum].changeDirection(True)

#1 = right, 2 = left, 3 = up, 4 = down
def move(direction) :
    global savedX, savedY, dead, points, switchesOn, whatLevel, invent, won
    endGame = False
    if direction == 1 :
        if savedX + 13 < len(level[0]) :
            letter = level [savedY + 6][savedX + 7]
            #ground : G
            if letter == "G" :
                moveCharacter(1)
            #f : switch
            elif letter == "f" :
                moveCharacter(1)
                switchesOn = not switchesOn
            #Move up : w
            elif letter == "q" :
                moveCharacter(1)
                if switchesOn :
                    move(3)
            #Move right : d
            elif letter == "d" :
                moveCharacter(1)
                if switchesOn:
                    move(1)
            #Move down : s
            elif letter == "s" :
                moveCharacter(1)
                if switchesOn:
                    move(4)
            #Move left : a
            elif letter == "a" :
                moveCharacter(1)
                if switchesOn:
                    move(2)
            #hints : #
            elif letter in {"1", "2", "3", "4", "5", "6"} :
                moveCharacter(1)
                drawHint(letter)
            #redKey : r
            elif letter == "r" :
                level[savedY + 6][savedX + 7] = "G"
                invent.getRedKey()
                moveCharacter(1)
            #redDoor : R
            elif letter == "R" and invent.returnRedKey() :
                level[savedY + 6][savedX + 7] = "G"
                invent.loseRedKey()
                moveCharacter(1)
            # blueKey : b
            elif letter == "b":
                level[savedY + 6][savedX + 7] = "G"
                invent.getBlueKey()
                moveCharacter(1)
            # blueDoor : B
            elif letter == "B" and invent.returnBlueKey():
                level[savedY + 6][savedX + 7] = "G"
                invent.loseBlueKey()
                moveCharacter(1)
            # greenKey : g
            elif letter == "g":
                level[savedY + 6][savedX + 7] = "G"
                invent.getGreenKey()
                moveCharacter(1)
            # greenDoor : D
            elif letter == "D" and invent.returnGreenKey():
                level[savedY + 6][savedX + 7] = "G"
                invent.loseGreenKey()
                moveCharacter(1)
            #squeaky floor : J : no socks
            elif letter == "J" and invent.returnSocks() == False :
                pygame.mixer.Channel(0).play(audioOne, loops=0, maxtime=2000)
                moveCharacter(1)
                pygame.mixer_music.stop()
                time.sleep(2.5)
                endGame = True
            #squeaky floor : J : with socks
            elif letter == "J" and invent.returnSocks() :
                moveCharacter(1)
            #waterBoots : j
            elif letter == "j" :
                level[savedY + 6][savedX + 7] = "G"
                invent.getSocks()
                moveCharacter(1)
            #water : W : no boots
            elif letter == "W" and invent.returnWaterBoot() == False :
                pygame.mixer.Channel(0).play(audioTwo, loops=0, maxtime=4000)
                moveCharacter(1)
                pygame.mixer_music.stop()
                time.sleep(2.75)
                endGame = True
            #water : W : with boots
            elif letter == "W" and invent.returnWaterBoot() :
                level[savedY + 6][savedX + 7] = "G"
                moveCharacter(1)
            #waterBoots : w
            elif letter == "w" :
                level[savedY + 6][savedX + 7] = "G"
                invent.getWaterBoot()
                moveCharacter(1)
            # flashlight : F
            elif letter == "F":
                level[savedY + 6][savedX + 7] = "G"
                invent.getFlashlight()
                moveCharacter(1)
            #ice : I : no skates
            elif letter == "I" and invent.returnIceSkate() == False :
                moveCharacter(1)
                move(1)
            #ice : I : with skates
            elif letter == "I" and invent.returnIceSkate() :
                moveCharacter(1)
            #iceSkates : i
            elif letter == "i" :
                level[savedY + 6][savedX + 7] = "G"
                invent.getIceSkate()
                moveCharacter(1)
            # cookies : c
            elif letter == "c":
                level[savedY + 6][savedX + 7] = "G"
                points += 1
                moveCharacter(1)
            elif letter == "V" and points == pointsNeeded :
                moveCharacter(1)
                if whatLevel != 3:
                    whatLevel += 1
                    nextLevel()
                elif whatLevel == 3:
                    won = True
            elif letter == "T":
                switchesOn = True
                invent = Inventory()
                drawInventory()
                moveCharacter(1)
            # end door without points : V
            elif letter == "V" and points != pointsNeeded :
                drawHint(6)
    elif direction == 2 :
        if savedX > 0 :
            letter = level[savedY + 6][savedX + 5]
            #ground : G
            if letter == "G" :
                moveCharacter(2)
            # flashlight : F
            elif letter == "F":
                level[savedY + 6][savedX + 5] = "G"
                invent.getFlashlight()
                moveCharacter(2)
            #squeaky floor : J : no socks
            elif letter == "J" and invent.returnSocks() == False :
                pygame.mixer.Channel(0).play(audioOne, loops=0, maxtime=2000)
                moveCharacter(2)
                pygame.mixer_music.stop()
                time.sleep(2.5)
                endGame = True
                moveCharacter(2)
            #squeaky floor : J : with socks
            elif letter == "J" and invent.returnSocks() :
                moveCharacter(2)
            #waterBoots : j
            elif letter == "j" :
                level[savedY + 6][savedX + 5] = "G"
                invent.getSocks()
                moveCharacter(2)
            #f : switch
            elif letter == "f" :
                moveCharacter(2)
                switchesOn = not switchesOn
            # Move up : w
            elif letter == "q":
                moveCharacter(2)
                if switchesOn:
                    move(3)
            # Move right : d
            elif letter == "d":
                moveCharacter(2)
                if switchesOn:
                    move(1)
            # Move down : s
            elif letter == "s":
                moveCharacter(2)
                if switchesOn:
                    move(4)
            # Move left : a
            elif letter == "a":
                moveCharacter(2)
                if switchesOn:
                    move(2)
            # hints : #
            elif letter in {"1", "2", "3", "4", "5", "6"} :
                moveCharacter(2)
                drawHint(letter)
            #redKey : r
            elif letter == "r" :
                level[savedY + 6][savedX + 5] = "G"
                invent.getRedKey()
                moveCharacter(2)
            #redDoor : R
            elif letter == "R" and invent.returnRedKey() :
                level[savedY + 6][savedX + 5] = "G"
                invent.loseRedKey()
                moveCharacter(2)
            # blueKey : b
            elif letter == "b":
                level[savedY + 6][savedX + 5] = "G"
                invent.getBlueKey()
                moveCharacter(2)
            # blueDoor : B
            elif letter == "B" and invent.returnBlueKey():
                level[savedY + 6][savedX + 5] = "G"
                invent.loseBlueKey()
                moveCharacter(2)
            # greenKey : g
            elif letter == "g":
                level[savedY + 6][savedX + 5] = "G"
                invent.getGreenKey()
                moveCharacter(2)
            # greenDoor : D
            elif letter == "D" and invent.returnGreenKey():
                level[savedY + 6][savedX + 5] = "G"
                invent.loseGreenKey()
                moveCharacter(2)
            #water : W : with boots
            elif letter == "W" and invent.returnWaterBoot() :
                level[savedY + 6][savedX + 5] = "G"
                moveCharacter(2)
            #water : W : no boots
            elif letter == "W" and invent.returnWaterBoot() == False :
                pygame.mixer.Channel(0).play(audioTwo, loops=0, maxtime=4000)
                moveCharacter(2)
                pygame.mixer_music.stop()
                time.sleep(2.75)
                endGame = True
            #waterBoots : w
            elif letter == "w" :
                level[savedY + 6][savedX + 5] = "G"
                invent.getWaterBoot()
                moveCharacter(2)
            # ice : I : no skates
            elif letter == "I" and invent.returnIceSkate() == False:
                moveCharacter(2)
                move(2)
            # ice : I : with skates
            elif letter == "I" and invent.returnIceSkate():
                moveCharacter(2)
            # iceSkates : i
            elif letter == "i":
                level[savedY + 6][savedX + 5] = "G"
                invent.getIceSkate()
                moveCharacter(2)
            # cookies : c
            elif letter == "c":
                level[savedY + 6][savedX + 5] = "G"
                points += 1
                moveCharacter(2)
            # end door with points : V
            elif letter == "V" and points == pointsNeeded :
                moveCharacter(2)
                if whatLevel != 3:
                    whatLevel += 1
                    nextLevel()
                elif level == 3:
                    won = True
            # end door without points : V
            elif letter == "V" and points != pointsNeeded :
                drawHint(6)
            elif letter == "T":
                switchesOn = True
                invent = Inventory()
                drawInventory()
                moveCharacter(2)
    elif direction == 3 :
        if savedY > 0 :
            letter = level[savedY + 5][savedX + 6]
            #ground : G
            if letter == "G" :
                moveCharacter(3)
            # end door without points : V
            elif letter == "V" and points != pointsNeeded:
                drawHint(6)
            # flashlight : F
            elif letter == "F":
                level[savedY + 5][savedX + 6] = "G"
                invent.getFlashlight()
                moveCharacter(3)
            #squeaky floor : J : no socks
            elif letter == "J" and invent.returnSocks() == False :
                pygame.mixer.Channel(0).play(audioOne, loops=0, maxtime=2000)
                moveCharacter(3)
                pygame.mixer_music.stop()
                time.sleep(2.5)
                endGame = True
                moveCharacter(3)
            #squeaky floor : J : with socks
            elif letter == "J" and invent.returnSocks() :
                moveCharacter(3)
            #waterBoots : j
            elif letter == "j" :
                level[savedY + 5][savedX + 6] = "G"
                invent.getSocks()
                moveCharacter(3)
            #f : switch
            elif letter == "f" :
                moveCharacter(3)
                switchesOn = not switchesOn
            # Move up : w
            elif letter == "q":
                moveCharacter(3)
                if switchesOn:
                    move(3)
            # Move right : d
            elif letter == "d":
                moveCharacter(3)
                if switchesOn:
                    move(1)
            # Move down : s
            elif letter == "s":
                moveCharacter(3)
                if switchesOn:
                    move(4)
            # Move left : a
            elif letter == "a":
                moveCharacter(3)
                if switchesOn:
                    move(2)
            # hints : #
            elif letter in {"1", "2", "3", "4", "5", "6"} :
                moveCharacter(3)
                drawHint(letter)
            #redKey : r
            elif letter == "r" :
                level[savedY + 5][savedX + 6] = "G"
                invent.getRedKey()
                moveCharacter(3)
            #redDoor : R
            elif letter == "R" and invent.returnRedKey() :
                level[savedY + 5][savedX + 6] = "G"
                invent.loseRedKey()
                moveCharacter(3)
            # blueKey : b
            elif letter == "b":
                level[savedY + 5][savedX + 6] = "G"
                invent.getBlueKey()
                moveCharacter(3)
            # blueDoor : B
            elif letter == "B" and invent.returnBlueKey():
                level[savedY + 5][savedX + 6] = "G"
                invent.loseBlueKey()
                moveCharacter(3)
            # greenKey : g
            elif letter == "g":
                level[savedY + 5][savedX + 6] = "G"
                invent.getGreenKey()
                moveCharacter(3)
            # greenDoor : D
            elif letter == "D" and invent.returnGreenKey():
                level[savedY + 5][savedX + 6] = "G"
                invent.loseGreenKey()
                moveCharacter(3)
            #water : W : with boots
            elif letter == "W" and invent.returnWaterBoot() :
                level[savedY + 5][savedX + 6] = "G"
                moveCharacter(3)
            #water : W : no boots
            elif letter == "W" and invent.returnWaterBoot() == False :
                pygame.mixer.Channel(0).play(audioTwo, loops=0, maxtime=4000)
                moveCharacter(3)
                pygame.mixer_music.stop()
                time.sleep(2.75)
                endGame = True
            #waterBoots : w
            elif letter == "w" :
                level[savedY + 5][savedX + 6] = "G"
                invent.getWaterBoot()
                moveCharacter(3)
            # ice : I : no skates
            elif letter == "I" and invent.returnIceSkate() == False:
                moveCharacter(3)
                move(3)
            # ice : I : with skates
            elif letter == "I" and invent.returnIceSkate():
                moveCharacter(3)
            # iceSkates : i
            elif letter == "i":
                level[savedY + 5][savedX + 6] = "G"
                invent.getIceSkate()
                moveCharacter(3)
            # cookies : c
            elif letter == "c":
                level[savedY + 5][savedX + 6] = "G"
                points += 1
                moveCharacter(3)
            elif letter == "V" and points == pointsNeeded :
                moveCharacter(3)
                if whatLevel != 3:
                    whatLevel += 1
                    nextLevel()
                elif whatLevel == 3:
                    won = True
            elif letter == "T":
                switchesOn = True
                invent = Inventory()
                drawInventory()
                moveCharacter(3)
    elif direction == 4 :
        if savedY + 13 < len(level) :
            letter = level[savedY + 7][savedX + 6]
            #ground : G
            if letter == "G" :
                moveCharacter(4)
            # end door without points : V
            elif letter == "V" and points != pointsNeeded :
                drawHint(6)
            # flashlight : F
            elif letter == "F":
                level[savedY + 7][savedX + 6] = "G"
                invent.getFlashlight()
                moveCharacter(4)
            elif letter == "V" and points == pointsNeeded :
                moveCharacter(4)
                print(str(whatLevel))
                if whatLevel != 3:
                    whatLevel += 1
                    nextLevel()
                elif whatLevel == 3:
                    won = True
            # stealing block : T
            elif letter == "T":
                switchesOn = True
                invent = Inventory()
                drawInventory()
                moveCharacter(4)
            #squeaky floor : J : no socks
            elif letter == "J" and invent.returnSocks() == False :
                pygame.mixer.Channel(0).play(audioOne, loops=0, maxtime=2000)
                moveCharacter(4)
                pygame.mixer_music.stop()
                time.sleep(2.5)
                endGame = True
                moveCharacter(4)
            #squeaky floor : J : with socks
            elif letter == "J" and invent.returnSocks() :
                moveCharacter(4)
            #waterBoots : j
            elif letter == "j" :
                level[savedY + 7][savedX + 6] = "G"
                invent.getSocks()
                moveCharacter(4)
            #f : switch
            elif letter == "f" :
                moveCharacter(4)
                switchesOn = not switchesOn
            # Move up : w
            elif letter == "q":
                moveCharacter(4)
                if switchesOn:
                    move(3)
            # Move right : d
            elif letter == "d":
                moveCharacter(4)
                if switchesOn:
                    move(1)
            # Move down : s
            elif letter == "s":
                moveCharacter(4)
                if switchesOn:
                    move(4)
            # Move left : a
            elif letter == "a":
                moveCharacter(4)
                if switchesOn:
                    move(2)
            # hints : #
            elif letter in {"1", "2", "3", "4", "5", "6"} :
                moveCharacter(4)
                drawHint(letter)
            #redKey : r
            elif letter == "r" :
                level[savedY + 7][savedX + 6] = "G"
                invent.getRedKey()
                moveCharacter(4)
            #redDoor : R
            elif letter == "R" and invent.returnRedKey() :
                level[savedY + 7][savedX + 6] = "G"
                invent.loseRedKey()
                moveCharacter(4)
            # blueKey : b
            elif letter == "b":
                level[savedY + 7][savedX + 6] = "G"
                invent.getBlueKey()
                moveCharacter(4)
            # blueDoor : B
            elif letter == "B" and invent.returnBlueKey():
                level[savedY + 7][savedX + 6] = "G"
                invent.loseBlueKey()
                moveCharacter(4)
            # greenKey : g
            elif letter == "g":
                level[savedY + 7][savedX + 6] = "G"
                invent.getGreenKey()
                moveCharacter(4)
            # greenDoor : D
            elif letter == "D" and invent.returnGreenKey():
                level[savedY + 7][savedX + 6] = "G"
                invent.loseGreenKey()
                moveCharacter(4)
            #water : W : with boots
            elif letter == "W" and invent.returnWaterBoot() :
                level[savedY + 7][savedX + 6] = "G"
                moveCharacter(4)
            #water : W : no boots
            elif letter == "W" and invent.returnWaterBoot() == False :
                pygame.mixer.Channel(0).play(audioTwo, loops=0, maxtime=4000)
                moveCharacter(4)
                pygame.mixer_music.stop()
                time.sleep(2.75)
                endGame = True
            #waterBoots : w
            elif letter == "w" :
                level[savedY + 7][savedX + 6] = "G"
                invent.getWaterBoot()
                moveCharacter(4)
            #ice : I : no skates
            elif letter == "I" :
                moveCharacter(4)
                move(4)
            # ice : I : no skates
            elif letter == "I" and invent.returnIceSkate() == False:
                moveCharacter(4)
                move(4)
            # ice : I : with skates
            elif letter == "I" and invent.returnIceSkate():
                moveCharacter(4)
            # iceSkates : i
            elif letter == "i":
                level[savedY + 7][savedX + 6] = "G"
                invent.getIceSkate()
                moveCharacter(4)
            # cookies : c
            elif letter == "c":
                level[savedY + 7][savedX + 6] = "G"
                points += 1
                moveCharacter(4)

    if endGame == True :
        youDied()

def drawHint(hintNum):
    pygame.draw.rect(SCREEN, white, ((149, 149, 452, 202)))
    pygame.draw.rect(SCREEN, black, ((150, 150, 450, 200)))

    #legos hint
    if hintNum == "1":
        hintText = fontObjThirtyType.render("The lego blocks can be", True, text, None)
        SCREEN.blit(hintText, (160, 160))
        hintText = fontObjThirtyType.render("passed when the legos are", True, text, None)
        SCREEN.blit(hintText, (160, 200))
        hintText = fontObjThirtyType.render("in a toy box", True, text, None)
        SCREEN.blit(hintText, (160, 240))
    #Switches hint
    if hintNum == "2":
        hintText = fontObjThirtyType.render("Switches turn the", True, text, None)
        SCREEN.blit(hintText, (160, 160))
        hintText = fontObjThirtyType.render("directional floors off", True, text, None)
        SCREEN.blit(hintText, (160, 200))
        hintText = fontObjThirtyType.render("and on.", True, text, None)
        SCREEN.blit(hintText, (160, 240))
    #Squeaky floor hint
    if hintNum == "3":
        hintText = fontObjThirtyType.render("You need socks to be", True, text, None)
        SCREEN.blit(hintText, (160, 160))
        hintText = fontObjThirtyType.render("quiet on the squeaky", True, text, None)
        SCREEN.blit(hintText, (160, 200))
        hintText = fontObjThirtyType.render("floors.", True, text, None)
        SCREEN.blit(hintText, (160, 240))
    # really bad hint
    if hintNum == "4":
        hintText = fontObjThirtyType.render("You are near the end. Press", True, text, None)
        SCREEN.blit(hintText, (160, 160))
        hintText = fontObjThirtyType.render("G to go through the final", True, text, None)
        SCREEN.blit(hintText, (160, 200))
        hintText = fontObjThirtyType.render("door.", True, text, None)
        SCREEN.blit(hintText, (160, 240))
    # only helpful hint
    if hintNum == "5":
        hintText = fontObjThirtyType.render("You are near the end. If", True, text, None)
        SCREEN.blit(hintText, (160, 160))
        hintText = fontObjThirtyType.render("you press any buttons but", True, text, None)
        SCREEN.blit(hintText, (160, 200))
        hintText = fontObjThirtyType.render("the space and arrow keys,", True, text, None)
        SCREEN.blit(hintText, (160, 240))
        hintText = fontObjThirtyType.render("You will restart the level.", True, text, None)
        SCREEN.blit(hintText, (160, 280))

    # only helpful hint
    if hintNum == 6:
        print("here")
        hintText = fontObjThirtyType.render("You still have to find", True, text, None)
        SCREEN.blit(hintText, (160, 160))
        hintText = fontObjThirtyType.render(str(pointsNeeded - points) + " cookies.", True, text, None)
        SCREEN.blit(hintText, (160, 200))

    pygame.display.update()

def moveCharacter(direction):
    """Move the player and redraw the visible board."""
    global savedX, savedY
    offsets = {1: (1, 0), 2: (-1, 0), 3: (0, -1), 4: (0, 1)}
    if direction in offsets:
        dx, dy = offsets[direction]
        savedX += dx
        savedY += dy

    drawInventory()
    for i in range(13):
        for j in range(13):
            drawBlock(i, j)
    drawScore()
    drawCharacter()
    if hasEnemy:
        drawEnemy(0)

def drawBlock(x, y) :
    j = y
    i = x
    testingY = j + savedY
    testingX = i + savedX
    if (testingY <= 25 or testingY >= 69) or ((j in {5, 6, 7}) and (i in {5, 6, 7}) and invent.returnFlashlight() == True) :
        if level[j + savedY][i + savedX] == "G":
            ground = pygame.image.load("assets/groundTwo.png")
            ground = pygame.transform.scale(ground, (50, 50)).convert_alpha()
            SCREEN.blit(ground, (50 + (i * 50), 100 + (j * 50)))
        # stealing block : T
        if level[j + savedY][i + savedX] == "T":
            ground = pygame.image.load("assets/takeBlock.png")
            ground = pygame.transform.scale(ground, (50, 50)).convert_alpha()
            SCREEN.blit(ground, (50 + (i * 50), 100 + (j * 50)))
        # end door : V
        if level[j + savedY][i + savedX] == "V" :
            ground = pygame.image.load("assets/endDoor.png")
            ground = pygame.transform.scale(ground, (50, 50)).convert_alpha()
            SCREEN.blit(ground, (50 + (i * 50), 100 + (j * 50)))
        # squeaky floor : J
        if level[j + savedY][i + savedX] == "J" :
            ground = pygame.image.load("assets/squeakySteps.png")
            ground = pygame.transform.scale(ground, (50, 50)).convert_alpha()
            SCREEN.blit(ground, (50 + (i * 50), 100 + (j * 50)))
        # socks : j
        if level[j + savedY][i + savedX] == "j":
            ground = pygame.image.load("assets/groundTwo.png")
            ground = pygame.transform.scale(ground, (50, 50)).convert_alpha()
            SCREEN.blit(ground, (50 + (i * 50), 100 + (j * 50)))
            keyImage = pygame.image.load("assets/socks.png")
            keyImage = pygame.transform.scale(keyImage, (50, 50)).convert_alpha()
            SCREEN.blit(keyImage, (50 + (i * 50), 100 + (j * 50)))
        # switch : f
        if level[j + savedY][i + savedX] == "f":
            if switchesOn :
                ground = pygame.image.load("assets/switchOn.png")
                ground = pygame.transform.scale(ground, (50, 50)).convert_alpha()
                SCREEN.blit(ground, (50 + (i * 50), 100 + (j * 50)))
            else :
                ground = pygame.image.load("assets/switchOff.png")
                ground = pygame.transform.scale(ground, (50, 50)).convert_alpha()
                SCREEN.blit(ground, (50 + (i * 50), 100 + (j * 50)))
        # right : d
        if level[j + savedY][i + savedX] == "d":
            ground = pygame.image.load("assets/rightFloor.png")
            ground = pygame.transform.scale(ground, (50, 50)).convert_alpha()
            SCREEN.blit(ground, (50 + (i * 50), 100 + (j * 50)))
        # left : a
        if level[j + savedY][i + savedX] == "a":
            ground = pygame.image.load("assets/leftFloor.png")
            ground = pygame.transform.scale(ground, (50, 50)).convert_alpha()
            SCREEN.blit(ground, (50 + (i * 50), 100 + (j * 50)))
        # up : q
        if level[j + savedY][i + savedX] == "q":
            ground = pygame.image.load("assets/upFloor.png")
            ground = pygame.transform.scale(ground, (50, 50)).convert_alpha()
            SCREEN.blit(ground, (50 + (i * 50), 100 + (j * 50)))
        # down : s
        if level[j + savedY][i + savedX] == "s":
            ground = pygame.image.load("assets/downFloor.png")
            ground = pygame.transform.scale(ground, (50, 50)).convert_alpha()
            SCREEN.blit(ground, (50 + (i * 50), 100 + (j * 50)))
        # hint : 1, 2, 3, 4, etc.
        if level[j + savedY][i + savedX] in {"1", "2", "3", "4", "5", "6"} :
            ground = pygame.image.load("assets/hintBlock.png").convert_alpha()
            SCREEN.blit(ground, (50 + (i * 50), 100 + (j * 50)))
        # enemy : E
        if level[j + savedY][i + savedX] == "E":
            ground = pygame.image.load("assets/groundTwo.png")
            ground = pygame.transform.scale(ground, (50, 50)).convert_alpha()
            SCREEN.blit(ground, (50 + (i * 50), 100 + (j * 50)))
            characterImage = pygame.image.load("assets/enemyOne.png")
            updateImage = pygame.transform.scale(characterImage, (50, 50)).convert_alpha()
            SCREEN.blit(updateImage, (50 + (i * 50), 100 + (j * 50)))
            level[j + savedY][i + savedX] = "G"
        # wall : n
        if level[j + savedY][i + savedX] == "n":
            ground = pygame.image.load("assets/wall.png")
            ground = pygame.transform.scale(ground, (50, 50)).convert_alpha()
            SCREEN.blit(ground, (50 + (i * 50), 100 + (j * 50)))
        # redDoor : R
        if level[j + savedY][i + savedX] == "R":
            ground = pygame.image.load("assets/redDoor.png")
            ground = pygame.transform.scale(ground, (50, 50)).convert_alpha()
            SCREEN.blit(ground, (50 + (i * 50), 100 + (j * 50)))
        # blueDoor : B
        if level[j + savedY][i + savedX] == "B" :
            ground = pygame.image.load("assets/blueDoor.png")
            ground = pygame.transform.scale(ground, (50, 50)).convert_alpha()
            SCREEN.blit(ground, (50 + (i * 50), 100 + (j * 50)))
        # greenDoor : D
        if level[j + savedY][i + savedX] == "D":
            ground = pygame.image.load("assets/greenDoor.png")
            ground = pygame.transform.scale(ground, (50, 50)).convert_alpha()
            SCREEN.blit(ground, (50 + (i * 50), 100 + (j * 50)))
        # redKey : r
        if level[j + savedY][i + savedX] == "r":
            ground = pygame.image.load("assets/groundTwo.png")
            ground = pygame.transform.scale(ground, (50, 50)).convert_alpha()
            SCREEN.blit(ground, (50 + (i * 50), 100 + (j * 50)))
            keyImage = pygame.image.load("assets/redKey.png")
            keyImage = pygame.transform.scale(keyImage, (50, 50)).convert_alpha()
            SCREEN.blit(keyImage, (50 + (i * 50), 100 + (j * 50)))
        # blueKey : b
        if level[j + savedY][i + savedX] == "b":
            ground = pygame.image.load("assets/groundTwo.png")
            ground = pygame.transform.scale(ground, (50, 50)).convert_alpha()
            SCREEN.blit(ground, (50 + (i * 50), 100 + (j * 50)))
            keyImage = pygame.image.load("assets/blueKey.png")
            keyImage = pygame.transform.scale(keyImage, (50, 50)).convert_alpha()
            SCREEN.blit(keyImage, (50 + (i * 50), 100 + (j * 50)))
        # greenKey : g
        if level[j + savedY][i + savedX] == "g":
            ground = pygame.image.load("assets/groundTwo.png")
            ground = pygame.transform.scale(ground, (50, 50)).convert_alpha()
            SCREEN.blit(ground, (50 + (i * 50), 100 + (j * 50)))
            keyImage = pygame.image.load("assets/greenKey.png")
            keyImage = pygame.transform.scale(keyImage, (50, 50)).convert_alpha()
            SCREEN.blit(keyImage, (50 + (i * 50), 100 + (j * 50)))
        # legos : W
        if level[j + savedY][i + savedX] == "W":
            ground = pygame.image.load("assets/legos.png")
            ground = pygame.transform.scale(ground, (50, 50)).convert_alpha()
            SCREEN.blit(ground, (50 + (i * 50), 100 + (j * 50)))
        # toyBox : w
        if level[j + savedY][i + savedX] == "w":
            ground = pygame.image.load("assets/groundTwo.png")
            ground = pygame.transform.scale(ground, (50, 50)).convert_alpha()
            SCREEN.blit(ground, (50 + (i * 50), 100 + (j * 50)))
            image = pygame.image.load("assets/toyBox.png")
            image = pygame.transform.scale(image, (50, 50)).convert_alpha()
            SCREEN.blit(image, (50 + (i * 50), 100 + (j * 50)))
        # ice : I
        if level[j + savedY][i + savedX] == "I":
            ground = pygame.image.load("assets/slickFloor.png")
            ground = pygame.transform.scale(ground, (50, 50)).convert_alpha()
            SCREEN.blit(ground, (50 + (i * 50), 100 + (j * 50)))
        # iceSkate : i
        if level[j + savedY][i + savedX] == "i":
            ground = pygame.image.load("assets/groundTwo.png")
            ground = pygame.transform.scale(ground, (50, 50)).convert_alpha()
            SCREEN.blit(ground, (50 + (i * 50), 100 + (j * 50)))
            image = pygame.image.load("assets/iceSkate.png")
            image = pygame.transform.scale(image, (50, 50)).convert_alpha()
            SCREEN.blit(image, (50 + (i * 50), 100 + (j * 50)))
        # cookie : c
        if level[j + savedY][i + savedX] == "c":
            ground = pygame.image.load("assets/groundTwo.png")
            ground = pygame.transform.scale(ground, (50, 50)).convert_alpha()
            SCREEN.blit(ground, (50 + (i * 50), 100 + (j * 50)))
            image = pygame.image.load("assets/cookie.png")
            image = pygame.transform.scale(image, (50, 50)).convert_alpha()
            SCREEN.blit(image, (50 + (i * 50), 100 + (j * 50)))
        # flashlight : F
        if level[j + savedY][i + savedX] == "F":
            ground = pygame.image.load("assets/groundTwo.png")
            ground = pygame.transform.scale(ground, (50, 50)).convert_alpha()
            SCREEN.blit(ground, (50 + (i * 50), 100 + (j * 50)))
            image = pygame.image.load("assets/flashlight.png")
            image = pygame.transform.scale(image, (50, 50)).convert_alpha()
            SCREEN.blit(image, (50 + (i * 50), 100 + (j * 50)))
        # enemy : E
        if level[j + savedY][i + savedX] == "E":
            ground = pygame.image.load("assets/groundTwo.png")
            ground = pygame.transform.scale(ground, (50, 50)).convert_alpha()
            SCREEN.blit(ground, (50 + (i * 50), 100 + (j * 50)))
            image = pygame.image.load("assets/enemyOne.png")
            image = pygame.transform.scale(image, (50, 50)).convert_alpha()
            SCREEN.blit(image, (50 + (i * 50), 100 + (j * 50)))

        if hasEnemy :
            if j + savedY == enemySetOne[0].getBoardY() - savedY and i + savedX == enemySetOne[0].getBoardX() - savedX :
                moveEnemy(0)

    else :
        pygame.draw.rect(SCREEN, black, (50 + (i * 50), 100 + (j * 50), 50, 50))

def drawScreen():
    drawBackground()

    pygame.draw.line(SCREEN, line, (47, 97), (703, 97), 3)
    pygame.draw.line(SCREEN, line, (47, 753), (703, 753), 3)
    pygame.draw.line(SCREEN, line, (47, 97), (47, 753), 3)
    pygame.draw.line(SCREEN, line, (703, 97), (703, 753), 3)
    pygame.draw.rect(SCREEN, line, (750, 100, 230, 650))

    nameText = fontObjForty.render("Quiet", True, text, None)
    centreX = nameText.get_width()
    SCREEN.blit(nameText, (870 - (centreX / 2), 130))

    nameText = fontObjThreeNine.render("Quiet", True, water, None)
    centreX = nameText.get_width()
    SCREEN.blit(nameText, (870 - (centreX / 2), 130))

    timerText = fontObjTwenty.render("Level " + str(whatLevel), True, text, None)
    SCREEN.blit(timerText, (900, 170))

    timerText = fontObjThirty.render("Time : ", True, text, None)
    SCREEN.blit(timerText, (760, 200))

    scoreText = fontObjThirty.render("Cookies : ", True, text, None)
    SCREEN.blit(scoreText, (760, 240))

    scoreText = fontObjTwenty.render("Press R to restart", True, text, None)
    SCREEN.blit(scoreText, (50, 70))

    drawInventory()
    drawScore()

    for i in range(0, 13, 1) :
        for j in range(0, 13, 1) :
            drawBlock(i, j)
    drawCharacter()

    pygame.display.update()

def drawInventory():
    pygame.draw.rect(SCREEN, lineDark, (763, 398, 204, 104))

    pygame.draw.line(SCREEN, text, (763, 398), (763, 502), 2)
    pygame.draw.line(SCREEN, text, (967, 398), (967, 502), 2)
    pygame.draw.line(SCREEN, text, (763, 398), (967, 398), 2)
    pygame.draw.line(SCREEN, text, (763, 502), (967, 502), 2)
    pygame.draw.line(SCREEN, text, (763, 450), (967, 450), 1)
    pygame.draw.line(SCREEN, text, (815, 398), (815, 502), 1)
    pygame.draw.line(SCREEN, text, (865, 398), (865, 502), 1)
    pygame.draw.line(SCREEN, text, (915, 398), (915, 502), 1)

    if invent.returnInventLen() != 0:
        for i in range(0, invent.returnInventLen(), 1):
            if i <= 3:
                y = 400
                x = i
            else :
                y = 450
                x = i - 4

            SCREEN.blit(invent.returnPic(i), (765 + (x * 50), y))
    pygame.display.update()

def drawScore() :
    global points
    pygame.draw.rect(SCREEN, line, (870, 240, 110, 40))
    scoreText = fontObjThirty.render(str(points), True, text, None)
    SCREEN.blit(scoreText, (870, 240))
    pygame.display.update()

def drawTime() :
    global time
    pygame.draw.rect(SCREEN, line, (850, 240, 130, 40))
    scoreText = fontObjThirty.render(str(time), True, text, None)
    SCREEN.blit(scoreText, (850, 240))
    pygame.display.update()

def drawBackground():
    SCREEN.fill(backGround)

    pygame.display.update()

if __name__ == '__main__':
    main()