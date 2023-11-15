import sys
from HOAStryngS import HOAStryngS

# will check for a new client connection
# will loop through client IDs
# run pollClientForRequest() for each clientID...

class hangmanServer:
    
    def __init__(self, serverPort):
        self.net = HOAStryngS(serverPort)
        self.clientIDToUsername = dict()
        #end init

    def __processRegister(self, clientID, RegisterRequest):
        username = RegisterRequest["Username"]
        # print for now - to check that everything is working
        print(username)
        # check if username is valid

        #### MORE HANDLING HERE LATER..................................................
        
        # assign username to clientID
        self.clientIDToUsername[clientID] = username

        # send status back to client
        self.net.sendRegistrationStatus(clientID, "20", "OK")
        #end __processRegister


    def __processList(self, clientID, RegisterRequest):
        print(clientID)
        #end __processList
    
    def __processCreate(self, clientID, RegisterRequest):
        print(clientID)
        #end __processList

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

    def __processGetScoreBoard(self, clientID, RegisterRequest):
        print(clientID)
        #end __processList


    #more process requests methods here...

    def server(self):
        while(True):
            
            #check for new client
            newClientID = self.net.pollForNewClientConnection()
            
            #if new ID was created, save it
            if(newClientID != -1):  ##is not None):
                self.clientIDToUsername[newClientID] = "" 

            #poll each of the clients to see if they have sent a request
            for clientID in self.clientIDToUsername:
                newRequest = self.net.pollClientForRequest(clientID)
                newRequestMethodType = newRequest["Method Type"]

                # call the approperiate processing helper method
                if(newRequestMethodType == "REGI"):
                    self.__processRegister(clientID, newRequest)

                elif(newRequestMethodType == "LIST"):
                    self.__processList(clientID, newRequest)

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