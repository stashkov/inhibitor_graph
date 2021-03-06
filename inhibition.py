import copy
from collections import defaultdict
import sys
import graphtools
import pprint
import string


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


def generate_bin_of_edges(adjacency_matrix):
    in_degree = graphtools.get_in_degree(adjacency_matrix)
    out_degree = graphtools.get_out_degree(adjacency_matrix)
    graph_dict = graphtools.convert_adj_matrix_to_dict(adjacency_matrix)
    inhibited_edges = graphtools.get_inhibited_edges(adjacency_matrix)

    inhibition_degree = graphtools.get_inhibition_degree(inhibited_edges)

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


def remove_incompatible_nodes_1(d, node):
    """process composite nodes"""
    if len(node) == 2:  # if A1 was picked then A1B1 is incompatible
        for key, values in d.items():
            if key != node and node in key:
                del d[key]
    elif len(node) > 2:  # if A1B1 was picked then A1 and B1 are incompatible
        for key, values in d.items():
            if key != node and key in node:
                del d[key]
    else:  # there is no such case
        pass
    return d


def remove_incompatible_nodes_2(d, lst):
    """the idea is to remove keys that are in lst and values that are in lst
    and if values is emtpy - remove the key"""

    for i in lst:  # if key is from lst, delete key
        if i in d.keys():
            del d[i]

    for i in lst:  # if inside {key: value} value has an element from lst, remove that element
        for key, value in d.items():
            if i in value:
                d[key].remove(i)

    for key, value in d.items():
        if value == []:
            del d[key]
    return d


def get_incompatible_nodes(node, d):
    """based on a node and a graph dict return list of incompatible with that setup nodes"""
    all_nodes = flatten_dict_to_list(d)
    if len(node) > 2:  # given A1B0 incompatible are A1,A0,B1,B0, and anything that contains them
        inc_nodes = split_composite_node(node)  # split A1B0 to ['A1','B0']
        swp = swap_0_and_1(inc_nodes)
        inc_nodes.extend(swp)  # extend to [A1,B0,B1,A0]
        inc_nodes.append(swap_0_and_1(node))  # add A0B1 (reverse of original)
        for node in copy.deepcopy(inc_nodes):
            for e in all_nodes:  # TODO this can be done better
                if node in e:
                    inc_nodes.append(e)  # append any composite node which contains inc_nodes
    if len(node) == 2:  # given A1 incompatible are A0, and anything that contains A1 and A0
        inc_nodes = []
        swap_n = swap_0_and_1(node)  # assign [A0]
        for e in all_nodes:  # look for anything that contains A0
            if swap_n in e:
                inc_nodes.append(e)  # got A0B1, A0B0
        inc_nodes.append(swap_n)
    for item in copy.deepcopy(inc_nodes):
        if item in d.keys():
            inc_nodes.extend(d[item])
    #TODO if node is A0B1C0 it does not says that A1B0 is incompatible
    return list(set(inc_nodes))


def split_composite_node(s):
    """given string A1B0 returns list [A1, B0]"""
    return [s[i * 2:i * 2 + 2] for i, blah in enumerate(s[::2])]


def swap_0_and_1(args):
    if isinstance(args, list):
        for i, string in enumerate(args):
            args[i] = string.replace('0', '2').replace('1', '0').replace('2', '1')
    if isinstance(args, str):
        args = args.replace('0', '2').replace('1', '0').replace('2', '1')
    return args


def flatten_dict_to_list(d):
    all_nodes_values = {x for v in d.itervalues() for x in v}
    all_nodes_keys = {k for k in d.keys()}
    return sorted(list(all_nodes_values | all_nodes_keys))


def intersection_with_negated_nodes(d):
    all_nodes = flatten_dict_to_list(d)
    all_nodes_negated = swap_0_and_1(copy.deepcopy(all_nodes))
    inc_nodes_within = []  # is incompatible if A1,B1,A1B1 are present in all_nodes
    for i in all_nodes:
        for j in all_nodes:
            if i != j and i in j:
                inc_nodes_within.append(i)
                inc_nodes_within.append(j)
    return set(all_nodes) & (set(all_nodes_negated) | set(inc_nodes_within))


