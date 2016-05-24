import string
import networkx as nx
import matplotlib.pyplot as plt
import numpy as np
import random as rnd
import copy
from collections import defaultdict
import random

"""
input: graph as an adjacency matrix, where 1 means regular edge, -1 means inhibited edge
output: hash table with pool of values with which you can construct a new graph
see example graph_I
"""

graph_I = [
    [
        0, -1, 0
    ],
    [
        0, 0, 1
    ],
    [
        0, 0, 0
    ]
]
graph_II = [
    [
        0, 0, 1
    ],
    [
        0, 0, -1
    ],
    [
        0, 0, 0
    ]
]
graph_III = [
    [
        0, 0, -1
    ],
    [
        0, 0, -1
    ],
    [
        0, 0, 0
    ]
]
graph_IV = [
    [
        0, -1, 0
    ],
    [
        0, 0, -1
    ],
    [
        0, 0, 0
    ]
]
graph_V = [
    [
        0, 1
    ],
    [
        0, 0
    ]
]
graph_VI = [
    [
        0, 0, 1
    ],
    [
        0, 0, 1
    ],
    [
        0, 0, 0
    ]
]
graph_X = [
    [
        0, 0, 0, -1
    ],
    [
        0, 0, 0, -1
    ],
    [
        0, 0, 0, -1
    ],
    [
        0, 0, 0, 0
    ]
]
graph_test = [[0, 0, 1, 0, 0, 0, 0],
              [0, 0, 1, 0, 0, 0, 0],
              [0, 0, 0, -1, 1, 0, 0],
              [0, 0, 0, 0, 0, 0, 0],
              [0, 0, 0, 0, 0, -1, 0],
              [0, 0, 0, 0, 0, 0, 1],
              [0, 0, 0, 0, 0, 0, 0]]
graph_XXI = [[ 0, -1,  1,  1,  1],
             [ 0,  0,  0,  1,  0],
             [ 0,  0,  0,  0, -1],
             [ 0,  0,  0,  0,  0],
             [ 0,  0,  0,  0,  0]]


def get_out_degree(adjacency_matrix):
    vertices = list(string.ascii_uppercase[0:len(adjacency_matrix)])
    dict_out_degree = {}
    for vertex in vertices:
        dict_out_degree[vertex] = 0
    row_number = 0
    for row in adjacency_matrix:
        for value in row:
            if abs(value) == 1:
                dict_out_degree[vertices[row_number]] += 1
        row_number += 1
    return dict_out_degree


def get_in_degree(adjacency_matrix):
    vertices = list(string.ascii_uppercase[0:len(adjacency_matrix)])
    dict_in_degree = {}
    for vertex in vertices:
        dict_in_degree[vertex] = 0
    adjacency_matrix_transpose = [list(i) for i in zip(*adjacency_matrix)]
    row_number = 0
    for row in adjacency_matrix_transpose:
        for value in row:
            if abs(value) == 1:
                dict_in_degree[vertices[row_number]] += 1
        row_number += 1
    return dict_in_degree


def get_inhibited_edges(adjacency_matrix):
    vertices = list(string.ascii_uppercase[0:len(adjacency_matrix)])
    inhibited_edges = []
    for i in range(len(adjacency_matrix)):
        for j in range(len(adjacency_matrix)):
            if adjacency_matrix[i][j] == -1:
                inhibited_edges.append((vertices[i], vertices[j]))
    return inhibited_edges


def convert_adj_matrix_to_dict(adjacency_matrix):
    vertices = list(string.ascii_uppercase[0:len(adjacency_matrix)])
    graph_dict = {}
    for vertex in vertices:
        graph_dict[vertex] = []
    for i in range(len(adjacency_matrix)):
        for j in range(len(adjacency_matrix)):
            if abs(adjacency_matrix[i][j]) == 1:
                graph_dict[vertices[i]].append(str(vertices[j]))
    return graph_dict


def get_inhibition_degree(list_of_edges):
    inhibition_degree = {}
    for edge in list_of_edges:
        u, v = edge
        if v not in inhibition_degree.keys():
            inhibition_degree[v] = 1
        else:
            inhibition_degree[v] += 1
    return inhibition_degree


