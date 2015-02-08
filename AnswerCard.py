#No idea how to edit a file, so I'll just put some stuff here, feel free to copypaste elsewhere
#class for a generic answer card
#nvm found how to edit

class Answer:

      #MEMBER VARIABLES#
        # ansText - a string describing the scenario
        # pointVal - an int that will keep track of how many points playing this card will give. Changes based on scenario
        # beenDealt - a boolean that keeps track of whether or not an answer card has been dealt to a player already
        # beenPlayed - a boolean that keeps track of whether or not the scenario has already been in play during the current game
        #Note that beenPlayed may or may not be optional for this since we haven't decided if we want to recycle cards yet
  
  #cons      
  def __init__(self, cardText):
    self.ansText = cardText
    self.beenDealt = false
    self.beenPlayed = false
  
  #call this to change the number of points an answer is worth each round
  def setPoints(self, points):
    self.pointVal = points
  
  #unsure of if I want to put this as a part of the answer class or the player class. Player playing card vs card being played 
  #also if we put this in the Player class then ew can do self.points = self.points + 5 or something, easier imo
  #ok nvm already in player class :)
  def playCard(self):
    self.beenPlayed = true
    #following line incorrect since scoring system hasn't been started yet
    #pointsOfPlayer = pointsofPlayer + pointVal
    

    
  
    
