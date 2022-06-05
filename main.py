import pandas as pd
import numpy as np
import plotly.express as px
from sqlalchemy import true
from ast import literal_eval


def create_locations_ids_coords_dicts():
    '''Create 2 dictionaries: one where the keys are the locations_ids in
       in the warehouse and the values are the coords of those locations, 
       and a second one that is vice versa'''
    # prepare the empty dicts
    locations_ids_to_coords_dict = dict()
    coords_to_locations_ids_dict = dict()
    # create locations ids and coords using a nested loop, and fill the dictionaries
    loc_count = 0
    for col in range(5, 45, 2):
        for row in range(4, 24, 2):
            loc_count +=1
            locations_ids_to_coords_dict[loc_count] = "[{}, {}]".format(row,col)
            coords_to_locations_ids_dict["[{}, {}]".format(row,col)] = loc_count
    # return the dictionaries
    return locations_ids_to_coords_dict, coords_to_locations_ids_dict


def distance_from_I_O(Loc):
    '''Calculate Distance between the I/O point (0,0) and the given location'''
    x, y = Loc
    return x + y  #distance from (0,0)


def allocate_items_to_locations(coords_to_locations_ids_dict, locations_ids_to_coords_dict, file_name):
    ''' This function allocates items to locations in the warehouse based on their
    distance from I/O location and their frequency in orders (the more frequent 
    they are, the closer they should be to the I/O location). '''
    # sort locations by distance from I/O in ascending order
    sorted_locations = sorted(locations_ids_to_coords_dict.values(),
                              key=lambda loc: distance_from_I_O(literal_eval(loc)))
    # get list of items sorted by their frequency in orders in descending order
    item_frequencies = pd.read_csv(file_name)
    items_ordered_by_frequency = item_frequencies["item_id"].tolist()
    # create df with item_id and coords 
    df_locations_of_items = pd.DataFrame({"item_id": items_ordered_by_frequency,
                             "coords": sorted_locations})
    # match the location ids to the coords 
    ordered_location_ids = [coords_to_locations_ids_dict[coord] for coord in sorted_locations]
    df_locations_of_items["location_id"] = ordered_location_ids 
    # remove coords collumn and switch order of columns
    df_locations_of_items = df_locations_of_items[["location_id", "item_id"]]
    # order the rows by loaction_id in ascending order
    df_locations_of_items = df_locations_of_items.sort_values(by=["location_id"])
    return df_locations_of_items


# read the input file of orderlines
df_hamat_orderlines = pd.read_csv("orderlines.csv")
#df_hamat_orderlines = pd.read_csv("orderlines_big.csv")

#print("df_hamat_orderlines: ",df_hamat_orderlines)


# create needed dicts using the create_locations_ids_coords_dicts function
locations_ids_to_coords_dict, coords_to_locations_ids_dict = create_locations_ids_coords_dicts()
# craete a df of location ids and coords using the above dicts
df_locations = pd.DataFrame({"location_id": locations_ids_to_coords_dict.keys(),
                             "coords": locations_ids_to_coords_dict.values() })
# Make the allocation of items to locations by creating a df
df_hamat_locations_of_items = allocate_items_to_locations(coords_to_locations_ids_dict, locations_ids_to_coords_dict, "item_frequencies.csv")
print("allocate_items_to_locations:\n", df_hamat_locations_of_items, "\n")
# Join all of our df based on specific collumns 
df_joined = pd.merge(df_hamat_orderlines,df_hamat_locations_of_items,on='item_id')
df_joined_2 = pd.merge(df_joined, df_locations, on='location_id')
print("df_joined_2: \n", df_joined_2, "\n")
# Get only the relevant columns for the running of the algorithms
df_filtered = df_joined_2.filter(["orderline_id","PCS", "coords"])
df_filtered = df_filtered.sort_values("orderline_id")
print("df_filtered: \n",df_filtered)


print(df_filtered["coords"].values)

# asdf = df_filtered["coords"].values
# gggg = []
# for i in range(1,len(asdf),4):
#     gggg.append(asdf[i]






# import pandas as pd
 
# # making data frame from csv file
# data = df_filtered
 
# # sorting by first name
# data.sort_values("coords", inplace = True)

# print(data[200:230])

# # dropping ALL duplicate values
# data.drop_duplicates(subset ="coords", keep = "first", inplace = True)
 
# # displaying data
# print(data)
# print(len(data))
