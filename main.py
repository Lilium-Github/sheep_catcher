import pygame
import random
from constants import *
from sheep import Sheep

#set up pygame stuff
pygame.init()  
pygame.display.set_caption("top down game")  # sets the window title
screen = pygame.display.set_mode((800, 800))  # creates game screen
screen.fill((0,0,0))
clock = pygame.time.Clock() #set up clock

#game variables
timer = 0 #used for sheep movement
score = 0

#images and fonts
SheepPic = pygame.image.load("sheep_catcher/sheep.jpg")
font = pygame.font.Font('freesansbold.ttf', 32)
text = font.render('Score:', True, (200, 200, 0))
text2 = font.render(str(score), True, (200, 200, 0))
text3 = font.render('YOU WIN!', True, (200, 200, 0))

#file IO***********************************************************************
scoresFile = open("sheep_catcher/scores.txt", "r") #open the file
scoreData = scoresFile.read() #read in the data
scoresList = scoreData.replace('\n', ' ').split(" ") #shove the data into a list

#here's a cool trick I just learned: convert the list to a dictionary:
it = iter(scoresList)
scoresDict = dict(zip(it, it))

#print the stuff to see if it worked
print("List:", scoresList)
print("dictionary: ", scoresDict)

#spicy challenge: can you figure out how to sort the scores?

#print stuff to the game screen
counter = 0
for x in scoresDict:
    counter+=1
    title = font.render("Most Recent Scores:", True, (200, 200, 0))
    scoretext = font.render(x, True, (200, 200, 0)) #print dictionary key
    scoretext2 = font.render(scoresDict[x], True, (200, 200, 0)) #print dictionary value

    screen.blit(title, (50, 50))
    screen.blit(scoretext, (100, 100*counter))
    screen.blit(scoretext2, (300, 100*counter))

    pygame.display.flip()
    pygame.time.wait(300)#short pause between drawing each score

pygame.time.wait(2000)
scoresFile.close()



#create sheep!
#numbers in list represent xpos, ypos, direction moving, and whether it's been caught or not!
flock = []

for i in range(1,8):
    newSheep = Sheep(random.randrange(100, 700, step=50), random.randrange(100, 700, step=50), SheepPic, i%4)
    flock.append(newSheep)
#make more sheeps here!



#player variables
xpos = 500 #xpos of player
ypos = 200 #ypos of player
vx = 0 #x velocity (left/right speed) of player
vy = 0 #y velocity (up/down speed) of player
keys = [False, False, False, False] #this list holds whether each key has been pressed

while score<7: #GAME LOOP############################################################
    clock.tick(60) #FPS
    timer+=1
   
   
    #Input Section------------------------------------------------------------
    for event in pygame.event.get(): #quit game if x is pressed in top corner
        if event.type == pygame.QUIT:
            gameover = True
     
        #check if a key has been PRESSED
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_LEFT:
                keys[LEFT] = True
            elif event.key == pygame.K_RIGHT:
                keys[RIGHT] = True
            elif event.key == pygame.K_DOWN:
                keys[DOWN] = True
            elif event.key == pygame.K_UP:
                keys[UP] = True

        #check if a key has been LET GO
        elif event.type == pygame.KEYUP:
            if event.key == pygame.K_LEFT:
                keys[LEFT] = False
            elif event.key == pygame.K_RIGHT:
                keys[RIGHT] = False
            elif event.key == pygame.K_DOWN:
                keys[DOWN] = False
            elif event.key == pygame.K_UP:
                keys[UP] = False
         
    #physics
    #section--------------------------------------------------------------------
   
    #player movement!--------
    if keys[LEFT] == True:
        vx = -3
    elif keys[RIGHT] == True:
        vx = 3
    else:
        vx = 0

    if keys[UP] == True:
        vy = -3
    elif keys[DOWN] == True:
        vy = 3
    else:
        vy = 0    


    #player/sheep collision!
    for index, sheep in enumerate(flock):
        score = sheep.collide(xpos, ypos, score)

    #update player position
    xpos+=vx
    ypos+=vy
   
    #update sheep position
    for index, sheep in enumerate(flock):
        sheep.move(timer)
 
    # RENDER
    # Section--------------------------------------------------------------------------------
           
    screen.fill((0,0,0)) #wipe screen so it doesn't smear
 
    #draw player
    pygame.draw.rect(screen, (100, 200, 100), (xpos, ypos, 40, 40))

    #draw sheep
    for index, sheep in enumerate(flock):
        sheep.draw(screen)
   
    #display score
    screen.blit(text, (20, 20))
    text2 = font.render(str(score), True, (200, 200, 0))#update score number
    screen.blit(text2, (140, 20))

    pygame.display.flip()#this actually puts the pixel on the screen
   
#end game loop------------------------------------------------------------------------------

#end screen
screen.fill((0,0,0))
screen.blit(text3, (400,400))
pygame.display.flip()
pygame.time.wait(2000)#pause for a bit before ending

#write score to file
scoresFile = open("sheep_catcher/scores.txt", "w") #open the file
#scoresDict.pop(next(iter(scoresDict))) #get rid of *oldest* score (another new thing I just learned)
name = input("enter 3 initials:")

scoresDict.update({name : random.randrange(100, 900)})#add in initials and a random score
print("updated dictionary:", scoresDict)


for i, j in scoresDict.items(): #write updated dictionary to file
    scoresFile.write(i)
    scoresFile.write(" ")
    scoresFile.write(str(j))
    scoresFile.write("\n")

scoresFile.close()



pygame.quit()