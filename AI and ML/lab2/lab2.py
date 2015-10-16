# Fall 2012 6.034 Lab 2: Search
#
# Your answers for the true and false questions will be in the following form.  
# Your answers will look like one of the two below:
#ANSWER1 = True
#ANSWER1 = False

# 1: True or false - Hill Climbing search is guaranteed to find a solution
#    if there is a solution
ANSWER1 = False

# 2: True or false - Best-first search will give an optimal search result
#    (shortest path length).
#    (If you don't know what we mean by best-first search, refer to
#     http://courses.csail.mit.edu/6.034f/ai3/ch4.pdf (page 13 of the pdf).)
ANSWER2 = False

# 3: True or false - Best-first search and hill climbing make use of
#    heuristic values of nodes.
ANSWER3 = True

# 4: True or false - A* uses an extended-nodes set.
ANSWER4 = True

# 5: True or false - Breadth first search is guaranteed to return a path
#    with the shortest number of nodes.
ANSWER5 = True

# 6: True or false - The regular branch and bound uses heuristic values
#    to speed up the search for an optimal path.
ANSWER6 = True

# Import the Graph data structure from 'search.py'
# Refer to search.py for documentation
from search import Graph
from graphs import *
## Optional Warm-up: BFS and DFS
# If you implement these, the offline tester will test them.
# If you don't, it won't.
# The online tester will not test them.

def bfs(graph, start, goal):
    agenda = []
    newpath = []
    top = 0
    begin = 0
    agenda = [start]
    while agenda:          
        connected_nodes = graph.get_connected_nodes(agenda[-1])
        print 'connected nodes',connected_nodes

        #below is the only difference between bfs and dfs
        #we pop the element at the end of the list
        smma = agenda.pop(0)
        if smma not in newpath:
            newpath.append(smma)
            agenda.extend(connected_nodes)
            if smma == goal:
                break

    return newpath

##NODE1="NODE1"
##NODE2="NODE2"
##bfs(GRAPH1,'Common Area','Statues')
## Once you have completed the breadth-first search,
## this part should be very simple to complete.
def dfs(graph, start, goal):
    agenda = []
    newpath = []
    top = 0
    begin = 0
    agenda = [start]
    while agenda:          
        connected_nodes = graph.get_connected_nodes(agenda[-1])
        print 'connected nodes',connected_nodes

        #below is the only difference between bfs and dfs
        #we pop the element at the end of the list
        smma = agenda.pop()
        if smma not in newpath:
            newpath.append(smma)
            agenda.extend(connected_nodes)
            if smma == goal:
                break

    return newpath


## Now we're going to add some heuristics into the search.  
## Remember that hill-climbing is a modified version of depth-first search.
## Search direction should be towards lower heuristic values to the goal.
def hill_climbing(graph, start, goal):
    
    print 'inside function'
    path = []
    stack = []
    top = 0
    stack = [start]
    loop = 0
    print 'len of stack',len(stack)
    while stack:
        print 'loop #',loop
        connected_nodes = graph.get_connected_nodes(stack[-1])
        index = 0
        leastHeuristic = 100
        for i in range(len(stack)):
            if i is not goal:
                
                if graph.get_heuristic(stack[i],goal) <= leastHeuristic:
                    leastHeuristic = graph.get_heuristic(stack[i],goal)
                    index = i
        print 'from the connected_nodes',stack,' the least heuristic is ',stack[index]  
        v = stack.pop(index)
        if v not in path:
            path.append(v)
            stack.extend(connected_nodes)
            if v == goal:
                break
        loop = loop + 1
    return path

## Now we're going to implement beam search, a variation on BFS
## that caps the amount of memory used to store paths.  Remember,
## we maintain only k candidate paths of length n in our agenda at any time.
## The k top candidates are to be determined using the 
## graph get_heuristic function, with lower values being better values.
def beam_search(graph, start, goal, beam_width):
    print 'inside function'
    path = []
    stack = []
    top = 0
    stack = [start]
    loop = 0
    while stack:
        
        connected_nodes = graph.get_connected_nodes(stack[-1])
        print 'connected_nodes',connected_nodes
        index = 0
        leastHeuristic = 100
        myDict = {}
        for i in connected_nodes:
            myDict[graph.get_heuristic(i,goal)] = i
        smallList = myDict.keys()
        smallList.sort()
        print 'smallList',smallList
        anList = smallList[:beam_width]
        anList.reverse()
        myNodes = []
        for x in anList:
            myNodes.append(myDict[x])            
        v = stack.pop()
        
        if v not in path:
            path.append(v)
            stack.extend(myNodes)
            if v == goal:
                break
            
            
        loop = loop + 1
    return path

##myPath = beam_search(GRAPH1,'Stairs','Common Area',2)
##print 'myPath',myPath
## Now we're going to try optimal search.  The previous searches haven't
## used edge distances in the calculation.

## This function takes in a graph and a list of node names, and returns
## the sum of edge lengths along the path -- the total distance in the path.
def path_length(graph, node_names):
    length = 0
    loop = 0
    
    for i in range(len(node_names)):
        print 'loop #',loop
        if i + 1 <= (len(node_names) - 1):
            length = length + graph.get_edge(node_names[i],node_names[i + 1]).get_length()
        loop += 1
    return length 

#print path_length(GRAPH1,myPath)

def branch_and_bound(graph, start, goal):
    print 'inside function'
    path = []
    stack = []
    top = 0
    stack = [start]
    loop = 0
    pathDist = {}
    while stack:
        
        connected_nodes = graph.get_connected_nodes(stack[-1])
        print 'connected_nodes of ',stack[-1],'are ',connected_nodes
        index = 0
        leastHeuristic = 100
        count = 0
        for i in connected_nodes:
            print 'connected_node',i
            aList = [stack[-1],i]
            myDist = path_length(graph,aList)
            print 'returned distance',myDist
            
            pathDist[i] = path_length(graph,aList)
            count = pathDist[i] + count
            pathDist[i] = count
        smallList = pathDist.values()
        smallList.sort()
        print 'pathDist',pathDist
        print 'smallList',smallList
        anList = smallList[:2]
        smallList.reverse()
        print 'smallList after reversal',smallList
        myNodes = []
        for x in smallList:
            myNodes.append(pathDist[x])            
        v = stack.pop()
        
        if v not in path:
            path.append(v)
            stack.extend(myNodes)
            if v == goal:
                break
            
            
        loop = loop + 1
    return path

    
    
myPath = dfs(GRAPH1,'Necessary Room','Common Area')
print 'myPath',myPath

def a_star(graph, start, goal):
    raise NotImplementedError


## It's useful to determine if a graph has a consistent and admissible
## heuristic.  You've seen graphs with heuristics that are
## admissible, but not consistent.  Have you seen any graphs that are
## consistent, but not admissible?

def is_admissible(graph, goal):
    raise NotImplementedError

def is_consistent(graph, goal):
    raise NotImplementedError

HOW_MANY_HOURS_THIS_PSET_TOOK = ''
WHAT_I_FOUND_INTERESTING = ''
WHAT_I_FOUND_BORING = ''
