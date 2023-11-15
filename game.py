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
    #roundWon() # word found
    #roundLost() # hangman fullly displayed
    #roundInProgress()
    #getNumPlayers()
    #getword()
    #getCensoredWord()
    #startNewRound() 
    #getGuesser() {return clientID}




    #end of game class
#
