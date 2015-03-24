#Things marked as important, including those which should potentially be changed down the line, are marked with "#NOTE"
#Important question:  We should ask about the screen resolutions of the computers that the game will primarily be played on.  Because we could definitely program the game in a dynamic way such that the screenc ould be resized and screen elements would change in size appropriately, but it would be significantly easier to not have to worry about that and instead just have some static screen size to build around.

import pygame
import random
import pygame.mixer
import math
from textrect import *

pygame.init()

#Loads in all of the fonts used by the game
font = pygame.font.SysFont(None, 25)
answer_card_font = pygame.font.Font('fonts/OpenSans-Regular.ttf', 16)
scenario_card_font = pygame.font.Font('fonts/OpenSans-Regular.ttf', 32)
big_bold_font = pygame.font.Font('fonts/OpenSans-Bold.ttf', 36)

#Initializes the mixer and loads in all of the sounds used by the game
pygame.mixer.init()
sound_blop = pygame.mixer.Sound('sound/Blop-Mark_DiAngelo-79054334_CHOPPED.ogg')
sound_applause = pygame.mixer.Sound('sound/Auditorium_Applause_CHOPPED.ogg')

#In the following section, a number of constants are defined.
#These variables have self explanatory names, and are referred to throughout the rest of the code but never change in value.
#Editing these values in the code can change various aspects of the gameplay, like the player's speed.
COLOR_RED = (255,0,0)
COLOR_GREEN = (0,255,0)
COLOR_BLUE = (0,0,255)
COLOR_LIGHTPINK = (255,225,255)
COLOR_LIGHTGREEN = (204,255,204)
COLOR_LIGHTBLUE = (204, 225, 255)
COLOR_WHITE = (255,255,255)
COLOR_BLACK = (0,0,0)
COLOR_POINTS_0 = (204,0,0)
COLOR_POINTS_1 = (204,44,0)
COLOR_POINTS_2 = (204,84,0)
COLOR_POINTS_3 = (204,124,0)
COLOR_POINTS_4 = (204,164,0)
COLOR_POINTS_5 = (204,204,0)
COLOR_POINTS_6 = (164,204,0)
COLOR_POINTS_7 = (124,204,0)
COLOR_POINTS_8 = (84,204,0)
COLOR_POINTS_9 = (44,204,0)
COLOR_POINTS_10 = (0,204,0)
GAME_WIDTH = 1024
GAME_HEIGHT = 768
FRAMES_PER_SECOND = 30
ANSWERS_PER_PLAYER = 2 #The number of answer cards that each player will have at any given time.  Currently set to 2 just because I don't have many answer cards written.
GOOD_CARD_POINTS = 6
POINTS_TO_WIN = 120
startTime = 0
#The rest of these constants relate specifically to the locations of images on the game screen.  Tweaking with these could definitely mess up how everything looks.

#Main Menu
POS_BOTTOMCORNER = (0, 512)
POS_TOPCORNER = (768, 0)
POS_LOGO = (180, 60)
POS_PLAYGAME = (90, 450)
POS_HOWTOPLAY = (390, 450)
POS_OPTIONS = (690, 450)

#In-Game Screen
POS_ANSWER1 = (190,570)
POS_ANSWER2 = (325,570)
POS_ANSWER3 = (460,570)
POS_ANSWER4 = (595,570)
POS_ANSWER5 = (730,570)
POS_PLAY = (740, 300)
POS_SCENARIO = (385, 285)
POS_MAINMENU = (0, 0)
POS_SCORE = (768, 0)
POS_SCENARIODECK = (25, 285)
POS_ANSWERDECK = (45, 570)
POS_POINTVALS = [(240,680),(375,680),(510,680),(645,680),(780,680)]
POS_SCORETEXT = (788,10)

#Customization
POS_SQUARE_WHITE = (570, 365)
POS_SQUARE_LIGHTPINK = (770, 365)
POS_SQUARE_LIGHTBLUE = (570, 565)
POS_SQUARE_LIGHTGREEN = (770, 565)
POS_CARD_CUBES = (70, 365)
POS_CARD_MARBLE = (215, 365)
POS_CARD_PINK = (360, 365)
POS_CARD_STONE = (70, 565)
POS_CARD_TILE = (215, 565)
POS_CARD_WOVEN = (360, 565)
POS_BOX_SOUND = (768, 0)
POS_SELECT_ARTWORK = (150, 210)
POS_CHOOSE_BACKGROUND = (630, 210)

backgroundColor = COLOR_WHITE
soundOn = True

class Object(pygame.sprite.Sprite):
	def __init__(self, file_name, position):
		self.image = pygame.image.load(file_name)
		self.rect = pygame.Rect(position[0], position[1], self.image.get_size()[0], self.image.get_size()[1])

#These two lines create the window in which the game is played, titling it "Pairs to Peers".
gameDisplay = pygame.display.set_mode((GAME_WIDTH,GAME_HEIGHT))
pygame.display.set_caption("Pairs to Peers")

#Loads in all of the objects and sprites necessary for the game
#Main Menu
spr_bottomCorner = pygame.image.load("img/corner_blue_bottomleft.png")
spr_topCorner = pygame.image.load("img/corner_blue_topright.png")
obj_logo = Object("img/logo.png", POS_LOGO)
obj_buttonPlayGame = Object("img/button_Play_Game.png", POS_PLAYGAME)
obj_buttonHowToPlay = Object("img/button_How_To_Play.png", POS_HOWTOPLAY)
obj_buttonOptions = Object("img/button_Options.png", POS_OPTIONS)

