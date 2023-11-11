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
        #end __processRegister

    #more process requests methods here...

    def server(self):
        while(True):
            
            #check for new client
            newClientID = self.net.pollForNewClientConnection()
            
            #if new ID was created, save it
            if(newClientID is not None):
                self.clientIDToUsername[newClientID] = "" 

            #poll each of the clients to see if they have sent a request
            for clientID in self.clientIDToUsername:
                newRequest = self.net.pollClientForRequest(clientID)
                newRequestMethodType = newRequest["Method Type"]
                self.__processRegister(clientID, newRequest)
                # match newRequestMethodType:
                #    case "REGI":
                #        self.__processRegister(clientID, newRequest)
        #end server


  #end hangmanServer

def main():
    args = sys.argv[1:]
    serverPort = int(args[0])
    server = hangmanServer(serverPort)
    server.server()
    #endmain
    
main()