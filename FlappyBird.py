import pygame
import random
import math

pygame.init()
Boldfont = pygame.font.SysFont("impact", 70)
Normalfont = pygame.font.SysFont("arial", 25)
clock = pygame.time.Clock()

# Makes the screen for the game
width = 1400
height = 700
screen = pygame.display.set_mode((width, height), pygame.RESIZABLE)

# Get images
birdImg = pygame.image.load("./Images/FlappyBird.png")
birdImg = pygame.transform.scale(birdImg, (64, 45)) # Original size: 630px * 444px

backgroundImg = pygame.image.load("./Images/Background.png")
backgroundImg = pygame.transform.scale(backgroundImg, (height*1.785714285714286, height)) # Original size: 900px * 504px

pipeImg = pygame.image.load("./Images/Pipe.png")
pipeImgBottom = pygame.transform.scale(pipeImg, (65, 1000)) # Original size: 260px * 4000px
pipeImgTop = pygame.transform.rotate(pipeImgBottom, 180)

# Setting up some variables
birdXPos = 250
birdYPos = 250
birdYSpeed = 0
gravity = 0.0015
jumpHeight = -0.6

score = 0
highScore = 0

pipes = []
pipeGap = 200
pipeSpeed = 0.25

backgroundPos = 0

enableDebug = False
enableInvincibility = False
enableFreeze = False

MOVEEVENT = pygame.USEREVENT
pygame.time.set_timer(MOVEEVENT, 2000)

# Setting up the pipe class

class Pipe:
    def __init__(self):
        self.xPipe = width
        self.yPipe = random.randint(100, height-pipeGap-100)
        self.increasedScore = False

    def run(self):
        # Define pipe rectangles
        topRect = (self.xPipe, self.yPipe-1000, 50, 1000)
        bottomRect = (self.xPipe, self.yPipe+pipeGap,
                      50, height-self.yPipe-pipeGap)

        # Move pipes
        self.xPipe -= pipeSpeed * deltaTime

        # Collision Detection
        bottomCollide = bird.colliderect(bottomRect)
        topCollide = bird.colliderect(topRect)

        if bottomCollide or topCollide:
            gameOver()

        # Draw rectangles
        # pygame.draw.rect(screen, (80, 200, 120), bottomRect)
        # pygame.draw.rect(screen, (80, 200, 120), topRect)
        screen.blit(pipeImgBottom, bottomRect)
        screen.blit(pipeImgTop, topRect)

        # Remove rectangle when offscreen
        if self.xPipe < -600:
            pipes.pop(0)


def gameOver():
    global birdYPos
    global birdYSpeed
    global score
    global highScore

    birdYPos = 250

    if not enableInvincibility:
        if score > highScore:
            highScore = score

        score = 0
        pipes.clear()
        birdYSpeed = 0


def writeText(content, pos):
    screen.blit(Normalfont.render(content, 0, (0, 0, 0)), pos)


# Game loop that will constantly run during the game
runGame = True
while runGame:
    # Goes through all events in the game
    for event in pygame.event.get():
        # Checks if user has closed the window
        if event.type == pygame.QUIT:
            runGame = False
        
        # Properly resize game to screen
        if event.type == pygame.VIDEORESIZE:
            if width != event.w or height != event.h:
                width, height = event.size

                if width < 500:
                    width = 500

                if height < 500:
                    height = 500

                backgroundImg = pygame.transform.scale(backgroundImg, (height*1.785714285714286, height))
                screen = pygame.display.set_mode((width, height), pygame.RESIZABLE)

        # Checks for mouse presses
        if event.type == pygame.MOUSEBUTTONDOWN:
            birdYSpeed = jumpHeight

        # Checks for key presses
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_SPACE:
                birdYSpeed = jumpHeight

            if event.key == pygame.K_ESCAPE:
                runGame = False

            if event.key == pygame.K_F1:
                enableDebug = not enableDebug

            if event.key == pygame.K_F2:
                enableInvincibility = not enableInvincibility

            if event.key == pygame.K_F3:
                enableFreeze = not enableFreeze

        # Spawn new pipe
        if event.type == MOVEEVENT:
            pipes.append(Pipe())

    # Get the time since last frame. Used to set a fixed framerate so the game runs at the same speed on all computers.
    deltaTime = clock.tick(60)

    # Draw background and move background
    screen.fill((255, 0, 0))

    backgroundPos -= 0.1 * deltaTime
    for i in range(math.ceil(width / (height*1.785714285714286+backgroundPos))):
        screen.blit(backgroundImg, (backgroundPos+(height*1.785714285714286*i)-i, 0))
    if backgroundPos < -height*1.785714285714286+2:
        backgroundPos = 0


    # Draw the bird and make it fall
    if not enableFreeze or not enableDebug:
        birdYPos = birdYPos + birdYSpeed * deltaTime
        birdYSpeed = birdYSpeed + gravity * deltaTime

    bird = pygame.Rect(birdXPos, birdYPos-25, 50, 50)
    new_birdImg = pygame.transform.rotate(birdImg, birdYSpeed * -50 + 10)
    new_rect = new_birdImg.get_rect(center = birdImg.get_rect(topleft = (birdXPos-9, birdYPos-22)).center)
    screen.blit(new_birdImg, new_rect)

    # Run and draw the pipes
    for pipe in pipes:
        pipe.run()

        # Increment Score
        if birdXPos > pipe.xPipe and pipe.increasedScore == False:
            score += 1
            pipe.increasedScore = True

    # Display score
    screen.blit(Boldfont.render(str(score), 0, (0, 0, 0)), (width/2, 100))
    screen.blit(Normalfont.render("Score: " +
                str(score), 0, (0, 0, 0)), (40, 40))
    screen.blit(Normalfont.render("High Score: " +
                str(highScore), 0, (0, 0, 0)), (40, 80))

    # If bird is out of the screen, cause a game over
    if birdYPos > height+50 or birdYPos < -50:
        gameOver()

    # Debug Stuff
    if enableDebug:
        container = pygame.Surface((600, 260), pygame.SRCALPHA) # Container size
        container.fill((255, 255, 255, 180)) # Container color
        screen.blit(container, (-10, height-260)) # Container position

        writeText("Debug Stuff (F1)", (20, height-250))

        writeText("Invincible (F2): " + str(enableInvincibility), (20, height-200))
        writeText("FPS: " + str(math.floor(clock.get_fps())), (20, height-160))
        writeText("Delta Time: " + str(deltaTime), (20, height-120))
        writeText("Fun: " + str(random.randint(0, 1000)), (20, height-80))
        writeText("Screen: " + str(width) + "*" + str(height), (20, height-40))

        writeText("Freeze (F3): " + str(enableFreeze), (280, height-200))
        writeText("Background Pos: " + str(backgroundPos), (280, height-160))
        writeText("Pipe Count: " + str(len(pipes)), (280, height-120))
        writeText("Bird Y-Pos: " + str(math.floor(birdYPos)), (280, height-80))
        writeText("Bird Y-Speed: {:0.4f}".format(birdYSpeed), (280, height-40))
        

    # Draws the screen
    pygame.display.flip()

pygame.quit()
