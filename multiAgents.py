# multiAgents.py
# --------------
# Licensing Information:  You are free to use or extend these projects for
# educational purposes provided that (1) you do not distribute or publish
# solutions, (2) you retain this notice, and (3) you provide clear
# attribution to UC Berkeley, including a link to http://ai.berkeley.edu.
# 
# Attribution Information: The Pacman AI projects were developed at UC Berkeley.
# The core projects and autograders were primarily created by John DeNero
# (denero@cs.berkeley.edu) and Dan Klein (klein@cs.berkeley.edu).
# Student side autograding was added by Brad Miller, Nick Hay, and
# Pieter Abbeel (pabbeel@cs.berkeley.edu).


from util import manhattanDistance
from game import Directions
import random, util

from game import Agent

class ReflexAgent(Agent):
    """
    A reflex agent chooses an action at each choice point by examining
    its alternatives via a state evaluation function.

    The code below is provided as a guide.  You are welcome to change
    it in any way you see fit, so long as you don't touch our method
    headers.
    """


    def getAction(self, gameState):
        """
        You do not need to change this method, but you're welcome to.

        getAction chooses among the best options according to the evaluation function.

        Just like in the previous project, getAction takes a GameState and returns
        some Directions.X for some X in the set {NORTH, SOUTH, WEST, EAST, STOP}
        """
        # Collect legal moves and successor states
        legalMoves = gameState.getLegalActions()

        # Choose one of the best actions
        scores = [self.evaluationFunction(gameState, action) for action in legalMoves]
        bestScore = max(scores)
        bestIndices = [index for index in range(len(scores)) if scores[index] == bestScore]
        chosenIndex = random.choice(bestIndices) # Pick randomly among the best

        "Add more of your code here if you want to"
        return legalMoves[chosenIndex]

    def evaluationFunction(self, currentGameState, action):
        """
        Design a better evaluation function here.

        The evaluation function takes in the current and proposed successor
        GameStates (pacman.py) and returns a number, where higher numbers are better.

        The code below extracts some useful information from the state, like the
        remaining food (newFood) and Pacman position after moving (newPos).
        newScaredTimes holds the number of moves that each ghost will remain
        scared because of Pacman having eaten a power pellet.

        Print out these variables to see what you're getting, then combine them
        to create a masterful evaluation function.
        """
        # Useful information you can extract from a GameState (pacman.py)
        successorGameState = currentGameState.generatePacmanSuccessor(action)
        newPos = successorGameState.getPacmanPosition()
        newFood = successorGameState.getFood()
        newGhostStates = successorGameState.getGhostStates()
        newScaredTimes = [ghostState.scaredTimer for ghostState in newGhostStates]

        "*** YOUR CODE HERE ***"
        #making sure that Pacman doesn't stop
        if(action == 'Stop'): 
            return -100

        availableFood = newFood.asList() #getting the food that is avaliable in the grid

        bestDistanceYet = 9999
        for food in availableFood:
            if(bestDistanceYet > manhattanDistance(newPos, food)):
                bestDistanceYet = manhattanDistance(newPos, food)
            #end of loop


       # closeGhost = 9999
        ghostDistances = 1
        for ghost in newGhostStates:
            # find summation ghost distances
            ghostDistances += manhattanDistance(newPos, ghost.getPosition()) 

                                                  # 2/float(bestdist)   - 10/float(ghost distance)?
        return successorGameState.getScore() + 1/float (bestDistanceYet)  - 1/float(ghostDistances)


def scoreEvaluationFunction(currentGameState):
    """
    This default evaluation function just returns the score of the state.
    The score is the same one displayed in the Pacman GUI.

    This evaluation function is meant for use with adversarial search agents
    (not reflex agents).
    """
    return currentGameState.getScore()

class MultiAgentSearchAgent(Agent):
    """
    This class provides some common elements to all of your
    multi-agent searchers.  Any methods defined here will be available
    to the MinimaxPacmanAgent, AlphaBetaPacmanAgent & ExpectimaxPacmanAgent.

    You *do not* need to make any changes here, but you can if you want to
    add functionality to all your adversarial search agents.  Please do not
    remove anything, however.

    Note: this is an abstract class: one that should not be instantiated.  It's
    only partially specified, and designed to be extended.  Agent (game.py)
    is another abstract class.
    """

    def __init__(self, evalFn = 'scoreEvaluationFunction', depth = '2'):
        self.index = 0 # Pacman is always agent index 0
        self.evaluationFunction = util.lookup(evalFn, globals())
        self.depth = int(depth)

