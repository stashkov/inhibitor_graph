import networkx as nx
import numpy as np
import string
import matplotlib as plt


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