def two_or_more_all_inhibited(graph_dict, u, v, bin_of_edges):
    new_node = new_node_ = ''  # CASE III.2 and CASE III.3
    for key, value in graph_dict.items():
        if v in value:  # find nodes, other than u, going to v
            bin_of_edges[key + '0'].add(v + '1')  # CASE III.1
            bin_of_edges[key + '1'].add(v + '0')  # CASE III.4
            new_node += key + '0'  # CASE III.2
            new_node_ += key + '1'  # CASE III.3
    bin_of_edges[new_node].add(v + '1')  # CASE III.2
    bin_of_edges[new_node_].add(v + '0')  # CASE III.3
    return bin_of_edges


def exactly_one_one_inhibited(graph_dict, u, v, bin_of_edges):
    bin_of_edges[u + '0'].add(v + '1')  # CASE I.1
    bin_of_edges[u + '1'].add(v + '0')  # CASE I.2
    for vertex in graph_dict[v]:
        bin_of_edges[v + '1'].add(vertex + '1')  # CASE I.1
        # TODO: in case A-|B-|C we get 'B0':['C1','C0']
        #bin_of_edges[v + '1'].add(vertex + '1')  # CASE I.2
    return bin_of_edges


def more_than_one_one_inhibited(graph_dict, u, v, bin_of_edges):
    bin_of_edges[u + '1'].add(v + '1')  # CASE II.1
    bin_of_edges[u + '0'].add(v + '0')  # CASE II.4
    new_node = new_node_ = ''  # CASE II.2 and CASE II.3
    for key, value in graph_dict.items():
        if v in value:  # find nodes, other than u, going to v
            if key != u:
                bin_of_edges[key + '0'].add(v + '1')  # CASE II.1
                bin_of_edges[key + '1'].add(v + '0')  # CASE II.4
                new_node += key + '0'  # CASE II.2
                new_node_ += key + '1'  # CASE II.3
    bin_of_edges[new_node + u + '1'].add(v + '1')  # CASE II.2
    bin_of_edges[new_node_ + u + '0'].add(v + '0')  # CASE II.3
    return bin_of_edges


def more_than_one_no_inhibited(graph_dict, v, bin_of_edges):
    new_node = ''  # CASE VI.1
    for key, value in graph_dict.items():
        if v in value:  # find nodes, other than u, going to v
            new_node += key + '1'  # CASE VI.1
            bin_of_edges[key + '1'].add(v + '1')  # CASE VI.2
            bin_of_edges[key + '0'].add(v + '0')  # CASE VI.3 TODO add to latex
    bin_of_edges[new_node].add(v + '1')  # CASE VI.1
    return bin_of_edges


def exactly_one_no_inhibited(graph_dict, v, bin_of_edges):
    # CASE V
    for key, value in graph_dict.items():
        if v in value:  # find nodes, other than u, going to v
            bin_of_edges[key + '1'].add(v + '1')
    return bin_of_edges


def main(adjacency_matrix):
    in_degree = get_in_degree(adjacency_matrix)
    out_degree = get_out_degree(adjacency_matrix)
    graph_dict = convert_adj_matrix_to_dict(adjacency_matrix)
    inhibited_edges = get_inhibited_edges(adjacency_matrix)

    inhibition_degree = get_inhibition_degree(inhibited_edges)

    vertices = set(graph_dict.keys())
    inhibited_vertices = set([edge[1] for edge in inhibited_edges])
    non_inhibited_vertices = list(vertices - inhibited_vertices)

    print 'input graph --------------->', graph_dict
    print 'in degree for each node --->', in_degree
    print 'out degree for each node -->', out_degree
    print 'inhibited edges ----------->', inhibited_edges
    print 'number of inhibited edges going into a node -->', inhibition_degree
    print 'non inhibited vertices ---->', non_inhibited_vertices

    bin_of_edges = defaultdict(set)

    for edge in inhibited_edges:
        u, v = edge
        if in_degree[v] == 1:  # CASE I
            bin_of_edges = exactly_one_one_inhibited(graph_dict, u, v, bin_of_edges)
        if in_degree[v] > 1 and inhibition_degree[v] == 1:  # CASE II
            bin_of_edges = more_than_one_one_inhibited(graph_dict, u, v, bin_of_edges)
        # if in_degree[v] > 1 and inhibition_degree[v] > 1 and \
        #    in_degree[v] != inhibition_degree[v]:  # CASE not yet exists :)
        #     # TODO every possible combination of AND OR over input set
        #     pass  # many AND OR cases
        if in_degree[v] == inhibition_degree[v] == 2:  # CASE III
            bin_of_edges = two_or_more_all_inhibited(graph_dict, u, v, bin_of_edges)

    for v in non_inhibited_vertices:
        if in_degree[v] > 1:  # CASE VI
            bin_of_edges = more_than_one_no_inhibited(graph_dict, v, bin_of_edges)
        if in_degree[v] == 1:  # CASE V
            bin_of_edges = exactly_one_no_inhibited(graph_dict, v, bin_of_edges)
    return bin_of_edges


