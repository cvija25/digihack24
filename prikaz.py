import random
import matplotlib.pyplot as plt
import networkx as nx

num_stores = 50
stores = [f"P{i+1}" for i in range(num_stores)]

graph = {store: [] for store in stores}

def add_edge(graph, start, end, weight):
    graph[start].append((end, weight))
    graph[end].append((start, weight))  

for i in range(num_stores):
    for j in range(i + 1, num_stores):
        if random.random() < 0.2:
            weight = random.randint(10, 100)
            add_edge(graph, stores[i], stores[j], weight)

def print_graph(graph):
    for node, edges in graph.items():
        print(f"{node}: {edges}")

print_graph(graph)

G = nx.Graph()

for store in stores:
    G.add_node(store)

for start, edges in graph.items():
    for end, weight in edges:
        G.add_edge(start, end, weight=weight)

pos = nx.spring_layout(G)
edges = G.edges(data=True)

nx.draw_networkx_nodes(G, pos, node_size=500)

nx.draw_networkx_edges(G, pos)
nx.draw_networkx_labels(G, pos)

edge_labels = {(start, end): f"{data['weight']}" for start, end, data in edges}
nx.draw_networkx_edge_labels(G, pos, edge_labels=edge_labels)

plt.title("Graf tržnog centra sa 50 prodavnica")
plt.axis('off')
plt.show()

