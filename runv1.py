'''
Authors: Shari and Janice
Date: Dec 6, 2018
File Name: runOrangeRun.py
Description: This game's objective is to not be turned into orange juice.
Edit: version 1, look at 'run orange run.py' to see v2
'''
import pygame
import random

pygame.init()

#screen size
WIDTH = 800
HEIGHT= 600
screen = pygame.display.set_mode((WIDTH,HEIGHT))


#colours
WHITE = (255,255,255)
GRAY = (120, 120, 120)
DARKGRAY = (70, 70, 70)
ORANGE = (234, 153, 39)
BLUE = (168, 188, 219)
BROWN = (112, 72, 42)
BLACK = (0, 0, 0)

#########################
#### pictures
#######################

wallpaper = pygame.image.load("wallpaper.png")
wallpaper2 = pygame.image.load("wallpaper2.png")
pauseMenu = pygame.image.load("pause menu.png")
instructionPage = pygame.image.load("instruction.png")
gameOverMenu = pygame.image.load("gameOverMenu.png")
mainPage = pygame.image.load("mainPage.png")
soundMenu = pygame.image.load("sound menu.png")

#running character frames
pos1 = pygame.image.load("1.PNG")
pos2 = pygame.image.load("2.PNG")
pos3 = pygame.image.load("3.PNG")
pos4 = pygame.image.load("4.PNG")
pos5 = pygame.image.load("5.PNG")
pos6 = pygame.image.load("6.PNG")
pos7 = pygame.image.load("7.PNG")
pos8 = pygame.image.load("8.PNG")
pos9 = pygame.image.load("9.PNG")
pos10 = pygame.image.load("10.PNG")
pos11 = pygame.image.load("11.PNG")
pos12 = pygame.image.load("12.PNG")
pos13 = pygame.image.load("13.PNG")
pos14 = pygame.image.load("14.PNG")
pos15 = pygame.image.load("15.PNG")
pos16 = pygame.image.load("16.PNG")
pos17 = pygame.image.load("17.PNG")

#blender image
blend2 = pygame.image.load("blend2.png")

#juicer obstacle
juicer = pygame.image.load("juicer.png")
juicer2 = pygame.image.load("juicer2.png")

#knife obstacle
knife = pygame.image.load("knife.png")

#jumping character picture
jumpOrng = pygame.image.load("orangeJumping.png")

#rolling character images
rollingOrng1 = pygame.image.load("rolling1.png")
rollingOrng2 = pygame.image.load("rolling2.png")

wallpaperWidth = wallpaper.get_width()
wallpaper2Width = wallpaper2.get_width()

#sound effects
jumpSound = pygame.mixer.Sound("jump_11.wav")
jumpSound.set_volume(0.8)

rollSound = pygame.mixer.Sound("whoosh.wav")
rollSound.set_volume(0.3)

buttonClick = pygame.mixer.Sound("button.wav")
buttonClick.set_volume(0.7)

#background music
pygame.mixer.music.load("Surreal-Chase_Looping.mp3")

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
def drawOneFrame(frameName, x, y, speed):
    drawBackground(speed)
    screen.blit(frameName, (x, y))
    pygame.time.delay(10)
    pygame.display.update()

    return x, x + 110, y, y + 130


def drawTempSquare(x, y, width, height, speed):
    drawBackground(speed)
    pygame.draw.rect(screen, ORANGE, (x, y, width, height))
    pygame.time.delay(10)
    pygame.display.update()

    return x, x + width, y, y + height

    
#running
i = 0  #variable won't get reset every time the function is called
def running():
    posNameList = [pos1, pos2, pos3, pos4, pos5, pos6, pos7, pos8, pos9, pos10, pos11, pos12, pos13, pos14, pos15, pos16, pos17]
    global i, orangeX, orangeX2, orangeY, orangeY2
    
    if i != 17:
        orangeX, orangeX2, orangeY, orangeY2 = drawOneFrame(posNameList[i], 350, 350, 10 + speedChange)
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
        orangeX, orangeX2, orangeY, orangeY2 = drawOneFrame(rollingOrng1, 350, 430, 30 + speedChange)
        rolling1 = False
    else:        
        orangeX, orangeX2, orangeY, orangeY2 = drawOneFrame(rollingOrng2, 350, 430, 30 + speedChange)
        rolling1 = True

    pygame.display.update()


