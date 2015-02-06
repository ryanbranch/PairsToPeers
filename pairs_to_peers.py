import pygame
import random

pygame.init()

#In the following section, a number of constants are defined.
#These variables have self explanatory names, and are referred to throughout the rest of the code but never change in value.
#Editing these values in the code can change various aspects of the gameplay, like the player's speed.
COLOR_RED = (255,0,0)
COLOR_GREEN = (0,255,0)
COLOR_BLUE = (0,0,255)
COLOR_WHITE = (255,255,255)
COLOR_BLACK = (0,0,0)
GAME_WIDTH = 1366
GAME_HEIGHT = 768
FRAMES_PER_SECOND = 30
FONT = pygame.font.SysFont(None, 25)

#These two lines create the window in which the game is played, titling it "Pairs to Peers".
gameDisplay = pygame.display.set_mode((GAME_WIDTH,GAME_HEIGHT))
pygame.display.set_caption("Pairs to Peers")

#This class defines the players of the game
class Player:
    
    #MEMBER VARIABLES#
        # isHuman - a boolean denoting whether the player is a human (true) or an AI (false)
        # playerName - a string of the name of the player
        # playerNum - the integer value denoting the player's number (1 = Player 1, 2 = Player 2, etc.)
        # score - the integer value of the player's score
    
    #Constructor Method
    def __init__(self, name, number, human):
        self.isHuman = human
        self.playerName = name
        self.playerNum = number
        self.score = 0 #Players are initialized with 0 points

    #This method is used to increase a player's score by a given number of points
    def addPoints(self, pointsToAdd):
        self.score += pointsToAdd

#This class defines the scenario cards, which players consider when playing their corresponding action card.
class Scenario:
    
    #MEMBER VARIABLES#
        # scenarioText - a string describing the scenario
        # beenPlayed - a boolean that keeps track of whether or not the scenario has already been in play during the current game
    
    #Constructor Method
    def __init__(self, cardText):
        self.scenarioText = cardText
        self.beenPlayed = False #Scenario cards are initialized having not been played

    #This method is used to denote that the scenario card has now been played
    def play(self):
        self.beenPlayed = True

#This function takes a string, a color, and a coordinate as input and displays text on the screen accordingly
def displayMessage(messageText,messageColor,messageLocation):
    screen_text = FONT.render(messageText, True, messageColor)
    gameDisplay.blit(screen_text, messageLocation)

#This is the main function of the program.  It handles everything that's going on at each moment of the game
def gameLoop():
    
    gameRun = True #Boolean that stores whether the game should be running
    gameOver = False #Boolean that stores whether the player has lost
    clock = pygame.time.Clock()
    playerArray = []#Initializes the array that will eventually store the players of the game
    scenarioArray = []#Initializes the array that will eventually store the scenario cards
    
    while gameRun: #Continues to execute until gameRun is set to false
        
        while gameOver: #Executes after the game has ended
            gameDisplay.fill(COLOR_BLACK)
            displayMessage("GAME OVER!  Press ENTER to play again, or SPACE to quit.",COLOR_RED,[GAME_WIDTH/3,GAME_HEIGHT/2])
            pygame.display.update()
            
            for event in pygame.event.get():
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_RETURN:
                        gameLoop() #Restarts the game if the player presses the ENTER key
                    if event.key == pygame.K_SPACE:
                        gameRun = False #Closes the game if the player presses the SPACE key
                        gameOver = False
        
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                gameRun = False #Ends the game if they user attempts to close the window
            #Handles events when a key is pressed
            if event.type == pygame.KEYDOWN:
                    
                #This line is just here as a placeholder for future keyboard events to be added
                if event.key == pygame.K_RETURN:
                    gameOver = True
                
        gameDisplay.fill(COLOR_WHITE) #Creates a white background
        displayMessage("The game is running.  Press ENTER to go to the Game Over screen.",COLOR_BLACK,[32,32]) #Draws the score
        pygame.display.update() #Updates the screen every frame
        
        clock.tick(FRAMES_PER_SECOND)
    
    pygame.quit()
    quit()
    
gameLoop()