import requests
import networkx as nx
import matplotlib.pyplot as plt
import json


def graph_to_json(graph, filename):
    data = nx.json_graph.node_link_data(graph)
    with open(filename+'.json', 'w') as f:
        json.dump(data, f)


def json_to_graph(filename):
    with open(filename, 'r') as f:
        data = json.load(f)
        graph = nx.json_graph.node_link_graph(data)
        return graph
    return None

def draw_graph(graph, filename):
    plt.figure(figsize=(20, 20))
    pos = nx.spring_layout(graph, k=0.15, iterations=20)

    nx.draw_networkx_nodes(graph, pos, node_size=50,
                           node_color='blue', alpha=0.7)
    nx.draw_networkx_edges(graph, pos, alpha=0.5)
    plt.savefig(filename+'.png')
