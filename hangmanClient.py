import sys
import HOAStryngC


class hangmanClient:

    def __init__(self, serverName, serverPort):
        
        net = HOAStryngC(serverName, serverPort)
        #end init

        


    def client(self):
        # Register
        response = self.net.register("this is a great username")
        statusCode = response["Status Code"]
        print(statusCode)
        #end 



    
    #end hangman client






def main():
    args = sys.argv[1:]
    serverName = args[0]
    serverPort = args[1]

    client = hangmanClient(serverName, serverPort)
    client()
    #end main  