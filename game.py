### game class...

# win/loss  - determine from word vs censored word, use a gameWon() method, and hangman state
# InProgress/OtherPlayerQuit


class game:
    NUM_ROUNDS_TILL_LOSE = 6
    MAX_PLAYERS = 2

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
    def startNewRound(self):
        # switch who is guessing

        # reset game variables
        self.word = None
        self.censoredWord = None
        self.numIncorrectGuesses = 0
        self.roundNumber = 0
        #end startNewRound()


    # round status methods NOTE: this doesnt work becuase " " vs "_" 
    def roundWon(self): # word found
        return ((self.word is not None) and (self.word == self.censoredWord))
        #end roundWon()
    

    def roundLost(self): # hangman fullly displayed
        return self.numIncorrectGuesses >= self.NUM_ROUNDS_TILL_LOSE
        #end roundLost()
    

    def roundInProgress(self):
        return (not (self.roundWon() or self.roundLost()) and self.word is not None)
        #end roundInProgres()



    # word status methods 
    def getWord(self):
        return self.word
        #end getWord


    def setWord(self, word: str):
        self.word = word.lower()
        
        cWord = ""
        
        for char in self.word:
            #" " -> _            
            if char == " ":
                cWord += "_"
            #a-z,A-z,0-9, etc. -> *
            else:
                cWord += "*"

        self.censoredWord = cWord
        #end setWord


    def getCensoredWord(self):
        return self.censoredWord
        #end getCensoredWord
    


    # get player status method
    def getNumPlayers(self):
        return len(self.clientIDtoScore.keys())
        #end getNumPlayers


    def gameIsFull(self): 
        return self.getNumPlayers() >= self.MAX_PLAYERS
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