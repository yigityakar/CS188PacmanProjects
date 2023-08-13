# search.py
# ---------
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


"""
In search.py, you will implement generic search algorithms which are called by
Pacman agents (in searchAgents.py).
"""

import util
class SearchProblem:
    """
    This class outlines the structure of a search problem, but doesn't implement
    any of the methods (in object-oriented terminology: an abstract class).

    You do not need to change anything in this class, ever.
    """

    def getStartState(self):
        """
        Returns the start state for the search problem.
        """
        util.raiseNotDefined()

    def isGoalState(self, state):
        """
          state: Search state

        Returns True if and only if the state is a valid goal state.
        """
        util.raiseNotDefined()

    def getSuccessors(self, state):
        """
          state: Search state

        For a given state, this should return a list of triples, (successor,
        action, stepCost), where 'successor' is a successor to the current
        state, 'action' is the action required to get there, and 'stepCost' is
        the incremental cost of expanding to that successor.
        """
        util.raiseNotDefined()

    def getCostOfActions(self, actions):
        """
         actions: A list of actions to take

        This method returns the total cost of a particular sequence of actions.
        The sequence must be composed of legal moves.
        """
        util.raiseNotDefined()


def tinyMazeSearch(problem):
    """
    Returns a sequence of moves that solves tinyMaze.  For any other maze, the
    sequence of moves will be incorrect, so only use this for tinyMaze.
    """
    from game import Directions
    s = Directions.SOUTH
    w = Directions.WEST
    return  [s, s, w, s, w, w, s, w]

def depthFirstSearch(problem):
    from util import Stack
    """
    Search the deepest nodes in the search tree first.

    Your search algorithm needs to return a list of actions that reaches the
    goal. Make sure to implement a graph search algorithm.

    To get started, you might want to try some of these simple commands to
    understand the search problem that is being passed in:

  
    """
    "*** YOUR CODE HERE ***"
    #print("Start:", problem.getStartState())
    #print("Is the start a goal?", problem.isGoalState(problem.getStartState()))
    #print("Start's successors:", problem.getSuccessors(problem.getStartState()))
   
    state=problem.getStartState()
  
    s = Stack()   #state stack
    s.push(state)
    visit=[]      #visited list
    #visit.append(state)
    moves=Stack() #moves list
    loop = True

    moves.push([])
    while loop==True:

      
        state=s.pop()
        visit.append(state)
        qt= moves.pop()
  
        if problem.isGoalState(state):

            break
        else:
            successors=problem.getSuccessors(state)
            if len(successors)!=0: 
                hh=qt.copy()
                for successor in successors:
                    if successor[0] not in visit:
                        s.push(successor[0])
                        ss=successor[1]   
                        hh.append(ss)

                        moves.push(hh)  
                        hh=qt.copy()

    return qt
    
    util.raiseNotDefined()

def breadthFirstSearch(problem):
    from util import Queue
    state=problem.getStartState()
    q=Queue()
    q.push(state)
    visit=[] #visited list
    queued_list=[]
             
    #visit.append(state)
    moves=Queue() #moves list
    loop = True

    moves.push([])
    while q.isEmpty()!=True:
        
      
        state=q.pop()
        visit.append(state)
        qt= moves.pop()
        #print("st: ",state)
        if problem.isGoalState(state):
            #print("goal reached")
            break
        else:
            successors=problem.getSuccessors(state)
            if len(successors)!=0: 
                hh=qt.copy()
                for successor in successors:
                    #print("succs",successor[0])
                    if successor[0] not in visit and successor[0] not in queued_list:
                        
                        q.push(successor[0])
                        queued_list.append(successor[0])
                        ss=successor[1]   
                        hh.append(ss)

                        moves.push(hh)  
                        hh=qt.copy()

    return qt
        
        
    
    
    """Search the shallowest nodes in the search tree first."""
    "*** YOUR CODE HERE ***"
def uniformCostSearch(problem):
    """Search the node of least total cost first."""
    
    from util import PriorityQueue
    state=problem.getStartState()
    q=PriorityQueue()
    q.push(state,0)
    visit=[] #visited list
    queued_list=[]
             
    #visit.append(state)
    moves=PriorityQueue() #moves list
    loop = True

    moves.push([],0)
    while loop==True:

      
        state=q.pop()
        qt= moves.pop()
        cost = problem.getCostOfActions(qt)
        if state not in visit:
                
            visit.append(state)
            
            if problem.isGoalState(state):
        
                break
            else:
                successors=problem.getSuccessors(state)
                if len(successors)!=0: 
                    hh=qt.copy()
                    for successor in successors:
                        if successor[0] not in visit:
                            q.push(successor[0],cost+successor[2])
                            #queued_list.append(successor[0])
                            ss=successor[1]   
                            hh.append(ss)
                            moves.push(hh,cost+successor[2])  
                            hh=qt.copy()

    return qt
    "*** YOUR CODE HERE ***"
    util.raiseNotDefined()

def nullHeuristic(state, problem=None):
    """
    A heuristic function estimates the cost from the current state to the nearest
    goal in the provided SearchProblem.  This heuristic is trivial.
    """
    return 0

def aStarSearch(problem, heuristic=nullHeuristic):
    """Search the node that has the lowest combined cost and heuristic first."""
    "*** YOUR CODE HERE ***"
    from util import PriorityQueue
    state=problem.getStartState()
    q=PriorityQueue()
    q.push(state,0)
    visit=[] #visited list
    queued_list=[]
             
    #visit.append(state)
    moves=PriorityQueue() #moves list
    loop = True
    a=0
    moves.push([],0)
    while loop==True:

      
        state=q.pop()
        qt= moves.pop()
        cost = problem.getCostOfActions(qt)
        if state not in visit:
                
            visit.append(state)
            
            if problem.isGoalState(state):
        
                break
            else:
                successors=problem.getSuccessors(state)
                if len(successors)!=0: 
                    hh=qt.copy()
                    for successor in successors:
                        if successor[0] not in visit:
                            a = successor[2] + heuristic(successor[0],problem)
                            q.push(successor[0],cost+a)
                            #queued_list.append(successor[0])
                            ss=successor[1]   
                            hh.append(ss)
                            moves.push(hh,cost+a)  
                            hh=qt.copy()

    return qt
    util.raiseNotDefined()


# Abbreviations
bfs = breadthFirstSearch
dfs = depthFirstSearch
astar = aStarSearch
ucs = uniformCostSearch