#In-game screen
cardArtwork = "cubes"
obj_answerCard1 = Object("img/answerCard_blue.png", POS_ANSWER1)
obj_answerCard2 = Object("img/answerCard_blue.png", POS_ANSWER2)
obj_answerCard3 = Object("img/answerCard_blue.png", POS_ANSWER3)
obj_answerCard4 = Object("img/answerCard_blue.png", POS_ANSWER4)
obj_answerCard5 = Object("img/answerCard_blue.png", POS_ANSWER5)
obj_playCard = Object("img/button_medium_green.png", POS_PLAY)
obj_scoreDisplay = Object("img/button_medium_blue.png", POS_SCORE)
obj_buttonMainMenu = Object("img/button_Main_Menu.png", POS_MAINMENU)
answerObjArray = [obj_answerCard1, obj_answerCard2, obj_answerCard3, obj_answerCard4, obj_answerCard5]
spr_scenarioCard = pygame.image.load("img/scenarioCard_blue.png")
spr_backOfAnswerCard = pygame.image.load("img/card_back_small_" + cardArtwork + ".png")
spr_backOfScenarioCard = pygame.image.load("img/card_back_large_" + cardArtwork + ".png")

#Customization screen
#Due to the nature of the customization in this game, the paths of some of these images are stored as strings in order to save space later on.

obj_square_white = Object("img/square_white_green.png", POS_SQUARE_WHITE)
obj_square_lightpink = Object("img/square_lightpink.png", POS_SQUARE_LIGHTPINK)
obj_square_lightblue = Object("img/square_lightblue.png", POS_SQUARE_LIGHTBLUE)
obj_square_lightgreen = Object("img/square_lightgreen.png", POS_SQUARE_LIGHTGREEN)
obj_card_cubes = Object("img/card_back_small_cubes_green.png", POS_CARD_CUBES)
obj_card_marble = Object("img/card_back_small_marble.png", POS_CARD_MARBLE)
obj_card_pink = Object("img/card_back_small_pink.png", POS_CARD_PINK)
obj_card_stone = Object("img/card_back_small_stone.png", POS_CARD_STONE)
obj_card_tile = Object("img/card_back_small_tile.png", POS_CARD_TILE)
obj_card_woven = Object("img/card_back_small_woven.png", POS_CARD_WOVEN)
obj_box_sound = Object("img/box_sound_on.png", POS_BOX_SOUND)
spr_selectArtwork = pygame.image.load("img/box_select_artwork.png")
spr_chooseBackground = pygame.image.load("img/box_choose_background.png")
squareObjArray = [obj_square_white, obj_square_lightpink, obj_square_lightblue, obj_square_lightgreen]
cardBackObjArray = [obj_card_cubes, obj_card_marble, obj_card_pink, obj_card_stone, obj_card_tile, obj_card_woven, obj_box_sound]

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

	def getPoints(self):
		return self.score
	
	def dealAns(self):
		cardCount = 0
		#NOTE: Commented out these lines for now until more of a framework is built around this functionality
		#while(cardCount < 5):
			#randNum = random.randint(0, totalnumberofcards)
			#if(Answer.beenDealt == False)
				#handArray[cardCount] = Answer(randNum)
				#cardCount = cardCount + 1
				
	def getHand(self):
		return self.handArray
	
	def clearHand(self):
		self.handArray = []

#This class defines the scenario cards, which players consider when playing their corresponding answer card.
class Scenario:

	#MEMBER VARIABLES#
		# scenarioText - a string describing the scenario
		# arrPoints - array containing answer point vals
		# beenPlayed - a boolean that keeps track of whether or not the scenario has already been in play during the current game

	#Constructor Method
	def __init__(self, cardText, arrPoints):
		self.scenarioText = cardText
		self.beenPlayed = False #Scenario cards are initialized having not been played
		self.arrPoints = arrPoints
	#This method is used to denote that the scenario card has now been played
	def play(self):
		self.beenPlayed = True

	def getPointVal(self, cardNum):
		return self.arrPoints[cardNum]

class Answer:

	#MEMBER VARIABLES#
		# ansText - a string describing the scenario
		# numCard - number of the action card
		# pointVal - an int that will keep track of how many points playing this card will give. Changes based on scenario
		# beenDealt - a boolean that keeps track of whether or not an answer card has been dealt to a player already
		# beenPlayed - a boolean that keeps track of whether or not the scenario has already been in play during the current game
		#NOTE: that beenPlayed may or may not be optional for this since we haven't decided if we want to recycle cards yet

	#cons
	def __init__(self, cardText, cardNum):
		self.ansText = cardText
		self.beenDealt = False
		self.beenPlayed = False
		self.numCard = cardNum
		
	#call this to change the number of points an answer is worth each round
	def setPoints(self, points):
		self.pointVal = points

	#NOTE: Let's add some sort of description for this method.
	def playCard(self):
		self.beenPlayed = True
		#following line incorrect since scoring system hasn't been started yet
		#pointsOfPlayer = pointsofPlayer + pointVal
	
	def getCardNum(self):
		return self.numCard	
	
	def getText(self):
		return self.ansText
		

