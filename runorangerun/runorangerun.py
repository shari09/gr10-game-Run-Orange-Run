'''
Authors: Shari and Janice
Date: Dec 6, 2018 - Jan 15, 2019
File Name: runOrangeRun.py
Description: This game's objective is to not be turned into orange juice.
'''
import pygame
import random

import os
x = os.path.dirname(os.path.realpath(__file__)) + '/../'
print(x)
os.chdir(x)

pygame.init()

#screen size
WIDTH = 800
HEIGHT= 600
screen = pygame.display.set_mode((WIDTH,HEIGHT))

#colours
BLACK = (0, 0, 0)

#########################
#### pictures and data
#######################

wallpaper = pygame.image.load("wallpaper.png")
wallpaper2 = pygame.image.load("wallpaper2.png")
pauseMenu = pygame.image.load("pause menu.png")
instructionPage = pygame.image.load("instruction.png")
gameOverMenu = pygame.image.load("gameOverMenu.png")
mainPage = pygame.image.load("mainPage.png")
soundMenu = pygame.image.load("sound menu.png")

#running character frames
runningImageNames = ["1.PNG", "2.PNG", "3.PNG", "4.PNG", "5.PNG", "6.PNG", "7.PNG", "8.PNG", \
                  "9.PNG", "10.PNG", "11.PNG", "12.PNG", "13.PNG", "14.PNG", "15.PNG", "16.PNG", \
                  "17.PNG"]
runningPosList = []
for i in range(len(runningImageNames)):
    runningPosList.append(pygame.image.load(runningImageNames[i]))

####obstacle properties (blank for now)
obstacleProperties = {
    "moving knife": {"image": pygame.image.load("knife.png"), \
    "width": 196, "height": 35, "xPos": 800, "yPos": 330, "movable": 0},
    
    "knife": {"image": pygame.image.load("knifeRack.png"), \
    "width": 169, "height": 137, "xPos": 800, "yPos": 230, "movable": 0},
    
    "moving juicer": {"image": pygame.image.load("juicer2.png"), \
    "width": 120, "height": 185, "xPos": 800, "yPos": 325, "movable": "horizontal"},
    
    "hand juicer": {"image": pygame.image.load("juicer.png"), \
    "width": 123, "height": 95, "xPos": 800, "yPos": 415, "movable": 0},
    
    "blender": {"image": pygame.image.load("blend2.png"), \
    "width": 100, "height": 200, "xPos": 800, "yPos": 310, "movable": 0}
    }
    

#jumping character picture
jumpOrng = pygame.image.load("orangeJumping.png")

#rolling character images
rollingOrange1 = pygame.image.load("rolling1.png")
rollingOrange2 = pygame.image.load("rolling2.png")

#sound effects
jumpSound = pygame.mixer.Sound("jump_11.wav")
jumpSound.set_volume(0.8)

rollSound = pygame.mixer.Sound("whoosh.wav")
rollSound.set_volume(0.3)

buttonClick = pygame.mixer.Sound("button.ogg")
buttonClick.set_volume(0.7)

#background music
pygame.mixer.music.load("Surreal-Chase_Looping.mp3")

#button positions (x1, x2, y1, y2)
mainMenuButtons = {
    "play": [350, 490, 250, 400], 
    "exit": [30, 180, 28, 90], 
    "instruction": [650, 770, 28, 90], 
    "sound": [490, 610, 28, 90] 
    }

instructionPageButtons = {"back": [50, 191, 480, 572]}

pauseMenuButtons = {
    "resume": [270, 510, 270, 470], 
    "main menu": [120, 260, 300, 450], 
    "restart": [530, 780, 290, 460] 
    }

soundMenuButtons = {
    "on": [240, 360, 270, 370], 
    "off": [440, 560, 270, 370], 
    "back": [220, 300, 410, 440] 
    }

#wallpaper width
wallpaperWidth = wallpaper.get_width()
wallpaper2Width = wallpaper2.get_width()

#######################
#    functions      #
######################

#background
def drawBackground(speed):
    global backgroundX, backgroundX2, isFirstBackground, isSecondBackground, wallpaperWidth, wallpaper2Width, score

    #first background   
    if isFirstBackground or backgroundX2 + wallpaper2Width <= WIDTH:
        isFirstBackground = True
            
        screen.blit(wallpaper, (backgroundX, 0))

        if backgroundX + wallpaperWidth <= 0:   #first background disappears after it gets to the end
                backgroundX = backgroundX2 + wallpaperWidth
                isFirstBackground = False

    backgroundX -= speed #move the background

    #second background           
    if backgroundX + wallpaperWidth <= WIDTH or isSecondBackground:
        isSecondBackground = True     #keeps it true even if the first condition doesn't match anymore    

        screen.blit(wallpaper2, (backgroundX2, 0))  
               
        if backgroundX2 + wallpaper2Width <= 0: #second background stops after it disappears
            backgroundX2 = backgroundX + wallpaperWidth  #connects with the first background
            isSecondBackground = False
                   
    backgroundX2 -= speed #move the background to match the first one
            
    #other running functions while the game is being played
    generateObstacles(speed)
    addGameScore()
    changeGameSpeed()

