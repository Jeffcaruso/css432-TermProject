import sys
import time
from HOAStryngC import HOAStryngC
from termios import TCIFLUSH, TCOFLUSH, tcflush
import select

"""
Hangman - Term Project
with Hanging on a Stryng protocol
authors : Jeffrey Caruso, Cordelia Notbohm
date    : Fall 2023
file    : hangmanClient.py
class   : hangmanClient
"""

# A client program that talks to a hangman server
# to play a game of hangman
class hangmanClient:

    def __init__(self):
        self.net = HOAStryngC()
        self.registeredWithServer = False
        #end init


    # the main gameplay loops
    # that keep the program running as long as the client wants to play
    def client(self):
        # loop and keep showing the start menu till player decides to quit
        stillPlaying = True
        while stillPlaying:
            stillPlaying = self.startMenu()
        
            #loop and keep showing main menu till user decides to unregister 
            while stillPlaying and self.registeredWithServer :
                # if there are any exceptions/bugs that we did not 
                # manage to find elegant solutions to
                # then just unregister from the server and fail gracefully
                # returing to the start menu
                try:
                    self.mainMenu()
                except:
                    self.net.unregister()
                    self.registeredWithServer = False
                    print("Unexpected error: disconnected from server")
                    print()
        #end client


    # the start up menu that provides an option to register to a server
    def startMenu(self):
        # print main menu options 
        print("Welcome To Hangman")
        self.printHangmanDisplay(6)
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
        

    # asks for all connection info, and attepts to 
    # register with the client 
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

        except: #otherwise just return to start menu
            print("Could not connect to a server with that hostname/port")
            print()
        # end connectToAServer()


    # the main gameplay menu, with all the options to start up 
    # a game or get info from a particular server 
    def mainMenu(self):
        # print main menu 
        print("Select an option from this list (enter the #)")
        print("1 - Create a new Game")
        print("2 - Find a game to join (list games)")
        print("3 - Join an existing game")
        print("4 - See Scoreboard")
        print("5 - Disconnect from server (unregister)")

        # poll user for option 
        try:
            option = int(input("Enter option number: "))
            print()
        except:
            option = -1

        # act on option
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


    # gets all info needed to create a game and creates a game
    # if succesful starts waiting for another player to join 
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


    # gets the list of games from the server 
    # and prints it out nicely for the user
    # if successful
    def listGame(self):
        response = self.net.requestGamesList()
        statusCode = response["Status Code"]

        if(statusCode == "20"):
            gameList = response["Data"]
            print("Game List:")
            for gameInfo in gameList:
                print("Game ID: " +  str(gameInfo["gameID"]) + "\t" + "Players: " + str(gameInfo["usernames"]))
            print()
        else:
            print("unexpected error")
        #end list game


    # gets all the info needed to join a game and 
    # then attepts to join. if successful then 
    # start playing the game
    def joinGame(self):
        # get game id
        gameID = int(input("Enter gameID: "))
        print()

        # try to join
        response = self.net.joinGame(gameID)
        statusCode = response["Status Code"]
        
        # if success, play game 
        if statusCode == "20":
            print("Joined game " + str(gameID))
            IAmGuesser = response["Data"]["You Are Guesser"]
            self.playGame(IAmGuesser)
        else:
            print("could not join game " + str(gameID))
        #end joingame
    

    # waits fopr another player to join the game
    # giving the user an option to leave 
    # every once and a while
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
                # print options
                numWaitCyclesSinceChecked = 0
                print()
                print("Select an option from this list (enter the #)")
                print("1 - Keep Waiting")
                print("2 - Exit this game")
            
                # poll for option
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
                
                # act on option
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
    

    # Enter the correct client play function based on if
    # you were randomly selected to be the guesser or word selector
    def playGame(self, IAmGuesser):
        if(IAmGuesser):
            self.playGuesser()
        else:
            self.playSelector()
        #end playGame


    # play a game as a guesser
    def playGuesser(self):
        print("You are the Guesser!")
        print("Waiting for other player to enter a word for you to guess")
        
        numWaitCyclesSinceChecked = 0
        response = self.net.askGameState()
        while(response["Status Code"] != "20" or response["Data"]["Censored Word"] is None):
            #wait for the selector to select a word
            print("wait...")
            time.sleep(5)
            numWaitCyclesSinceChecked += 1
            
            # if they have been waiting a while give them a chance to leave
            # the game
            if (numWaitCyclesSinceChecked > 4):
                numWaitCyclesSinceChecked = 0
                # print options
                print()
                print("Select an option from this list (enter the #)")
                print("1 - Keep Waiting")
                print("2 - Exit this game")
            
                # poll for option
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
                
                # act on option
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
        
        # get game state variables
        numIncorrectGuesses = response["Data"]["Incorrect Guesses"]
        censoredWord = response["Data"]["Censored Word"]
        gameState = response["Data"]["Game State"]

        # while the game is in progess let the guesser guess 
        while gameState == "IN_PROGRESS":
            # print menu 
            self.printHangmanDisplay(numIncorrectGuesses)
            print(censoredWord)
            print()
            print("Select an option from this list (enter the #)")
            print("1 - Guess a Letter")
            print("2 - Exit this game")
            
            # poll for option
            try:
                option = int(input("Enter option number: "))
                print()
            except:
                option = -1

            # act on option
            if option == 1:
                # guess a letter 
                suppliedLetter = input("letter: ")
                suppliedLetter = suppliedLetter[0]
                response = self.net.guessLetter(suppliedLetter) 
                
                # update game state variables 
                oldNumIncorrectGuesses = numIncorrectGuesses
                numIncorrectGuesses = response["Data"]["Incorrect Guesses"]
                censoredWord = response["Data"]["Censored Word"]
                gameState = response["Data"]["Game State"]
                
                # print if the guess was correct
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
            # end while 

        # print out hangman one last time and if they won
        self.printHangmanDisplay(numIncorrectGuesses)
        print(censoredWord)
        print()

        if gameState == "WON":
            print("You Won!")
            time.sleep(2)            

        if gameState == "LOST":
            print("You lost")
            time.sleep(2)            

        # exit the game and return to main menu
        print("Exiting game")
        print()
        response = self.net.exitGame()
        #end playGuesser


    # play the game as a selector (If you were randomly chosen to be the selector)
    def playSelector(self):
        print("You are the Selector!")
        word = input("Enter a word for the other player to guess:")

        # have them select a wo
        response = self.net.selectWord(word)
        while(response["Status Code"] != "20"):
            # while it is not accepted try again
            word = input("Enter a word for the other player to guess:")
            response = self.net.selectWord(word)

        # get game state variables
        numIncorrectGuesses = response["Data"]["Incorrect Guesses"]
        censoredWord = response["Data"]["Censored Word"]
        gameState = response["Data"]["Game State"]
        lastGuess = response["Data"]["Last Guess"]
        numWaitCyclesSinceChecked = 0
        should_print_hangman = True

        # while the game is in progess 
        while gameState == "IN_PROGRESS":
            # if something has changed print out game state
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

            # if they have been waiting for a while
            if (numWaitCyclesSinceChecked > 10):
                #give them a chance to leave 
                # print options
                numWaitCyclesSinceChecked = 0
                print("Select an option from this List:")
                print("1 - Stay")
                print("2 - Exit this game")

                # poll for option
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

                # act on option
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

        # print state one last time
        print("Other Player Guessed: " + lastGuess)
        self.printHangmanDisplay(numIncorrectGuesses)
        print(censoredWord)
        print()

        # Win/lost in game state is based on if word was guessed. so for word selector, they are flipped.
        if gameState == "WON":
            print("You Lost")
            time.sleep(2)            

        if gameState == "LOST":
            print("You Won!")
            time.sleep(2)            
        
        # exit game and return to main menu
        print("Exiting game")
        print()
        response = self.net.exitGame()
        #end playSelector


    # prints the hangman display based on the number of 
    # incorrect guesses 
    # from 0 - no hangman
    # To 6 - full hangman (lost games)
    def printHangmanDisplay(self, numIncorrectGuesses):
        if numIncorrectGuesses > 6:
            numIncorrectGuesses = 6

        filepath = 'hangmanDisplay/' + str(numIncorrectGuesses) + 'IncorrectGuesses.txt'
        f = open(filepath, 'r')
        file_contents = f.read()
        print (file_contents)
        f.close()
        #end printHangmanDisplay


    # get the scoreboard from the server and display the scoreboard 
    # note, the users score is only saved to the SB once they unregister.
    def displayScoreboard(self):
        response = self.net.getScoreboard()
        data = response["Data"]
        yourScore = data["your score"]
        scoreboard = data["scoreboard"]
        
        print("Your current number of wins: " + str(yourScore))
        print("NOTE: Your score is only saved to the scoreboard when you unregister from the game")
        print()
        print("Current Scoreboard:")
        for score in scoreboard:
            print(score["username"].ljust(20) + "Wins: " + str(score["wins"]))        
        print()
        #end displayScoreboard

# start client app
def main():
    client = hangmanClient()
    client.client()
    #end main  

# start client app
if __name__ == "__main__":
    main()
