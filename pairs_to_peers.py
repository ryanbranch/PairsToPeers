#Things marked as important, including those which should potentially be changed down the line, are marked with "#NOTE"
#Important question:  We should ask about the screen resolutions of the computers that the game will primarily be played on.  Because we could definitely program the game in a dynamic way such that the screenc ould be resized and screen elements would change in size appropriately, but it would be significantly easier to not have to worry about that and instead just have some static screen size to build around.

import pygame
import random
from textrect import *

pygame.init()
#In the following section, a number of constants are defined.
#These variables have self explanatory names, and are referred to throughout the rest of the code but never change in value.
#Editing these values in the code can change various aspects of the gameplay, like the player's speed.
COLOR_RED = (255,0,0)
COLOR_GREEN = (0,255,0)
COLOR_BLUE = (0,0,255)
COLOR_WHITE = (255,255,255)
COLOR_BLACK = (0,0,0)
GAME_WIDTH = 1024
GAME_HEIGHT = 768
FRAMES_PER_SECOND = 30
ANSWERS_PER_PLAYER = 2 #The number of answer cards that each player will have at any given time.  Currently set to 2 just because I don't have many answer cards written.
FONT = pygame.font.SysFont(None, 25)
ANSWER_CARD_FONT = pygame.font.Font('fonts/OpenSans-Regular.ttf', 18)

#The rest of these constants relate specifically to the locations of images on the game screen.  Tweaking with these could definitely mess up how everything looks.
POS_ANSWER1 = (190,570)
POS_ANSWER2 = (325,570)
POS_ANSWER3 = (460,570)
POS_ANSWER4 = (595,570)
POS_ANSWER5 = (730,570)

#These two lines create the window in which the game is played, titling it "Pairs to Peers".
gameDisplay = pygame.display.set_mode((GAME_WIDTH,GAME_HEIGHT))
pygame.display.set_caption("Pairs to Peers")

spr_answerCard1 = pygame.image.load('img/answerCard_blue.png')
spr_answerCard2 = pygame.image.load('img/answerCard_blue.png')
spr_answerCard3 = pygame.image.load('img/answerCard_blue.png')
spr_answerCard4 = pygame.image.load('img/answerCard_blue.png')
spr_answerCard5 = pygame.image.load('img/answerCard_blue.png')
answerSpriteArray = [spr_answerCard1, spr_answerCard2, spr_answerCard3, spr_answerCard4, spr_answerCard5]

#This class defines the players of the game
class Player:

	#MEMBER VARIABLES#
		# isHuman - a boolean denoting whether the player is a human (true) or an AI (false)
		# playerName - a string of the name of the player
		# playerNum - the integer value denoting the player's number (1 = Player 1, 2 = Player 2, etc.)
		# score - the integer value of the player's score
		# handArray - array that stores the cards in a player's hand

	#Constructor Method
	def __init__(self, name, number, human):
		self.isHuman = human
		self.playerName = name
		self.playerNum = number
		self.score = 0 #Players are initialized with 0 points
		self.handArray = []#Initializes handArray as an empty array

	#This method is used to increase a player's score by a given number of points
	def addPoints(self, pointsToAdd):
		self.score += pointsToAdd

	def dealAns(self):
		cardCount = 0
		#NOTE: Commented out these lines for now until more of a framework is built around this functionality
		#while(cardCount < 5):
			#randNum = random.randint(0, totalnumberofcards)
			#if(Answer.beenDealt == False)
				#handArray[cardCount] = Answer(randNum)
				#cardCount = cardCount + 1

#This class defines the scenario cards, which players consider when playing their corresponding answer card.
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

