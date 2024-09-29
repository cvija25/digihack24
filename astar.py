import json
import numpy as np

def get_next_node(open_set, heuristic_guess):
    v = None
    min_d = float('inf')
    for node in open_set:
        if node in heuristic_guess:
            guess = heuristic_guess[node]
            if guess < min_d:
                min_d = guess
                v = node
    return v

def astar(adj_list, start_node, target_node, h):
    open_set = set([start_node])
    
    parents = {}
    parents[start_node] = None
    
    cheapest_paths = {v:float('inf') for v in adj_list}
    cheapest_paths[start_node] = 0
    
    heuristic_guess = {v:float('inf') for v in adj_list}
    heuristic_guess[start_node] = h(start_node, target_node)
    
    path_found = False
    while len(open_set) > 0:
        current_node = get_next_node(open_set, heuristic_guess)
        
        if current_node == target_node:
            path_found = True
            break
        
        open_set.remove(current_node)
        for (neighbour_node, weight) in adj_list[current_node]:
            new_cheapest_path = cheapest_paths[current_node] + weight
            
            if new_cheapest_path < cheapest_paths[neighbour_node]:
                parents[neighbour_node] = current_node
                cheapest_paths[neighbour_node] = new_cheapest_path
                heuristic_guess[neighbour_node] = new_cheapest_path + h(neighbour_node, target_node)
                
                if neighbour_node is not open_set:
                    open_set.add(neighbour_node)
        
    path = []
    if path_found:
        while target_node is not None:
            path.append(target_node)
            target_node = parents[target_node]
        path.reverse()
    
    return path

def h(n, target_node):
    with open('testgraph.json') as f:
        data = json.load(f)

    graph_coord = {}

    for node in data["nodes"]:
        label = node["label"]
        x = int(node["center"]["x"])
        y = int(node["center"]["y"])
        graph_coord[label] = [x, y]

    # Prikaz rezultata
    #print(graph_coord)
    
    dist = (graph_coord[n][0] - graph_coord[target_node][0])**2 + (graph_coord[n][1] - graph_coord[target_node][1])**2 

    dist = np.sqrt(dist)

    return 0

# if __name__ == "__main__":
def get_path():
    adj_list = {
        'A': [('B', 1), ('C', 4)],
        'B': [('A', 1), ('C', 2), ('D', 5)],
        'C': [('A', 4), ('B', 2), ('D', 1)],
        'D': [('B', 5), ('C', 1)]
    }
    with open('adj_list.json') as f:
        graph = json.load(f)
    start_node = 'p24'
    target_node = 'p11'
    
    path = astar(graph, start_node, target_node, h)
    return path
    
    if path:
        print(f"Najkraći put od {start_node} do {target_node} je: {path}")
    else:
        print(f"Nema puta od {start_node} do {target_node}.")