class MinimaxAgent(MultiAgentSearchAgent):
    """
    Your minimax agent (question 2)
    """

    def getAction(self, gameState):
        """
        Returns the minimax action from the current gameState using self.depth
        and self.evaluationFunction.

        Here are some method calls that might be useful when implementing minimax.

        gameState.getLegalActions(agentIndex):
        Returns a list of legal actions for an agent
        agentIndex=0 means Pacman, ghosts are >= 1

        gameState.generateSuccessor(agentIndex, action):
        Returns the successor game state after an agent takes an action

        gameState.getNumAgents():
        Returns the total number of agents in the game

        gameState.isWin():
        Returns whether or not the game state is a winning state

        gameState.isLose():
        Returns whether or not the game state is a losing state
        """
        "*** YOUR CODE HERE ***"
       

        ##should probably change numAgents to numGhosts, which is what this is really recieving...
        def maximize(gameState, depth, numAgents):            
            #print('maximize')
            # won/lost return self.evaluationFunction(gameState)
            if(gameState.isWin() | gameState.isLose()):
                return self.evaluationFunction(gameState)
            
            #maximum value
            maximum = -99999
            #best(max) action
            actionToTake = Directions.STOP
            
            for action in gameState.getLegalActions(0):
                #next state is successor doing action
                succ = gameState.generateSuccessor(0,action)
                #utility (informed by what minimizing agents would do)
                utility = minimize(succ, depth, 1, numAgents)
                # if utililty is the best option yet
                if utility > maximum: 
                    #update max possible utility
                    maximum = utility
                    #save best action to take
                    actionToTake = action            
           
            # finishing out (depth check, returning...) 
            if(depth > 1):
                return maximum            
            
            return actionToTake
            # end of maximize....................


        def minimize(gameState, depth, agentIndex, numGhosts):
            #print('minimize')

            # won/lost return self.evaluationFunction(gameState)
            if(gameState.isWin() | gameState.isLose()):
                return self.evaluationFunction(gameState)

            #Useful values
            #value of minimizing option
            minimumValue = 99999
            # legal moves
            legalActions = gameState.getLegalActions(agentIndex)
            # positions from legal moves
            newPositions = []
            for action in legalActions:
                # new positions are the successors of current position and legal actions
                newPositions.append(gameState.generateSuccessor(agentIndex, action))

            # if are on the last ghost at this depth...
            if(agentIndex == numGhosts):
                if depth < self.depth:
                    # can go deeper
                    for newPos in newPositions:
                        #minimum value is the most minimizing action at this depth among all agents at bext depth.
                        minimumValue = min(minimumValue, maximize(newPos, depth + 1, numGhosts))
                else:
                    for newPos in newPositions:
                        #minimum value is the most minimizing action at this depth among all agents.
                        minimumValue = min(minimumValue, self.evaluationFunction(newPos)) 
                #end of if
            else:
                #aren't on last ghost at this depth
                for newPos in newPositions:
                    # minimum value is the most minimizing action at this depth among all agents.
                    minimumValue = min(minimumValue,minimize(newPos, depth, agentIndex + 1, numGhosts))

            # returning minimum value at this depth
            return minimumValue
            #end of minimize.....................

        # 'main' funtion items...
        # number of agents
        numGhosts = gameState.getNumAgents() -1      
        # call and return result from maximize
        return maximize(gameState, 1, numGhosts)
        ## end of minima

class AlphaBetaAgent(MultiAgentSearchAgent):
    """
    Your minimax agent with alpha-beta pruning (question 3)
    """

    def getAction(self, gameState):
        """
        Returns the minimax action using self.depth and self.evaluationFunction
        """
        "*** YOUR CODE HERE ***"
        #might have to pass
        def maximize(gameState, depth, numAgents,alpha,beta):            
        #print('maximize')
        # won/lost return self.evaluationFunction(gameState)
            if(gameState.isWin() | gameState.isLose()):
                return self.evaluationFunction(gameState)

            #maximum value
            maximum = -99999
            #best(max) action
            actionToTake = Directions.STOP
            
            for action in gameState.getLegalActions(0):
                #next state is successor doing action
                succ = gameState.generateSuccessor(0,action)
                #utility (informed by what minimizing agents would do)
                utility = minimize(succ, depth, 1, numAgents,alpha,beta)
                # if utililty is the best option yet
                if utility > maximum: 
                    #update max possible utility
                    maximum = utility
                    #save best action to take
                    actionToTake = action          

                #returning best max for pruning
                if maximum > beta:
                    return maximum
                
                #get new largest alpha 
                alpha = max(alpha,maximum)               
                
            # finishing out (depth check, returning...) 
            if(depth > 1):
                return maximum            
            
            return actionToTake
            # end of maximize....................


        def minimize(gameState, depth, agentIndex, numGhosts,alpha,beta):
            #print('minimize')

            # won/lost return self.evaluationFunction(gameState)
            if(gameState.isWin() | gameState.isLose()):
                return self.evaluationFunction(gameState)

            #value of minimizing option
            minimumValue = 99999

            for action in gameState.getLegalActions(agentIndex):
                #next state is successor doing action
                succ = gameState.generateSuccessor(agentIndex,action)
                
                #if on last ghost
                if(agentIndex == numGhosts):
                    if depth < self.depth:
                        #minimum value is the most minimizing action at this depth among all agents at next depth.
                        minimumValue = min(minimumValue, maximize(succ, depth + 1, numGhosts,alpha,beta))  
                    else:
                        #minimum value is the most minimizing action at this depth among all agents.
                        minimumValue = min(minimumValue, self.evaluationFunction(succ))    
                else:
                    # aren't on last ghost at this depth
                    # minimum value is the most minimizing action at this depth among all agents.
                    minimumValue = min(minimumValue,minimize(succ, depth, agentIndex + 1, numGhosts,alpha,beta))
                
                #get new min beta 
                beta = min(beta,minimumValue)
                
                #pruning 
                if minimumValue < alpha:   
                    return minimumValue            
                #end of loop...
                     
            # returning minimum value at this depth
            return minimumValue
            #end of minimize.....................

            

        # 'main' funtion items...
        #alpha
        alpha = -99999
        #beta
        beta  = 99999
        # number of agents
        numGhosts = gameState.getNumAgents() -1      
        # call and return result from maximize
        return maximize(gameState, 1, numGhosts,alpha,beta)
    #END OF A-B Pruning