def pretty_print(dictionary):
    if dictionary.keys():
        print ''
        print 'number of keys in dict:', len(dictionary.keys())
        print '-'*10 + 'result' + '-'*10
        sep = max([len(x) for x in dictionary.keys()])
        for key, value in sorted(dictionary.items()):
            print key, '--'*(sep-len(key)/2), '>', list(value)
        print '-'*26
    else:
        print 'pretty print says dict supplied is empty'
    return '-'*26, 'Iteration Completed', '-'*26


def generate_adj_matrix(vertices, inhibition_degree=2):
    """generate square matrix with max inihigibiton degree"""
    import random as rnd
    matrix = [[0 for x in range(vertices)] for y in range(vertices)]
    for i, row in enumerate(matrix):
        for j, element in enumerate(row):
            if i > j:
                if row.count(-1) == inhibition_degree:
                    matrix[i][j] = rnd.choice([0, 1])
                else:
                    matrix[i][j] = rnd.choice([-1, 1, 0])

    matrix = [list(i) for i in zip(*matrix)]
    return matrix


def draw_graph(adjacency_matrix):
    matrix = np.matrix(adjacency_matrix)
    graph = nx.from_numpy_matrix(matrix, create_using=nx.DiGraph())
    print matrix

    vertices = list(string.ascii_uppercase[0:len(adjacency_matrix)])
    labels = {i: vertex for (i, vertex) in enumerate(vertices)}

    edge_color = ['b' if x == 1 else 'r' for row in adjacency_matrix for x in row if x in [-1, 1]]
    width = [1*len(edge_color)]
    node_color = ['w' for _ in edge_color]

    nx.draw(graph,
            node_size=5000,
            labels=labels,
            with_labels=True,
            font_size=30,
            edge_color=edge_color,
            width=width,
            node_color=node_color)
    plt.show()
    return None


def compatible_pool_composite_node(dict_compatible, picked_node):
    # if A1 was picked then A1B1 is incompatible
    if len(picked_node) == 2:
        for key, values in dict_compatible.items():
            if key != picked_node and picked_node in key:
                del dict_compatible[key]

    # if A1B1 was picked then A1 and B1 are incompatible
    if len(picked_node) > 2:
        for key, values in dict_compatible.items():
            if key != picked_node and key in picked_node:
                del dict_compatible[key]
    return dict_compatible


def compatible_pool(dict_compatible, list_of_incompatible_nodes):
    for key, value in dict_compatible.items():
        if key in list_of_incompatible_nodes:
            if key in dict_compatible.keys():
                del dict_compatible[key]

    for key, value in dict_compatible.items():
        for x in list_of_incompatible_nodes:
            if x in key:
                if key in dict_compatible.keys():
                    del dict_compatible[key]

    for key, value in dict_compatible.items():
        for node in list_of_incompatible_nodes:
            if node in value:  # remove just that node
                dict_compatible[key].remove(node)

    for key, value in dict_compatible.items():
        if dict_compatible[key] == set([]) or dict_compatible[key] == []:  # remove key if it has empty set
            del dict_compatible[key]

    return dict_compatible


def incompatible_pool(random_node, dict_of_edges):
    import itertools
    """based on a node and a graph dict return incompatible with that setup nodes"""
    #print 'diagnostic info:'
    #print 'random node:',random_node
    #print 'chain:', flatten_dict_to_list(dict_of_edges)
    if random_node in dict_of_edges.keys(): # TODO refactor this...
        incompatible = list(dict_of_edges[random_node])
        for i, string in enumerate(incompatible):  # swap 0's and 1's
            incompatible[i] = string.replace('0', '2').replace('1', '0').replace('2', '1')
        random_node = random_node.replace('0', '2').replace('1', '0').replace('2', '1')
        incompatible.append(random_node)
        n = 2
        #print 'incompatible inside function1', incompatible
        for node in incompatible: # split into chunks of len=2 (e.g. give A0B0 get [A0, B0]
            if len(node) > n:
                #print 'node inside function1', node
                for x in [node[i * n:i * n + n] for i, blah in enumerate(node[::n])]:
                    incompatible.append(x)
                    incompatible.append(x.replace('0', '2').replace('1', '0').replace('2', '1'))
                incompatible.remove(node)
    else:
        incompatible = []
        random_node = random_node.replace('0', '2').replace('1', '0').replace('2', '1')
        incompatible.append(random_node)
        n = 2
        #print 'incompatible inside function', incompatible
        for node in incompatible:  # split into chunks of len=2 (e.g. give A0B0 get [A0, B0]
            if len(node) > n:
                #print 'node inside function', node
                for x in [node[i * n:i * n + n] for i, blah in enumerate(node[::n])]:
                    incompatible.append(x)
                    incompatible.append(x.replace('0', '2').replace('1', '0').replace('2', '1'))
                incompatible.remove(node)
    return incompatible



