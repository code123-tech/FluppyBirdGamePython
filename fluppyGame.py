import random  #For Generating Random Numbers
import sys     #For exit the Game or Programme
import pygame  #Game Library 
from pygame.locals import * 

#Global Game Variables
FPS = 32
SCREENWIDTH = 289
SCREENHEIGHT = 511
SCREEN = pygame.display.set_mode((SCREENWIDTH,SCREENHEIGHT))
GROUNDY = SCREENHEIGHT * 0.8
GAME_SPRITES = {}
GAME_SOUNDS = {}
PLAYER = "gallery/sprites/bird.png"
BACKGROUND = "gallery/sprites/background.png"
PIPE = "gallery/sprites/pipe.png"

def welcomeScreen():
    """
    Shows Welcome Images on the Screen.
    
    """
    playerx = int(SCREENWIDTH/5)
    playery = int((SCREENHEIGHT - GAME_SPRITES['player'].get_height())/2)
    messagex = int((SCREENWIDTH - GAME_SPRITES['message'].get_width())/2)
    messagey = int(SCREENHEIGHT*0.13)
    basex = 0
    while True:
        for event in pygame.event.get():
            # if User Clicks on Cross Button to close the Game
            if(event.type == QUIT or (event.type == KEYDOWN and event.key == K_ESCAPE)):
                pygame.quit()
                sys.exit()
            
            #If the user press Space key or Enter Key to start the Game or Up arrow Key
            elif(event.type == KEYDOWN and (event.key == K_SPACE or event.key == K_UP or event.key == K_KP_ENTER)):
                return 
            #Blit the Images on Screen
            else:
                SCREEN.blit(GAME_SPRITES['background'],(0,0))
                SCREEN.blit(GAME_SPRITES['player'],(playerx,playery))
                SCREEN.blit(GAME_SPRITES['message'],(messagex,messagey))
                SCREEN.blit(GAME_SPRITES['base'],(basex,GROUNDY))
                pygame.display.update()   
                FPSCLOCK.tick(FPS)

#Main Game Function
def mainGame():
    score = 0
    playerx = int(SCREENWIDTH/5)
    playery = int(SCREENHEIGHT/2)
    basex = 0
    
    #Create pipe for bliting on the Screen
    newPipe1 = getRandomPipe()
    newPipe2 = getRandomPipe()
    
    #List of Upper Pipe
    upperPipes = [
        {'x':SCREENWIDTH+200 , 'y':newPipe1[0]['y']},
        {'x':SCREENWIDTH+200 + (SCREENWIDTH/2) , 'y':newPipe2[0]['y']},
    ]
    #list of Lower Pipes
    lowerPipes = [
        {'x':SCREENWIDTH+200 , 'y':newPipe1[1]['y']},
        {'x':SCREENWIDTH+200 + (SCREENWIDTH/2) , 'y':newPipe2[1]['y']},
    ]
    
    pipeVelX = -4
    playerVelY = -9
    playerMaxVelY = 10
    playerMinVelY = -8
    playerAccY = 1
    
    playerFlappAccv = -8  #Velocity While Flapping
    playerFlapped = False  #It is Only True When Bird is Flapping
    
    while True:
        for event in pygame.event.get():
            if(event.type == QUIT or (event.type == KEYDOWN and event.key == K_ESCAPE)):
                pygame.quit()
                sys.exit()
            if(event.type == KEYDOWN and (event.key == K_SPACE or event.key == K_UP or event.key == K_KP_ENTER)):
                if(playery>0):
                    playerVelY = playerFlappAccv
                    playerFlapped = True
                    GAME_SOUNDS['wing'].play()
        #Function For testing Whether the Bird is not collide with Pipes
        crashTest = isCollide(playerx,playery,upperPipes,lowerPipes)
        if crashTest:
            return
        
        #Check For Score
        playerMidPos = playerx + GAME_SPRITES['player'].get_width()/2
        for pipe in upperPipes:
            pipeMidPos = pipe['x'] + GAME_SPRITES['pipe'][0].get_width()/2      #here
            if pipeMidPos <= playerMidPos < pipeMidPos+4:
                score += 1