#jumping
airTime = 16
def jumping():
    global airTime, orangeX, orangeX2, orangeY, orangeY2

    #sound effect
    if gameMusic:
        jumpSound.play()
    
        
    gravity = 40
    refY = 350
    up = True
    jump = True

    while jump == True:
        orangeX, orangeX2, orangeY, orangeY2 = drawOneFrame(jumpOrng, 350, refY, 10+speedChange)

    #move the object up
        if up == True:
            refY -= gravity
        if refY <= 100:
            up = False
    #move the object down
        if up == False and airTime == 0:
            refY += gravity 
            if refY == 350:
                jump = False
                airTime = 16 - speedChange/2
        else:
            airTime -= 1

        if inGame == False:
            jump = False
            airTime = 16 - speedChange/2
            
    #continuously move the background
        drawBackground(15)
        
#blender collision
blenderX = 800
def blenderObstacle(speed):
    global blenderX, inGameOverMenu, inGame, noObstacle
    
    screen.blit(blend2,(blenderX, 310))

    #moving the blender
    if blenderX + 100 >= 0:
        blenderX -= speed
    else:
        blenderX = 800
        noObstacle = True  #allow generation of new obstacles


    #if the orange touches the blender
    if (blenderX + 100 > orangeX2 > blenderX or blenderX + 100 > orangeX > blenderX) \
       and (orangeY > 310 or orangeY2 > 310):
        inGame = False
        inGameOverMenu = True
        blenderX = 800

#hand juicer obstacle
handJuicerX = 800
def handJuicerObstacle(speed):
    global handJuicerX, inGameOverMenu, inGame, noObstacle
    
    screen.blit(juicer,(handJuicerX, 415))

    #moving the hand juicer
    if handJuicerX + 123 >= 0:
        handJuicerX -= speed
    else:
        handJuicerX = 800
        noObstacle = True  #allow generation of new obstacles


    #if the orange coordinate is "in" the hand juicer
    if (handJuicerX + 123 > orangeX2 > handJuicerX or handJuicerX + 123 > orangeX > handJuicerX) \
       and (orangeY > 415 or orangeY2 > 415):
        inGame = False
        inGameOverMenu = True
        handJuicerX = 800

#knife obstacle
knifeX = 800
def knifeObstacle(speed):
    global knifeX, inGameOverMenu, inGame, noObstacle
    
    screen.blit(knife,(knifeX, 330))

    #moving the knife
    if knifeX + 196 >= 0:
        knifeX -= speed
    else:
        knifeX = 800
        noObstacle = True  #allow generation of new obstacles


    #if the orange coordinate collides with the knife
    if (knifeX + 196 > orangeX2 > knifeX or knifeX + 196 > orangeX > knifeX) \
       and (365 > orangeY > 330 or 365 > orangeY2 > 330):
        inGame = False
        inGameOverMenu = True
        knifeX = 800

#moving knife obstacle
movingKnifeX = 800
movingKnifeY = 250
movingKnifeDown = True
def movingKnifeObstacle(speed):
    global movingKnifeX, movingKnifeY, movingKnifeDown, inGameOverMenu, inGame, noObstacle
    
    screen.blit(knife,(movingKnifeX, movingKnifeY))

    #moving the knife to the left
    if movingKnifeX + 196 >= 0:
        movingKnifeX -= speed
    else:
        movingKnifeX = 800
        noObstacle = True  #allow generation of new obstacles

    #moving the knife up and down
    if movingKnifeY + 35 <= 500 and movingKnifeDown:
        movingKnifeY += 2
        if movingKnifeY + 35 >= 500:
            movingKnifeDown = False
    else:
        movingKnifeY -= 2
        if movingKnifeY <= 250:
            movingKnifeDown = True
    
    #if the orange coordinate collides with the knife
    if (movingKnifeX + 196 > orangeX2 > movingKnifeX or movingKnifeX + 196 > orangeX > movingKnifeX) \
       and (movingKnifeY + 35 > orangeY > movingKnifeY or movingKnifeY + 35 > orangeY2 > movingKnifeY):
        inGame = False
        inGameOverMenu = True
        movingKnifeX = 800

