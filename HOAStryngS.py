from socket import *

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
    
    def __init__(self, serverPort):
        self.activeClientConnections = dict()
        self.__prepListener(serverPort)
        # end init

    # prep listener
    def __prepListener(self, serverPort):
        self.serverListenerSock = socket(AF_INET, SOCK_STREAM)
        self.serverListenerSock.bind(('', serverPort))
        #end prepListener

    def __sendToSocket(self, clientID, packet):
        # send the packet to the proper client connection
        self.activeClientConnections[clientID].send(packet)      
        #end of sendToSocket


    # methods to parse the different kinds of requests
    def __parseRegisterPacket(self, packet):

        # return tuple with first value being method type, and the rest being the parameters 
        # that the client sent with that method. 
        # end __parseRegisterPacket
    
    def __parseListGames(self, packet):
       
       # end __parseListGames


    def __parseCreateGame(self, packet):
        
        # end __parseCreateGame
      

    def __parseJoinGame(self, packet):
        
        # end __parseJoinGame


    def __parseUnregister(self, packet):
        
        # end __parseUnregister
    

    def __parseGuessLetter(self, packet):
        
        # end __parseGuessLetter


    def __parseGuessWord(self, packet):
        
        #end __parseGuessWord



    def __parseSelectWord(self, packet):
        
        #end __parseSelectWord
    


    def __parseInitGuesser(self, packet):
        
        #end __parseInitGuesser



    def __parseSendingGameState(self, packet):
        
        #end __parseInitGuesser


    def __parseSendScoreBoard(self, packet):

        #end __parseSendScoreBoard
    




    # poll for client request
    def pollClientForRequest(self, clientID):
        # see if socket has anything to read

        # read packet from client socket till we reach delimiter 
        
        # find the first 4 bytes of the packet determine the method type
        
        # call appropriate parser to parse packet

        # return tuple with first value being method type, and the rest being the parameters 
        # that the client sent with that method. (whatever the parser returns)
        if(regi)
        {
            return __parseRegisterPacket(packet)
        }
        #end of pollClientForRequest


    # send ACK for register (or NACK) 
    def sendRegistrationStatus(self, clientID, registrationStatus):
                
        # end sendRegistrationStatus

    # send game list
    def sendGameList(self, clientID, gameList):
        
        # end sendGameList

    # send game id to ACK create/join game + who starts first 
    def sendGameInfoInit(self, clientID, intialGameState):

        # end sendGameInfoInit

    # # send ACK for leaving game - Probably dont need these
    # def sendGameExit():

    #     #end processGameExit


    # # send ACK for unregistering


    # ACK letter guess give updated amount of word known
    def sendUpdatedGameData(self, clientID, currentWordData):

        #end sendUpdatedGameData

    # ACK guess word (optional)


    # ACK word select (if it is accepted)
    def sendWordSelectionACK(self, clientID, wordOk):

        #end sendWordSelectionACK


    # # initialize guesser (send initial word)
    # def initGuesser() # use sendUpdatedGameData


    # send game state (win,loss,InProgress,OtherPlayerQuit, points)
    def sendGameState(self, clientID, WoL, inProgress, points):
        
        #end sendGameState

    # send scoreboard
    def sendScoreboard(self, clientID, scoreboard):

        # end sendScoreboard

    #end HOAStryngS


    












    