def recursive_teardown(my_dict, my_node):
    width = 30
    write_to_file(logs_file, 'Given (%s)-dict :%s' % (len(my_dict), my_dict) + '\n')
    incompatible_nodes = get_incompatible_nodes(my_node, my_dict)
    write_to_file(logs_file, 'For a given %s, incompatible nodes are %s' % (my_node, incompatible_nodes) + '\n')
    write_to_file(logs_file, '...removing, associated with the list above, nodes...' + '\n')
    my_dict = remove_incompatible_nodes_1(my_dict, my_node)
    my_dict = remove_incompatible_nodes_2(my_dict, incompatible_nodes)

    intrsctn = intersection_with_negated_nodes(my_dict)
    if intrsctn == set([]):
        write_to_file(logs_file, '!!!Unbelievable!!! We got a solution!!!' + '\n')
        #write_to_file(logs_file, str(pprint.pprint(my_dict, width=width)) + '\n')
        write_to_file(results_file, str(my_dict) + '\n')

    else:  # intrsctn != set([]):  # if not empty pick elements from it sequentially
        for x in list(intrsctn):
            write_to_file(logs_file, '\nAfter this iteration we got' + '\n')
            write_to_file(logs_file, 'Dict of len %s :\n%s' % (len(my_dict), my_dict) + '\n')
            write_to_file(logs_file, '\nBut this graph is not final, because it has: %s' % list(intrsctn) + '\n')
            write_to_file(logs_file, 'from the list above pick: %s' % x + '\n')
            temp_dict_ = copy.deepcopy(my_dict)
            a = recursive_teardown(temp_dict_, x)
            write_to_file(logs_file, 'Result dict is:\n%s' % a + '\n')
            write_to_file(logs_file, '\n')
    return my_dict

##################
#current_graph = graphtools.generate_adj_matrix(20)
current_graph = graph_test
##################

# visualize the graph
from graphviz import draw_graph
draw_graph(current_graph)

bin_of_edges = generate_bin_of_edges(current_graph)
pretty_print(bin_of_edges)

sys.setrecursionlimit(999999)


# make a normal dict istead of default dict
bin_of_edges = defaultdict(list, ((k, list(v)) for k, v in bin_of_edges.items()))
bin_of_edges = dict(bin_of_edges)

# erase contents of the file
open('result.txt', 'w').close()
results_file = open('result.txt', 'w')
# erase contents of the file
open('logs.txt', 'w').close()
logs_file = open('logs.txt', 'w')


def write_to_file(f, string):
    f.write(string)


def dedupe_file(f):
    unique_results = open('unique_result.txt', 'w')
    lines_seen = set()
    for line in open(f, 'r'):
        if line not in lines_seen:
            unique_results.write(line)
            lines_seen.add(line)
    unique_results.close()

all_nodes = flatten_dict_to_list(bin_of_edges)
result = []

write_to_file(logs_file, 'We are given:\n %s' % bin_of_edges + '\n')
write_to_file(logs_file, 'Therefore all nodes are:\n %s' % all_nodes + '\n')
write_to_file(logs_file, 'We are going to go through them sequentially.')
write_to_file(logs_file, '\n\n\n\n')

for i, node in enumerate(all_nodes):
    print 'currently on node %s out of %s' % (i+1, len(all_nodes))
    temp_dict = copy.deepcopy(bin_of_edges)
    write_to_file(logs_file, 'main loop, picked node: %s' % node + '\n')
    recursive_teardown(temp_dict, node)
    write_to_file(logs_file, '\n\n\n\n')




results_file.close()
dedupe_file('result.txt')

print '\nNumber of unique solutions: %s' % sum(1 for line in open('unique_result.txt'))


from graphtools import convert_dict_to_adj_matrix
with open('unique_result.txt', 'r') as f:
    for line in f:
        d = eval(line)
        m = convert_dict_to_adj_matrix(d)
        labels = flatten_dict_to_list(d)
        draw_graph(m, labels)