import sys
from HOAStryngS import HOAStryngS
import random
from game import game

# will check for a new client connection
# will loop through client IDs
# run pollClientForRequest() for each clientID...

class hangmanServer:
    
    def __init__(self, serverPort):
        self.net = HOAStryngS(serverPort)
        self.clientIDToUsername = dict()
        self.gameIDtoGame = dict()
        self.clientIDToGameID = dict()
        #end init

    def __processRegister(self, clientID, RegisterRequest):
        username = RegisterRequest["Data"]
        # print for now - to check that everything is working
        print(username)
        
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

        # send status back to client
        self.net.sendDataToClient(clientID, "20", "OK")
        #end __processRegister


    def __processList(self, clientID):
        print("got to processList")

        #NOTE, these need to be gameID, username
        gameList = list()
        #gameID, username1, username2

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


    def __processCreate(self, clientID, RegisterRequest):
        if self.__alreadyInGame(clientID):
            self.net.sendDataToClient(clientID, "42", "Illegal Request")
            return
        
        # generate new (unique) gameID and create new game
        gameID = self.__getNewGameID()
        self.gameIDtoGame[gameID] = game(gameID)

        creationInfo = dict()
        creationInfo["GameID"] = gameID
        
        #decide guesser
        if random.randrange(0, 2, 1):
            creationInfo["You Are Guesser"] = True
            self.gameIDtoGame[gameID].guesser = clientID            
        else:
            creationInfo["You Are Guesser"] = False

        # add the creator to the game - and return status
        if self.gameIDtoGame[gameID].addPlayer(clientID):
            self.clientIDToGameID[clientID] = gameID
            self.net.sendDataToClient(clientID, "20", "OK", creationInfo)
        else:
            del self.gameIDtoGame[gameID] 
            self.net.sendDataToClient(clientID, "50", "Internal Server Error")
        #end __processCreate


    def __processJoin(self, clientID, JoinRequest):
        gameID = int(JoinRequest["Data"])

        if self.__alreadyInGame(clientID):
            self.net.sendDataToClient(clientID, "42", "Illegal Request")
            return

        # Phase 1 :check if gameID exists (and is valid)
        if gameID not in self.gameIDtoGame.keys():
            self.net.sendDataToClient(clientID, "44", "Cannot Join Game")
            return
    

        joinInfo = dict()
        #implicit guesser decision
        if self.gameIDtoGame[gameID].getGuesser() is None:
            #youre it
            joinInfo["You Are Guesser"] = True
            self.gameIDtoGame[gameID].guesser = clientID    

        else:
            joinInfo["You Are Guesser"] = False
        
        # Phase 2: send the stuff out
        # add the creator to the game - and return status
        if self.gameIDtoGame[gameID].addPlayer(clientID):
            self.clientIDToGameID[clientID] = gameID
            self.net.sendDataToClient(clientID, "20", "OK", joinInfo)
        else:
            self.net.sendDataToClient(clientID, "44", "Cannot Join Game")
        #end __processJoin


    def __alreadyInGame(self, clientID):
        return clientID in self.clientIDToGameID.keys()
        #end already in game


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
        
        # Phase 2: exit game
        if self.gameIDtoGame[gameID].removePlayer(clientID):
            del self.clientIDToGameID[clientID]
            if self.gameIDtoGame[gameID].getNumPlayers() == 0:
                del self.gameIDtoGame[gameID]
            self.net.sendDataToClient(clientID, "20", "OK")
        else:
            self.net.sendDataToClient(clientID, "50", "Internal Server Error")
        #end __processList


    def __processUnregister(self, clientID, unregisterRequest):
        #Phase 1: check if in game
        if clientID in self.clientIDToGameID.keys():
            gameID = self.clientIDToGameID[clientID]
            self.gameIDtoGame[gameID].removePlayer(clientID)
            if self.gameIDtoGame[gameID].getNumPlayers() == 0:
                del self.gameIDtoGame[gameID]
            del self.clientIDToGameID[clientID]
        
        # Phase 2: Unregister (will already not be in a game by here...)
        # remove from association of clientID to usernames (removing them from being a valid player...?)
        del self.clientIDToUsername[clientID]
        self.net.sendDataToClient(clientID, "20", "OK")
        
        self.net.removeClient(clientID)
        #end __processList


    def __processGuessWord(self, clientID, guessWordRequest):
        print(clientID)
        #end __processList
    

    def __processSelectWord(self, clientID, selectWordRequest):
        
        # validate if they can select a word (not the guesser, game is not in progress)
        if clientID not in self.clientIDToGameID.keys():
            self.net.sendDataToClient(clientID, "42", "Illegal Request")
            
        gameID = self.clientIDToGameID[clientID]
        game = self.gameIDtoGame[gameID]

        #NOTE: this breaks it: and not game.roundInProgress()
        if ((clientID != game.getGuesser()) and (not game.roundInProgress())):
            # you are allowed to set the word
            # decide if word is valid - for now just accept all
            word = selectWordRequest["Data"]
            game.setWord(word)
            #ack
            #####self.net.sendDataToClient(clientID, "20", "OK")
            censoredWord = game.getCensoredWord()
            #collect, then send dictionary of info
            info = {
                "Censored Word" : censoredWord,
                "Incorrect Guesses" : 0
            }
            
            self.net.sendDataToClient(clientID, "20", "OK", info)

            return
            
        #nak
        self.net.sendDataToClient(clientID, "42", "Illegal Request")
        #end __processList


    def __processInitGuesser(self, clientID, initGuesserRequest):
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

        # get censored word
        censoredWord = game.getCensoredWord()

        if censoredWord is None:
            self.net.sendDataToClient(clientID, "35", "Wait")
            return 

        #collect, then send dictionary of info
        info = {
            "Censored Word" : censoredWord,
            "Incorrect Guesses" : 0
        }
        
        self.net.sendDataToClient(clientID, "20", "OK", info)
        #end __processList


    def __processAskGameState(self, clientID, askGameStateRequest):
        print(clientID)
        #end __processList


    def __processGetMyPoints(self, clientID, getMyPointsRequest):
        print(clientID)
        #end __GetMyPoints


    def __processGetOpponentPoints(self, clientID, getOpponentPointsRequest):
        print(clientID)
        #end __GetOpponentPoints


    def __processGetScoreBoard(self, clientID, getScoreBoardRequest):
        print(clientID)
        #end __processList



    def server(self):

        while(True):

            #check for new client
            newClientID = self.net.pollForNewClientConnection()
            
            #if new ID was created, save it
            if(newClientID != -1):  ##is not None):
                newRequest = None
                while (newRequest is None):
                    newRequest = self.net.pollClientForRequest(newClientID)

                newRequestMethodType = newRequest["Method Type"]
                if (newRequestMethodType == "REGI"):
                    self.__processRegister(newClientID, newRequest)
                else:
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


                # call the approperiate processing helper method
                # if(newRequestMethodType == "REGI"):
                #     self.__processRegister(clientID, newRequest)

                if(newRequestMethodType == "LIST"):
                    self.__processList(clientID)

                elif(newRequestMethodType == "CREA"):
                    self.__processCreate(clientID, newRequest)

                elif(newRequestMethodType == "JOIN"):
                    self.__processJoin(clientID, newRequest)

                elif(newRequestMethodType == "EXIT"):
                    self.__processExit(clientID, newRequest)

                elif(newRequestMethodType == "UNRG"):
                    self.__processUnregister(clientID, newRequest)

                # game specific processing below
                elif(newRequestMethodType == "GUEL"):
                    self.__processGuessWord(clientID, newRequest)

                elif(newRequestMethodType == "SLWD"):
                    self.__processSelectWord(clientID, newRequest)

                elif(newRequestMethodType == "INIG"):
                    self.__processInitGuesser(clientID, newRequest)

                elif(newRequestMethodType == "AKGS"):
                    self.__processAskGameState(clientID, newRequest)

                elif(newRequestMethodType == "GMPT"):
                    self.__processGetMyPoints()
                
                elif(newRequestMethodType == "GOPT"):
                    self.__processGetOpponentPoints()

                elif(newRequestMethodType == "GTSB"):
                    self.__processGetScoreBoard(clientID, newRequest)

                else:
                    #unexpected to reach here because HOAStryngS should have it filtered out.
                    print("Something went wrong with a recent recieved request (Malformed Request)")                
                #end for                    
        #end server


  #end hangmanServer

def main():
    args = sys.argv[1:]
    serverPort = int(args[0])
    server = hangmanServer(serverPort)
    server.server()
    #endmain
    
main()