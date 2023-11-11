from socket import *
import select
import random

    #     addr = ("", 8080)  # all interfaces, port 8080
    # if socket.has_dualstack_ipv6():
    #     s = socket.create_server(addr, family=socket.AF_INET6, dualstack_ipv6=True)
    # else:
    #     s = socket.create_server(addr)


# # connection class
# class ClientConnection:
#     def __init__(self, ):
#         self.connectionSocket


#     # end ClientConnection
  


class HOAStryngS:
    DELIM = "~~~~~~()"
    PROTOCOL_HEADER = "HOAS/1.0 "


    def __init__(self, serverPort):
        self.activeClientConnections = dict()
        self.__prepListener(serverPort)
        # end init


    # prep listener
    def __prepListener(self, serverPort):
        self.serverListenerSock = socket(AF_INET, SOCK_STREAM)
        self.serverListenerSock.bind(('', serverPort))
        self.serverListenerSock.setblocking(0)
        #end prepListener


    def __sendToSocket(self, clientID, packet):
        # send the packet to the proper client connection
        self.activeClientConnections[clientID].send(packet)      
        #end of sendToSocket


    # does a non blocking read on the given connectionSocket
    # returns the packet read, or none if the connection
    # has not sent anything to this socket
    def __nonBlockingRecieveFrom(self, connectionSocket):
        # the connectionSocket was set to non-blocking earlier
        packet = connectionSocket.recv(1024).decode()

        # if connection didnt send anything return none
        if packet.size() == 0:
            return None

        # while we have yet to get the end of the packet
        # (haven't found the delimiter)
        # we don't need to check if there is something after the 
        # delimiter becuase in our protocol the client would not
        # be sending two packets in a row, it waits for a response
        # before issuing another request 
        while packet.find(self.DELIM) == -1:
            packet += connectionSocket.recv(1024).decode()

        return packet
        #end of __nonBlockingRecieveFrom


    # methods to parse the different kinds of requests
    def __parseRegisterPacket(self, packet):
        #Protocol_header + method_type + "\n" + requestData + delim
        
        # first space is the end of the protocol header
        hdr = packet.split(" ", 1)
        
        # next \n is the end of the statusCode
        # get status code
        methodType = hdr[1].split("\n",1)

        # then delim is the end of the username
        username = methodType[1].split(self.DELIM)

        returnDict = {
            "Method Type" : methodType,
            "Username" : username
        }
        return returnDict
        # end __parseRegisterPacket
    
    def __parseListGames(self, packet):
       print("delete this later")
       # end __parseListGames


    def __parseCreateGame(self, packet):
        print("delete this later")
        # end __parseCreateGame
      

    def __parseJoinGame(self, packet):
        print("delete this later")
        # end __parseJoinGame


    def __parseExitGame(self, packet):
        print("delete this later")
        # end __parseExitGame


    def __parseUnregister(self, packet):
        print("delete this later")
        # end __parseUnregister
    

    def __parseGuessLetter(self, packet):
        print("delete this later")
        # end __parseGuessLetter


    def __parseGuessWord(self, packet):
        print("delete this later")
        #end __parseGuessWord



    def __parseSelectWord(self, packet):
        print("delete this later")
        #end __parseSelectWord
    


    def __parseInitGuesser(self, packet):
        print("delete this later")
        #end __parseInitGuesser



    def __parseAskGameState(self, packet):
        print("delete this later")
        #end __parseInitGuesser


    def __parseSendScoreBoard(self, packet):
        print("delete this later")
        #end __parseSendScoreBoard
    

    # generates a new unique four digit client ID number
    def __getNewClientID(self):
        # generate random # [0,9999]
        tempID = random.randrange(0, 9999, 1)

        while(tempID in self.activeClientConnections.keys()):
            #while tempIDis one of the keys, keep trying
            tempID = random.randrange(0, 9999, 1)
            
        return tempID
        #end __createNewClientID


    # polls for any new client connection by doing a 
    # non-blocking accept on the lister Socket
    # return the new clientID or -1 if no new clients were found
    def pollForNewClientConnection(self):
        # accept from the Listener (which was set to non blocking)
        connectionSocket, clientAddress = self.serverListenerSock.accept()

        # if we recieved a connection request
        # add generate unique ID and add connection to list of active clients
        if connectionSocket is not None:
            clientID = self.__getNewClientID()
            # set connection to be non-blocking so we can poll 
            connectionSocket.setblocking(0)
            self.activeClientConnections[clientID] = connectionSocket
            return clientID
        else:
            return -1
        #end of pollForNewClientConnection


    # poll for client request
    # return tuple with first value being method type, and the rest being the parameters 
    # that the client sent with that method.
    def pollClientForRequest(self, clientID):
        # see if socket has anything to read
        clientConnection = self.activeClientConnections[clientID]
        packet = self.__nonBlockingRecieveFrom(clientConnection)

        if packet is None:
            return
        
        # first 8 Bytes is the PROTOCOL_HEADER
        # find the next 4 bytes of the packet determine the method type
        methodType = packet[8 : 12] #[8,11]
        
        packet = packet[12:] #[12,end]
        # call appropriate parser to parse packet return whatever the parser returns)
        match methodType:
            case "REGI":
                return self.__parseRegisterPacket(packet)
        
            case "LIST":
                return self.__parseListGames(packet)
        
            case "CREA":
                return self.__parseCreateGame(packet)
            
            case "JOIN":
                return self.__parseJoinGame(packet)

            case "EXIT":
                return self.__parseExitGame(packet)

            case "UNRG":
                return self.__parseUnregister(packet)

            case "GUEL":
                return self.__parseGuessLetter(packet)
            
            case "GUEW": ##optional
                return self.__parseGuessWord(packet)

            case "SLWD": 
                return self.__parseSelectWord(packet)

            case "AKGS": 
                return self.__parseAskGameState(packet)
                
            case "GTSB": ##optional
                return self.__parseSendScoreBoard(packet)
            
            case _:
                # error, invalid method type
                # NOTE: send a NACK of some kind
                self.__sendToSocket((self.PROTOCOL_HEADER + "40 " + "Invalid Method Type\n" + self.DELIM))
        #end of pollClientForRequest


    # send ACK for register (or NACK) 
    # registrationStatus is either OK or NO
    def sendRegistrationStatus(self, clientID, statusCode: str, statusMessage="OK"):
        packet = self.PROTOCOL_HEADER + statusCode + " " + statusMessage + "\n" + self.DELIM
        self.__sendToSocket(clientID, packet)
        # end sendRegistrationStatus

    # send game list
    def sendGameList(self, clientID, gameList):
        print("delete this later")
        # end sendGameList

    # send game id to ACK create/join game + who starts first 
    def sendGameInfoInit(self, clientID, intialGameState):
        print("delete this later")
        # end sendGameInfoInit

    # # send ACK for leaving game - Probably dont need these
    # def sendGameExit():

    #     #end processGameExit


    # # send ACK for unregistering


    # ACK letter guess give updated amount of word known
    def sendUpdatedGameData(self, clientID, currentWordData):
        print("delete this later")
        #end sendUpdatedGameData

    # ACK guess word (optional)


    # ACK word select (if it is accepted)
    def sendWordSelectionACK(self, clientID, wordOk):
        print("delete this later")
        #end sendWordSelectionACK


    # # initialize guesser (send initial word)
    # def initGuesser() # use sendUpdatedGameData


    # send game state (win,loss,InProgress,OtherPlayerQuit, points)
    def sendGameState(self, clientID, WoL, inProgress, points):
        print("delete this later")
        #end sendGameState

    # send scoreboard
    def sendScoreboard(self, clientID, scoreboard):
        print("delete this later")
        # end sendScoreboard

    #end HOAStryngS


    












    