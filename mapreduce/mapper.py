#!/usr/bin/env python
import sys
import json
import networkx as nx

for line in sys.stdin:
    line = line.strip()
    try:
        with open(line, 'r') as file:
            data = json.load(file)
            graph = nx.node_link_graph(data)
            serialized_graph = json.dumps(nx.node_link_data(graph))
            print(f'key\t{serialized_graph}')
    except Exception as e:
        print(e)