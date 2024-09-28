import json
import copy
from collections import defaultdict

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
    heuristic_guess[start_node] = h(start_node)
    
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
                heuristic_guess[neighbour_node] = new_cheapest_path + h(neighbour_node)
                
                if neighbour_node is not open_set:
                    open_set.add(neighbour_node)
        
    path = []
    if path_found:
        while target_node is not None:
            path.append(target_node)
            target_node = parents[target_node]
        path.reverse()
    
    return path

def h(n):
    return 0

if __name__ == "__main__":
     adj_list = {
        'A': [('B', 1), ('C', 4)],
        'B': [('A', 1), ('C', 2), ('D', 5)],
        'C': [('A', 4), ('B', 2), ('D', 1)],
        'D': [('B', 5), ('C', 1)]
    }
    graph = {
    'P1': [('P2', 50), ('P3', 80), ('P8', 60)],
    'P2': [('P1', 50), ('P6', 20)],
    'P3': [('P1', 80), ('P4', 30)],
    'P4': [('P3', 30), ('P5', 40)],
    'P5': [('P4', 40), ('P7', 15)],
    'P6': [('P2', 20), ('P7', 10)],
    'P7': [('P6', 10), ('P5', 15)],
    'P8': [('P1', 60)]
}
    
    start_node = 'A'
    target_node = 'D'
    
    path = astar(adj_list, start_node, target_node, h)
    
    if path:
        print(f"Najkraći put od {start_node} do {target_node} je: {path}")
    else:
        print(f"Nema puta od {start_node} do {target_node}.")