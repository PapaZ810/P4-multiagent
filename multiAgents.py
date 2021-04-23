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
import random, util, distance

from game import Agent

class ReflexAgent(Agent):
    """
    A reflex agent chooses an action at each choice point by examining
    its alternatives via a state evaluation function.

    The code below is provided as a guide.  You are welcome to change
    it in any way you see fit, so long as you don't touch our method
    headers.
    """
    def __init__(self):
        self.dc = None

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
        currentPosition = currentGameState.getPacmanPosition()
        newPos = successorGameState.getPacmanPosition()
        newFood = successorGameState.getFood()
        newGhostStates = successorGameState.getGhostStates()
        newScaredTimes = [ghostState.scaredTimer for ghostState in newGhostStates]
        foodNum = currentGameState.getFood().count()

        if self.dc == None:
            self.dc = distance.Calculator(currentGameState.data.layout)

        # Example of how to use Distance Calculator to calculate useful information:
        # foodPositions = newFood.asList()
        # foodDistances = [self.dc.getDistance(newPos, foodPosition) for foodPosition in foodPositions]

        "*** YOUR CODE HERE ***"
        foodPositions = newFood.asList()

        
        if(len(foodPositions)) == foodNum:
            dis = 10000
            for food in foodPositions:
                if self.dc.getDistance(food, newPos) < dis:
                    dis = self.dc.getDistance(food, newPos)
        else:
            dis = 0
        for ghost in newGhostStates:
            dis += 4 ** (2-self.dc.getDistance(ghost.getPosition(), newPos))

        return -dis

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
        val, move = self.moveMax(gameState, 0)
        return move #I think this is giving pacman the wrong move
    
    def moveMin(self, gameState, ghostNum, depth):
        if gameState.isWin() or gameState.isLose():
            return self.evaluationFunction(gameState), None
        nextMoves = gameState.getLegalActions(ghostNum)
        chosenMove = None
        value = float("inf")
        if (ghostNum < gameState.getNumAgents() - 1):
            for action in nextMoves:
                val2, act2 = self.moveMin(gameState.generateSuccessor(ghostNum, action), ghostNum+1, depth)
                if val2 < value:
                    value, chosenMove = val2, action
            return value, chosenMove
        else:
            for action in nextMoves:
                val2, act2 = self.moveMax((gameState.generateSuccessor(ghostNum, action)), depth)
                if(val2 < value):
                    value, chosenMove = val2, action
            return value, chosenMove

    def moveMax(self, gameState, depth):
        if depth == self.depth or (len(gameState.getLegalActions(0))<1) or gameState.isWin() or gameState.isLose():
            return self.evaluationFunction(gameState), None
        depth = depth+1
        value = float("-inf")
        chosenMove = None
        nextMoves = gameState.getLegalActions(0)
        for action in nextMoves:
            val2, act2 = self.moveMin(gameState.generateSuccessor(0, action), 1, depth)
            if val2 > value:
                value, chosenMove = val2, action
        return value, chosenMove


class AlphaBetaAgent(MultiAgentSearchAgent):
    """
    Your minimax agent with alpha-beta pruning (question 3)
    """

    def getAction(self, gameState):
        """
        Returns the minimax action using self.depth and self.evaluationFunction
        """
        "*** YOUR CODE HERE ***"
        value, move = self.moveMax(gameState, 0, float("-inf"), float("inf"))
        return move
    
    def moveMax(self, gameState, depth, alpha, beta):
        if gameState.isLose() or gameState.isWin() or depth == self.depth or (len(gameState.getLegalActions(0))<1):
            return self.evaluationFunction(gameState), None
        depth=depth+1
        value = float("-inf")
        chosenMove = None
        nextMoves = gameState.getLegalActions(0)
        for action in nextMoves:
            val2, act2 = self.moveMin(gameState.generateSuccessor(0, action), depth, alpha, beta, 1)
            if val2 > value:
                value, chosenMove = val2, action
                alpha = max(alpha, value)
            if value >= beta:
                return value, chosenMove
        return value, chosenMove

    def moveMin(self, gameState, depth, alpha, beta, num):
        if gameState.isLose() or gameState.isWin():
            return self.evaluationFunction(gameState), None
        value = float("inf")
        chosenMove = None
        nextMoves = gameState.getLegalActions(num)
        if (num < gameState.getNumAgents() - 1):
            for action in nextMoves:
                val2, act2 = self.moveMin(gameState.generateSuccessor(num, action), depth, alpha, beta, num+1)
                if val2 < value:
                    value, chosenMove = val2, action
                    beta = min(beta, value)
                if value <= alpha:
                    return value, chosenMove
            return value, chosenMove
        else:
            for action in nextMoves:
                val2, act2 = self.moveMax(gameState.generateSuccessor(num, action), depth, alpha, beta)
                if val2 < value:
                    value, chosenMove = val2, action
                    beta = min(beta, value)
                if value <= alpha:
                    return value, chosenMove
            return value, chosenMove

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
        value, move = self.moveMax(gameState, 0)
        return move

    def moveMax(self, gameState, depth):
        if gameState.isLose() or gameState.isWin() or depth == self.depth or (len(gameState.getLegalActions(0))<1):
            return self.evaluationFunction(gameState), None
        v = float("-inf")
        chosenMove = None
        nextMoves = gameState.getLegalActions(0)
        for action in nextMoves:
            val2, act2 = self.moveExp(gameState.generateSuccessor(0, action), 1, depth+1)
            if val2 > v:
                v, chosenMove = val2, action
        return v, chosenMove

    def moveExp(self, gameState, num, depth):
        if gameState.isLose() or gameState.isWin():
            return self.evaluationFunction(gameState), None
        value = 0
        chosenMove = None
        nextMoves = gameState.getLegalActions(num)
        if (num < gameState.getNumAgents() - 1):
            for action in nextMoves:
                val2, act2 = self.moveExp(gameState.generateSuccessor(num, action), num+1, depth)
                p = 1.0/len(nextMoves)
                value += p * val2
            return value, chosenMove
        else:
            for action in nextMoves:
                val2, act2 = self.moveMax((gameState.generateSuccessor(num, action)), depth)
                p = 1.0/len(nextMoves)
            return value, chosenMove


def betterEvaluationFunction(currentGameState):
    """
    Your extreme ghost-hunting, pellet-nabbing, food-gobbling, unstoppable
    evaluation function (question 5).

    DESCRIPTION: <write something here so we know what you did>
    """
    "*** YOUR CODE HERE ***"
    util.raiseNotDefined()

# Abbreviation
better = betterEvaluationFunction