#This function takes in a one-dimensional array and "shuffles" the contents, ordering them randomly.
#NOTE: I realize that this python's random.shuffle() function makes this an incredibly simple task, but I figure we should have it as a separate function instead of just calling random.shuffle() directly every time, in case there's every any sort of functionality we need to add to shuffling.
def shuffle(inArray):
	random.shuffle(inArray)
	return inArray

#NOTE: Potentially down the line we should have the scenarios and answer cards read in from files instead of having tons of lines in the program to handle it
#This function builds the deck of scenario cards.  More lines can be added accordingly whenever more cards are to be added.
def buildScenarios():
	scenarios = []
	card = Scenario("A person walks up to you on the first day of school and says hello.", [0, 6, 0, 0, 0, 0, 0, 10, 10, 9, 6, 0, 0, 0, 0, 0, 0, 0, 0, 0, 4, 0, 0])
	scenarios.append(card)
	card = Scenario("Your friend is crying.", [7, 9, 0, 0, 5, 0, 0, 4, 4, 5, 0, 0, 0, 0, 10, 0, 10, 8, 0, 0, 0, 0, 0])
	scenarios.append(card)
	card = Scenario("You are hungry.", [0, 8, 0, 10, 5, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 8, 0, 0, 0, 6, 0, 0, 0])
	scenarios.append(card)
	card = Scenario("You are looking for a pencil but can't find one", [0, 8, 0, 0, 9, 0, 0, 0, 0, 0, 0, 4, 0, 0, 0, 8, 0, 0, 0, 5, 0, 0, 0])
	scenarios.append(card)
	card = Scenario("There is a bully, saying mean things, who won't leave you alone.", [0, 8, 10, 0, 5, 0, 0, 4, 4, 4, 0, 0, 5, 0, 0, 9, 0, 0, 8, 5, 0, 0, 0])
	scenarios.append(card)
	card = Scenario("You notice that someone in your class has candy and you want some.", [0, 6, 0, 5, 0, 0, 0, 9, 9, 8, 0, 0, 0, 0, 0, 4, 0, 0, 0, 10, 0, 0, 0])
	scenarios.append(card)
	card = Scenario("You are offered candy by a friend.", [0, 0, 0, 0, 0, 0, 0, 5, 6, 6, 8, 7, 0, 0, 0, 0, 5, 0, 0, 9, 10, 0, 0])
	scenarios.append(card)
	#card = Scenario("another scenario goes here")
	#scenarios.append(card)
	return scenarios

#This function builds the deck of answer cards.  More lines can be added accordingly whenever more cards are to be added.
def buildAnswers():
	answers = []
	card = Answer("Say you're sorry", 0)
	answers.append(card)
	card = Answer("Ask for help", 1)
	answers.append(card)
	card = Answer("Turn around and walk away", 2)
	answers.append(card)
	card = Answer("Eat some food", 3)
	answers.append(card)
	card = Answer("Look around", 4)
	answers.append(card)
	card = Answer("Clap your hands", 5)
	answers.append(card)
	card = Answer("Yell at them", 6)
	answers.append(card)
	card = Answer("Say hello", 7)
	answers.append(card)
	card = Answer("Introduce yourself", 8)
	answers.append(card)
	card = Answer("Ask for their name", 9)
	answers.append(card)
	card = Answer("Nod your head", 10)
	answers.append(card)
	card = Answer("Shrug your shoulders", 11)
	answers.append(card)
	card = Answer("Do nothing", 12)
	answers.append(card)
	card = Answer("Call 911", 13)
	answers.append(card)
	card = Answer("Offer to help", 14)
	answers.append(card)
	card = Answer("Ask for help", 15)
	answers.append(card)
	card = Answer("Give them a hug", 16)
	answers.append(card)
	card = Answer("Offer them tissues", 17)
	answers.append(card)
	card = Answer("Run away", 18)
	answers.append(card)
	card = Answer("Say please", 19)
	answers.append(card)
	card = Answer("Say thank you", 20)
	answers.append(card)
	card = Answer("Congratulate them", 21)
	answers.append(card)
	card = Answer("another answer goes here", 22)
	answers.append(card)
	return answers

def resetSquares():
	obj_square_white.image = pygame.image.load("img/square_white.png")
	obj_square_lightpink.image = pygame.image.load("img/square_lightpink.png")
	obj_square_lightgreen.image = pygame.image.load("img/square_lightgreen.png")
	obj_square_lightblue.image = pygame.image.load("img/square_lightblue.png")

def resetCardBacks():
	obj_card_cubes.image = pygame.image.load("img/card_back_small_cubes.png")
	obj_card_marble.image = pygame.image.load("img/card_back_small_marble.png")
	obj_card_pink.image = pygame.image.load("img/card_back_small_pink.png")
	obj_card_stone.image = pygame.image.load("img/card_back_small_stone.png")
	obj_card_tile.image = pygame.image.load("img/card_back_small_tile.png")
	obj_card_woven.image = pygame.image.load("img/card_back_small_woven.png")

#This function takes a string, a color, and a coordinate as input and displays text on the screen accordingly
def displayMessage(messageText,messageColor,messageLocation, font=font):
	screen_text = font.render(messageText, True, messageColor)
	gameDisplay.blit(screen_text, messageLocation)

#This function takes some text and the coordinates of a button rectangle and places text on the button appropriately.
def buttonText(text, color, xPos, yPos, width, height, size):
	return 0 #Not exactly sure if this is how we want to do it, but if so, add to this later.

