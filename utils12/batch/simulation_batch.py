
from turtle import distance
from utils12.batch.mapping_batch import *
from utils12.cluster.mapping_cluster import *
from utils12.routing.routes import *


def simulation_wave(y_low, y_high, origin_loc, orders_number, df_orderlines, list_wid, list_dst, list_route, list_ord, hamat_df_orderlines, forklift_attributes, mathematic_alogorithm):
	''' Simulate of total picking distance with n orders per wave'''
	distance_route = 0 
	# Create waves
	df_orderlines, waves_number = orderlines_mapping(df_orderlines, orders_number)


	df_orderlines.to_csv(r'exported_df_orderlines.csv', index = False)
	df_orderlines = pd.read_csv("C:/Users/maxpo/OneDrive/Desktop/Hamat_picking_route/imported_df_orderlines.csv")
	waves_number = 2
	#hamat_df_orderlines["orderline_id"] = list(range(len(hamat_df_orderlines)))
	#print("\nhamat_df_orderlines before mapping:\n ", hamat_df_orderlines, "\n")
	hamat_df_orderlines['WaveID'] = (hamat_df_orderlines.orderline_id%orders_number == 0).shift(1).fillna(0).cumsum() 
	#print("\nhamat_df_orderlines AFTER mapping:\n ", hamat_df_orderlines, "\n")

	#hamat_df_orderlines = hamat_df_orderlines.groupby('WaveID').filter(lambda x : (x['WaveID'].count()>=2).any())
	#print("\nhamat_df_orderlines after changing wave_id:\n ", hamat_df_orderlines, "\n")

	
	df_orderlines = hamat_df_orderlines.copy()
	#waves_number = df_orderlines.WaveID.max() + 1
	waves_number = df_orderlines.WaveID.unique().size + 1
	# rename columns
	df_orderlines.columns = ['OrderID', 'PCS', 'Coord', 'WaveID']

	for wave_id in range(waves_number):
		# Listing of all locations for this wave
		#print("\ndf_orderlines inside simulation_wave func:\n ", df_orderlines, "\n")
		list_locs, n_locs, n_lines, n_pcs = locations_listing(df_orderlines, wave_id)
		#print("\nlist_locs inside simulation_wave func: ", list_locs, "\n")
		# Results


		#mathematic_alogorithm = "Greedy"

		## raise error if mathematic_alogorithm is not in the list (because of typo for example)
		if mathematic_alogorithm not in ["greedy", "2-opt", "SA"]:
			raise ValueError("No implementation for '{}' alogorithm here, ".format(mathematic_alogorithm)+ \
				"but hey it's ok man we all make mistakes")


		if mathematic_alogorithm == "greedy":
			wave_distance, list_chemin = create_picking_route_greedy(origin_loc, list_locs, y_low, y_high)
		elif mathematic_alogorithm == "2-opt":
			wave_distance, list_chemin = create_picking_route_2_OPT(origin_loc, list_locs, y_low, y_high)
		elif mathematic_alogorithm == "SA":
			wave_distance, list_chemin = create_picking_route_SA(origin_loc, list_locs, y_low, y_high)
    			
		#print("list_chemin inside simulation_wave func: ", list_chemin, "\n")
		distance_route = distance_route + wave_distance
		list_wid.append(wave_id)
		list_dst.append(wave_distance)
		list_route.append(list_chemin)
		list_ord.append(orders_number)
	return list_wid, list_dst, list_route, list_ord, distance_route

def simulate_batch(n1, n2, y_low, y_high, origin_loc, orders_number, df_orderlines, hamat_df_orderlines, forklift_attributes, mathematic_alogorithm):
	''' Loop with several scenarios of n orders per wave'''
	# Lists for results
	list_wid, list_dst, list_route, list_ord = [], [], [], []
	# Test several values of orders per wave
	for orders_number in range(n1, n2 + 1):
		list_wid, list_dst, list_route, list_ord, distance_route = simulation_wave(y_low, y_high, origin_loc, orders_number, 
		df_orderlines, list_wid, list_dst, list_route, list_ord, hamat_df_orderlines, forklift_attributes, mathematic_alogorithm)
		
		# print("Total distance covered for {} orders/wave: {:,} m".format(orders_number, distance_route))

		# print("\n")
		# print("list_route(first few points): ","\n",list_route[-5:-1],"\n")

	# By Wave
	df_waves = pd.DataFrame({'wave': list_wid,
				'distance': list_dst,
				'routes': list_route,
				'order_per_wave': list_ord})

	

	# print("third to last route: ","\n",df_waves["routes"].iloc[-3])
	# print("second to last route: ","\n",df_waves["routes"].iloc[-2])
	# print("last route: ","\n",df_waves["routes"].iloc[-1])

	# Results aggregate
	df_results = pd.DataFrame(df_waves.groupby(['order_per_wave'])['distance'].sum())
	df_results.columns = ['distance']

	#print("\ndf_results:\n",df_results, "\nhamat_df_orderlines:\n", hamat_df_orderlines)
	
	total_picking_times, total_loading_time = calculate_total_picking_time(df_results, forklift_attributes, hamat_df_orderlines )
	df_results["total_picking_time"], df_results["total_loading_time"] = total_picking_times, total_loading_time
	return df_waves, df_results.reset_index()



def calculate_total_picking_time(df_results, forklift_attributes, hamat_df_orderlines):
	# get total amount of units in the order
	total_num_of_units = hamat_df_orderlines["PCS"].sum()
	# get total loading time in the order
	total_loading_time = total_num_of_units * forklift_attributes["item_loading_time"]
	# get distances
	picking_distances = df_results["distance"].tolist()
	# get travel speed of forklift 
	speed = forklift_attributes["travel_speed"]
	# calculate total picking time of the order 
	total_picking_times = [((distance/speed) + total_loading_time) for distance in picking_distances] 
	return total_picking_times, total_loading_time