class Answer:

	#MEMBER VARIABLES#
		# ansText - a string describing the scenario
		# pointVal - an int that will keep track of how many points playing this card will give. Changes based on scenario
		# beenDealt - a boolean that keeps track of whether or not an answer card has been dealt to a player already
		# beenPlayed - a boolean that keeps track of whether or not the scenario has already been in play during the current game
		#NOTE: that beenPlayed may or may not be optional for this since we haven't decided if we want to recycle cards yet

	#cons
	def __init__(self, cardText):
		self.ansText = cardText
		self.beenDealt = False
		self.beenPlayed = False

	#call this to change the number of points an answer is worth each round
	def setPoints(self, points):
		self.pointVal = points

	#NOTE: Let's add some sort of description for this method.
	def playCard(self):
		self.beenPlayed = True
		#following line incorrect since scoring system hasn't been started yet
		#pointsOfPlayer = pointsofPlayer + pointVal

#This function takes in a one-dimensional array and "shuffles" the contents, ordering them randomly.
#NOTE: I realize that this python's random.shuffle() function makes this an incredibly simple task, but I figure we should have it as a separate function instead of just calling random.shuffle() directly every time, in case there's every any sort of functionality we need to add to shuffling.
def shuffle(inArray):
	random.shuffle(inArray)
	return inArray

#NOTE: Potentially down the line we should have the scenarios and answer cards read in from files instead of having tons of lines in the program to handle it
#This function builds the deck of scenario cards.  More lines can be added accordingly whenever more cards are to be added.
def buildScenarios():
	scenarios = []
	card = Scenario("A person walks up to you on the first day of school and says hello.")
	scenarios.append(card)
	card = Scenario("Your friend is crying.")
	scenarios.append(card)
	card = Scenario("You are hungry.")
	scenarios.append(card)
	card = Scenario("You are looking for a pencil but can't find one")
	scenarios.append(card)
	card = Scenario("There is a bully, saying mean things, who won't leave you alone.")
	scenarios.append(card)
	card = Scenario("You notice that someone in your class has candy and you want some.")
	scenarios.append(card)
	card = Scenario("You are offered candy by a friend.")
	scenarios.append(card)
	card = Scenario("another scenario goes here")
	scenarios.append(card)
	return scenarios

#This function builds the deck of answer cards.  More lines can be added accordingly whenever more cards are to be added.
def buildAnswers():
	answers = []
	card = Answer("Say you're sorry")
	answers.append(card)
	card = Answer("Ask for help")
	answers.append(card)
	card = Answer("Turn around and walk away")
	answers.append(card)
	card = Answer("Eat some food")
	answers.append(card)
	card = Answer("Look around")
	answers.append(card)
	card = Answer("Clap your hands")
	answers.append(card)
	card = Answer("Yell at them")
	answers.append(card)
	card = Answer("Say hello")
	answers.append(card)
	card = Answer("Introduce yourself")
	answers.append(card)
	card = Answer("Ask for their name")
	answers.append(card)
	card = Answer("Nod your head")
	answers.append(card)
	card = Answer("Shrug your shoulders")
	answers.append(card)
	card = Answer("Do nothing")
	answers.append(card)
	card = Answer("Call 911")
	answers.append(card)
	card = Answer("Offer to help")
	answers.append(card)
	card = Answer("Ask for help")
	answers.append(card)
	card = Answer("Give them a hug")
	answers.append(card)
	card = Answer("Offer them tissues")
	answers.append(card)
	card = Answer("Run away")
	answers.append(card)
	card = Answer("Say please")
	answers.append(card)
	card = Answer("Say thank you")
	answers.append(card)
	card = Answer("Congratulate them")
	answers.append(card)
	card = Answer("another answer goes here")
	answers.append(card)
	return answers

#This function takes a string, a color, and a coordinate as input and displays text on the screen accordingly
def displayMessage(messageText,messageColor,messageLocation):
	screen_text = FONT.render(messageText, True, messageColor)
	gameDisplay.blit(screen_text, messageLocation)

#This function takes some text and the coordinates of a button rectangle and places text on the button appropriately.
def buttonText(text, color, xPos, yPos, width, height, size):
	return 0 #Not exactly sure if this is how we want to do it, but if so, add to this later.

