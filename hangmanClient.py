import sys
import time
from HOAStryngC import HOAStryngC
from termios import TCIFLUSH, TCOFLUSH, tcflush
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
        print("4 - See Scoreboard")
        print("5 - Disconnect from server (unregister)")

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
            self.displayScoreboard()
        elif option == 5:
            self.net.unregister()
            self.registeredWithServer = False
        else:
            print("Option not supported")
        #end joinGame



    def createGame(self):
        response = self.net.createNewGame()
        statusCode = response["Status Code"]
        
        if statusCode == "20":
            print("Created game " + str(response["Data"]["GameID"]))
            IAmGuesser = response["Data"]["You Are Guesser"]
            if self.waitForAnotherPlayer():
                self.playGame(IAmGuesser)
            else:
                return
        else:
            print("could not create game")
        #end create game


    def listGame(self):
        response = self.net.requestGamesList()
        statusCode = response["Status Code"]

        if(statusCode == "20"):
            gameList = response["Data"]
            print("Game List:")
            for gameInfo in gameList:
                # str1 = ""
                # for x in gameInfo["usernames"]:
                #     str1 += x
                # str1.join(gameInfo["usernames"])
                print("Game ID: " +  str(gameInfo["gameID"]) + "\t" + "Players: " + str(gameInfo["usernames"]))
                #print(gameInfo)
            print()
        else:
            print("unexpected error")



        # response = self.net.getScoreboard()
        # data = response["Data"]
        # yourScore = data["your score"]
        # scoreboard = data["scoreboard"]
        
        # print("Your current number of wins: " + str(yourScore))
        # print("Current Scoreboard:")
        # for score in scoreboard:
        #     print(score["username"].ljust(20) + "Wins: " + str(score["wins"]))        
        # print()
        #end list game


    def joinGame(self):
        gameID = int(input("Enter gameID: "))
        print()
        response = self.net.joinGame(gameID)
        statusCode = response["Status Code"]
        
        if statusCode == "20":
            print("Joined game " + str(gameID))
            IAmGuesser = response["Data"]["You Are Guesser"]
            self.playGame(IAmGuesser)
        else:
            print("could not join game " + str(gameID))
        #end joingame
    
    
    def waitForAnotherPlayer(self):
        # check if the other player has joined yet
        print("Waiting for another player to join")
    
        numWaitCyclesSinceChecked = 0
        response = self.net.askGameState()
        
        while(response["Status Code"] != "20" or response["Data"]["Num Players"] < 2):
            # wait for another player
            print("wait...")
            time.sleep(5)
            numWaitCyclesSinceChecked += 1
            
            # if they have been waiting a while give them a chance to leave
            # the game
            if (numWaitCyclesSinceChecked > 4):
                numWaitCyclesSinceChecked = 0
                print()
                print("Select an option from this list (enter the #)")
                print("1 - Keep Waiting")
                print("2 - Exit this game")
            
                try:
                    print("Enter option number (you have 5 seconds):")
                    tcflush(sys.stdout, TCOFLUSH)
                    tcflush(sys.stdin, TCIFLUSH)
                    read, write, exc = select.select([sys.stdin], [], [], 5)

                    if (read):
                        option = sys.stdin.readline()
                        print()
                        option = int(option)
                    else:
                        option = 1

                except:
                    option = -1
                
                if option == 1:
                    print("Waiting for other Player")
                    print()
                elif option == 2:
                    print("exiting")
                    print()
                    response = self.net.exitGame()
                    return False
                else:
                    print("Option not supported")
                    print()
                
            response = self.net.askGameState()     
        #end wait loop
        
        print("Another player has joined!")
        return True
        #end waitForAnotherPlayer
    
    
    def playGame(self, IAmGuesser):
        if(IAmGuesser):
            self.playGuesser()
        else:
            self.playSelector()
        #end playGame


    def playGuesser(self):
        print("You are the Guesser!")
        print("Waiting for other player to enter a word for you to guess")
        
        numWaitCyclesSinceChecked = 0
        response = self.net.askGameState()
        while(response["Status Code"] != "20" or response["Data"]["Censored Word"] is None):
            #wait for the selector
            print("wait...")
            time.sleep(5)
            numWaitCyclesSinceChecked += 1
            
            # if they have been waiting a while give them a chance to leave
            # the game
            if (numWaitCyclesSinceChecked > 4):
                numWaitCyclesSinceChecked = 0
                print()
                print("Select an option from this list (enter the #)")
                print("1 - Keep Waiting")
                print("2 - Exit this game")
            
                try:
                    print("Enter option number (you have 5 seconds):")
                    tcflush(sys.stdout, TCOFLUSH)
                    tcflush(sys.stdin, TCIFLUSH)
                    read, write, exc = select.select([sys.stdin], [], [], 5)

                    if (read):
                        option = sys.stdin.readline()
                        print()
                        option = int(option)
                    else:
                        option = 1

                except:
                    option = -1
                
                if option == 1:
                    print("Waiting for other Player")
                    print()
                elif option == 2:
                    print("exiting")
                    print()
                    response = self.net.exitGame()
                    return
                else:
                    print("Option not supported")
                    print()
                
            response = self.net.askGameState()     
        #end wait loop
        
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
                suppliedLetter = suppliedLetter[0]
                response = self.net.guessLetter(suppliedLetter) 
                
                oldNumIncorrectGuesses = numIncorrectGuesses
                numIncorrectGuesses = response["Data"]["Incorrect Guesses"]
                censoredWord = response["Data"]["Censored Word"]
                gameState = response["Data"]["Game State"]
                
                if oldNumIncorrectGuesses == numIncorrectGuesses:
                    print("Good guess, " + suppliedLetter + " is in the word")
                else:
                    print("Nice try, but " + suppliedLetter + " is not in the word")
                    
            elif option == 2:
                print("exiting")
                response = self.net.exitGame()
                return
            else:
                print("Option not supported")

        self.printHangmanDisplay(numIncorrectGuesses)
        print(censoredWord)
        print()

        if gameState == "WON":
            print("You Won!")
            time.sleep(2)            

        if gameState == "LOST":
            print("You lost")
            time.sleep(2)            

        print("Exiting game")
        print()
        response = self.net.exitGame()
        #end playGuesser


    def playSelector(self):
        print("You are the Selector!")
        word = input("Enter a word for the other player to guess:")
        response = self.net.selectWord(word)
        while(response["Status Code"] != "20"):
            #try again
            word = input("Enter a word for the other player to guess:")
            response = self.net.selectWord(word)

        numIncorrectGuesses = response["Data"]["Incorrect Guesses"]
        censoredWord = response["Data"]["Censored Word"]
        gameState = response["Data"]["Game State"]
        lastGuess = response["Data"]["Last Guess"]
        numWaitCyclesSinceChecked = 0
        should_print_hangman = True

        while gameState == "IN_PROGRESS":
            # print out game state
            if (should_print_hangman):
                if lastGuess is not None:
                    print("Other player guessed: " + lastGuess)
                else:
                    print("Waiting for other player to guess")
                    
                self.printHangmanDisplay(numIncorrectGuesses) 
                print(censoredWord)
                print()

            # save old game state 
            oldCensoredWord = censoredWord
            oldNumIncorrectGuesses = numIncorrectGuesses

            # wait a bit, then get updated game state
            time.sleep(2.5)
            numWaitCyclesSinceChecked += 1
            
            response = self.net.askGameState()
            numIncorrectGuesses = response["Data"]["Incorrect Guesses"]
            censoredWord = response["Data"]["Censored Word"]
            gameState = response["Data"]["Game State"]
            lastGuess = response["Data"]["Last Guess"]

            # check if anything has changed 
            should_print_hangman = (oldCensoredWord != censoredWord) or (oldNumIncorrectGuesses != numIncorrectGuesses)

            if (numWaitCyclesSinceChecked > 10):
                #give them a chance to leave 
                numWaitCyclesSinceChecked = 0
                print("Select an option from this List:")
                print("1 - Stay")
                print("2 - Exit this game")

                try:
                    print("Enter option number (you have 5 seconds):")
                    tcflush(sys.stdout, TCOFLUSH)
                    tcflush(sys.stdin, TCIFLUSH)
                    read, write, exc = select.select([sys.stdin], [], [], 5)

                    if (read):
                        option = sys.stdin.readline()
                        print()
                        option = int(option)
                    else:
                        option = 1
                    
                except:
                    option = -1

                if option == 1:
                    print("Waiting for other Player")
                    print()
                elif option == 2:
                    print("exiting")
                    print()
                    response = self.net.exitGame()
                    return
                else:
                    print("Option not supported")
                    print()
                    #effect is waiting
            #otherwise, stay, so do nothing
            #end of while

        print("Other Player Guessed: " + lastGuess)
        self.printHangmanDisplay(numIncorrectGuesses)
        print(censoredWord)
        print()

        #NOTE: win/lost in game state is based on if word was guessed. so for word selector, they are flipped.
        if gameState == "WON":
            print("You Lost")
            time.sleep(2)            

        if gameState == "LOST":
            print("You Won!")
            time.sleep(2)            
        
        print("Exiting game")
        print()
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


    def displayScoreboard(self):
        # https://stackoverflow.com/questions/17330139/python-printing-a-dictionary-as-a-horizontal-table-with-headers 
        response = self.net.getScoreboard()
        data = response["Data"]
        yourScore = data["your score"]
        scoreboard = data["scoreboard"]
        
        print("Your current number of wins: " + str(yourScore))
        print("Current Scoreboard:")
        for score in scoreboard:
            print(score["username"].ljust(20) + "Wins: " + str(score["wins"]))        
        print()

        #end displayScoreboard


def main():
    client = hangmanClient()
    client.client()
    #end main  


if __name__ == "__main__":
    main()