#This is the main function of the program.	It handles everything that's going on at each moment of the game
def gameLoop():
	backgroundColor = COLOR_WHITE #NOTE:  I put this here instead of being like a global variable because I was having runtime errors and this seemed to fix it.  I'm adding this comment here to keep track of it because I'm not sure whether or not this could end up causing more problems down the line
	soundOn = True #NOTE:  Same with this one.
	cardArtwork = "cubes" #NOTE: Same with this one.
	pointFeedbackArray = []
	feedbackTextArray = []
	pointVal = 0

	gameRun = True #Boolean that stores whether the game should be running
	playersIn = False #Boolean that stores whether all of the player information has been input
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
	scenarioRect = pygame.Rect(POS_SCENARIO[0] + 20, POS_SCENARIO[1] + 20, 300, 216)
	playRect = pygame.Rect(POS_PLAY[0] + 20, POS_PLAY[1] + 20, 200, 100)
	feedbackTextRect = pygame.Rect(256, 50, 512, 75)
	feedbackSubtextRect = pygame.Rect(256, 125, 512, 100)
	scoreTextRect = pygame.Rect(788,10,216,90)

	cardSelected = -1
	canPlay = False
	nextRound = False
	hasWinningCard = False
	gameWon = False
	minPointsHand = 0
	TIME_ALLOWED = 5000
	nextRoundRendered = playCardRendered = render_textrect("Next Round", scenario_card_font, playRect, COLOR_BLACK, [191,255,191])

	#The gameSceen variable is used to set and determine which screen of the game should be currently displayed on the screen.
	#The following key describes the screen to which each individual integer corresponds
	#1 = About
	#2 = Main Menu
	#3 = Instructions
	#4 = Gameplay
	#5 = Endgame
	#6 = Player selection
	#7 = Customization
<<<<<<< HEAD
	#8 = Diagnostics
=======
	#8 = Difficulty
>>>>>>> origin/Difficulty
	gameScreen = 2

	#Creates a temporary fake array of 2 players just for the purposes of testing the game until the player creation screen is written
	player = Player('Ryan', 1, True)
	playerArray.append(player)
	#player = Player('Other Player', 2, True)
	#playerArray.append(player)

	currentScenario = scenarioArray.pop() #Effectively deals a scenario card to the game from the deck

	while gameRun: #Continues to execute until gameRun is set to false

		while (gameScreen == 1 and gameRun):
			gameDisplay.fill(backgroundColor)
			displayMessage("This is the ABOUT screen.",COLOR_RED,[GAME_WIDTH/3,GAME_HEIGHT/2])
			for event in pygame.event.get():
				if event.type == pygame.QUIT:
					gameRun = False #Ends the game if they user attempts to close the window
				if event.type == pygame.MOUSEBUTTONDOWN:
					# Set the x, y positions of the mouse click
					x, y = event.pos
					if ((obj_buttonMainMenu.rect.collidepoint(x, y))):
						if soundOn:
							sound_blop.play()
						gameScreen = 2
			gameDisplay.blit(obj_buttonMainMenu.image, obj_buttonMainMenu.rect)
			pygame.display.update() #Updates the screen every frame
			clock.tick(FRAMES_PER_SECOND)

		while (gameScreen == 2 and gameRun):
			gameDisplay.fill(backgroundColor)
			for event in pygame.event.get():
				if event.type == pygame.QUIT:
					gameRun = False #Ends the game if they user attempts to close the window
				if event.type == pygame.MOUSEBUTTONDOWN:
					# Set the x, y positions of the mouse click
					x, y = event.pos
					if ((obj_logo.rect.collidepoint(x, y))):
						if soundOn:
							sound_blop.play()
						gameScreen = 1
					elif ((obj_buttonPlayGame.rect.collidepoint(x, y))):
						if soundOn:
							sound_blop.play()
						startTime = pygame.time.get_ticks()
						gameScreen = 4
						
					elif ((obj_buttonHowToPlay.rect.collidepoint(x, y))):
						if soundOn:
							sound_blop.play()
						gameScreen = 3
					elif((obj_buttonOptions.rect.collidepoint(x, y))):
						if soundOn:
							sound_blop.play()
						gameScreen = 7
				if event.type == pygame.KEYDOWN:
					if event.key == pygame.K_d:
						gameScreen = 8

			gameDisplay.blit(obj_logo.image, obj_logo.rect)
			gameDisplay.blit(obj_buttonPlayGame.image, obj_buttonPlayGame.rect)
			gameDisplay.blit(obj_buttonHowToPlay.image,obj_buttonHowToPlay.rect)
			gameDisplay.blit(obj_buttonOptions.image, obj_buttonOptions.rect)
			gameDisplay.blit(spr_bottomCorner, POS_BOTTOMCORNER)
			gameDisplay.blit(spr_topCorner, POS_TOPCORNER)
			pygame.display.update() #Updates the screen every frame
			clock.tick(FRAMES_PER_SECOND)

		while (gameScreen == 3 and gameRun):
			gameDisplay.fill(backgroundColor)
			displayMessage("This is the INSTRUCTIONS screen.",COLOR_RED,[GAME_WIDTH/3,GAME_HEIGHT/2])
			for event in pygame.event.get():
				if event.type == pygame.QUIT:
					gameRun = False #Ends the game if they user attempts to close the window
				if event.type == pygame.MOUSEBUTTONDOWN:
					# Set the x, y positions of the mouse click
					x, y = event.pos
					if ((obj_buttonMainMenu.rect.collidepoint(x, y))):
						if soundOn:
							sound_blop.play()
						gameScreen = 2
			gameDisplay.blit(obj_buttonMainMenu.image, obj_buttonMainMenu.rect)
			pygame.display.update() #Updates the screen every frame
			clock.tick(FRAMES_PER_SECOND)

		while (gameScreen == 4 and gameRun):
			gameDisplay.fill(backgroundColor)
			for event in pygame.event.get():
				if event.type == pygame.QUIT:
					gameRun = False #Ends the game if they user attempts to close the window
