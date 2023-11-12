import sys
import json
import networkx as nx

def union_graphs(graphs):
    union_graph = nx.Graph()
    for graph in graphs:
        union_graph = nx.compose(union_graph, graph)
    return union_graph

graphs = []

for line in sys.stdin:
    _, serialized_graph = line.strip().split('\t', 1)
    graph = nx.node_link_graph(json.loads(serialized_graph))
    graphs.append(graph)

union_graph = union_graphs(graphs)
print(json.dumps(nx.node_link_data(union_graph)))