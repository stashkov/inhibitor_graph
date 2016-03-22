import string, random

def reservoir_pick(n):
    """
    pick list of n elements from 'abcde...z'
    """
    vertices_pool = list(string.ascii_lowercase)
    SAMPLE_COUNT = n

    random.seed()

    sample_titles = []
    for index, line in enumerate(vertices_pool):
            # Generate the reservoir
            if index < SAMPLE_COUNT:
                    sample_titles.append(line)
            else:
                    # Randomly replace elements in the reservoir
                    # with a decreasing probability.
                    # Choose an integer between 0 and index (inclusive)
                    r = random.randint(0, index)
                    if r < SAMPLE_COUNT:
                            sample_titles[r] = line
    return sample_titles

def get_vertices(n):
    """
    pick first n elements from string 'abcde...z' 
    """
    vertices_pool = list(string.ascii_lowercase)
    sample_vertices = []
    for i in vertices_pool[:n]:
        sample_vertices.append(i)
    return sample_vertices

def get_graph(number_of_edges, number_of_vertices):
    graph = {}
    for vertex in get_vertices(number_of_vertices):
        graph[vertex] = reservoir_pick(number_of_edges)

    for key, values in graph.items():
        if key in values:
            values.remove(key)  # remove edge if it's a loop to itself

    main_vertices = []
    sub_verticecs = []
    for key, value in graph.items():
        main_vertices.append(key)
        for item in value:
            sub_verticecs.append(item)

    # add 'z':[] if z does not have any vertices going out of it
    for item in sub_verticecs:
        if item not in main_vertices:
            graph[item] = []

    return graph


def get_inhibitors(graph):
    inhibitors = {}
    for key, value in graph.items():
        for vertex in value:
            inhibitors[(key, vertex)] = int(random.choice('01'))
    return inhibitors

def get_flag(graph):
    flag = {}
    for key, value in graph.items():
        flag[key] = 1
        for item in value:
            flag[item] = int(random.choice('01'))
    return flag


def draw_a_graph(list_of_inhibitors, list_of_flags, name_of_the_output_file):
    import pygraphviz as pgv
    
    A=pgv.AGraph()

    for key, value in list_of_inhibitors.items():
        A.add_edge(key)
        u, v = key
        edge = A.get_edge(u, v)
        edge.attr['label'] = value
        if value == 0:
            edge.attr['color'] = 'red'
    
    for key, value in list_of_flags.items():
        if A.get_node(key):
            vertex = A.get_node(key)
            if value == 0:
                vertex.attr['color'] = 'red'

    #print(A.string()) # print to screen
    #print("Wrote simple.dot")
    A.write(name_of_the_output_file + '.dot') # write to simple.dot

    B=pgv.AGraph(name_of_the_output_file + '.dot') # create a new graph from file
    B.layout() # layout with default (neato)
    B.draw(name_of_the_output_file + '.png') # draw png
    print("Wrote " + name_of_the_output_file + ".png")

def case_1b(graph, inhibitors, flag):
    import case_1b as case_1b
    g, i, f = case_1b.expansion_graph(graph, inhibitors, flag)
    return g, i, f

def case_1a(graph, inhibitors, flag):
    import case_1a as case_1a
    g, i, f = case_1a.expansion_graph(graph, inhibitors, flag)
    return g, i, f

def case_2(graph, inhibitors, flag):
    import case_2 as case_2
    g, i, f = case_2.expansion_graph(graph, inhibitors, flag)
    return g, i, f

def case_3a(graph, inhibitors, flag):
    import case_3a as case_3a
    g, i, f = case_3a.expansion_graph(graph, inhibitors, flag)
    return g, i, f

def case_3b(graph, inhibitors, flag):
    import case_3b as case_3b
    g, i, f = case_3b.expansion_graph(graph, inhibitors, flag)
    return g, i, f

graph = get_graph(3,5)
inhibitors = get_inhibitors(graph)
flag = get_flag(graph)

draw_a_graph(inhibitors, flag, 'source')

print 'graph =', graph
print 'inhibitors =', inhibitors
print 'flag =', flag

import copy
temp_graph = copy.deepcopy(graph)
temp_inhibitors = copy.deepcopy(inhibitors)
temp_flag = copy.deepcopy(flag)

result_graph, result_inhibitors, result_flag = case_1a(temp_graph, temp_inhibitors, temp_flag)
draw_a_graph(result_inhibitors, result_flag, 'result_1a')
print 'graph =', result_graph
print 'inhibitors =', result_inhibitors
print 'flag =', result_flag

result_graph, result_inhibitors, result_flag = case_1b(temp_graph, temp_inhibitors, temp_flag)
draw_a_graph(result_inhibitors, result_flag, 'result_1b')
print 'graph =', result_graph
print 'inhibitors =', result_inhibitors
print 'flag =', result_flag

# graph, inhibitors, flag = case_2(graph, inhibitors, flag)
# draw_a_graph(inhibitors, flag, 'result_2')
# print 'graph =', graph
# print 'inhibitors =', inhibitors
# print 'flag =', flag

# graph, inhibitors, flag = case_3a(graph, inhibitors, flag)
# draw_a_graph(inhibitors, flag, 'result_3a')
# print 'graph =', graph
# print 'inhibitors =', inhibitors
# print 'flag =', flag

# graph, inhibitors, flag = case_3b(graph, inhibitors, flag)
# draw_a_graph(inhibitors, flag, 'result_3b')
# print 'graph =', graph
# print 'inhibitors =', inhibitors
# print 'flag =', flag



# A=pgv.AGraph()

# for key, value in i.items():
#     A.add_edge(key)

# #print(A.string()) # print to screen
# #print("Wrote simple.dot")
# A.write('1simple.dot') # write to simple.dot

# B=pgv.AGraph('1simple.dot') # create a new graph from file
# B.layout() # layout with default (neato)
# B.draw('1simple.png') # draw png
# print("Wrote 1simple.png")
