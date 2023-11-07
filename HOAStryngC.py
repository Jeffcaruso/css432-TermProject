from socket import *


class HOAStryngC:
    # <start of class>

    # funtions

    def __init__(self):
        self.clientSocket

    # set up socket 
    def __prepSocket(self, portNumber, hostName):
        self.clientSocket = socket(AF_INET, SOCK_STREAM)
        self.clientSocket.connect((hostName, portNumber))        
        # end of prepSocket

    # send though server socket
    def __sendToSocket(self, packet):
        self.clientSocket.send(packet)
      
        #end of sendToSocket

    # register
    def register(self, hostName, portNumber, username):
        # build the packet using our protocol 

        # send the packet

        # return bool for success or failure?
        # end of register

    # request list of games
    def requestGamesList(self):
        # build the packet using our protocol 

        # send the packet
        
        # return list of games
        # end of requestGamesList

    # create a new game
    def createNewGame(self):
        # build the packet using our protocol 

        # send the packet
      
        # return the game ID of new game
        # end of createNewGame

    # join a game 
    def joinGame(self, gameID):
        # build the packet using our protocol 

        # send the packet
        # return if you are "starting first" 
        # end join game

    # exit the game
    def exitGame(self):
        # build the packet using our protocol 

        # send the packet

        # end exitGame

    # unregister 
    def unregister(self):
        # build the packet using our protocol 

        # send the packet

        # end unregister

    # guess letter
    def guessLetter(self, guessedLetter):
        # build the packet using our protocol 

        # send the packet

        # return new word state (if the guess was correct or not) 
        # end guessLetter

    #NOTE, not necessary, complete this later
    # guess word (optional)
    def __guessWord(self, guessedWord):
        # build the packet using our protocol 

        # send the packet

        # return new word state (if the guess was correct or not) 
        #end guessWord


    # select a word
    def selectWord(self, enteredWord):
        # build the packet using our protocol 

        # send the packet

        # handle if server rejected your word
        
        #end selectWord


    # initialize guesser 
    def initGuesser(self):
        # build the packet using our protocol 

        # send the packet

        #end initGuesser


    # ask game state
    def askGameState():
        # build the packet using our protocol 

        # send the packet
        
        # return game state
        #end askGameState


    ## NOTE, EC, complete this later...
    # get scoreboard
    def getScoreboard():
        # build the packet using our protocol 

        # send the packet
        
        # return scoreboard
        #end getScoreboard


    # <end of class>

