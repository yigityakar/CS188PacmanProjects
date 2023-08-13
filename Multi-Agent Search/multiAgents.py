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
        oldGhostStates =currentGameState.getGhostStates()
        #print(newGhostStates[0].getPosition())
        newScaredTimes = [ghostState.scaredTimer for ghostState in newGhostStates]
        oldScaredTimes = [ghostState.scaredTimer for ghostState in oldGhostStates]
        #print(oldScaredTimes)
        "*** YOUR CODE HERE ***"
        food_val=0
        ghost_val=0
        penalty=0
        #print(newFood.asList())
        if newPos == currentGameState.getPacmanPosition():
            #very little penalty to avoid thrashing state
            penalty=-0.001
        
        if len(newFood.asList())!=0:
           
            for food in newFood.asList():
                food_val-= manhattanDistance(newPos,food)
            food_val=food_val/len(newFood.asList())
          
            if len(newFood.asList()) < len(currentGameState.getFood().asList()): #eating a food         
                food_val+=25
        else:
            if len(newFood.asList()) < len(currentGameState.getFood().asList()):
                     
                food_val+=99999  # eating last food to end the game is encouraged
      
          
        for i in range(0,len(newGhostStates)):
            if newPos==newGhostStates[i].getPosition():
                if newScaredTimes[i]>0:
                    print("ghost ate")
                    ghost_val +=10000
                else:
                    ghost_val -=10000
                    
           
            if newScaredTimes[i]>0:
                ghost_val -=manhattanDistance(newPos,newGhostStates[i].getPosition())  #scared ghosts could be closer
            else:
                ghost_val += manhattanDistance(newPos,newGhostStates[i].getPosition()) #regular ghosts should be further
        
        ghost_val=ghost_val/len(newGhostStates)
        if sum(newScaredTimes)> sum(oldScaredTimes): # if the pacman scared the ghosts
        
            ghost_val+=sum(newScaredTimes)/2
          
        return (ghost_val/100  + food_val/(100-len(newFood.asList()))) + penalty
       
    
        #return 0.75*ghost_val + 5*food_val/(1+len(newFood.asList()))
        #return 0.5*ghost_val + 5*food_val/(1+1.1*len(newFood.asList())) # returns a combination
        #return ghost_val/1000 + 1.25*food_val/(1000-len(newFood.asList()))
        #return successorGameState.getScore()

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
        #print(self.depth)
        v_list=[]
        agentCount=gameState.getNumAgents()
        
        for action in gameState.getLegalActions(0):
            suc=gameState.generateSuccessor(0, action)
            v_list.append(self.minmaxval(suc,1,agentCount-1,0))
     
       
        retAction= gameState.getLegalActions(0)[v_list.index(max(v_list))]     
        return retAction
        
        util.raiseNotDefined()
        
        
    def minmaxval(self,gameState,agent,agentcount,dep):
        
        
        if agent == agentcount+1:
            dep+=1
            if dep==self.depth:
                ret = self.evaluationFunction(gameState)
                #print(ret)
            else:     #MAX AGENT STEP
                ret=-99999999
                if len(gameState.getLegalActions(0))==0:
                    ret = self.evaluationFunction(gameState)
                else:
                    for action in gameState.getLegalActions(0):
                         suc=gameState.generateSuccessor(0, action)
                         #ab=self.minval(suc,1,agentcount,dep)
                         ret = max(ret,self.minmaxval(suc,1,agentcount,dep))
        else:
            ret = 99999999
            if len(gameState.getLegalActions(0))==0:
                ret = self.evaluationFunction(gameState)
            else:
                for action in gameState.getLegalActions(agent):                
                    ret = min(ret,self.minmaxval(gameState.generateSuccessor(agent, action) ,agent+1,agentcount,dep))  
        
        return ret