#main menu
def displayMainMenu():
    global highScore
    
    screen.blit(mainPage,(0,0))

    #high score
    arial = pygame.font.SysFont("Arial", 20)
    highScoreGraphics = arial.render("High Score: " + str(highScore), 1, BLACK)
    screen.blit(highScoreGraphics, (660, 100))

#pause menu
def displayPauseMenu():
    screen.blit(pauseMenu, (75, 75, 650, 450))
    pygame.display.update()
    
#sound menu
def displaySoundMenu():
    screen.blit(soundMenu, (100,100))
    pygame.display.update()

#drawing one position/frame
def drawOneFrame(frameName, y, speed):
    x = 200
    drawBackground(speed)
    screen.blit(frameName, (x, y))
    pygame.time.delay(10)
    pygame.display.update()

    return x, x + 110, y, y + 130

#running
i = 0  #variable won't get reset every time the function is called
def running():
    global i, orangeX, orangeX2, orangeY, orangeY2, runningPosList
    
    if i != 17:
        orangeX, orangeX2, orangeY, orangeY2 = drawOneFrame(runningPosList[i], 350, 10 + speedChange)
        pygame.display.update()
        i += 1
    else:
        i = 0

#rolling
rolling1 = True # variable will not get reset each time
def rolling():
    global orangeX, orangeY, orangeX2, orangeY2, rolling1

    #sound effects
    if gameMusic:
        rollSound.play()
                   
    if rolling1:
        orangeX, orangeX2, orangeY, orangeY2 = drawOneFrame(rollingOrange1, 430, 30 + speedChange)
        rolling1 = False
    else:        
        orangeX, orangeX2, orangeY, orangeY2 = drawOneFrame(rollingOrange2, 430, 30 + speedChange)
        rolling1 = True

    pygame.display.update()


#jumping
jump = False
airTime = 14
refY = 350
up = True
def jumping():
    global airTime, orangeX, orangeX2, orangeY, orangeY2, jump, refY, up

    #sound effect
    if gameMusic and jump == False:
        jumpSound.play()
    
        
    speed = 40
    jump = True

    if jump == True:
        orangeX, orangeX2, orangeY, orangeY2 = drawOneFrame(jumpOrng, refY, 10+speedChange)

    #move the object up
        if up == True:
            refY -= speed
        if refY <= 100:
            up = False
    #move the object down
        if up == False and airTime == 0:
            refY += speed 
            if refY == 350:
                jump = False
        else:
            airTime -= 1

        if inGame == False:
            jump = False
            
            
    #continuously move the background
        drawBackground(15)

#obstacle collision with the orange
def obstacleCollision(obstacle):
    global inGame, inGameOverMenu
    if (obstacle["xPos"] + obstacle["width"] > orangeX2 > obstacle["xPos"] or \
        obstacle["xPos"] + obstacle["width"] > orangeX > obstacle["xPos"]) \
       and \
       (obstacle["yPos"] + obstacle["height"] > orangeY > obstacle["yPos"] or \
        obstacle["yPos"] + obstacle["height"] > orangeY2 > obstacle["yPos"]):
        
        inGame = False
        inGameOverMenu = True
        obstacle["xPos"] = 800

    return obstacle
    
#obstacle movement
movingObstacleDown = True
movingObstacleLeft = True
horizontalChange = 0
def obstacleMovement(obstacleName, speed):
    global obstacleProperties, inGameOverMenu, inGame, horizontalChange,\
           noObstacle, movingObstacleDown, movingObstacleLeft
    
    #pull the obstacle information out from the big data dictionary
    obstacle = obstacleProperties[obstacleName]
    
    screen.blit(obstacle["image"],(obstacle["xPos"], obstacle["yPos"]))

    #moving the obstacle to match the background
    if obstacle["xPos"] + obstacle["width"] >= 0:
        obstacle["xPos"] -= speed
    else:
        obstacle["xPos"] = 800
        noObstacle = True  #allow generation of new obstacles

    #moving the obstacle horizontally
    if obstacle["movable"] == "horizontal":
        if horizontalChange <= 5 and movingObstacleLeft:
            horizontalChange += 1
            if horizontalChange == 5:
                movingObstacleLeft = False
        else:
            horizontalChange -= 1
            if horizontalChange == 0:
                movingObstacleLeft = True

    obstacle["xPos"] -= horizontalChange

    #colliding with the orange
    obstacle = obstacleCollision(obstacle)
        
    #update the properties
    obstacleProperties[obstacleName] = obstacle
        
