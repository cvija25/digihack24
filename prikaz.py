import random

# Generisanje 50 prodavnica
num_stores = 50
stores = [f"P{i+1}" for i in range(num_stores)]

# Inicijalizacija praznog grafa
graph = {store: [] for store in stores}

# Funkcija za dodavanje ivica
def add_edge(graph, start, end, weight):
    graph[start].append((end, weight))
    graph[end].append((start, weight))  # Graf je neusmeren

# Nasumično povezivanje prodavnica
for i in range(num_stores):
    for j in range(i + 1, num_stores):
        # Verovatnoća za povezivanje (možeš promeniti vrednost da bi dobio više ili manje ivica)
        if random.random() < 0.2:  # 20% šanse da se povežu
            weight = random.randint(10, 100)  # Udaljenost između 10 i 100 metara
            add_edge(graph, stores[i], stores[j], weight)

# Funkcija za prikaz grafa
def print_graph(graph):
    for node, edges in graph.items():
        print(f"{node}: {edges}")

# Ispis grafa
print_graph(graph)


import matplotlib.pyplot as plt
import networkx as nx

# Kreiranje NetworkX grafa
G = nx.Graph()

# Dodavanje čvorova
for store in stores:
    G.add_node(store)

# Dodavanje ivica i težina
for start, edges in graph.items():
    for end, weight in edges:
        G.add_edge(start, end, weight=weight)

# Crtanje grafa
pos = nx.spring_layout(G)
edges = G.edges(data=True)

# Crtanje čvorova
nx.draw_networkx_nodes(G, pos, node_size=500)

# Crtanje ivica sa težinama
nx.draw_networkx_edges(G, pos)
nx.draw_networkx_labels(G, pos)

# Prikazivanje težina ivica
edge_labels = {(start, end): f"{data['weight']}" for start, end, data in edges}
nx.draw_networkx_edge_labels(G, pos, edge_labels=edge_labels)

# Prikazivanje grafa
plt.title("Graf tržnog centra sa 50 prodavnica")
plt.axis('off')
plt.show()