class AlphaBetaAgent(MultiAgentSearchAgent):
    """
    Your minimax agent with alpha-beta pruning (question 3)
    """
    
    def getAction(self, gameState):
        """
        Returns the minimax action using self.depth and self.evaluationFunction
        """
        "*** YOUR CODE HERE ***"
        v_list=[]
        agentCount=gameState.getNumAgents()
        alpha=-99999999
        beta=99999999
        for action in gameState.getLegalActions(0):
            suc=gameState.generateSuccessor(0, action)
            
            value=self.minmaxval(suc,1,agentCount-1,0,alpha,beta)
            v_list.append(value)
            alpha = max(alpha,value)
     
       
        retAction= gameState.getLegalActions(0)[v_list.index(max(v_list))]
        
        return retAction
        util.raiseNotDefined()
    def minmaxval(self,gameState,agent,agentcount,dep,alpha,beta):
        
        
            if agent == agentcount+1:
                dep+=1
                if dep==self.depth:
                    ret = self.evaluationFunction(gameState)
                    #print(ret)
                else:     #MAX AGENT STEP
                    ret=-99999999
                    if len(gameState.getLegalActions(0))==0:
                        ret = self.evaluationFunction(gameState)
                    else:
                        for action in gameState.getLegalActions(0):
                             suc=gameState.generateSuccessor(0, action)
                             
        
                             
                             #ab=self.minval(suc,1,agentcount,dep)
                             ret = max(ret,self.minmaxval(suc,1,agentcount,dep,alpha,beta))
                             if ret > beta:
                                  
                                  break
                             alpha=max(ret,alpha)
            else:
                ret = 99999999
                if len(gameState.getLegalActions(0))==0:
                    ret = self.evaluationFunction(gameState)
                else:
                    for action in gameState.getLegalActions(agent):                
                        ret = min(ret,self.minmaxval(gameState.generateSuccessor(agent, action) ,agent+1,agentcount,dep,alpha,beta))  
                        

                        if ret < alpha:
                            
                            break
                        beta = min(ret,beta)
            return ret

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
        v_list=[]
        agentCount=gameState.getNumAgents()
        
        for action in gameState.getLegalActions(0):
            suc=gameState.generateSuccessor(0, action)
            v_list.append(self.expmaxval(suc,1,agentCount-1,0))
     
       
        retAction= gameState.getLegalActions(0)[v_list.index(max(v_list))]     
        return retAction
    
    def expmaxval(self,gameState,agent,agentcount,dep):
        
        
        if agent == agentcount+1:
            dep+=1
            if dep==self.depth:
                ret = self.evaluationFunction(gameState)
                #print(ret)
            else:     #MAX AGENT STEP
                ret=-99999999
                if len(gameState.getLegalActions(0))==0:
                    ret = self.evaluationFunction(gameState)
                else:
                    for action in gameState.getLegalActions(0):
                         suc=gameState.generateSuccessor(0, action)
                         #ab=self.minval(suc,1,agentcount,dep)
                         ret = max(ret,self.expmaxval(suc,1,agentcount,dep))
        else:
            ret = 0
            if len(gameState.getLegalActions(0))==0:
                ret = self.evaluationFunction(gameState)
            else:
                for action in gameState.getLegalActions(agent):                
                    ret += self.expmaxval(gameState.generateSuccessor(agent, action) ,agent+1,agentcount,dep)
        
        return ret
    
        
        util.raiseNotDefined()

def betterEvaluationFunction(currentGameState):
    """
    Your extreme ghost-hunting, pellet-nabbing, food-gobbling, unstoppable
    evaluation function (question 5).

    DESCRIPTION: <write something here so we know what you did>
    """
    "*** YOUR CODE HERE ***"
    
    pos = currentGameState.getPacmanPosition()
    food = currentGameState.getFood()
    ghostStates = currentGameState.getGhostStates()
    #print(newGhostStates[0].getPosition())
    scaredTimes = [ghostState.scaredTimer for ghostState in ghostStates]
    food_val=0
    ghost_val=0
    cap_val=0
    minfooddist=999999
    cw=4
    sc=0.001
    #a=currentGameState.getCapsules()
   
   
   
    for i in food.asList():
        food_val+= manhattanDistance(pos,i)
        if manhattanDistance(pos,i) < minfooddist:
            minfooddist=manhattanDistance(pos,i)
 
    if len(food.asList())!=0:
        food_val = food_val/len(food.asList())
       
    
    for c in currentGameState.getCapsules():
        dis=manhattanDistance(c,pos)
        cap_val += dis
        
    if len(currentGameState.getCapsules())!=0:
        cap_val/len((currentGameState.getCapsules()))
    else:
        cw=0
    for g in range(0,len(ghostStates)):
        if scaredTimes[g]>0:
            
            continue
        else:
            ghost_val += manhattanDistance(ghostStates[g].getPosition(),pos)
            sc+=1/len(ghostStates)
    ghost_val = ghost_val/len(ghostStates)
   
   
    
   
    if len(food.asList())==0:
       ret = 10**10
   
    else:
        ret = 1/(food_val+0.001)  - sc/(ghost_val+0.001) +  cw/((len(currentGameState.getCapsules())+0.001)* (cap_val+0.001)) + 5/(len(food.asList()))
        ret -= len(currentGameState.getCapsules())*3
    #print(ret)
    return ret
    
    
    util.raiseNotDefined()

# Abbreviation
better = betterEvaluationFunction
