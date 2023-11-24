
class game:
    """A hangman game class that keeps track of the current status of 
    a game of hangman

    Args:
        gameID (int): the unique id associated with this game
    """
    
    # Game constants 
    NUM_ROUNDS_TILL_LOSE = 6
    MAX_PLAYERS = 2


    def __init__(self, gameID : int):
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
    
    
    ###############################################
    # Main Gameplay Logic Methods 
    ###############################################

    def startNewRound(self):
        # switch who is guessing
        for client in self.clientIDtoScore.keys():
            if self.getGuesser != client:
                self.setGuesser = client

        # reset game variables
        self.word = None
        self.censoredWord = None
        self.numIncorrectGuesses = 0
        self.roundNumber = self.roundNumber + 1
        #end startNewRound()


    # word status methods 
    #NOTE: still need to decide how points will work and 
    # and add that processing in here 
    def processGuessLetter(self, letter : str):
        # if round has been won or lost, don't update anything
        if not self.roundInProgress():
            return False
        
        # if letter is in word, reveal those letters
        letter = letter.lower()
        if letter in self.word:
            index = 0
            for char in self.word:
                if char == letter:
                    letterWasInWord = True
                    self.censoredWord[index] = letter
                index = index + 1
            return True
        # otherwise increment incorrect guesses
        else: 
            self.numIncorrectGuesses = self.numIncorrectGuesses + 1
            return False
        #end processGuessLetter


    ###############################################
    # round status methods 
    ###############################################
    
    def roundWon(self): # word found
        return ((self.word is not None) and (self.word == self.censoredWord))
        #end roundWon()
    

    def roundLost(self): # hangman fullly displayed
        return self.numIncorrectGuesses >= self.NUM_ROUNDS_TILL_LOSE
        #end roundLost()
    

    def roundInProgress(self):
        return (not (self.roundWon() or self.roundLost()) and self.word is not None)
        #end roundInProgres()
        
        
    def getNumIncorrectGuesses(self):
        return self.getNumIncorrectGuesses
        #end getNumIncorrectGuesses
        
    
    ###############################################
    # Game Word methods 
    ###############################################
    
    def getWord(self):
        return self.word
        #end getWord


    def setWord(self, word: str):
        word = word.lower()
        
        #censored word
        cWord = ""
        #modified word (lowercase and with "_" instead of " ")
        mWord = ""
        
        for char in self.word:
            #" " -> _            
            if char == " ":
                cWord += "_"
                mWord += "_"
            #a-z,A-z,0-9, etc. -> *
            else:
                cWord += "*"
                mWord += char

        self.censoredWord = cWord
        self.word = mWord
        #end setWord


    def getCensoredWord(self):
        return self.censoredWord
        #end getCensoredWord
    


    ###############################################
    # game Player Methods
    ###############################################

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
        # check if client is in the game 
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
        
        
    def getScore(self, clientID): 
        return self.clientIDtoScore[clientID]
        #end getScore

    #end of game class