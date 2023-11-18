### game class...

# win/loss  - determine from word vs censored word, use a gameWon() method, and hangman state
# InProgress/OtherPlayerQuit


class game:
    def __init__(self, gameID):
        #generally staying the same once filled *except score, increasing over multiple rounds*
        self.gameID = gameID
        self.clientIDtoScore = dict()

        #per round variables 
        self.guesser = None #clientID of the guessing client
        self.word = None
        self.censoredWord = None
        self.numIncorrectGuesses = 0  # hangman State
        self.roundNumber = 0
        #end init
    

    # round status methods...
    #startNewRound() 


    # round status methods
    #roundWon() # word found
    #roundLost() # hangman fullly displayed
    #roundInProgress()

    # word status methods 
    def getWord(self):
        return self.word
        #end getWord

    def getCensoredWord(self):
        return self.censoredWord
        #end getCensoredWord
    

    # get player status method
    def getNumPlayers(self):
        return len(self.clientIDtoScore.keys())
        #end getNumPlayers


    def gameIsFull(self): 
        return self.getNumPlayers() >= 2
        #end gameIsFull


    def addPlayer(self, clientID):
        # check if game is full
        if self.gameIsFull():
            return False
        
        self.clientIDtoScore[clientID] = 0
        return True
        #end addPlayer 


    def removePlayer(self, clientID):
        if clientID not in self.clientIDtoScore.keys():
            return False
        
        del self.clientIDtoScore[clientID]
        return True
        #end removePlayer 


    def getGuesser(self):
        return self.guesser
        #end getGuesser 

    
    def setGuesser(self, clientID):
        self.guesser = clientID
        #end setGuesser


    #end of game class