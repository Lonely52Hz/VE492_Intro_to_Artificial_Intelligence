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
        score = successorGameState.getScore()
        foodPosition = newFood.asList()
        foodManhattan = []
        if len(foodPosition) != 0:
            for food in foodPosition:
                foodManhattan.append(manhattanDistance(food, newPos))
            score += 1 / (min(foodManhattan))
        ghostManhattan = []
        for ghost in newGhostStates:
            ghostManhattan.append(manhattanDistance(newPos, ghost.getPosition()))
        score -= 2 / (min(ghostManhattan) + 0.1)
        return score

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
        def minValue(gameState, depth, agentIndex):
            if gameState.isWin() or gameState.isLose() or depth == self.depth:
                return self.evaluationFunction(gameState)
            v = 1000000000000000
            for a in gameState.getLegalActions(agentIndex):
                if agentIndex == gameState.getNumAgents() - 1:
                    v = min(v, maxValue(gameState.generateSuccessor(agentIndex, a), depth + 1, 0))
                else:
                    v = min(v, minValue(gameState.generateSuccessor(agentIndex, a), depth, agentIndex + 1))
            return v
        
        def maxValue(gameState, depth, agentIndex):
            if gameState.isWin() or gameState.isLose() or depth == self.depth:
                return self.evaluationFunction(gameState)
            v = -1000000000000000
            for a in gameState.getLegalActions(agentIndex):
                v = max(v, minValue(gameState.generateSuccessor(agentIndex, a), depth, agentIndex + 1))
            return v
        
        v = -1000000000000000
        index = 0
        legalActionList = gameState.getLegalActions(0)
        for i in range(len(legalActionList)):
            t = minValue(gameState.generateSuccessor(0, legalActionList[i]), 0, 1)
            if t > v:
                v = t
                index = i
        return legalActionList[index]

class AlphaBetaAgent(MultiAgentSearchAgent):
    """
    Your minimax agent with alpha-beta pruning (question 3)
    """

    def getAction(self, gameState):
        """
        Returns the minimax action using self.depth and self.evaluationFunction
        """
        "*** YOUR CODE HERE ***"
        def minValue(gameState, depth, agentIndex, alpha, beta):
            if gameState.isWin() or gameState.isLose() or depth == self.depth:
                return self.evaluationFunction(gameState)
            v = 1000000000000000
            for a in gameState.getLegalActions(agentIndex):
                if agentIndex == gameState.getNumAgents() - 1:
                    v = min(v, maxValue(gameState.generateSuccessor(agentIndex, a), depth + 1, 0, alpha, beta))
                else:
                    v = min(v, minValue(gameState.generateSuccessor(agentIndex, a), depth, agentIndex + 1, alpha, beta))
                if v < alpha:
                    return v
                beta = min(beta, v)
            return v
        
        def maxValue(gameState, depth, agentIndex, alpha, beta):
            if gameState.isWin() or gameState.isLose() or depth == self.depth:
                return self.evaluationFunction(gameState)
            v = -1000000000000000
            for a in gameState.getLegalActions(agentIndex):
                v = max(v, minValue(gameState.generateSuccessor(agentIndex, a), depth, agentIndex + 1, alpha, beta))
                if v > beta:
                    return v
                alpha = max(alpha, v)
            return v
        
        v = -1000000000000000
        alpha = -1000000000000000
        index = 0
        legalActionList = gameState.getLegalActions(0)
        for i in range(len(legalActionList)):
            t = minValue(gameState.generateSuccessor(0, legalActionList[i]), 0, 1, alpha, 1000000000000000)
            if t > v:
                v = t
                index = i
            alpha = max(alpha, v)
        return legalActionList[index]

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
        def expValue(gameState, depth, agentIndex):
            if gameState.isWin() or gameState.isLose() or depth == self.depth:
                return self.evaluationFunction(gameState)
            v = 0
            Pr = 1 / len(gameState.getLegalActions(agentIndex))
            for a in gameState.getLegalActions(agentIndex):
                if agentIndex == gameState.getNumAgents() - 1:
                    v += Pr * maxValue(gameState.generateSuccessor(agentIndex, a), depth + 1, 0)
                else:
                    v += Pr * expValue(gameState.generateSuccessor(agentIndex, a), depth, agentIndex + 1)
            return v
        
        def maxValue(gameState, depth, agentIndex):
            if gameState.isWin() or gameState.isLose() or depth == self.depth:
                return self.evaluationFunction(gameState)
            v = -1000000000000000
            for a in gameState.getLegalActions(agentIndex):
                v = max(v, expValue(gameState.generateSuccessor(agentIndex, a), depth, agentIndex + 1))
            return v
        
        v = -1000000000000000
        index = 0
        legalActionList = gameState.getLegalActions(0)
        for i in range(len(legalActionList)):
            t = expValue(gameState.generateSuccessor(0, legalActionList[i]), 0, 1)
            if t > v:
                v = t
                index = i
        return legalActionList[index]

def betterEvaluationFunction(currentGameState):
    """
    Your extreme ghost-hunting, pellet-nabbing, food-gobbling, unstoppable
    evaluation function (question 5).

    DESCRIPTION: <write something here so we know what you did>
    A = 10 / the smallest manhattanDistance from pacman to food
    B = 100 / the smallest manhattanDistance from pacman to normal ghost
    C = 20 / the smallest manhattanDistance from pacman to scared ghost
    score = currentGameState.getSocre() + A - B + C
    """
    "*** YOUR CODE HERE ***"
    score = currentGameState.getScore()
    foodPosition = currentGameState.getFood().asList()
    pacmanPosition = currentGameState.getPacmanPosition()
    ghostState = currentGameState.getGhostStates()
    foodManhattan = []
    if len(foodPosition) != 0:
        for food in foodPosition:
            foodManhattan.append(manhattanDistance(food, pacmanPosition))
        score += 10 / (min(foodManhattan))
    ghostWeightedDistance = []
    ghostScaredDistance = []
    ghostWeightedDistance.append(0)
    ghostScaredDistance.append(0)
    for ghost in ghostState:
        distance = manhattanDistance(pacmanPosition, ghost.getPosition())
        if ghost.scaredTimer == 0:
            ghostWeightedDistance.append(100 / (distance + 0.1))
        else:
            ghostScaredDistance.append(20 / (distance + 0.1))
    score -= max(ghostWeightedDistance)
    score += max(ghostScaredDistance)
    return score

# Abbreviation
better = betterEvaluationFunction
