import sys
import time
from HOAStryngC import HOAStryngC
# Import the libraries inputimeout, TimeoutOccurred 
# from inputimeout import inputimeout # Import the libraries inputimeout, TimeoutOccurred 
# from inputimeout import inputimeout 
import select

class hangmanClient:

    def __init__(self):
        self.net = HOAStryngC()
        self.registeredWithServer = False
        #end init

    
    def client(self):
        # loop and keep showing the start menu till player decides to quit
        stillPlaying = True
        while stillPlaying:
            stillPlaying = self.startMenu()
        
            #loop and keep showing main menu till user decides to unregister 
            while stillPlaying and self.registeredWithServer :
                self.mainMenu()
        #end client


    def startMenu(self):
        # main menu options 
        print("Welcome To Hangman")
        self.printHangmanDisplay(0)
        print()
        print("Select an option from this list (enter the #)")
        print("1 - Join a Server (Register)")
        print("2 - Quit (Stop Playing)")
        
        # poll user for their choice  
        try:
            option = int(input("Enter option number: "))
            print()
        except:
            option = -1
        
        # act based on their choice 
        if option == 1:
            self.connectToAServer()
        elif option == 2:
            return False    
        else:
            print("Option not supported")
        return True
        #end startMenu 
        

    def connectToAServer(self):
        # get regisitration info from user 
        serverName = input("Enter server hostname: ")
        serverPort = -1
        while serverPort < 0: 
            try:
                serverPort = int(input("Enter server port: "))
            except:
                print("server port needs to be an number")
                
        userName = input("Enter your display name: ")
        print()

        # if we can connect to the server 
        try:
            # keep trying to register till the user enters a unique name
            response = self.net.register(serverName, serverPort, userName)
            statusCode = response["Status Code"]
            
            while(statusCode != "20"):
                print("Display name already taken")
                userName = input("Enter a new display name (up to 20 characters):")
                response = self.net.register(serverName, serverPort, userName)
                print()
                statusCode = response["Status Code"]
                #end while
                
            print("Registration Successful")
            print()   
            self.registeredWithServer = True
        except:
            print("Could not connect to a server with that hostname/port")
            print()
        # end connectToAServer()


    def mainMenu(self):
        print("Select an option from this list (enter the #)")
        print("1 - Create a new Game")
        print("2 - Find a game to join (list games)")
        print("3 - Join an existing game")
        print("4 - Disconnect from server (unregister)")

        try:
            option = int(input("Enter option number: "))
            print()
        except:
            option = -1

        if option == 1:
            self.createGame()
        elif option == 2:
            self.listGame()
        elif option == 3:
            self.joinGame()
        elif option == 4:
            self.net.unregister()
            self.registeredWithServer = False
        else:
            print("Option not supported")
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
        if(IAmGuesser):
            self.playGuesser()
        else:
            self.playSelector()
        #end playGame


    def playGuesser(self):
        print("Waiting for other player to enter a word for you to guess")
        
        numWaitCyclesSinceChecked = 0
        response = self.net.initGuesser()
        while(response["Status Code"] != "20"):
            #wait for the selector
            print("wait...")
            time.sleep(2.5)
            numWaitCyclesSinceChecked += 1
            
            # if they have been waiting a while give them a chance to leave
            # the game
            if (numWaitCyclesSinceChecked > 10):
                print("Select an option from this list (enter the #)")
                print("1 - Keep Waiting")
                print("2 - Exit this game")
            
                try:
                    option = int(input("Enter option number: "))
                    print()
                except:
                    option = -1
                
                if option == 1:
                    numWaitCyclesSinceChecked = 0
                elif option == 2:
                    return
                else:
                    print("Option not supported")
                
            response = self.net.initGuesser()     
        #end wait loop

        print(response)
        
        numIncorrectGuesses = response["Data"]["Incorrect Guesses"]
        censoredWord = response["Data"]["Censored Word"]
        gameState = response["Data"]["Game State"]

        #while True:
        while gameState == "IN_PROGRESS":
            self.printHangmanDisplay(numIncorrectGuesses)
            print(censoredWord)
            print()
            print("Select an option from this list (enter the #)")
            print("1 - Guess a Letter")
            print("2 - Exit this game")
            
            try:
                option = int(input("Enter option number: "))
                print()
            except:
                option = -1

            if option == 1:
                suppliedLetter = input("letter: ")
                response = self.net.guessLetter(suppliedLetter) 
                
                numIncorrectGuesses = response["Data"]["Incorrect Guesses"]
                censoredWord = response["Data"]["Censored Word"]
                gameState = response["Data"]["Game State"]
                
            elif option == 2:
                print("exiting")
                response = self.net.exitGame()
                return
            else:
                print("Option not supported")


        if gameState == "WON":
            print("You Won!")
            print()
            time.sleep(2)            
            response = self.net.exitGame()

        if gameState == "LOST":
            print("You lost")
            print()
            time.sleep(2)            
            response = self.net.exitGame()
        #end playGuesser
        #end playGuesser




    def playSelector(self):
        word = input("Enter a word for the other player to guess:")
        response = self.net.selectWord(word)
        while(response["Status Code"] != "20"):
            #try again
            print(response)
            word = input("Enter a word for the other player to guess:")
            response = self.net.selectWord(word)

        print(response)
        numIncorrectGuesses = response["Data"]["Incorrect Guesses"]
        censoredWord = response["Data"]["Censored Word"]
        gameState = response["Data"]["Game State"]
        numWaitCyclesSinceChecked = 0
        should_print_hangman = True

        while gameState == "IN_PROGRESS":
            # print out game state
            if (should_print_hangman):
                self.printHangmanDisplay(numIncorrectGuesses) 
                print(censoredWord)
                print()
            # save old g
            oldCensoredWord = censoredWord
            oldNumIncorrectGuesses = numIncorrectGuesses
            oldNumIncorrectGuesses = numIncorrectGuesses
            # wait a bit, then get updated game state
            time.sleep(2.5)
            response = self.net.askGameState()
            #
            numIncorrectGuesses = response["Data"]["Incorrect Guesses"]
            censoredWord = response["Data"]["Censored Word"]
            gameState = response["Data"]["Game State"]
            should_print_hangman = (oldCensoredWord != censoredWord) or (oldNumIncorrectGuesses != numIncorrectGuesses)

            if (numWaitCyclesSinceChecked > 10):
                #game menu
                print("Select an option from this List:")
                print("1 - Stay")
                print("2 - Exit this game")

                try:
                    print("Enter option number:")
                    option = select.select([sys.stdin], 2)
                    # option = int(input("Enter option number: "))
                    # print()
                except:
                    option = -1

                if option == 1:
                    print("Waiting for other Player")

                elif option == 2:
                    print("exiting")
                    response = self.net.exitGame()
                    return
                else:
                    print("Option not supported")

            
            
            #otherwise, stay, so do nothing

        if gameState == "WON":
            print("You Won!")
            print()
            time.sleep(2)            
            response = self.net.exitGame()

        if gameState == "LOST":
            print("You lost")
            print()
            time.sleep(2)            
            response = self.net.exitGame()

        #end playSelector




    def printHangmanDisplay(self, numIncorrectGuesses):
        if numIncorrectGuesses > 6:
            numIncorrectGuesses = 6

        filepath = 'hangmanDisplay/' + str(numIncorrectGuesses) + 'IncorrectGuesses.txt'
        f = open(filepath, 'r')
        file_contents = f.read()
        print (file_contents)
        f.close()
        #end printHangmanDisplay


def main():
    client = hangmanClient()
    client.client()
    #end main  


if __name__ == "__main__":
    main()






















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