#moving juicer obstacle
movingJuicerX = 800
movingJuicerChange = 0
movingJuicerLeft = True
def movingJuicerObstacle(speed):
    global movingJuicerX, movingJuicerChange, movingJuicerLeft, inGameOverMenu, inGame, noObstacle
    
    screen.blit(juicer2,(movingJuicerX - movingJuicerChange, 325))
    

    #moving the juicer
    if movingJuicerX - movingJuicerChange + 120 >= 0:
        movingJuicerX -= speed
    else:
        movingJuicerX = 800
        movingJuicerChange = 0
        noObstacle = True  #allow generation of new obstacles

    #moving the juicer left and right
    if movingJuicerChange <= 120 and movingJuicerLeft:
        movingJuicerChange += 2
        if movingJuicerChange == 115:
            movingJuicerLeft = False
    else:
        movingJuicerChange -= 2
        if movingJuicerChange == 0:
            movingJuicerLeft = True


    #if the orange coordinate collides with the juicer
    if (movingJuicerX - movingJuicerChange + 120 > orangeX2 > movingJuicerX - movingJuicerChange \
        or movingJuicerX - movingJuicerChange + 120 > orangeX > movingJuicerX - movingJuicerChange) \
       and (510 > orangeY > 325 or 510> orangeY2 > 325):
        inGame = False
        inGameOverMenu = True
        movingJuicerX = 800
        
#random obstacles
noObstacle = True  #no current obstacles on the screen

def generateObstacles(speed):
    global noObstacle, randNum
    

    #generating new numbers
    if noObstacle:
        randNum = random.randint(0, 5)
        
    #randomizing the obstacles
    if randNum == 1:
        noObstacle = False
        blenderObstacle(speed)
        
    elif randNum == 2:
        noObstacle = False
        handJuicerObstacle(speed)
        
    elif randNum == 3:
        noObstacle = False
        knifeObstacle(speed)
        
    elif randNum == 4:
        noObstacle = False
        movingKnifeObstacle(speed)
        
    elif randNum == 5:
        noObstacle = False
        movingJuicerObstacle(speed)

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
    
#draw a grid guideline   
def drawGrid():
    GRIDSIZE = 10
    for x in range(0,WIDTH,GRIDSIZE):
        pygame.draw.line(screen, GRAY, (x,0),(x,HEIGHT),1)
    for y in range(0,HEIGHT,GRIDSIZE):
        pygame.draw.line(screen, GRAY, (0,y),(WIDTH,y),1) 
    for x in range(0,WIDTH,10*GRIDSIZE):
        pygame.draw.line(screen, DARKGRAY, (x,0),(x,HEIGHT),2)
    for y in range(0,HEIGHT,10*GRIDSIZE):
        pygame.draw.line(screen, DARKGRAY, (0,y),(WIDTH,y),2)