#                 print(f"Your Score is : {score}")
                GAME_SOUNDS['point'].play()
            
        #Control Movement of the Bird Now
        if playerVelY < playerMaxVelY and not playerFlapped:
            playerVelY += playerAccY
        
        if playerFlapped:
            playerFlapped = False
            
        playerHeight = GAME_SPRITES['player'].get_height()
        playery = playery + min(playerVelY,GROUNDY - playery - playerHeight)
        
        
        #Move Pipes to left
        for upperpipe, lowerpipe in zip(upperPipes,lowerPipes):
            upperpipe['x'] += pipeVelX
            lowerpipe['x'] += pipeVelX
        #Add a new Pipe when First Pipe is about to cross the leftmost part of the Screen
        if 0<upperPipes[0]['x']<5:
            newpipe = getRandomPipe()
            upperPipes.append(newpipe[0])
            lowerPipes.append(newpipe[1])
        
        #If the Pipe is Out of The Screen, Remove it from the screen
        if upperPipes[0]['x'] < -GAME_SPRITES['pipe'][0].get_width():
            upperPipes.pop(0)
            lowerPipes.pop(0)
        
        #Lets Bilt Stripes Now
        SCREEN.blit(GAME_SPRITES['background'],(0,0))
        for upperpipe, lowerpipe in zip(upperPipes,lowerPipes):
            SCREEN.blit(GAME_SPRITES['pipe'][0],(upperpipe['x'],upperpipe['y']))
            SCREEN.blit(GAME_SPRITES['pipe'][1],(lowerpipe['x'],lowerpipe['y']))
        SCREEN.blit(GAME_SPRITES['base'],(basex,GROUNDY))
        SCREEN.blit(GAME_SPRITES['player'],(playerx,playery))
        
        myDigits = [int(x) for x in list(str(score))]
        width = 0
        for digit in myDigits:
            width += GAME_SPRITES['numbers'][digit].get_width()
        XOffset = (SCREENWIDTH - width)/2
        for digit in myDigits:
            SCREEN.blit(GAME_SPRITES['numbers'][digit],(XOffset,SCREENHEIGHT*0.12))
            XOffset += GAME_SPRITES['numbers'][digit].get_width()
        pygame.display.update()
        FPSCLOCK.tick(FPS)
        
def isCollide(playerx,playery,upperPipes,lowerPipes):
    if playery > GROUNDY-25 or playery<0:
        GAME_SOUNDS['hit'].play()
        return True
    
    for pipe in upperPipes:
        pipeHeight = GAME_SPRITES['pipe'][0].get_height()
        if(playery < pipeHeight+pipe['y'] and (abs(playerx - pipe['x']))<GAME_SPRITES['pipe'][0].get_width()):
            GAME_SOUNDS['hit'].play()
            return True
    for pipe in lowerPipes:
        if(playery + GAME_SPRITES['player'].get_height() > pipe['y']) and (abs(playerx - pipe['x']))<GAME_SPRITES['pipe'][0].get_width():
            GAME_SOUNDS['hit'].play()
            return True
    return False
        
    
def getRandomPipe():
    """
    Generate Position of two pipes for  bliting (One Bottom Straight and One Top Rotated) on the Screen
    
    """
    pipeHeight = GAME_SPRITES['pipe'][0].get_height()
    offset = SCREENHEIGHT/3
    y2 = offset + random.randrange(0,int(SCREENHEIGHT-GAME_SPRITES['base'].get_height() - 1.2*offset))
    pipeX = SCREENWIDTH + 10
    y1 = pipeHeight - y2 +offset
    pipe = [
        {'x':pipeX,'y':-y1}, #upper Pipe
        {'x':pipeX,'y':y2}  #lower pipe
    ]
    return pipe
    
if __name__ == "__main__":
    # This will be the main function from where game will start
    pygame.init()  #Initialize all pygame Modules
    FPSCLOCK = pygame.time.Clock()
    pygame.display.set_caption("Play Fluppy Bird")
    GAME_SPRITES['numbers'] = (
        pygame.image.load('gallery/sprites/0.png').convert_alpha(),
        pygame.image.load('gallery/sprites/1.png').convert_alpha(),
        pygame.image.load('gallery/sprites/2.png').convert_alpha(),
        pygame.image.load('gallery/sprites/3.png').convert_alpha(),
        pygame.image.load('gallery/sprites/4.png').convert_alpha(),
        pygame.image.load('gallery/sprites/5.png').convert_alpha(),
        pygame.image.load('gallery/sprites/6.png').convert_alpha(),
        pygame.image.load('gallery/sprites/7.png').convert_alpha(),
        pygame.image.load('gallery/sprites/8.png').convert_alpha(),
        pygame.image.load('gallery/sprites/9.png').convert_alpha(),
    ) 
    GAME_SPRITES['message'] = pygame.image.load("gallery/sprites/message.png").convert_alpha()
    GAME_SPRITES['base'] = pygame.image.load("gallery/sprites/base.png").convert_alpha()
    GAME_SPRITES['pipe'] = (
        pygame.transform.rotate(pygame.image.load(PIPE).convert_alpha(),180),
        pygame.image.load(PIPE).convert_alpha()
    )
    GAME_SPRITES['background'] = pygame.image.load(BACKGROUND).convert()
    GAME_SPRITES['player'] = pygame.image.load(PLAYER).convert_alpha()
    

#Game Sounds
GAME_SOUNDS['die'] = pygame.mixer.Sound("gallery/audio/die.wav")
GAME_SOUNDS['hit'] = pygame.mixer.Sound("gallery/audio/hit.wav")
GAME_SOUNDS['point'] = pygame.mixer.Sound("gallery/audio/point.wav")
GAME_SOUNDS['swoosh'] = pygame.mixer.Sound("gallery/audio/swoosh.wav")
GAME_SOUNDS['wing'] = pygame.mixer.Sound("gallery/audio/wing.wav")

#Game Loop Now
while True:
    welcomeScreen()  #Shows Welcome Screen To user until No press is Done
    mainGame()      #Main Game 