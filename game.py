"""
Hangman - Term Project
with Hanging on a Stryng protocol
authors : Jeffrey Caruso, Cordelia Notbohm
date    : Fall 2023
file    : game.py
class   : game
"""

# class that keeps track of a single game 
class game:
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
        self.lastGuess = None
        self.numIncorrectGuesses = 0  # hangman State
        self.roundNumber = 0
        #end init
    
    
    ###############################################
    # Main Gameplay Logic Methods 
    ###############################################

    # word status methods 
    # and add that processing in here 
    def processGuessLetter(self, letter : str):
        # if round has been won or lost, don't update anything
        if not self.roundInProgress():
            return False
        
        # if letter is in word, reveal those letters
        letter = letter.lower()
        self.lastGuess = letter
        if letter in self.word:
            newCensoredWord = ""
            index = 0
            for char in self.word:
                if char == letter:
                    newCensoredWord += letter
                else:
                    newCensoredWord += self.censoredWord[index]
                index += 1
            self.censoredWord = newCensoredWord
            return True
        
        # otherwise increment incorrect guesses
        else: 
            self.numIncorrectGuesses = self.numIncorrectGuesses + 1
            return False
        #end processGuessLetter
        

    # create a dictonary with all the info
    # a client might want about a game
    def getGameInfo(self, clientID):

        # get a string that represents the
        # current state of the game
        if (self.word == None):
            gameState = "INIT"
        elif (self.roundWon()):
            gameState = "WON"
        elif (self.roundLost()):
            gameState = "LOST"
        else:
            gameState = "IN_PROGRESS"
        
        # fill in other variables
        gameInfo = {
            "GameID" : self.gameID,
            "Num Players" : self.getNumPlayers(),
            "You Are Guesser" : bool(self.guesser == clientID),
            "Censored Word" : self.censoredWord,
            "Incorrect Guesses" : self.numIncorrectGuesses,
            "Last Guess" : self.lastGuess,
            "Game State" : str(gameState)
        }
        
        return gameInfo
        #end getGameState


    ###############################################
    # round status methods 
    ###############################################
    
    def roundWon(self): # word found
        return ((self.word is not None) and (self.word == self.censoredWord))
        #end roundWon()
    

    def roundLost(self): # hangman fully displayed
        return self.numIncorrectGuesses >= self.NUM_ROUNDS_TILL_LOSE
        #end roundLost()
    

    def roundInProgress(self): # game has word but not won or lost
        return (not (self.roundWon() or self.roundLost()) and self.word is not None)
        #end roundInProgres()
        
        
    def getNumIncorrectGuesses(self): # get num incorrect guesses 
        return self.getNumIncorrectGuesses
        #end getNumIncorrectGuesses
        
    
    ###############################################
    # Game Word methods 
    ###############################################
    
    def getWord(self): # get the word 
        return self.word
        #end getWord


    def setWord(self, word: str): # set the word and censored word
        word = word.lower()
        #censored word
        cWord = ""
        #modified word (lowercase and with "_" instead of " ")
        mWord = ""
        
        # for each letter constuct both words
        for char in word:
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


    def getCensoredWord(self): # get the censored word
        return self.censoredWord
        #end getCensoredWord
    


    ###############################################
    # game Player Methods
    ###############################################

    def getNumPlayers(self): # get the number of players
        return len(self.clientIDtoScore.keys())
        #end getNumPlayers


    def gameIsFull(self):  # true if game is full
        return self.getNumPlayers() >= self.MAX_PLAYERS
        #end gameIsFull


    def addPlayer(self, clientID): # add a player if not full
        # check if game is full
        if self.gameIsFull():
            return False
        
        self.clientIDtoScore[clientID] = 0
        return True
        #end addPlayer 


    def removePlayer(self, clientID): # remove the player if they are in the game
        # check if client is in the game 
        if clientID not in self.clientIDtoScore.keys():
            return False
        
        del self.clientIDtoScore[clientID]
        return True
        #end removePlayer 


    def getGuesser(self): # get the guesser
        return self.guesser
        #end getGuesser 

    
    def setGuesser(self, clientID): # set the guesser
        self.guesser = clientID
        #end setGuesser
        
        
    def getScore(self, clientID): # get the score of a client id 
        return self.clientIDtoScore[clientID]
        #end getScore

    #end of game class