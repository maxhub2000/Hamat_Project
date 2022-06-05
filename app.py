import pandas as pd
import numpy as np
import plotly.express as px
from sqlalchemy import true
from ast import literal_eval


from utils12.batch.simulation_batch import simulate_batch 
from utils12.results.plot import plot_simulation
from utils12.results.plot import plot_simulation_big


import streamlit as st
from streamlit import caching

from main import *
hamat_df_orderlines = df_filtered

# Set page configuration
st.set_page_config(page_title ="HAMAT Pre-assembly warehouse Picking Order Optimization",
                    initial_sidebar_state="expanded",
                    layout='wide',
                    page_icon="🛒")

# Set up the page
@st.cache(persist=False,
          allow_output_mutation=True,
          suppress_st_warning=True,
          show_spinner= True)

# Preparation of data
def load(filename, n):
    df_orderlines = pd.read_csv(IN + filename).head(n)
    return df_orderlines


# Prepare logo of hamat
img = "hamat_logo.png"
#st.image(img)
st.sidebar.image(img, use_column_width=True)

# Alley Coordinates on y-axis
#y_low, y_high = 5.5, 50
y_low, y_high = 4.0, 44 #Those are actually the y-coords of the highest and lowest shelf in the warehouse
# Origin Location
origin_loc = [0.0, 0.0]		
IN = 'static/in/'
# Store Results by WaveID
list_wid, list_dst, list_route, list_ord, list_lines, list_pcs, list_monomult = [], [], [], [], [], [], []
list_results = [list_wid, list_dst, list_route, list_ord, list_lines, list_pcs, list_monomult]	# Group in list
# Store Results by Simulation (Order_number)
list_ordnum , list_dstw = [], []


# MAX VARIABLES
forklift_attributes = {
	"item_capacity" : 7, 
	"item_loading_time" : 5, 
	"travel_speed" : 1.94
}

mathematic_alogorithms = ["greedy", "2-opt", "SA"]


## MAX IDEA
## maybe when picking number of lines, add option that allows to pick all 
## lines thats in orderlines.csv, like for example a button that says:
## "choose all lines", and it will make it to choose all order lines.

# Simulation 1: Order Batch
# SCOPE SIZE
#st.header("**🥇 Impact of the wave size in orders (Orders/Wave) **")
st.header("HAMAT Pre-assembly warehouse Picking Order Optimization")
st.subheader('''
        🛠️ HOW MANY ORDER LINES DO YOU WANT TO INCLUDE IN YOUR ANALYSIS?
    ''')
col1, col2 = st.columns(2)
with col1:
	n = st.slider(
				'SIMULATION 1 SCOPE (ORDERS BY INTERVALS OF 10)', 1, 20 , value = 2)
with col2:
	#lines_number = 1000 * n
	lines_number = 10 * n 
	st.write('''🛠️{:,} \
		order lines'''.format(lines_number))
# SIMULATION PARAMETERS
st.subheader('''
        🛠️ SIMULATE ORDER PICKING BY WAVE OF N ORDERS PER WAVE WITH N IN [N_MIN, N_MAX] ''')
col_11 , col_22 = st.columns(2)
with col_11:
	n1 = st.slider(
				'SIMULATION 1: N_MIN (ORDERS/WAVE)', 0, 20 , value = 7)
	n2 = st.slider(
				'SIMULATION 1: N_MAX (ORDERS/WAVE)', n1 + 1, 20 , value = int(np.max([n1+1 , 5])))
with col_22:
		st.write('''[N_MIN, N_MAX] = [{:,}, {:,}]'''.format(n1, n2))
# START CALCULATION
start_1= False
if st.checkbox('SIMULATION 1: START CALCULATION',key='show', value=False): # change value here to False later
	start_1 = True
# Calculation
if start_1:
	results_per_algorithm = {}
	for alg in mathematic_alogorithms:
		df_orderlines = load('df_lines.csv', lines_number)
		df_waves, df_results = simulate_batch(n1, n2, y_low, y_high, origin_loc, lines_number, df_orderlines, hamat_df_orderlines, forklift_attributes, alg)
		print("df_results of {} algorithm:\n".format(alg), df_results, "\n")
		#results_per_algorithm[alg] = {"df_waves" : df_waves, "df_results" : df_results} # we'll add that to plot_simulation1 func later
		results_per_algorithm[alg] = [df_waves , df_results]
		#plot_simulation1(df_results, lines_number, df_waves, alg, results_per_algorithm) # after we add the dict here, we'll move it out of the for loop
	
	plot_simulation(df_results, lines_number, df_waves, alg, results_per_algorithm)
		#break






