import  pygame
import random
import math
from pygame import mixer


#initializing pygame
pygame.init()

#setting the screen
screen = pygame.display.set_mode((800,600))

#setting the title
pygame.display.set_caption("Space Invaders")

#setting the background
background = pygame.image.load('background.png')

#setting background music
mixer.music.load('background.wav')
mixer.music.play(-1)

#setting the icon
icon = pygame.image.load('ufo.png')
pygame.display.set_icon(icon)

#scoring and fonting
score = 0
font = pygame.font.Font('freesansbold.ttf', 32)
textX = 10
textY = 10

OVER_font = pygame.font.Font('freesansbold.ttf', 64)


#painting score
def show_score(x, y):
    scoretext = font.render("Score : " + str(score),True, (255,255,255))
    screen.blit(scoretext, (x, y))

def game_over_text():
    OVER_text = OVER_font.render("GAME OVER", True, (255,255,255))
    screen.blit(OVER_text,(200,250))

#setting the player
playerImg = pygame.image.load('player.png')
playerX = 370
playerY = 480
playerX_change = 0
playerSpeed = 3

#setting the enemy
enemyImg = []
enemyX = []
enemyY = []
enemySpeed = []
enemyX_change = []
enemyY_change = []
no_enemies = 6
for i in range(no_enemies):
    enemyImg.append(pygame.image.load('enemy.png'))
    enemyX.append(random.randint(0,736))
    enemyY.append(random.randint(50,150))
    enemySpeed.append(2)
    enemyX_change.append(enemySpeed[i])
    enemyY_change.append(40)

#setting the ammo
#state: ready - Can't see the bullet
#state: fire - bullet is moving
ammoImg = pygame.image.load('ammo.png')
ammoX = 0
ammoY = 480
ammoSpeed = 10
ammoX_change = 0
ammoY_change = ammoSpeed
ammo_state = "ready"

#painting the player
def player(x,y):
     screen.blit(playerImg,(x,y))

#painting the enemy
def enemy(x,y, i):
     screen.blit(enemyImg[i],(x,y))

#painting the fired bullet
def fire_bullet(x, y):
    global ammo_state
    ammo_state = "fire"
    screen.blit(ammoImg,(x + 16, y + 10))

#if bullet hit the enemy returns true else false
def isCollision(enemyX,enemyY,ammoX,ammoY):
    distance = math.sqrt((math.pow((enemyX-ammoX),2))+(math.pow((enemyY-ammoY),2)))
    if distance < 27:
        return True
    else:
        return False

#infinite loop where the program executes
running = True
while running:
    #coloring the bg
    screen.fill((24, 43, 53))
    #coloring the background
    screen.blit(background,(0,0))

    #events in the game
    for event in pygame.event.get():
        
        if event.type == pygame.QUIT: #to check if game is closed
            running = False
        
        if event.type == pygame.KEYDOWN: #checking if key pressed
            
            if event.key == pygame.K_LEFT: #checking if key pressed is left key
                playerX_change -= playerSpeed #moving player to left
            
            if event.key == pygame.K_RIGHT: #checking if key pressed is right key
                playerX_change += playerSpeed #moving player to right
            
            if event.key == pygame.K_SPACE: #checking if key pressed is space
                
                if ammo_state == "ready": #bullet only goes if state is ready
                    ammoSound = mixer.Sound('laser.wav')
                    ammoSound.play()
                    ammoX = playerX #fixing the x-pos
                    fire_bullet(ammoX,ammoY) #paiting the ammo
        
        if event.type == pygame.KEYUP: #checking if key released
            playerX_change += 0

    playerX += playerX_change #changing the x-pos of player

    #code if player goes out of boundaries, and getting it back in the window
    if playerX <= 0:
        playerX = 0
    elif playerX >= 736:
        playerX = 736


    for i in range(no_enemies):
        
        #game over
        if enemyY[i] > 440:
            for j in range(no_enemies):
                enemyY[j] = 2000
            game_over_text()
            break  


        enemyX[i] += enemyX_change[i] #changing the x-pos of enemy

        #code if enemy goes out of boundaries, and getting it back in the window
        if enemyX[i] <= 0: #going right if touched the left boundary
            enemyX_change[i] = enemySpeed[i]
            enemyY[i] += enemyY_change[i] #incrementing x-pos so it may move right
        elif enemyX[i] >= 736: #going left if touched the left boundary
            enemyX_change[i] = -enemySpeed[i]
            enemyY[i] += enemyY_change[i] #decrementing x-pos so it may move left
        
        collision = isCollision(enemyX[i],enemyY[i],ammoX,ammoY)
        if collision: #if enemy hit then
            explodeSound = mixer.Sound('explosion.wav')
            explodeSound.play()
            ammoY = 480 #reset bullet y-pos
            ammo_state = "ready" #reset bullet state to ready
            score += 1 #increment score
            enemyX[i] = random.randint(0,736) #reset that enemies x-pos
            enemyY[i] = random.randint(50,150) #reset that enemies y-pos

        enemy(enemyX[i],enemyY[i], i)    #painting the enemy


    #bullte movement
    if ammoY <= 0: #resetting y-pos if it croses border
            ammo_state = "ready"        
            ammoY = 480
    if ammo_state == "fire": #firing only if state is fire
        fire_bullet(ammoX, ammoY) #paiting the ammo
        ammoY -= ammoY_change #decrementing the y-pos so the bullet may move
        
    


    player(playerX,playerY)    #painting the player
    show_score(textX, textY)    #painting the score
    pygame.display.update()     #updating the window with new positions