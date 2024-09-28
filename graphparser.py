import json
import matplotlib.pyplot as plt
import networkx as nx
from matplotlib.animation import FuncAnimation
import matplotlib.image as mpimg  # Biblioteka za učitavanje slike
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

# Lista za čuvanje prethodnih pozicija tačke (plavi trag)
trail_x = []
trail_y = []

# Funkcija za ažuriranje pozicije tačke tokom animacije
def update(frame, path, point, line):
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

            # Čuvanje prethodnih pozicija u trag (plavi trag)
            trail_x.append(x)
            trail_y.append(y)

            # Ažuriranje linije (trag) sa novim pozicijama
            line.set_data(trail_x, trail_y)
            break

    return point, line

# Crtanje osnovnog grafa

fig, ax = plt.subplots(figsize=(8, 6))
nx.draw(G, pos, with_labels=True, node_size=500, node_color="skyblue", font_size=10, font_weight="bold", ax=ax)

# Dodavanje roze linije koja prikazuje putanju po kojoj se tačka kreće
path_points_x = [pos[node][0] for node in path]
path_points_y = [pos[node][1] for node in path]
ax.plot(path_points_x, path_points_y, color='pink', linewidth=2, linestyle='--', label='Planirana putanja')

# Dodavanje plave tačke koja simulira kretanje
point, = ax.plot([], [], 'bo', markersize=15)  # Plava tačka
line, = ax.plot([], [], color='blue', linewidth=2)  # Plavi trag tačke

# Animacija kretanja tačke kroz čvorove sa konstantnom brzinom
ani = FuncAnimation(fig, update, frames=total_frames, fargs=(path, point, line), interval=50, repeat=False)

# Prikazivanje grafa
plt.title("Graf sa tačkom koja ostavlja plavi trag i roze putanju")
plt.axis('off')
plt.legend()
plt.show()
