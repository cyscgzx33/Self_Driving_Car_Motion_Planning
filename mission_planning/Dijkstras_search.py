'''
we will be relying on the OSMNX library to generate Python graphs from Open Street Map (OSM) data. 
These graphs will be represented using the NetworkX library. 
Both of these links are to the documentation, 
which you will find useful in this assessment.
'''

import osmnx as ox
import networkx as nx
import queue
import math
import priority_dict

map_graph = ox.graph_from_place('Berkeley, California', network_type='drive')
origin = ox.get_nearest_node(map_graph, (37.8743, -122.277))
destination = list(map_graph.nodes())[-1]

shortest_path = nx.shortest_path(map_graph, origin, destination, weight='length')
fig, ax = ox.plot_graph_route(map_graph, shortest_path)


# For a given graph, origin vertex key, and goal vertex key,
# computes the shortest path in the graph from the origin vertex
# to the goal vertex using Dijkstra's algorithm.
# Returns the shortest path as a list of vertex keys.
def dijkstras_search(origin_key, goal_key, graph):
    
    # The priority queue of open vertices we've reached.
    # Keys are the vertex keys, vals are the distances.
    open_queue = priority_dict.priority_dict({})
    
    # The dictionary of closed vertices we've processed.
    closed_dict = {}
    
    # The dictionary of predecessors for each vertex.
    predecessors = {}
    
    # Add the origin to the open queue.
    open_queue[origin_key] = 0.0

    # Iterate through the open queue, until we find the goal.
    # Each time, perform a Dijkstra's update on the queue.
    # TODO(done): Implement the Dijstra update loop.
    goal_found = False
    while (open_queue):
        vtx, dis = open_queue.pop_smallest()
        if (vtx == goal_key):
            goal_found = True
            break
        for edge in graph.out_edges([vtx], data=True):
            next_vtx = edge[1]
            if next_vtx in closed_dict:
                continue
            weight = edge[2]['length']
            if next_vtx in open_queue:
                if dis + weight < open_queue[next_vtx]:
                    open_queue[next_vtx] = dis + weight
                    predecessors[next_vtx] = vtx
            else:
                open_queue.update( {next_vtx : dis + weight} )
                predecessors.update( {next_vtx : vtx} )
        closed_dict[vtx] = dis
    
    # If we get through entire priority queue without finding the goal,
    # something is wrong.
    if not goal_found:
        raise ValueError("Goal not found in search.")
    
    # Construct the path from the predecessors dictionary.
    return get_path(origin_key, goal_key, predecessors)



# This function follows the predecessor
# backpointers and generates the equivalent path from the
# origin as a list of vertex keys.
def get_path(origin_key, goal_key, predecessors):
    key = goal_key
    path = [goal_key]
    
    while (key != origin_key):
        key = predecessors[key]
        path.insert(0, key)
        
    return path


path = dijkstras_search(origin, destination, map_graph)        
fig, ax = ox.plot_graph_route(map_graph, path) 