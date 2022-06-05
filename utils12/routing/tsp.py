# tsp.py
from calendar import c
import numpy as np
import random

##### MAX LINES:
from utils12.routing.distances import distance_picking


def get_route_distance(route, route_to_locations_dict, y_low, y_high):
    new_locations = [route_to_locations_dict[r] for r in route]
    total_dist = 0
    for i in range(len(new_locations)-1):
        total_dist += distance_picking(new_locations[i], new_locations[i+1], y_low, y_high)
    return total_dist



# Calculate the euclidian distance in n-space of the route r traversing locations c, ending at the path start.
#path_distance = lambda r,c: np.sum([np.linalg.norm(c[r[p]]-c[r[p-1]]) for p in range(len(r))])
# Reverse the order of all elements from element i to element k in array r.
two_opt_swap = lambda r,i,k: np.concatenate((r[0:i],r[k:-len(r)+i-1:-1],r[k+1:len(r)]))

def two_opt(locations, improvement_threshold, y_low, y_high):
    poss_locs = [[4, 33],[12, 17], [4, 11] ,[10, 27], [22, 35], [6, 37], [8, 11], [16, 37],
                [12, 29] ,[16, 25] ,[10, 37], [18, 33] ,[22, 31],[20, 43],[16, 17], [14, 25], [16, 35], [10, 9], [22, 11]]
    random.shuffle(poss_locs)

    if len(locations) <2:
        locations = np.array(poss_locs[0:8])


    print("\nlen(locations): ", len(locations), "\n") 
    route = np.arange(locations.shape[0]) # Make an array of row numbers corresponding to locations.
    route_to_locations_dict = {r : list(locations[r]) for r in route} # Dict to hold locations of locations.
    
    improvement_factor = 1 # Initialize the improvement factor.
    #best_distance = path_distance(route,locations) # Calculate the distance of the initial path.    
    best_distance = get_route_distance(route, route_to_locations_dict, y_low, y_high) # Calculate the distance of the initial path.
    while improvement_factor > improvement_threshold: # If the route is still improving, keep going!
        distance_to_beat = best_distance # Record the distance at the beginning of the loop.
        print("\ndistance_to_beat: ", distance_to_beat, "\n")
        print("\nroute: ", route, "\n")
        for swap_first in range(1,len(route)-2): # From each location except the first and last,
            for swap_last in range(swap_first+1,len(route)): # to each of the locations following,
                new_route = two_opt_swap(route,swap_first,swap_last) # try reversing the order of these locations
                #new_distance = path_distance(new_route,locations) # and check the total distance with this modification.
                new_distance = get_route_distance(new_route, route_to_locations_dict, y_low, y_high) # and check the total distance with this modification.
                if new_distance < best_distance: # If the path distance is an improvement,
                    route = new_route # make this the accepted best route
                    best_distance = new_distance # and update the distance corresponding to this route.
        improvement_factor = 1 - best_distance/distance_to_beat # Calculate how much the route has improved.
    
    last_distance = get_route_distance(route, route_to_locations_dict, y_low, y_high) # Get distance for latest route.
    locations_in_route = [route_to_locations_dict[r] for r in route] # Get the locatios.
    return locations_in_route, last_distance # When the route is no longer improving substantially, stop searching and return the route and the distance.