#This function is used to handle everything that's going on during a player's turn.
def doTurn(thePlayer, answerDeck):
	cardsInHand = len(thePlayer.handArray)
	for x in xrange(0, (5 - cardsInHand)): #Iterates until the user's hand is full
		thePlayer.handArray.append(answerDeck.pop()) #This is effectively dealing a card, as it removes the last element from the answer deck and palces it in the player's hand

#This is the main function of the program.	It handles everything that's going on at each moment of the game
def gameLoop():
	gameRun = True #Boolean that stores whether the game should be running
	playersIn = False #Boolean that stores whether all of the player information has been input
	gameOver = False #Boolean that stores whether the player has lost
	clock = pygame.time.Clock()
	playerArray = []#Initializes the array that will eventually store the players of the game
	scenarioArray = []#Initializes the array that will eventually store the scenario cards
	scenarioArray = buildScenarios()
	answerArray = buildAnswers()
	scenarioArray = shuffle(scenarioArray)
	answerArray = shuffle(answerArray)
	answerRects = [pygame.Rect(POS_ANSWER1[0] + 10, POS_ANSWER1[1] + 10, 108, 150),
				   pygame.Rect(POS_ANSWER2[0] + 10, POS_ANSWER2[1] + 10, 108, 150),
				   pygame.Rect(POS_ANSWER3[0] + 10, POS_ANSWER3[1] + 10, 108, 150),
				   pygame.Rect(POS_ANSWER4[0] + 10, POS_ANSWER4[1] + 10, 108, 150),
				   pygame.Rect(POS_ANSWER5[0] + 10, POS_ANSWER5[1] + 10, 108, 150)]

	while gameRun: #Continues to execute until gameRun is set to false

		"""  Commenting this out until beta.  It will actually be it's own file though most likely.
		#PLAYER SELECTION SCREEN
		#For some reason it appears that the game is stuck in an unresponsive state during this time.  Definitely need to fix this.
		while not playersIn: #name, number, human

			print("caught in a loop.")
			gameDisplay.fill(COLOR_WHITE) #Creates a white background
			displayMessage("This will be the player selection screen.",COLOR_BLACK,[32,32]) #Draws some text
			pygame.draw.rect(gameDisplay,COLOR_BLUE,(150,500,100,50))
			pygame.draw.rect(gameDisplay,COLOR_BLUE,(300,500,100,50))
			pygame.draw.rect(gameDisplay,COLOR_BLUE,(450,500,100,50))
			pygame.draw.rect(gameDisplay,COLOR_BLUE,(600,500,100,50))
			pygame.display.update() #Updates the screen every frame
		"""

		while gameOver: #Executes after the game has ended
			gameDisplay.fill(COLOR_BLACK)
			displayMessage("GAME OVER!	Press ENTER to play again, or SPACE to quit.",COLOR_RED,[GAME_WIDTH/3,GAME_HEIGHT/2])
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
		displayMessage("The game is running.  Press ENTER to go to the Game Over screen.",COLOR_BLACK,[32,32]) #Draws some text
		gameDisplay.blit(spr_answerCard1, POS_ANSWER1)
		gameDisplay.blit(spr_answerCard2, POS_ANSWER2)
		gameDisplay.blit(spr_answerCard3, POS_ANSWER3)
		gameDisplay.blit(spr_answerCard4, POS_ANSWER4)
		gameDisplay.blit(spr_answerCard5, POS_ANSWER5)
		for x in xrange(0,5):
			cardRendered = render_textrect(answerArray[x].ansText, ANSWER_CARD_FONT, answerRects[x], COLOR_BLACK, COLOR_WHITE)
			if cardRendered:
				gameDisplay.blit(cardRendered, answerRects[x].topleft)
		pygame.display.update() #Updates the screen every frame

		clock.tick(FRAMES_PER_SECOND)

	pygame.quit()
	quit()

gameLoop()
