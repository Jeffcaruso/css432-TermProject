import sys
from HOAStryngC import HOAStryngC


class hangmanClient:

    def __init__(self):
        self.net = HOAStryngC()
        #end init

        
    def client(self, serverName, serverPort):
        # Register
        print("*** Register ***")
        response = self.net.register(serverName, serverPort,"this is a great username")
        statusCode = response["Status Code"]
        print(statusCode)

        print("here HC - 5")

        print("*** Register ***")
        response = self.net.register(serverName, serverPort, "this is a great username")
        statusCode = response["Status Code"]
        print(statusCode)

        print("*** List Games ***")
        games = self.net.requestGamesList()
        statusCode = games["Status Code"]
        print(statusCode)
        gamesList = games["Data"]
        print(gamesList.items())
        #end 


        Info = self.net.createNewGame()
        print("Create Game:")
        print("GameID: " + str(Info["Data"]["GameID"]))
        print("AreGuesser: " + str(Info["Data"]["You Are Guesser"]))


        Info2 = self.net.joinGame(Info["Data"]["GameID"])
        print("Join Game:")
        print("status code: " + Info2["Status Code"])
        print("AreGuesser: " + str(Info2["Data"]["You Are Guesser"]))

        Info3 = self.net.exitGame()
        print("exit Game:")
        print("status code: " + Info3["Status Code"])


        Info4 = self.net.unregister()
        print("unregister:")
        print("Status code: " + Info4["Status Code"])
        



    
    #end hangman client



def main():
    args = sys.argv[1:]
    serverName = args[0]
    serverPort = int(args[1])

    client = hangmanClient()
    client.client(serverName, serverPort)
    #end main  
    
main()