#music function
def playMusic():
    global noMusic, gameMusic
    if gameMusic:
        if inGame and noMusic:
            pygame.mixer.music.play(-1)
            pygame.mixer.music.set_volume(0.4)
            noMusic = False
        elif not inGame:
            pygame.mixer.music.stop()
            pygame.mixer.music.set_volume(0.4)
            noMusic = True


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

        movingKnifeX = 800
        movingKnifeY = 200
        movingKnifeDown = True

        knifeX = 800
        blenderX = 800
        handJuicerX = 800
        
        movingJuicerX = 800
        movingJuicerChange = 0
        movingJuicerLeft = True

        noObstacle = True
        ####################

        #mouse input
        for event in pygame.event.get():
            if event.type == pygame.MOUSEBUTTONUP:
                mousePos = pygame.mouse.get_pos()   #get the position of the mouse

                #sound effect
                if gameMusic:
                    buttonClick.play()


                #if the play button is clicked
                if 350 < mousePos[0] < 490 and 250 < mousePos[1] < 400:
                    inMainMenu = False
                    inGame = True

                    
                #exit button is clicked
                elif 30 < mousePos[0] < 180 and 28 < mousePos[1] < 90:
                    inMainMenu = False
                    gameIsRunning = False

                    
                #instruction button pressed
                elif 650 < mousePos[0] < 770 and 28 < mousePos[1] < 90:
                    inMainMenu = False
                    inInstructionPage = True

                    
                #sound button is clicked
                elif 490 < mousePos[0] < 610 and 28 < mousePos[1] < 90:
                    inMainMenu = False
                    inSoundMenu = True



        #display the actual menu and music
        displayMainMenu()
        playMusic()

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
        playMusic()
        pygame.display.update()

        #mouse input
        for event in pygame.event.get():
            if event.type == pygame.MOUSEBUTTONUP:
                mousePos = pygame.mouse.get_pos()   #get the position of the mouse
                
                #sound effect
                if gameMusic:
                    buttonClick.play()

                #if the back key is pressed
                if 50 < mousePos[0] < 191 and 480 < mousePos[1] < 572:
                    inInstructionPage = False
                    inMainMenu = True

              
    
    ########################
    ######     IN GAME     #########
    ##########################
    while inGame:
        pygame.event.get()
        playMusic()
    
        #keyboard input
        keys = pygame.key.get_pressed()
        
        if keys[pygame.K_ESCAPE]:   #escape key
            inGame = False
            inPauseMenu = True
        elif keys[pygame.K_s] and allowRoll:  #rolling
            rolling()
            rollTime += 1
            if rollTime == 15:
                allowRoll = False
                rollTime = 0

        else:   #running
            running()

        #roll timer countdown
        if not allowRoll and rollTimer != 0:
            rollTimer -= 1

        #keydown inputs
        for event in pygame.event.get():
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_w:
                    jumping()

                elif event.key == pygame.K_s:  #pressing 's'  again
                    if rollTimer == 0:
                        allowRoll = True
                        rollTimer = 30  #reset the timer after it reaches 0
            elif event.type == pygame.KEYUP:   
                if event.key == pygame.K_s:     # 's' key is released
                    if allowRoll == True:
                        rollTimer = rollTime * 2    #roll timer "matches" the roll time
                    rollTime = 0
                    allowRoll = False
                     
        
    ###################
    ##  pause  menu  ##
    ###################
    while inPauseMenu:
        displayPauseMenu()
        playMusic()


       #mouse input
        for event in pygame.event.get():
            if event.type == pygame.MOUSEBUTTONUP:
                mousePos = pygame.mouse.get_pos()   #get the position of the mouse

                #sound effect
                if gameMusic:
                    buttonClick.play()

                #if the resume button is clicked
                if 270 < mousePos[0] < 510 and 270 < mousePos[1] < 470:  
                    inPauseMenu = False
                    inGame = True
                    
                elif 120 < mousePos[0] < 260 and 300 < mousePos[1] < 450:  #home button
                    inPauseMenu = False
                    inMainMenu = True
                    #checking the high score
                    if score > highScore:
                        highScore = score

                elif 530 < mousePos[0] < 780 and 290 < mousePos[1] < 460:  #restart button
                    inPauseMenu = False
                    inMainMenu = True
                    restart = True
                    #checking the high score
                    if score > highScore:
                        highScore = score
                    

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
                if 240 < mousePos[0] < 360 and 270 < mousePos[1] < 370:
                    gameMusic = True

                #when "OFF" sound button is clicked
                if 440 < mousePos[0] < 560 and 270 < mousePos[1] < 370:
                    gameMusic = False

                #if back button is clicked
                elif 220 < mousePos[0] < 300 and 410 < mousePos[1] < 440:
                    inSoundMenu = False
                    inMainMenu = True




    ###################
    ## game over menu  ##
    ###################
    while inGameOverMenu:
        screen.blit(gameOverMenu, (100, 120))
        playMusic()

        #checking the high score
        if score > highScore:
            highScore = score
       
        #keyboard input
        for event in pygame.event.get():
            if event.type == pygame.MOUSEBUTTONUP:
                mousePos = pygame.mouse.get_pos()

                #sound effect
                if gameMusic:
                    buttonClick.play()

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





