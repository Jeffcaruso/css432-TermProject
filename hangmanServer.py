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
        #end init

    def __processRegister(self, clientID, RegisterRequest):
        username = RegisterRequest["Data"]
        # print for now - to check that everything is working
        print(username)
        # check if username is valid

        #### MORE HANDLING HERE LATER..................................................
        
        # assign username to clientID
        self.clientIDToUsername[clientID] = username

        # send status back to client
        self.net.sendDataToClient(clientID, "20", "OK")
        #end __processRegister


    def __processList(self, clientID):
        print("got to processList")

        #NOTE, these need to be gameID, username
        gameList = {1 : "usernameA",  2 : "usernameB" } 

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
            self.net.sendDataToClient(clientID, "20", "OK", creationInfo)
        else:
            self.net.sendDataToClient(clientID, "50", "Internal Server Error")
        #end __processCreate
        

    def __processJoin(self, clientID, RegisterRequest):
        print(clientID)
        #end __processList

    def __processExit(self, clientID, RegisterRequest):
        print(clientID)
        #end __processList

    def __processUnregister(self, clientID, RegisterRequest):
        print(clientID)
        #end __processList

    def __processGuessWord(self, clientID, RegisterRequest):
        print(clientID)
        #end __processList
    
    def __processSelectWord(self, clientID, RegisterRequest):
        print(clientID)
        #end __processList

    def __processInitGuesser(self, clientID, RegisterRequest):
        print(clientID)
        #end __processList

    def __processAskGameState(self, clientID, RegisterRequest):
        print(clientID)
        #end __processList

    def __processGetMyPoints(self, clientID, RegisterRequest):
        print(clientID)
        #end __GetMyPoints

    def __processGetOpponentPoints(self, clientID, RegisterRequest):
        print(clientID)
        #end __GetOpponentPoints

    def __processGetScoreBoard(self, clientID, RegisterRequest):
        print(clientID)
        #end __processList


    #more process requests methods here...

    def server(self):
        while(True):

            print("here HS - 2")

            #check for new client
            newClientID = self.net.pollForNewClientConnection()
            
            #if new ID was created, save it
            if(newClientID != -1):  ##is not None):
                self.clientIDToUsername[newClientID] = "" 

            print("here HS - 5")

            #poll each of the clients to see if they have sent a request
            for clientID in self.clientIDToUsername:

                print("here HS - 7")
                newRequest = self.net.pollClientForRequest(clientID)
                if newRequest is None:
                    #skip
                    continue
                
                newRequestMethodType = newRequest["Method Type"]


                # call the approperiate processing helper method
                if(newRequestMethodType == "REGI"):
                    self.__processRegister(clientID, newRequest)

                elif(newRequestMethodType == "LIST"):
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

                elif(newRequestMethodType == "SELW"):
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