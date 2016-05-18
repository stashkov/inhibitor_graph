import string
import networkx as nx
import matplotlib.pyplot as plt
import numpy as np
from collections import defaultdict

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

    print ''
    print '-'*10 + 'result' + '-'*10
    sep = max([len(x) for x in bin_of_edges.keys()])
    for key, value in bin_of_edges.items():
        print key, '--'*(sep-len(key)/2), '>', list(value)
    print '-'*26
    return bin_of_edges


def generate_adj_matrix(vertices, inhibition_degree=2):
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



##################
#current_graph = generate_adj_matrix(5)
current_graph = graph_XXI
##################

main(current_graph)
draw_graph(current_graph)

#main(graph_I)
#main(graph_II)
#main(graph_III)
#main(graph_IV)
#main(graph_V)
#main(graph_VI)

