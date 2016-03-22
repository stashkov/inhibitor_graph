"""
# input 
graph = {
        'a':['c'],
        'b': ['c'],
        'c': []
        }

inhibitors = {
            ('a','c'): 1,
            ('b','c'): 0,
            }

flag = {
        'a':1,
        'b':1,
        'c':1
        }

# output 
graph = {
        'a':['c'],
        'b': ['c'],
        'c': []
        }

inhibitors = {
            ('a','c'): 1,
            ('b','c'): 1, # change to 1
            }

flag = {
        'a':0, # change to 0
        'b':1,
        'c':0 # change to 0
        }
"""

graph = {
        'a':['c'],
        'b': ['c'],
        'c': []
        }

inhibitors = {
            ('a','c'): 1,
            ('b','c'): 0,
            }

flag = {
        'a':1,
        'b':1,
        'c':1
        }

def expansion_graph(graph, inhibitors, flag):
    #------------collect info about the graph--------------
    out_degree_count = {}
    in_degree_count = {}
    # initialize the mappings 0
    # time complexity: O|V|
    for key, value in graph.items():
        out_degree_count[key] = 0
        in_degree_count[key] = 0
    # iterate through each edge, incrementing the respective mappings for u,v
    # time complexity: O|E|
    for key, value in inhibitors.items():
        out_degree_count[key[0]] += 1
        in_degree_count[key[1]] += 1
    #------------------------------------------------------

    # time complexity: O|E| + some part of |V|
    for key, value in inhibitors.items():
        # if inhibitor is 0 and target node has degree > 1
        if (in_degree_count[key[1]] > 1) and value == 0:
            (u, v) = key

            inhibitors[(u, v)] = 1
            flag[v] = 0 

            # set every node that goes into target node to 0 except for source node
            for key, value in graph.items():
                if v in value and u != key:
                    flag[key] = 0
    return graph, inhibitors, flag
    
g, i, f = expansion_graph(graph, inhibitors, flag)

print 'graph:', g
print 'inhibitors:', i
print 'flag:', f