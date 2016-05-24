import string


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


def convert_doct_to_adj_matrix(dictionary):
    pass #TODO order dict by key, then enumerate alphabet if == then 1