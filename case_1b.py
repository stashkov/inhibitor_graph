"""
given a graph a -| b -> c

where '-|' means inhibition
convert it to two graphs without inhibition:
second graph: a -> not(b)  c  (notice that c is now disconnected vertex)


# inhibitors: 0 means "-|" ; 1 means "->""
# flag: 0 means "not(a)" ; 1 means "a"

"""

# graph = {
#         'a':['b'],
#         'b': ['c'],
#         'c': []
#         }

# inhibitors = {
#             ('a','b'): 0,
#             ('b','c'): 1,
#             }

# flag = {
#         'a':1,
#         'b':1,
#         'c':1
#         }


def expansion_graph(graph, inhibitors, flag):
	#------------collect info about the graph--------------
    out_degree_count = {}
    in_degree_count = {}
    # initialize the mappings 0
    # time complexity: O|V|
    for key, value in graph.items():
    	if len(key) == 1: # vertex is not a composite vertex i.e. 'a' or 'b', not 'ab'
        	out_degree_count[key] = 0
        	in_degree_count[key] = 0
    # iterate through each edge, incrementing the respective mappings for u,v
    # time complexity: O|E|
    for key, value in inhibitors.items():
        out_degree_count[key[0]] += 1
        in_degree_count[key[1]] += 1
    #------------------------------------------------------
    for key, value in inhibitors.items():
        if value == 0:
            (u, v) = key
            if in_degree_count[v] == 1:
                flag[v] = 0
                inhibitors[(u, v)] = 1
                graph[v] = []
                for _key, _value in inhibitors.items():
                	if v == _key[0]: # if arc goes from v to any other vertex - delete it
                		del inhibitors[_key]
    return graph, inhibitors, flag
    
# g, i, f = expansion_graph(graph, inhibitors, flag)

# print 'graph:', g
# print 'inhibitors:', i
# print 'flag:', f

                
                
                