#random obstacles
noObstacle = True  #no current obstacles on the screen
currentObstacle = ""
def generateObstacles(speed):
    global noObstacle, currentObstacle, obstacleProperties
    
    obstacleNames = []
    for i in obstacleProperties:
        obstacleNames.append(i)
    
    #randomizing the obstacles
    if noObstacle:
        currentObstacle = random.choice(obstacleNames)
        noObstacle = False
    else:
        obstacleMovement(currentObstacle, speed)
        

#changing game speed
def changeGameSpeed():
    global time, speedChange
    time += 1
    if time == 300 and speedChange <= 40:
        speedChange += 1
        time = 0

#adding the score
def addGameScore():
    global score
    score += 1
    arial = pygame.font.SysFont("Arial", 50)
    scoreGraphics = arial.render(str(score),1,BLACK)
    screen.blit(scoreGraphics, (370, 50))

#music function
def playBackgroundMusic():
    global noMusic, gameMusic, inGame
    if gameMusic:
        if inGame and noMusic:
            pygame.mixer.music.play(-1)
            pygame.mixer.music.set_volume(0.4)
            noMusic = False
        elif not inGame:
            pygame.mixer.music.stop()
            pygame.mixer.music.set_volume(0.4)
            noMusic = True

#button
def button(mousePos, buttonPos):
    x1 = buttonPos[0]
    x2 = buttonPos[1]
    y1 = buttonPos[2]
    y2 = buttonPos[3]
    
    if x1 < mousePos[0] < x2 and y1 < mousePos[1] < y2:
        return True
    else:
        return False
    

################
##game variables
###############
gameIsRunning = True

inMainMenu = True
inInstructionPage = False
inGame = False
inPauseMenu = False
inGameOverMenu = False
inSoundMenu = False
quitGame = False

mousePos = ()

isFirstBackground = True
isSecondBackground = False
backgroundX = 0
backgroundX2 = wallpaperWidth

rollTime = 0
rollTimer = 30
allowRoll = True

orangeX = 0
orangeX2 = 0
orangeY = 0
orangeY2 = 0

time = 0
speedChange = 0
score = 0
highScore = 0

restart = False
noMusic = True
gameMusic = True