<<<<<<< HEAD
=======
					
				if ((pygame.time.get_ticks() - startTime) > TIME_ALLOWED):
					#display message + no points this round
					nextRound = True
					canPlay = False
					
			
					
>>>>>>> origin/Difficulty
				if event.type == pygame.MOUSEBUTTONDOWN:
					# Set the x, y positions of the mouse click
					x, y = event.pos
					for card in range(len(answerObjArray)):
						if (answerObjArray[card].rect.collidepoint(x, y)):
							if (cardSelected >= 0):
								answerObjArray[cardSelected].image = pygame.image.load('img/answerCard_blue.png')
							answerObjArray[card].image = pygame.image.load('img/answerCard_green.png')
							if soundOn:
								sound_blop.play()
							cardSelected = card
							if nextRound == False:
								canPlay = True
								
							hand = player.getHand()
							cardNum = hand[cardSelected].getCardNum()
							#print(str(cardNum))
							cardText = hand[cardSelected].getText()
							#print(cardText)
							#print('POINTS' + str(currentScenario.getPointVal(cardNum)))
							
					# if ((obj_playCard.rect.collidepoint(x, y)) and (nextRound == True)): #placeholder for next round button
						# startTime = pygame.time.get_ticks()
						# nextRound = False
						# if soundOn:
							# sound_blop.play()
						# answerObjArray[cardSelected].image = pygame.image.load('img/answerCard_blue.png')

						# tempScenario = currentScenario
						# currentScenario = scenarioArray.pop()

						# scenarioArray.append(tempScenario)
						# scenarioArray = shuffle(scenarioArray)

						# cards = 0
						# while(cards < 5):
							# answerArray.append(hand[cards])
							# cards = cards + 1

						# answerArray = shuffle(answerArray)
						# player.clearHand()
						# cardsInHand = len(p.handArray)

						# for x in xrange(0, (5 - cardsInHand)): #Iterates until the user's hand is full
							# p.handArray.append(answerArray.pop()) #This is effectively dealing a card, as it removes the last element from the answer deck and places it in the player's hand

						# while (not hasWinningCard):
							# #print('Attempting to make the user\'s hand have a winning card')
							# answerArray.insert(0, p.handArray.pop())
							# p.handArray.append(answerArray.pop())
							# for card in p.handArray: #Iterates through all 5 cards in the user's hand
								# if (currentScenario.getPointVal(card.getCardNum()) > minPointsHand):
									# minPointsHand = currentScenario.getPointVal(card.getCardNum())
							# if (minPointsHand >= GOOD_CARD_POINTS):
								# p.handArray = shuffle(p.handArray)
								# hasWinningCard = True
								# #print('Should have one. minPointsHand = ' + str(minPointsHand))
						# hasWinningCard = False
						# minPointsHand = 0
						
					if ((obj_playCard.rect.collidepoint(x, y)) and ((canPlay == True) or (nextRound == True))):
						startTime = pygame.time.get_ticks()
						
						
						if soundOn:
							sound_blop.play()
							
						answerObjArray[cardSelected].image = pygame.image.load('img/answerCard_blue.png')
						hand = player.getHand()
						
						pointVal = 20
						
						if canPlay == True:
							pointVal = currentScenario.getPointVal(hand[cardSelected].getCardNum())
						
						if nextRound == True:
							pointVal = 0
							
						player.addPoints(pointVal)

<<<<<<< HEAD
						pointFeedbackArray = [] #Stores the integer value of points that each card is worth in the 0 through 4 positions.
						feedbackTextArray = [] #Stores the actual text 'objects' of the point values to be played on the screen.  Ordering is just like pointFeedbackArray.
						for card in range(5):
							pointFeedbackArray.append(currentScenario.getPointVal(hand[card].getCardNum()))
						#pointFeedbackArray.append(pointVal)

=======
						canPlay = False
						nextRound = False
						
>>>>>>> origin/Difficulty
						if(player.getPoints() >= POINTS_TO_WIN):
							gameWon = True
							canPlay = False
							if soundOn:
								sound_applause.play()
								gameScreen = 5

						tempScenario = currentScenario
						currentScenario = scenarioArray.pop()

						scenarioArray.append(tempScenario)
						scenarioArray = shuffle(scenarioArray)

						cards = 0
						while(cards < 5):
							answerArray.append(hand[cards])
							cards = cards + 1

						answerArray = shuffle(answerArray)
						player.clearHand()
						cardsInHand = len(p.handArray)

						for x in xrange(0, (5 - cardsInHand)): #Iterates until the user's hand is full
							p.handArray.append(answerArray.pop()) #This is effectively dealing a card, as it removes the last element from the answer deck and places it in the player's hand

						while (not hasWinningCard):
							#print('Attempting to make the user\'s hand have a winning card')
							answerArray.insert(0, p.handArray.pop())
							p.handArray.append(answerArray.pop())
							for card in p.handArray: #Iterates through all 5 cards in the user's hand
								if (currentScenario.getPointVal(card.getCardNum()) > minPointsHand):
									minPointsHand = currentScenario.getPointVal(card.getCardNum())
							if (minPointsHand >= GOOD_CARD_POINTS):
								p.handArray = shuffle(p.handArray)
								hasWinningCard = True
								#print('Should have one. minPointsHand = ' + str(minPointsHand))
						hasWinningCard = False
						minPointsHand = 0
					if (obj_buttonMainMenu.rect.collidepoint(x, y)):
						if (soundOn):
							sound_blop.play()
						gameScreen = 2