# Simulation BIG
# SCOPE SIZE
#st.header("**🥇 Impact of the wave size in orders (Orders/Wave) **")
st.write("\n\n")
st.header("Research section")
st.subheader('''
        🛠️ HOW MANY ORDER LINES DO YOU WANT TO INCLUDE IN YOUR ANALYSIS?
    ''')
_col1, _col2 = st.columns(2)
with _col1:
	_n = st.slider(
				'SIMULATION BIG SCOPE (ORDERS BY INTERVALS OF 100)', 1, 20 , value = 2)
with _col2:
	#lines_number = 1000 * n
	_lines_number = 100 * _n 
	st.write('''🛠️{:,} \
		order lines'''.format(_lines_number))
# SIMULATION PARAMETERS
st.subheader('''
        🛠️ SIMULATE ORDER PICKING BY WAVE OF N ORDERS PER WAVE WITH N IN [N_MIN, N_MAX] ''')
_col_11 , _col_22 = st.columns(2)
with _col_11:
	_n1 = st.slider(
				'SIMULATION BIG: N_MIN (ORDERS/WAVE)', 0, 20 , value = 5)
	_n2 = st.slider(
				'SIMULATION BIG: N_MAX (ORDERS/WAVE)', _n1 + 1, 20 , value = 16)
with _col_22:
		st.write('''[N_MIN, N_MAX] = [{:,}, {:,}]'''.format(_n1, _n2))
# START CALCULATION
start_big= True
if st.checkbox('SIMULATION BIG: START CALCULATION',key='show_big', value=False): # change value here to False later
	start_big = True
# Calculation
if start_big:
	counter = 0
	df_big_results = pd.DataFrame(columns=['order_per_wave', 'distance', 'total_picking_time', 'total_loading_time'])

	for j in range(0, _lines_number, 20):
		start = j
		end = j + 20
		results_per_algorithm = {}
		counter += 1
		print("counter: ",counter)
		for alg in mathematic_alogorithms:
			
			df_orderlines = load('df_lines.csv', lines_number)
			sliced_hamat_df_orderlines = hamat_df_orderlines.copy()[start:end]
			sliced_hamat_df_orderlines.drop_duplicates(subset ="coords", keep = "first", inplace = True)
			#print("sliced_hamat_df_orderlines:\n", sliced_hamat_df_orderlines)
			#print("len(sliced_hamat_df_orderlines): ",len(sliced_hamat_df_orderlines))
			new_lines_number = len(sliced_hamat_df_orderlines)
			_sliced_hamat_df_orderlines = sliced_hamat_df_orderlines.copy()
			#break
			df_waves, df_results = simulate_batch(_n1, _n2, y_low, y_high, origin_loc, new_lines_number, df_orderlines, _sliced_hamat_df_orderlines, forklift_attributes, alg)
			
			df_big_results = df_big_results.append(df_results, ignore_index = True)
			
			
			print("df_results of {} algorithm:\n".format(alg), df_results, "\n")
			results_per_algorithm[alg] = [df_waves , df_results]
	print("df_big_results:\n", df_big_results)
	df_big_results_grouped = df_big_results.groupby('order_per_wave')[['distance', 'total_picking_time', 'total_loading_time']].agg({'distance':'mean','total_picking_time':'mean','total_loading_time':'mean' })
	df_big_results_grouped.columns = ['mean_distance', 'mean_picking_time', 'mean_loading_time']
	print("df_big_results_grouped:\n", df_big_results_grouped)
	plot_simulation_big(df_big_results_grouped)
			#break















# # Simulation 2: Order Batch using Spatial Clustering 
# # SCOPE SIZE
# #st.header("**🥈 Impact of the order batching method **")
# st.subheader('''
#         🛠️ HOW MANY ORDER LINES DO YOU WANT TO INCLUDE IN YOUR ANALYSIS?
#     ''')
# col1, col2 = st.columns(2)
# with col1:
# 	n_ = st.slider(
# 				'SIMULATION 2 SCOPE (ORDERS BY INTERVALS OF 10)', 1, 20 , value = 5)
# with col2:
# 	lines_2 = 10 * n_ 
# 	st.write('''🛠️{:,} \
# 		order lines'''.format(lines_2))
# # START CALCULATION
# start_2 = False
# if st.checkbox('SIMULATION 2: START CALCULATION',key='show_2', value=False):
#     start_2 = True
# # Calculation
# if start_2:
# 	df_orderlines = load('df_lines.csv', lines_2)
# 	df_reswave, df_results = simulation_cluster(y_low, y_high, df_orderlines, list_results, n1, n2, 
# 			distance_threshold)
# 	#print(df_reswave)
# 	plot_simulation2(df_reswave, lines_2, distance_threshold)