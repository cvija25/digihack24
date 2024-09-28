import json
import matplotlib.pyplot as plt
import networkx as nx
from matplotlib.animation import FuncAnimation
import numpy as np
from astar import get_path

# Učitavanje grafa iz JSON fajla
with open('testgraph.json') as f:
    orig_graph = json.load(f)

width = orig_graph['dimensions']['width']
height = orig_graph['dimensions']['height']
nodes = orig_graph['nodes']
edges = orig_graph['edges']

# Skaliranje koordinata čvorova
for node in nodes:
    node['center']['x'] = node['center']['x'] / width
    node['center']['y'] = node['center']['y'] / height

# Kreiranje grafa NetworkX
G = nx.Graph()

# Dodavanje čvorova sa pozicijama
for node in nodes:
    G.add_node(node['label'], pos=(node['center']['x'], node['center']['y']))

# Dodavanje ivica
for edge in edges:
    source_label = nodes[edge['source']]['label']
    target_label = nodes[edge['target']]['label']
    G.add_edge(source_label, target_label)

# Dobijanje pozicija za čvorove
pos = nx.get_node_attributes(G, 'pos')

# Kreiranje putanje za tačku (primer)
# path = ["p8", "h1", "h5", "p2"]
path = get_path()

# Parametri animacije
speed_per_frame = 0.003  # Koliko jedinica (proporcija) će preći tačka po frejmu

# Funkcija za izračunavanje Euklidske udaljenosti između dve tačke
def calculate_distance(p1, p2):
    x1, y1 = pos[p1]
    x2, y2 = pos[p2]
    return np.sqrt((x2 - x1)**2 + (y2 - y1)**2)

# Izračunavanje ukupne udaljenosti puta
distances = [calculate_distance(path[i], path[i+1]) for i in range(len(path) - 1)]
total_distance = sum(distances)

# Računanje ukupnog broja frejmova potrebnog za konstantnu brzinu kretanja
total_frames = int(total_distance / speed_per_frame)

# Funkcija za interpolaciju između dve tačke
def interpolate(p1, p2, alpha):
    x1, y1 = pos[p1]
    x2, y2 = pos[p2]
    x = (1 - alpha) * x1 + alpha * x2
    y = (1 - alpha) * y1 + alpha * y2
    return x, y

# Funkcija za ažuriranje pozicije tačke tokom animacije
def update(frame, path, point):
    # Računanje ukupne pređene udaljenosti do trenutnog frejma
    distance_traveled = frame * speed_per_frame

    # Traženje trenutnog para čvorova na osnovu pređene udaljenosti
    cumulative_distance = 0
    for i in range(len(distances)):
        cumulative_distance += distances[i]
        if distance_traveled <= cumulative_distance:
            # Procenat udaljenosti između dva čvora
            prev_cumulative = cumulative_distance - distances[i]
            alpha = (distance_traveled - prev_cumulative) / distances[i]
            p1, p2 = path[i], path[i + 1]
            x, y = interpolate(p1, p2, alpha)
            point.set_data(x, y)  # Ažuriranje pozicije tačke
            break
    return point,

# Crtanje osnovnog grafa
plt.figure(figsize=(8, 6))
nx.draw(G, pos, with_labels=True, node_size=500, node_color="skyblue", font_size=10, font_weight="bold")

# Dodavanje plave tačke koja simulira kretanje
point, = plt.plot([], [], 'bo', markersize=15)  # Plava tačka

# Animacija kretanja tačke kroz čvorove sa konstantnom brzinom
ani = FuncAnimation(plt.gcf(), update, frames=total_frames, fargs=(path, point), interval=50, repeat=False)

# Prikazivanje grafa
plt.title("Graf sa tačkom koja se kreće konstantnom brzinom")
plt.axis('off')
plt.show()

# # Parsiranje u listu susedstva sa imenima čvorova
# i = 0
# node_map = {}
# for node in nodes:
#     node_map[i] = node['label']
#     i += 1

# adj_list = {}
# for edge in edges:
#     if node_map[edge['source']] not in adj_list:
#         adj_list[node_map[edge['source']]] = []

#     adj_list[node_map[edge['source']]].append((node_map[edge['target']], 1))

#     if node_map[edge['target']] not in adj_list:
#         adj_list[node_map[edge['target']]] = []

#     adj_list[node_map[edge['target']]].append((node_map[edge['source']], 1))

# # Čuvanje liste susedstva u JSON fajl
# with open('adj_list.json', 'w') as f:
#     json.dump(adj_list, f)

# print(adj_list)