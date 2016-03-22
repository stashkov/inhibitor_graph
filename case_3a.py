"""
-------------------
a -> 
     c
b -|
------------------
where '-|' means inhibition
convert it to a graph without inhibition:
--------------------
    a ->
         ab -> c
not(b)->
--------------------
# inhibitors: 0 means "-|" ; 1 means "->""
# flag: 0 means "not(a)" ; 1 means "a"

example:

# # input 
# graph = {
#         'a':['c'],
#         'b': ['c'],
#         'c': []
#         }

# inhibitors = {
#             ('a','c'): 1,
#             ('b','c'): 1,
#             }

# flag = {
#         'a':1,
#         'b':1,
#         'c':1
#         }

# # output 
# graph = {
#         'a':['ab'],  # swap 'c' to 'ab'
#         'b': ['ab'], # swap 'c' to 'ab'
#         'ab': ['c']  # add new 'ab' that goes to 'c'
#         'c': []
#         }

# inhibitors = {
#             ('a','ab'): 1, # change 'c' to 'ab'
#             ('b','ab'): 1, # change to 1 and change 'c' to 'ab'
#             ('ab', 'c'): 1 # add a new 'ab' to 'c'
#             }

# flag = {
#         'a':1,
#         'b':0,  # change to 0
#         'c':1
#         }


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
    	if len(key) == 1: # vertex is not a composite vertex i.e. 'a' or 'b', not 'ab'
        	out_degree_count[key] = 0
        	in_degree_count[key] = 0
    # iterate through each edge, incrementing the respective mappings for u,v
    # time complexity: O|E|
    for key, value in inhibitors.items():
        out_degree_count[key[0]] += 1
        in_degree_count[key[1]] += 1
    #------------------------------------------------------
    additional_vertices = {}
    # populate dict with {'degree_name': 'all incoming edges concatenated'}
    # e.g. {'c': 'ab'}
    for key, value in inhibitors.items():
        (u, v) = key

        if value == 0:
        	flag[u] = 0

        if in_degree_count[v] > 1:
        	if v not in additional_vertices.keys():
        		additional_vertices[v] = ''
        # concatenate a name for a new vertex
        additional_vertices[v] = additional_vertices[v] + u

    # replace vertices involved with a composite name
    for old_vertex, new_composite_vertex in additional_vertices.items():
    	for source_vertex, list_of_target_vertices in graph.items():
			for idx, item in enumerate(list_of_target_vertices):
				if item == old_vertex:
					list_of_target_vertices[idx] = new_composite_vertex
	
	# add composite vertices
	for old_vertex, new_composite_vertex in additional_vertices.items():
		graph[new_composite_vertex] = [old_vertex]
	
	# replace vertices involved with a composite name
	for old_vertex, new_composite_vertex in additional_vertices.items():
		for key, value in inhibitors.items():
			if key[1] == old_vertex:
				inhibitors[(key[0], new_composite_vertex)] = inhibitors.pop(key)
	
	# add composite vertices
	for old_vertex, new_composite_vertex in additional_vertices.items():
		inhibitors[(new_composite_vertex, old_vertex)] = 1



    return graph, inhibitors, flag
    
g, i, f = expansion_graph(graph, inhibitors, flag)

print 'graph:', g
print 'inhibitors:', i
print 'flag:', f
