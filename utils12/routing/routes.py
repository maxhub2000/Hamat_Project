import pandas as pd
import numpy as np 
import itertools
from ast import literal_eval
from utils12.routing.distances import *
from utils12.routing.tsp import two_opt

def create_picking_route_greedy(origin_loc, list_locs, y_low, y_high):
    '''Calculate total distance to cover for a list of locations'''
    # Total distance variable
    wave_distance = 0
    # Current location variable 
    start_loc = origin_loc
    # Store routes
    list_chemin = []
    list_chemin.append(start_loc)

    #print("new while:\n")
    while len(list_locs) > 0: # Looping until all locations are picked
        # Going to next location
        list_locs, start_loc, next_loc, distance_next = next_location(start_loc, list_locs, y_low, y_high)
        #print("list_locs inside create_picking_route_greedy func: ", list_locs)
        # Update start_loc 
        start_loc = next_loc
        list_chemin.append(start_loc)
        #print("list_chemin inside create_picking_route_greedy func: ", list_chemin, "\n")
        # Update distance
        wave_distance += distance_next 

    # Distance from last location to origin_loc
    wave_distance += distance_picking(start_loc, origin_loc, y_low, y_high)
    list_chemin.append(origin_loc)

    #print("last list_chemin inside create_picking_route_greedy func: ", list_chemin, "\n")

    return wave_distance, list_chemin






######### 2_OPT ############

def create_picking_route_2_OPT(origin_loc, list_locs, y_low, y_high):
    '''Calculate total distance to cover for a list of locations for 2_opt algorithm'''
    # Total distance variable
    wave_distance = 0
    # Store routes
    list_chemin = []
    # Add origin_loc
    list_chemin.append(origin_loc)
    # covert list to numpy object 
    np_list_locs = np.array(list_locs)
    print("np_list_locs: ", np_list_locs)
    # Set improvement threshold
    improvement_threshold = 0.001
    # Find a good route with 2-opt ("route" gives the order in which to travel to each location by row number.)
    route, route_distance = two_opt(np_list_locs, improvement_threshold, y_low, y_high)
    # Add locations in root to list_chemin 
    list_chemin.extend(route)
    # Update wave_distance
    wave_distance += route_distance
    # Distance from origin_loc to first location
    wave_distance += distance_picking(origin_loc, route[0], y_low, y_high)
    # Distance from last location to origin_loc
    wave_distance += distance_picking(route[-1], origin_loc, y_low, y_high)
    list_chemin.append(origin_loc)


    return wave_distance, list_chemin


######### 2_OPT ############





####### Simulated annealing #######

def create_picking_route_SA(origin_loc, list_locs, y_low, y_high):
    '''Calculate total distance to cover for a list of locations for Simulated Annealing algorithm'''
    # Total distance variable
    wave_distance = 0
    # Current location variable 
    start_loc = origin_loc
    # Store routes
    list_chemin = []
    list_chemin.append(start_loc)

    while len(list_locs) > 0: # Looping until all locations are picked
        # Going to next location
        list_locs, start_loc, next_loc, distance_next = next_location(start_loc, list_locs, y_low, y_high)
        # Update start_loc 
        start_loc = next_loc
        list_chemin.append(start_loc)
        # Update distance
        wave_distance += distance_next 

    # Distance from last location to origin_loc
    wave_distance += distance_picking(start_loc, origin_loc, y_low, y_high)
    list_chemin.append(origin_loc)

    return wave_distance, list_chemin



### SPECIAL FUNCTION FOR SIMULATED ANNEALING

def get_neighbors(route):
    # choose 3 random unique indeces
    indeces = np.random.choice(list(range(len(route))), 3, replace=False)
    i,j,k = indeces[0], indeces[1], indeces[2]
    # initialize neighbors list
    neighbors = []
    # initialize copies of route
    new_route1, new_route2, new_route3 = route.copy(), route.copy(), route.copy()
    # create new neighbors
    new_route1[i],new_route1[j] =  route[j], route[i]
    new_route2[j],new_route2[k] =  route[k], route[j]
    new_route3[k],new_route3[i] =  route[i], route[k]
    neighbors.extend([new_route1, new_route2, new_route3])
    return neighbors

### SPECIAL FUNCTION FOR SIMULATED ANNEALING



def create_picking_route_SA_for_project(origin_loc, list_locs, y_low, y_high):
    pass



####### Simulated annealing #######



























# Calculate total distance to cover for a list of locations
def create_picking_route_cluster(origin_loc, list_locs, y_low, y_high):
    # Total distance variable
    wave_distance = 0
    # Distance max
    distance_max = 0
    # Current location variable 
    start_loc = origin_loc
    # Store routes
    list_chemin = []
    list_chemin.append(start_loc)
    while len(list_locs) > 0: # Looping until all locations are picked
        # Going to next location
        list_locs, start_loc, next_loc, distance_next = next_location(start_loc, list_locs, y_low, y_high)
        # Update start_loc 
        start_loc = next_loc
        list_chemin.append(start_loc)
        if distance_next > distance_max:
            distance_max = distance_next
        # Update distance
        wave_distance = wave_distance + distance_next 
    # Final distance from last storage location to origin
    wave_distance = wave_distance + distance_picking(start_loc, origin_loc, y_low, y_high)
    list_chemin.append(origin_loc)
    return wave_distance, list_chemin, distance_max