<<<<<<< HEAD

=======
						
			#timer_event = pygame.USEREVENT + 1
			pygame.time.set_timer(pygame.USEREVENT + 1, 100)
			pygame.event.post(pygame.event.Event(pygame.USEREVENT + 1))
			
			
			gameDisplay.fill(backgroundColor)
>>>>>>> origin/Difficulty
			gameDisplay.blit(obj_answerCard1.image, obj_answerCard1.rect)
			gameDisplay.blit(obj_answerCard2.image, obj_answerCard2.rect)
			gameDisplay.blit(obj_answerCard3.image, obj_answerCard3.rect)
			gameDisplay.blit(obj_answerCard4.image, obj_answerCard4.rect)
			gameDisplay.blit(obj_answerCard5.image, obj_answerCard5.rect)
			gameDisplay.blit(obj_scoreDisplay.image, obj_scoreDisplay.rect)
			gameDisplay.blit(obj_buttonMainMenu.image, obj_buttonMainMenu.rect)
			gameDisplay.blit(spr_scenarioCard, POS_SCENARIO)

			spr_backOfAnswerCard = pygame.image.load("img/card_back_small_" + cardArtwork + ".png")
			spr_backOfScenarioCard = pygame.image.load("img/card_back_large_" + cardArtwork + ".png")
			gameDisplay.blit(spr_backOfScenarioCard, POS_SCENARIODECK)
			gameDisplay.blit(spr_backOfAnswerCard, POS_ANSWERDECK)

			for i in range(len(pointFeedbackArray)):
				numPoints = pointFeedbackArray[i]
				if (numPoints == 0):
					valColor = COLOR_POINTS_0
				elif (numPoints == 1):
					valColor = COLOR_POINTS_1
				elif (numPoints == 2):
					valColor = COLOR_POINTS_2
				elif (numPoints == 3):
					valColor = COLOR_POINTS_3
				elif (numPoints == 4):
					valColor = COLOR_POINTS_4
				elif (numPoints == 5):
					valColor = COLOR_POINTS_5
				elif (numPoints == 6):
					valColor = COLOR_POINTS_6
				elif (numPoints == 7):
					valColor = COLOR_POINTS_7
				elif (numPoints == 8):
					valColor = COLOR_POINTS_8
				elif (numPoints == 9):
					valColor = COLOR_POINTS_9
				elif (numPoints == 10):
					valColor = COLOR_POINTS_10
				feedbackText = big_bold_font.render(str(numPoints), True, valColor)
				feedbackTextArray.append(feedbackText)
			if (pointVal == 0):
				mainFeedbackString = "Sorry, that's incorrect."
			elif (pointVal <= 5):
				mainFeedbackString = "Okay, but think about different responses."
			elif (pointVal <= 10):
				mainFeedbackString = "Great answer!"
			#mainFeedbackText = scenario_card_font.render(mainFeedbackString, True, COLOR_BLACK)
			mainFeedbackTextRendered = render_textrect(mainFeedbackString, scenario_card_font, feedbackTextRect, COLOR_BLACK, COLOR_WHITE, 1)
			#mainFeedbackSubtext = big_bold_font.render("+ " + str(pointVal) + " points", True, COLOR_BLACK)
			mainFeedbackSubtextRendered = render_textrect(("+ " + str(pointVal) + " points"), big_bold_font, feedbackSubtextRect, COLOR_BLACK, COLOR_WHITE, 1)



			playCardRendered = render_textrect("Play Card", scenario_card_font, playRect, COLOR_BLACK, [191,255,191])
			nextRoundRendered = render_textrect("Next Round", scenario_card_font, playRect, COLOR_BLACK, [191,255,191])
			scenarioCardRendered = render_textrect(currentScenario.scenarioText, scenario_card_font, scenarioRect, COLOR_BLACK, COLOR_WHITE)
			score = str(player.getPoints())
<<<<<<< HEAD
			scoreBoxRendered = render_textrect(("SCORE: " + str(score)), big_bold_font, scoreTextRect, COLOR_BLACK, [158,206,255])
=======
			scoreBoxRendered = render_textrect(("SCORE: " + str(score)), big_bold_font, pygame.Rect(760,35,216,90), COLOR_BLACK, [158,206,255])
			time = int(math.floor(((TIME_ALLOWED - pygame.time.get_ticks())/1000 + startTime/1000) + 1.9))
			
			if time < 0:
				time = 0 
			timerRendered = render_textrect("Time: "+ str(time), big_bold_font, pygame.Rect(260,35,216,90), COLOR_BLACK, [158,206,255])	
			
			if timerRendered:
				gameDisplay.blit(timerRendered, pygame.Rect(260,35,108,160).topright)