def flatten_dict_to_list(dictionary):
    all_nodes_values = {x for v in dictionary.itervalues() for x in v}
    all_nodes_keys = {k for k in dictionary.keys()}
    return sorted(list(all_nodes_values | all_nodes_keys))

#TODO if picked B1 then A1B1 should also be incomaptible

def intersection_with_negated_nodes(dictionary):
    all_nodes = flatten_dict_to_list(dictionary)
    all_nodes_negated = copy.deepcopy(all_nodes)
    for i, string in enumerate(all_nodes_negated):  # swap 0's and 1's
        all_nodes_negated[i] = string.replace('0', '2').replace('1', '0').replace('2', '1')
    #TODO if node is A1B1 then A1 and B1 should be incompatible done as follows:
    n = 2
    composite_nodes_split = []
    for node in all_nodes:  # split into chunks of len=2 (e.g. give A0B0 get [A0, B0]
        if len(node) > n:
            for x in [node[i * n:i * n + n] for i, blah in enumerate(node[::n])]:
                composite_nodes_split.append(x)
                composite_nodes_split.append(x.replace('0', '2').replace('1', '0').replace('2', '1'))
    return set(all_nodes) & (set(all_nodes_negated) | set(composite_nodes_split))

#__________________________________________________________

##################
#current_graph = generate_adj_matrix(20)
current_graph = graph_test
##################

bin_of_edges = main(current_graph)
pretty_print(bin_of_edges)
# draw_graph(current_graph)

import sys, pprint
sys.setrecursionlimit(10000)
print '\nSTARTING THE ALGO'


def recursive_teardown(my_dict, my_node):
    width = 20
    all_nodes = flatten_dict_to_list(my_dict)
    print 'got node     :', my_node
    print 'got dict     :'
    pprint.pprint(my_dict, width=width)
    #print 'consisting of:', all_nodes

    incompatible_nodes = incompatible_pool(my_node, my_dict)
    print 'generated incompatible nodes:', incompatible_nodes
    print 'removing, associated with the list above, nodes...'
    my_dict = compatible_pool_composite_node(my_dict, my_node)
    my_dict = compatible_pool(my_dict, incompatible_nodes)


    intrsctn = intersection_with_negated_nodes(my_dict)
    if intrsctn == set([]):
        print 'Unbelievable! We got a solution!!'
        print 'the solution has following data:', pretty_print(my_dict)
        return my_dict
    if intrsctn != set([]):  # if not empty, pick at random and call again
        print '\nafter this iteration we got:'
        pprint.pprint(my_dict, width=width)
        print 'but this graph is not compatible yet, because it has:', list(intrsctn)
        print 'therefore recursive call initiated. Picking a random node from list above'
        print ''
        for x in list(intrsctn):
            temp_dict_ = copy.deepcopy(my_dict)
            recursive_teardown(temp_dict_, x)
        #recursive_teardown(my_dict, random.choice(list(intrsctn)))
    return my_dict


# make a normal dict istead of default dict
bin_of_edges = defaultdict(list, ((k, list(v)) for k, v in bin_of_edges.items()))
bin_of_edges = dict(bin_of_edges)

all_nodes = flatten_dict_to_list(bin_of_edges)
result = []
for node in all_nodes:
    temp_dict = copy.deepcopy(bin_of_edges)
    print '\nmain loop, picked node:', node
    #result.append(recursive_teardown(temp_dict, node))
    a = recursive_teardown(temp_dict, node)
    result.append(a)




print ''
print '-------final res--------'
print len(result)
print '-----dedup----------'


final = []
for x in result:
    if x not in final:
        final.append(x)


print len(final)

for item in final:
    print item
#main(graph_I)
#main(graph_II)
#main(graph_III)
#main(graph_IV)
#main(graph_V)
#main(graph_VI)

