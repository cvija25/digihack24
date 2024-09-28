import json

with open('testgraph.json') as f:
    orig_graph = json.load(f)

width = orig_graph['dimensions']['width']
height = orig_graph['dimensions']['height']
nodes = orig_graph['nodes']
edges = orig_graph['edges']
for node in nodes:
    node['center']['x'] = node['center']['x']/width
    node['center']['y'] = node['center']['y']/height

graph = {}
edges = orig_graph['edges']
for edge in edges:
    graph[edge['source']] = edge['target']

import matplotlib.pyplot as plt
import networkx as nx

G = nx.Graph()

# Add nodes with positions
for idx, node in enumerate(nodes):
    G.add_node(node['label'], pos=(node['center']['x'], node['center']['y']))

# Add edges
for edge in edges:
    source_label = nodes[edge['source']]['label']
    target_label = nodes[edge['target']]['label']
    G.add_edge(source_label, target_label)

# Get positions for nodes
pos = nx.get_node_attributes(G, 'pos')

# Draw the graph
plt.figure(figsize=(8, 8))
nx.draw(G, pos, with_labels=True, node_size=500, node_color="skyblue", font_size=10, font_weight="bold")
plt.title("Graph Visualization")
plt.show()