>>>>>>> origin/Difficulty
			if scoreBoxRendered:
				gameDisplay.blit(scoreBoxRendered, POS_SCORETEXT)
			if scenarioCardRendered:
				gameDisplay.blit(scenarioCardRendered, scenarioRect.topleft)

			if nextRound == True:
				gameDisplay.blit(obj_playCard.image, obj_playCard.rect)
				gameDisplay.blit(nextRoundRendered, playRect.topleft)
				
			if canPlay == True:
				gameDisplay.blit(obj_playCard.image, obj_playCard.rect)
				gameDisplay.blit(playCardRendered, playRect.topleft)
				
			
							
			if gameWon == True:
				displayMessage("Congratulations!  You won.",COLOR_BLACK,[278,158],big_bold_font) #Congratulates the user upon winning
				displayMessage("Press ENTER to go to the Game Over screen.",COLOR_BLACK,[32,32]) #Draws some text

			for p in playerArray:
				turnGoing = True
				if (p.isHuman): #Executes if the current player is a human player
					cardsInHand = len(p.handArray)

					for x in xrange(0, (5 - cardsInHand)): #Iterates until the user's hand is full
						p.handArray.append(answerArray.pop()) #This is effectively dealing a card, as it removes the last element from the answer deck and places it in the player's hand

					p.handArray.append(answerArray)
				#while turnGoing:
					for cardNum in xrange(0,5): #Shows answer cards on the screen
						answerCardRendered = render_textrect(p.handArray[cardNum].ansText, answer_card_font, answerRects[cardNum], COLOR_BLACK, COLOR_WHITE)
						if answerCardRendered:
							gameDisplay.blit(answerCardRendered, answerRects[cardNum].topleft)
				else: #Executes if the current player is a computer player
					print('COMPUTER PLAYER TURN')
<<<<<<< HEAD
			for i in range(len(pointFeedbackArray)):
				gameDisplay.blit(feedbackTextArray[i], POS_POINTVALS[i])
			gameDisplay.blit(mainFeedbackTextRendered, feedbackTextRect.topleft)
			gameDisplay.blit(mainFeedbackSubtextRendered, feedbackSubtextRect.topleft)