class ExpectimaxAgent(MultiAgentSearchAgent):
    """
      Your expectimax agent (question 4)
    """
    
    def getAction(self, gameState):
        """
        Returns the expectimax action using self.depth and self.evaluationFunction

        All ghosts should be modeled as choosing uniformly at random from their
        legal moves.
        """
        "*** YOUR CODE HERE ***"
        #might have to pass
        def maximize(gameState, depth, numAgents):            
        #print('maximize')
        # won/lost return self.evaluationFunction(gameState)
            if(gameState.isWin() | gameState.isLose()):
                return self.evaluationFunction(gameState)

            #maximum value
            maximum = -99999
            #best(max) action
            actionToTake = Directions.STOP
            
            for action in gameState.getLegalActions(0):
                #next state is successor doing action
                succ = gameState.generateSuccessor(0,action)
                #utility (informed by what minimizing agents would do)
                utility = expValue(succ, depth, 1, numAgents)
                # if utililty is the best option yet
                if utility > maximum: 
                    #update max possible utility
                    maximum = utility
                    #save best action to take
                    actionToTake = action          

            # finishing out (depth check, returning...) 
            if(depth > 1):
                return maximum            
            
            return actionToTake
            # end of maximize....................


        def expValue(gameState, depth, agentIndex, numGhosts):
            #print('minimize')

            # won/lost return self.evaluationFunction(gameState)
            if(gameState.isWin() | gameState.isLose()):
                return self.evaluationFunction(gameState)

            #starting value of expectimax option
            expResults = 0
            
            for action in gameState.getLegalActions(agentIndex):
                #probablity of one action
                p = 1.0 / float(len(gameState.getLegalActions(agentIndex)))
                #next state is successor doing action
                succ = gameState.generateSuccessor(agentIndex,action)
                #if on last ghost
                if(agentIndex == numGhosts):
                    if depth < self.depth:
                        #expectimax value is the most expectimaxing action at this depth among all agents at next depth.
                        expResults += p * maximize(succ, depth + 1, numGhosts)
                    else:
                        #expectimax value is the most expectimaxing action at this depth among all agents.
                        expResults += p * self.evaluationFunction(succ)

                else:
                    # aren't on last ghost at this depth
                    # expectimax value is the most expectimaxing action at this depth among all agents.
                    expResults += p * expValue(succ, depth, agentIndex + 1, numGhosts)
                     
            # returning expectimax value at this depth
            return expResults
            #end of expValue.....................
            

        # 'main' funtion items...
        # number of agents
        numGhosts = gameState.getNumAgents() -1      
        # call and return result from maximize
        return maximize(gameState, 1, numGhosts)
    # end of Q4
    

def betterEvaluationFunction(currentGameState):
    """
    Your extreme ghost-hunting, pellet-nabbing, food-gobbling, unstoppable
    evaluation function (question 5).

    DESCRIPTION: <write something here so we know what you did>
    """
    "*** YOUR CODE HERE ***"
 
    newPos = currentGameState.getPacmanPosition()
    newFood = currentGameState.getFood()
    newGhostStates = currentGameState.getGhostStates()

    availableFood = newFood.asList() #getting the food that is avaliable in the grid

    #desiring food
    bestDistanceYet = 9999
    for food in availableFood:
        if(bestDistanceYet > manhattanDistance(newPos, food)):
            bestDistanceYet = manhattanDistance(newPos, food)
        #end of loop

    # avoiding ghosts under normal conditions
    ghostDistances = 1
    for ghost in newGhostStates:
        # find summation ghost distances
        ghostDistances += manhattanDistance(newPos, ghost.getPosition())

    #scared ghost modifier (override avoiding ghosts!)
    scaredGhostNum = 0 
    for ghostState in newGhostStates:
        #if ghost still has time sacred 
        if ghostState.scaredTimer > 0:
            scaredGhostNum += 1
    # make scared ghosts value negative, so it flips the avoiding ghosts policy
    # make it * -5 so it strongly chases ghosts
    scaredGhostNum *= -5
    
    return currentGameState.getScore() + (1/float (bestDistanceYet))  - (1/float(ghostDistances) * scaredGhostNum)
    #end of Q6 better evaluation function...

# Abbreviation
better = betterEvaluationFunction