#####################################
#                                                                      #
#------               GAME LOOP                    -----#
#                                                                      #
#####################################
while gameIsRunning:

    ########################
    ##           HOME PAGE         ##
    ########################
    while inMainMenu:

        #reset variables
        ####################
        time = 0
        speedChange = 0
        score = 0

        isFirstBackground = True
        isSecondBackground = False
        backgroundX = 0
        backgroundX2 = wallpaperWidth

        rollTime = 0
        rollTimer = 30
        allowRoll = True

        movingObstacleDown = True
        movingObstacleLeft = True
        horizontalChange = 0

        for obstacle in obstacleProperties:
            obstacleProperties[obstacle]["xPos"] = 800

        noObstacle = True
        jump = False
        refY = 350
        up = True
        ####################

        #mouse input
        for event in pygame.event.get():
            if event.type == pygame.MOUSEBUTTONUP:
                mousePos = pygame.mouse.get_pos()   #get the position of the mouse

                #sound effect
                if gameMusic:
                    buttonClick.play()
                    
                #first assume it clicked a button
                inMainMenu = False

                #if the play button is clicked
                if button(mousePos, mainMenuButtons["play"]):
                    inGame = True
                    
                #exit button is clicked
                elif button(mousePos, mainMenuButtons["exit"]):
                    gameIsRunning = False
                    
                #instruction button pressed
                elif button(mousePos, mainMenuButtons["instruction"]):
                    inInstructionPage = True
                  
                #sound button is clicked
                elif button(mousePos, mainMenuButtons["sound"]):
                    inSoundMenu = True

                else: #back to true if no button is clicked
                    inMainMenu = True

        #display the actual menu and music
        displayMainMenu()
        playBackgroundMusic()

        #restart the game
        if restart:
            inMainMenu = False
            inGame = True
            restart = False
        else:
            pygame.display.update()

        
    ###############################
    ##       instruction page
    ###########################
    while inInstructionPage:
        screen.blit(instructionPage, (0, 0))
        playBackgroundMusic()
        pygame.display.update()

        #mouse input
        for event in pygame.event.get():
            if event.type == pygame.MOUSEBUTTONUP:
                mousePos = pygame.mouse.get_pos()   #get the position of the mouse
                
                #sound effect
                if gameMusic:
                    buttonClick.play()

                #if the back key is pressed
                if button(mousePos, instructionPageButtons["back"]):
                    inInstructionPage = False
                    inMainMenu = True

              
    
    ########################
    ######     IN GAME     #########
    ##########################
    while inGame:
        pygame.event.get()
        playBackgroundMusic()
    
        #keyboard input
        keys = pygame.key.get_pressed()
        
        if keys[pygame.K_ESCAPE]:   #escape key
            inGame = False
            inPauseMenu = True
        elif (keys[pygame.K_s] or keys[pygame.K_DOWN]) and allowRoll:  #rolling
            jump = False
            rolling()
            rollTime += 1
            if rollTime == 15:
                allowRoll = False
                rollTime = 0
        elif (keys[pygame.K_w] or keys[pygame.K_UP]) or jump == True: #jumping
            jumping()
        else:   #running
            running()

        #reset variables if jump is false
        if jump == False:
            airTime = 14 - speedChange/2
            refY = 350
            up = True

        #roll timer countdown
        if not allowRoll and rollTimer != 0:
            rollTimer -= 1

        #keydown inputs
        for event in pygame.event.get():
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_s or event.key == pygame.K_DOWN:  #pressing 's' or down arrow key again
                    if rollTimer == 0:
                        allowRoll = True
                        rollTimer = 30  #reset the timer after it reaches 0
            elif event.type == pygame.KEYUP:   
                if event.key == pygame.K_s or event.key == pygame.K_DOWN:     # 's' or down arrow key is released
                    if allowRoll == True:
                        rollTimer = rollTime * 2    #roll timer "matches" the roll time
                    rollTime = 0
                    allowRoll = False
                     
        
    ###################
    ##  pause  menu  ##
    ###################
    while inPauseMenu:
        displayPauseMenu()
        playBackgroundMusic()


       #mouse input
        for event in pygame.event.get():
            if event.type == pygame.MOUSEBUTTONUP:
                mousePos = pygame.mouse.get_pos()   #get the position of the mouse

                #sound effect
                if gameMusic:
                    buttonClick.play()

                inPauseMenu = False

                #if the resume button is clicked
                if button(mousePos, pauseMenuButtons["resume"]):  
                    inGame = True
                    
                elif button(mousePos, pauseMenuButtons["main menu"]):    #home button
                    inMainMenu = True
                    #checking the high score
                    if score > highScore:
                        highScore = score

                elif button(mousePos, pauseMenuButtons["restart"]):    #restart button
                    inMainMenu = True
                    restart = True
                    #checking the high score
                    if score > highScore:
                        highScore = score

                else:
                    inPauseMenu = True
                    

    ###################
    ##  sound  menu  ##
    ###################                    
    while inSoundMenu:
        displaySoundMenu()
        #mouse input
        for event in pygame.event.get():
            if event.type == pygame.MOUSEBUTTONUP:
                mousePos = pygame.mouse.get_pos()

                #sound effect
                if gameMusic:
                    buttonClick.play()

                #when "ON" sound button is clicked
                if button(mousePos, soundMenuButtons["on"]):  
                    gameMusic = True

                #when "OFF" sound button is clicked
                elif button(mousePos, soundMenuButtons["off"]):  
                    gameMusic = False

                #if back button is clicked
                elif button(mousePos, soundMenuButtons["back"]):  
                    inSoundMenu = False
                    inMainMenu = True

                    
    ###################
    ## game over menu  ##
    ###################
    while inGameOverMenu:
        screen.blit(gameOverMenu, (100, 120))
        playBackgroundMusic()

        #checking the high score
        if score > highScore:
            highScore = score
       
        #keyboard input
        for event in pygame.event.get():
            if event.type == pygame.MOUSEBUTTONUP:
                mousePos = pygame.mouse.get_pos()

                #if main menu is clicked
                if 240 < mousePos[0] < 380 and 440 < mousePos[1] < 480:
                    inGameOverMenu = False
                    inMainMenu = True


                #if replay is clicked
                if 420 < mousePos[0] < 560 and 440 < mousePos[1] < 480:
                    inGameOverMenu = False
                    inMainMenu = True
                    restart = True
                   
        pygame.display.update()

#quit pygame
pygame.quit()



