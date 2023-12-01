# Term Project - Hangman

## Network library - hanging on a stryng

## How to Play
### Requirements
- Be on a linux machine with python 3.

### Game Client Instructions
1) Know what server you are connecting to (its hostname and port for the game), creating your own if necessary.
2) On your terminal, enter either. Note option a requires that the execute (x) attribute is enable for the start script
    1) ./startClient.sh
    2) python3 hangmanClient.py 
3) Use the start menu within the game to connect to a server
4) Use the main menu once connected to the server to play the game with you and a friend

#### Files needed for Game Client
- hangmanClient.py
- HOAStryngC.py
- game.py
- startClient.sh (if you want to use shell script to run)


### Game Server Instructions - if you cannot find an already active server
1) Identify the computer you are going to run the server app on to (its hostname, an acceptable port to host the game on)
2) On your terminal, enter either. Note option a requires that the execute (x) attribute is enable for the start script
    1) ./startServer.sh <port#>
    2) python3 hangmanServer.py <port#>
        - e.g., "python3 hangmanServer.py 1234" to have the server port of 1234

#### Files needed for Game Server
- hangmanServer.py
- HOAStryngS.py
- game.py
- scoreboard.json
- startServer.sh (if you want to use shell script to run)



## Documentation Links
- [Protocol Documentation](https://docs.google.com/document/d/1NuUj9wqFaEueTtUwdIeYir1m1rvpkxbhUfHKuwzdIfk/edit?usp=sharing)
- [Instructions Documentation](https://docs.google.com/document/d/1YsQWbQr7iAAnxoI-eDzS7lgPOox7n_Z11neOFjEYy0s/edit?usp=sharing)