=======
>>>>>>> origin/Difficulty
			pygame.display.update() #Updates the screen every frame
			clock.tick(FRAMES_PER_SECOND)

		while (gameScreen == 5 and gameRun): #Executes after the game has ended
			gameDisplay.fill(COLOR_BLACK)
			displayMessage("GAME OVER!  Press ENTER to play again, or SPACE to quit.",COLOR_RED,[GAME_WIDTH/3,GAME_HEIGHT/2])

			for event in pygame.event.get():
				if event.type == pygame.KEYDOWN:
					if event.key == pygame.K_RETURN:
						gameLoop() #Restarts the game if the player presses the ENTER key
					if event.key == pygame.K_SPACE:
						gameRun = False #Closes the game if the player presses the SPACE key
			for event in pygame.event.get():
				if event.type == pygame.QUIT:
					gameRun = False #Ends the game if they user attempts to close the window
			pygame.display.update() #Updates the screen every frame
			clock.tick(FRAMES_PER_SECOND)

		while (gameScreen == 6 and gameRun):
			gameDisplay.fill(backgroundColor)
			displayMessage("This is the PLAYER SELECTION screen.",COLOR_RED,[GAME_WIDTH/3,GAME_HEIGHT/2])
			for event in pygame.event.get():
				if event.type == pygame.QUIT:
					gameRun = False #Ends the game if they user attempts to close the window
			pygame.display.update() #Updates the screen every frame
			clock.tick(FRAMES_PER_SECOND)
			timer_event = pygame.USEREVENT + 1
			pygame.time.set_timer(timer_event, 250)
			

		while (gameScreen == 7 and gameRun):
			#NOTE:  The entire "selecting" (changing an image to the green version and making sure the rest are blue when it is clicked on) process could be done a lot more efficiently using pointers.  For now, I don't really know how to do that.  Maybe we could figure out down the line, but it would be a very late game thing since these actions are taken so infrequently that there wouldn't really be a huge difference in efficiency.
			gameDisplay.fill(backgroundColor)
			for event in pygame.event.get():
				if event.type == pygame.QUIT:
					gameRun = False #Ends the game if they user attempts to close the window
				if event.type == pygame.MOUSEBUTTONDOWN:
					# Set the x, y positions of the mouse click
					x, y = event.pos
					if ((obj_buttonMainMenu.rect.collidepoint(x, y))):
						if soundOn:
							sound_blop.play()
						gameScreen = 2
					elif ((obj_square_white.rect.collidepoint(x, y))):
						if soundOn:
							sound_blop.play()
						backgroundColor = COLOR_WHITE
						resetSquares()
						obj_square_white.image = pygame.image.load("img/square_white_green.png")
					elif ((obj_square_lightpink.rect.collidepoint(x, y))):
						if soundOn:
							sound_blop.play()
						backgroundColor = COLOR_LIGHTPINK
						resetSquares()
						obj_square_lightpink.image = pygame.image.load("img/square_lightpink_green.png")
					elif ((obj_square_lightgreen.rect.collidepoint(x, y))):
						if soundOn:
							sound_blop.play()
						backgroundColor = COLOR_LIGHTGREEN
						resetSquares()
						obj_square_lightgreen.image = pygame.image.load("img/square_lightgreen_green.png")
					elif((obj_square_lightblue.rect.collidepoint(x, y))):
						if soundOn:
							sound_blop.play()
						backgroundColor = COLOR_LIGHTBLUE
						resetSquares()
						obj_square_lightblue.image = pygame.image.load("img/square_lightblue_green.png")
					elif ((obj_card_cubes.rect.collidepoint(x, y))):
						if soundOn:
							sound_blop.play()
						cardArtwork = "cubes"
						resetCardBacks()
						obj_card_cubes.image = pygame.image.load("img/card_back_small_cubes_green.png")
					elif ((obj_card_marble.rect.collidepoint(x, y))):
						if soundOn:
							sound_blop.play()
						cardArtwork = "marble"
						resetCardBacks()
						obj_card_marble.image = pygame.image.load("img/card_back_small_marble_green.png")
					elif((obj_card_pink.rect.collidepoint(x, y))):
						if soundOn:
							sound_blop.play()
						cardArtwork = "pink"
						resetCardBacks()
						obj_card_pink.image = pygame.image.load("img/card_back_small_pink_green.png")
					elif ((obj_card_stone.rect.collidepoint(x, y))):
						if soundOn:
							sound_blop.play()
						cardArtwork = "stone"
						resetCardBacks()
						obj_card_stone.image = pygame.image.load("img/card_back_small_stone_green.png")
					elif ((obj_card_tile.rect.collidepoint(x, y))):
						if soundOn:
							sound_blop.play()
						cardArtwork = "tile"
						resetCardBacks()
						obj_card_tile.image = pygame.image.load("img/card_back_small_tile_green.png")
					elif((obj_card_woven.rect.collidepoint(x, y))):
						if soundOn:
							sound_blop.play()
						cardArtwork = "woven"
						resetCardBacks()
						obj_card_woven.image = pygame.image.load("img/card_back_small_woven_green.png")
					elif((obj_box_sound.rect.collidepoint(x, y))):
						if soundOn:
							obj_box_sound.image = pygame.image.load("img/box_sound_off.png")
						elif not(soundOn):
							sound_blop.play()
							obj_box_sound.image = pygame.image.load("img/box_sound_on.png")
						soundOn = not(soundOn)
						
			gameDisplay.blit(obj_buttonMainMenu.image, obj_buttonMainMenu.rect)
			gameDisplay.blit(obj_square_white.image, obj_square_white.rect)
			gameDisplay.blit(obj_square_lightpink.image, obj_square_lightpink.rect)
			gameDisplay.blit(obj_square_lightblue.image,obj_square_lightblue.rect)
			gameDisplay.blit(obj_square_lightgreen.image, obj_square_lightgreen.rect)
			gameDisplay.blit(obj_card_cubes.image, obj_card_cubes.rect)
			gameDisplay.blit(obj_card_marble.image, obj_card_marble.rect)
			gameDisplay.blit(obj_card_pink.image, obj_card_pink.rect)
			gameDisplay.blit(obj_card_stone.image, obj_card_stone.rect)
			gameDisplay.blit(obj_card_tile.image, obj_card_tile.rect)
			gameDisplay.blit(obj_card_woven.image, obj_card_woven.rect)
			gameDisplay.blit(obj_box_sound.image, obj_box_sound.rect)
			gameDisplay.blit(spr_selectArtwork, POS_SELECT_ARTWORK)
			gameDisplay.blit(spr_chooseBackground, POS_CHOOSE_BACKGROUND)
			pygame.display.update() #Updates the screen every frame
			clock.tick(FRAMES_PER_SECOND)
<<<<<<< HEAD

		while (gameScreen == 8 and gameRun):
			gameDisplay.fill(backgroundColor)
			displayMessage("This is the DIAGNOSTICS screen.",COLOR_RED,[GAME_WIDTH/3,GAME_HEIGHT/2])
			displayMessage("Press the 'P' key to save this screen for printing.",COLOR_BLUE,[GAME_WIDTH/3,(GAME_HEIGHT/2) + 100])
			gameDisplay.blit(obj_buttonMainMenu.image, obj_buttonMainMenu.rect)

			#NOTE: In order for the output image to correctly contain all elements of the screen, the event handling portion of the while loop needs to come after any drawing that occurs.
			for event in pygame.event.get():
				if event.type == pygame.QUIT:
					gameRun = False #Ends the game if they user attempts to close the window
				if event.type == pygame.KEYDOWN:
					if event.key == pygame.K_p:
						pygame.image.save(gameDisplay, "diagnosticOutput.png") #NOTE: later on, change this so that it outputs the image with a dynamic name based on things like player name.
				if event.type == pygame.MOUSEBUTTONDOWN:
					# Set the x, y positions of the mouse click
					x, y = event.pos
					if ((obj_buttonMainMenu.rect.collidepoint(x, y))):
						if soundOn:
							sound_blop.play()
						gameScreen = 2
			pygame.display.update() #Updates the screen every frame
			clock.tick(FRAMES_PER_SECOND)

=======
			
		while (gameScreen == 8 and gameRun):
			#some button here:
				TIME_ALLOWED = 30000
				
			#some button here:
				TIME_ALLOWED = 20000
				
			#some button here:
				TIME_ALLOWED = 15000
				
			#some button here:
				TIME_ALLOWED = 10000
				
>>>>>>> origin/Difficulty
	pygame.quit()
	quit()

gameLoop()