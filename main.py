import string

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


"""SET THE CURRENT GRAPH"""
CURRENT_GRAPH = graph_X
"""SET THE CURRENT GRAPH"""

in_degree = get_in_degree(CURRENT_GRAPH)
out_degree = get_out_degree(CURRENT_GRAPH)
graph_dict = convert_adj_matrix_to_dict(CURRENT_GRAPH)
inhibited_edges = get_inhibited_edges(CURRENT_GRAPH)

inhibition_degree = get_inhibition_degree(inhibited_edges)

print 'graph dict: ', graph_dict
print 'in_degree:  ', in_degree
print 'out_degree: ', out_degree
print 'inhibited:  ', inhibited_edges
print 'inhib degr: ', inhibition_degree

bin_of_edges = {}

for edge in inhibited_edges:
    u, v = edge
    if in_degree[v] == 1:  # CASE I
        # CASE I.1
        bin_of_edges['not ' + u] = v
        for vertex in graph_dict[v]:
            bin_of_edges[v] = vertex
        # CASE I.2
        bin_of_edges[u] = 'not ' + v
        for vertex in graph_dict[v]:
            # TODO here should be a check for A -| B -| C, do not remove C
            # not sure if this is needed, since we are going to check for compatibility
            # during graph assembly stage
            bin_of_edges['remove ' + v] = 'remove ' + vertex
    if in_degree[v] > 1 and inhibition_degree[v] == 1:  # CASE II
        # CASE II.1
        bin_of_edges[u] = v
        for key, value in graph_dict.items():
            if v in value:  # find nodes, other than u, going to v
                if key != u:
                    bin_of_edges['not ' + key] = v
        # CASE II.4
        bin_of_edges['not ' + u] = v
        for key, value in graph_dict.items():
            if v in value:  # find nodes, other than u, going to v
                if key != u:
                    bin_of_edges[key] = 'not ' + v
        # CASE II.2
        new_node = ''
        for key, value in graph_dict.items():
            if v in value:  # find nodes, other than u, going to v
                if key != u:
                    new_node += 'not ' + key + ' + '
        new_node = new_node[:-3]  # remove last 3 characters
        bin_of_edges[new_node + u] = v
        # CASE II.3
        new_node = ''
        for key, value in graph_dict.items():
            if v in value:  # find nodes, other than u, going to v
                if key != u:
                    new_node += key + ' + '
        new_node = new_node[:-3]  # remove last 3 characters
        bin_of_edges[new_node + 'not ' + u] = 'not ' + v
    if in_degree[v] > 1 and inhibition_degree[v] > 1 and \
       in_degree[v] != inhibition_degree[v]:  # CASE not yet exists :)
        # TODO every possible combination of AND OR over input set
        pass  # many AND OR cases
    if in_degree[v] == inhibition_degree[v] == 2:  # CASE III
        # CASE III.1
        for key, value in graph_dict.items():
            if v in value:  # find nodes, other than u, going to v
                bin_of_edges['not ' + key] = v
        # CASE III.4
        for key, value in graph_dict.items():
            if v in value:  # find nodes, other than u, going to v
                bin_of_edges[key] = 'not ' + v
        # CASE II.2
        new_node = ''
        for key, value in graph_dict.items():
            if v in value:  # find nodes, other than u, going to v
                new_node += 'not ' + key + ' + '
        new_node = new_node[:-3]  # remove last 3 characters
        bin_of_edges[new_node] = v
        # CASE II.3
        new_node = ''
        for key, value in graph_dict.items():
            if v in value:  # find nodes, other than u, going to v
                new_node += key + ' + '
        new_node = new_node[:-3]  # remove last 3 characters
        bin_of_edges[new_node] = 'not ' + v

print bin_of_edges

# # print the output in human readable form
# for key, value in bin_of_edges.items():
#     print key, ' --> ', value


for edge in inhibited_edges:
    u, v = edge