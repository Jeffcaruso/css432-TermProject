import sys
from HOAStryngC import HOAStryngC


class hangmanClient:

    def __init__(self):
        self.net = HOAStryngC()
        #end init

    


    def client(self):
        #def client(self, serverName, serverPort):
        
        # Phase 1 : Join/Create, (all before first guess)
        self.setup()
        

        while self.mainMenu():
            loop = "forever"

        # Phase 2: actually playing the game.


        
        # Phase 3: Catching player at end of game.
        
             



        self.net.unregister()
        #end client


    def setup(self):
        # Register
        print("*** Register ***")
        serverName = input("Enter server hostname: ")
        serverPort = int(input("Enter server port: "))
        userName = input("Enter your userName: ")


        response = self.net.register(serverName, serverPort, userName)
        statusCode = response["Status Code"]
        #NOTE: ask if it is fine to crash when invalid port/server name is given
        print(statusCode)

        print("MADE IT HERE - 5")

        while(statusCode != "20"):
            print("MADE IT HERE - 7")
            print("Enter a unique username (up to 20 characters)")
            response = self.net.register(serverName, serverPort, userName)
            statusCode = response["Status Code"]
            #end while

        print("MADE IT HERE - 10")
        # end setup()


    def mainMenu(self):
        print("Select an option from this list (enter the #)")
        print("1 - Create a new Game")
        print("2 - Find a game to join (list games)")
        print("3 - Join an existing game")
        print("4 - Disconnect from server (unregister)")

        try:
            option = int(input("Enter option number: "))
        except:
            option = -1

        if option == 1:
            self.createGame()
        elif option == 2:
            self.listGame()
        elif option == 3:
            self.joinGame()
        elif option == 4:
            return False
        else:
            print("you done goofed, try again")

        return True
        #end joinGame



    def createGame(self):
        response = self.net.createNewGame()
        statusCode = response["Status Code"]
        
        
        if statusCode == "20":
            IAmGuesser = response["Data"]["You Are Guesser"]
            self.playGame(IAmGuesser)
        else:
            print("could not create game")
        #end create game


    def listGame(self):
        response = self.net.requestGamesList()
        statusCode = response["Status Code"]

        if(statusCode == "20"):
            gameList = response["Data"]
            for gameInfo in gameList:
                print(gameInfo)

        else:
            print("unexpected error")
        #end list game


    def joinGame(self):
        gameID = int(input("Enter gameID: "))
        response = self.net.joinGame(gameID)
        statusCode = response["Status Code"]
        
        if statusCode == "20":
            IAmGuesser = response["Data"]["You Are Guesser"]
            self.playGame(IAmGuesser)
        else:
            print("could not join game " + str(gameID))
        #end joingame
    
    
    def playGame(self, IAmGuesser):


        print("Playing the game")
        #end playGame



def main():
    client = hangmanClient()
    client.client()
    #end main  

main()
#do NOT remove the main() in the line above






















# # Register
#         print("*** Register ***")
#         response = self.net.register(serverName, serverPort,"this is a great username")
#         statusCode = response["Status Code"]
#         print(statusCode)

#         print("here HC - 5")

#         print("*** Register ***")
#         response = self.net.register(serverName, serverPort, "this is a great username")
#         statusCode = response["Status Code"]
#         print(statusCode)

#         print("*** List Games ***")
#         games = self.net.requestGamesList()
#         statusCode = games["Status Code"]
#         print(statusCode)
#         gamesList = games["Data"]
#         print(gamesList.items())
#         #end 


#         Info = self.net.createNewGame()
#         print("Create Game:")
#         print("GameID: " + str(Info["Data"]["GameID"]))
#         print("AreGuesser: " + str(Info["Data"]["You Are Guesser"]))


#         Info2 = self.net.joinGame(Info["Data"]["GameID"])
#         print("Join Game:")
#         print("status code: " + Info2["Status Code"])
#         print("AreGuesser: " + str(Info2["Data"]["You Are Guesser"]))

#         Info3 = self.net.exitGame()
#         print("exit Game:")
#         print("status code: " + Info3["Status Code"])


#         Info4 = self.net.unregister()
#         print("unregister:")
#         print("Status code: " + Info4["Status Code"])