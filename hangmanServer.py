import sys
from HOAStryngS import HOAStryngS
import random
import json
from game import game

"""
Hangman - Term Project
with Hanging on a Stryng protocol
authors : Jeffrey Caruso, Cordelia Notbohm
date    : Fall 2023
file    : hangmanServer.py
class   : hangmanServer
"""

# a hangman server that facilitates games of hangman
# will check for a new client connection
# will loop through client IDs
# run pollClientForRequest() for each clientID...
class hangmanServer:
    
    def __init__(self, serverPort):
        # initialize server data structures
        self.net = HOAStryngS(serverPort)
        self.clientIDToUsername = dict()
        self.gameIDtoGame = dict()
        self.clientIDToGameID = dict()
        self.clientIDtoWins = dict()

        # read in scoreboard from file
        try:
            with open('scoreboard.json', 'r') as openfile:
                self.scoreboard = list(json.load(openfile))
        except:
            self.scoreboard = list()
        #end init

    # process a clients register request
    def __processRegister(self, clientID, RegisterRequest):
        username = RegisterRequest["Data"]
        # print for now - to check that everything is working
        print(username + " : " + str(clientID))
        
        # check if username is valid (size limit) + unique 
        if len(username) > 20:
            self.net.sendDataToClient(clientID, "41", "Invalid Method Parameter")
            self.net.removeClient(clientID)
            return
        
        if username in self.clientIDToUsername.values():
            self.net.sendDataToClient(clientID, "41", "Invalid Method Parameter")
            self.net.removeClient(clientID)
            return
        
        # assign username to clientID
        self.clientIDToUsername[clientID] = username
        self.clientIDtoWins[clientID] = 0

        # send status back to client
        self.net.sendDataToClient(clientID, "20", "OK")
        #end __processRegister


    # process a clients list games request
    def __processList(self, clientID):
        # create a readable game list
        gameList = list()

        for gameID in self.gameIDtoGame.keys():
            game = self.gameIDtoGame[gameID]
            usernames = list()
            for client in game.clientIDtoScore:
                usernames.append(self.clientIDToUsername[client])
            
            gameInfo = {
                "gameID" : gameID,
                "usernames" : usernames
            }

            gameList.append(gameInfo)
            #access


        self.net.sendDataToClient(clientID, "20", "OK", gameList)
        #end __processList
    

    # generates a new unique four digit client ID number
    def __getNewGameID(self):
        # generate random # [0,9999]
        tempID = random.randrange(0, 9999, 1)

        while(tempID in self.gameIDtoGame.keys()):
            #while tempIDis one of the keys, keep trying
            tempID = random.randrange(0, 9999, 1)
            
        return tempID
        #end __createNewClientID


    # process a clients create game request
    def __processCreate(self, clientID, RegisterRequest):
        if self.__alreadyInGame(clientID):
            self.net.sendDataToClient(clientID, "42", "Illegal Request")
            return
        
        # generate new (unique) gameID and create new game
        gameID = self.__getNewGameID()
        newGame = game(gameID)
        self.gameIDtoGame[gameID] = newGame
        
        #decide guesser
        if random.randrange(0, 2, 1):
            newGame.guesser = clientID            

        info = newGame.getGameInfo(clientID)
        
        # add the creator to the game - and return status
        if newGame.addPlayer(clientID):
            self.clientIDToGameID[clientID] = gameID
            self.net.sendDataToClient(clientID, "20", "OK", info)
        else:
            del self.gameIDtoGame[gameID] 
            self.net.sendDataToClient(clientID, "50", "Internal Server Error")
        #end __processCreate


    # process a clients join game request
    def __processJoin(self, clientID, JoinRequest):
        gameID = int(JoinRequest["Data"])

        # Phase 0: check if already in game 
        if self.__alreadyInGame(clientID):
            self.net.sendDataToClient(clientID, "42", "Illegal Request")
            return

        # Phase 1 :check if gameID exists (and is valid)
        if gameID not in self.gameIDtoGame.keys():
            self.net.sendDataToClient(clientID, "44", "Cannot Join Game")
            return
    
        game = self.gameIDtoGame[gameID]
        #implicit guesser decision
        if game.getGuesser() is None:
            self.gameIDtoGame[gameID].guesser = clientID    
        
        # Phase 2: send the stuff out
        info = game.getGameInfo(clientID)
        
        # add the creator to the game - and return status
        if self.gameIDtoGame[gameID].addPlayer(clientID):
            self.clientIDToGameID[clientID] = gameID
            self.net.sendDataToClient(clientID, "20", "OK", info)
        else:
            self.net.sendDataToClient(clientID, "44", "Cannot Join Game")
        #end __processJoin


    # return true if a client is in a game already 
    def __alreadyInGame(self, clientID):
        return clientID in self.clientIDToGameID.keys()
        #end already in game


    # process a clients exit game request
    def __processExit(self, clientID, ExitRequest):
        # Phase 0: check if gameID is none
        if clientID not in self.clientIDToGameID.keys():
            self.net.sendDataToClient(clientID, "42", "Illegal Request")
            return

        gameID = self.clientIDToGameID[clientID]
        
        # Phase 1: check if gameID exists (and is valid)
        if gameID not in self.gameIDtoGame.keys():
            self.net.sendDataToClient(clientID, "50", "Internal Server Error")
            return
        
        # Phase 2: increment points if they won
        game = self.gameIDtoGame[gameID]
        if game.getGuesser() == clientID: #guesser
            if game.roundWon():
                self.clientIDtoWins[clientID] += 1
        else: #selector 
            if game.roundLost():
                self.clientIDtoWins[clientID] += 1

        # Phase 3: exit game
        if game.removePlayer(clientID):
            del self.clientIDToGameID[clientID]
            if game.getNumPlayers() == 0:
                del self.gameIDtoGame[gameID]
            self.net.sendDataToClient(clientID, "20", "OK")
        else:
            self.net.sendDataToClient(clientID, "50", "Internal Server Error")
        #end __processList


    # add a client to the scorebaord
    def __addClientsScoreToScoreboard(self, clientID):
        # creating dictionary with user's score 
        clientToScore = {
            "username" : self.clientIDToUsername[clientID],
            "wins" : self.clientIDtoWins[clientID]
        }

        # add users score
        self.scoreboard.append(clientToScore) 

        # sort the scoreboard
        self.scoreboard = sorted(self.scoreboard, key=lambda x:x['wins'], reverse=True)

        # trim scoreboard if above some length
        del self.scoreboard[20:]

        # persist scoreboard to file
        with open('scoreboard.json', 'w') as outfile:
            json.dump(self.scoreboard, outfile)

        #end __addClientsScoreToScoreboard


    # process a clients unregister request
    def __processUnregister(self, clientID, unregisterRequest):
        #Phase 1: check if in game
        if clientID in self.clientIDToGameID.keys():
            gameID = self.clientIDToGameID[clientID]
            self.gameIDtoGame[gameID].removePlayer(clientID)
            if self.gameIDtoGame[gameID].getNumPlayers() == 0:
                del self.gameIDtoGame[gameID]
            del self.clientIDToGameID[clientID]

        # Phase 2 add score to scoreboard
        self.__addClientsScoreToScoreboard(clientID)
        
        # Phase 3: Unregister (will already not be in a game by here...)
        # remove from association of clientID to usernames (removing them from being a valid player...?)
        del self.clientIDToUsername[clientID]
        del self.clientIDtoWins[clientID]
        self.net.sendDataToClient(clientID, "20", "OK")
        
        self.net.removeClient(clientID)
        #end __processList


    # process a clients guess letter request
    def __processGuessLetter(self, clientID, guessLetterRequest):
        #check that the client is actually in a game
        if clientID not in self.clientIDToGameID.keys():
            self.net.sendDataToClient(clientID, "42", "Illegal Request")
            return
        
        gameID = self.clientIDToGameID[clientID]
        game = self.gameIDtoGame[gameID]

        # check that they are actually a guesser 
        if clientID != game.getGuesser():
            self.net.sendDataToClient(clientID, "42", "Illegal Request")
            return
        
        #check that the game has a word
        censoredWord = game.getCensoredWord()
        if censoredWord is None:
            self.net.sendDataToClient(clientID, "35", "Wait")
            return 
        
        # letter can be guessed - have game do processing and return success
        guessedLetter = guessLetterRequest["Data"]
        game.processGuessLetter(guessedLetter)

        info = game.getGameInfo(clientID)
        self.net.sendDataToClient(clientID, "20", "OK", info)
        #end __processList
    

    # process a clients select request
    def __processSelectWord(self, clientID, selectWordRequest):
        # validate if they can select a word (not the guesser, game is not in progress)
        if clientID not in self.clientIDToGameID.keys():
            self.net.sendDataToClient(clientID, "42", "Illegal Request")
            
        gameID = self.clientIDToGameID[clientID]
        game = self.gameIDtoGame[gameID]

        if ((clientID != game.getGuesser()) and (not game.roundInProgress())):
            # you are allowed to set the word
            # decide if word is valid - for now just accept all
            if "Data" not in selectWordRequest.keys():
                self.net.sendDataToClient(clientID, "41", "Invalid Method Parameter")
                return
            
            word = selectWordRequest["Data"]
            game.setWord(word)
            #ack
            
            info = game.getGameInfo(clientID)
            self.net.sendDataToClient(clientID, "20", "OK", info)
            return
            
        #nak
        self.net.sendDataToClient(clientID, "42", "Illegal Request")
        #end __processSelectWord


    # process a clients ask game state request
    def __processAskGameState(self, clientID, askGameStateRequest):        
        #check that the client is actually in a game
        if clientID not in self.clientIDToGameID.keys():
            self.net.sendDataToClient(clientID, "42", "Illegal Request")
            return
        
        # get game state and send it
        gameID = self.clientIDToGameID[clientID]
        game = self.gameIDtoGame[gameID]
        info = game.getGameInfo(clientID)

        self.net.sendDataToClient(clientID, "20", "OK", info)
        #end __processAskGameState


    # process a clients get score board request
    def __processGetScoreBoard(self, clientID, getScoreBoardRequest):
        # for now prob skip checking clientID (not necessary at all it seems)
        clientScore = self.clientIDtoWins[clientID]

        ScoreInfo = {
            "scoreboard" : self.scoreboard,
            "your score" : clientScore
        }
        self.net.sendDataToClient(clientID, "20", "OK", ScoreInfo)
        #end __processGetScoreBoard


    # main loop for server.
    # 1) check for new client
    # 2) process requests for all clients on the client list
    # 3) repeat
    def server(self):

        while(True):
            #check for new client
            newClientID = self.net.pollForNewClientConnection()
            
            #if new ID was created, save it
            if(newClientID != -1):  ##is not None):
                newRequest = None
                while (newRequest is None):
                    newRequest = self.net.pollClientForRequest(newClientID)

                # register them with this server 
                newRequestMethodType = newRequest["Method Type"]
                if (newRequestMethodType == "REGI"):
                    self.__processRegister(newClientID, newRequest)
                else:
                    # if they don't register properly, then remove the connection
                    self.net.removeClient(newClientID)


            #get client list            
            clients = list(self.clientIDToUsername.keys())
            #poll each of the clients to see if they have sent a request
            for clientID in clients:
                newRequest = self.net.pollClientForRequest(clientID)
                if newRequest is None:
                    #skip
                    continue
                
                newRequestMethodType = newRequest["Method Type"]
                print("Serving a " + str(newRequestMethodType) + " request for client " + str(clientID))

                # call the approperiate processing helper method
                # (register gets checked for above)
                if(newRequestMethodType == "UNRG"):
                    self.__processUnregister(clientID, newRequest)

                elif(newRequestMethodType == "LIST"):
                    self.__processList(clientID)

                elif(newRequestMethodType == "CREA"):
                    self.__processCreate(clientID, newRequest)

                elif(newRequestMethodType == "JOIN"):
                    self.__processJoin(clientID, newRequest)

                elif(newRequestMethodType == "EXIT"):
                    self.__processExit(clientID, newRequest)

                # game specific processing methods below
                elif(newRequestMethodType == "SLWD"):
                    self.__processSelectWord(clientID, newRequest)
            
                elif(newRequestMethodType == "GUEL"):
                    self.__processGuessLetter(clientID, newRequest)

                elif(newRequestMethodType == "AKGS"):
                    self.__processAskGameState(clientID, newRequest)

                elif(newRequestMethodType == "GTSB"):
                    self.__processGetScoreBoard(clientID, newRequest)

                else:
                    #unexpected to reach here because HOAStryngS should have it filtered out.
                    print("Something went wrong with a recent recieved request (Malformed Request)")      
                    print(newRequest)          
                #end for                    
        #end server


  #end hangmanServer

#run server
def main():
    args = sys.argv[1:]
    serverPort = int(args[0])
    server = hangmanServer(serverPort)
    server.server()
    #endmain
    
#run server
if __name__ == "__main__":
    main()