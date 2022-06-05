import numpy as np
import pandas as pd
import itertools
from ast import literal_eval


def orderlines_mapping(df_orderlines, orders_number):
	'''Mapping orders with wave number'''
	#print("started running inside orderlines_mapping func\n")
	df_orderlines.sort_values(by='DATE', ascending = True, inplace = True)
	# Unique order numbers list
	list_orders = df_orderlines.OrderNumber.unique()
	#print("\n","list_orders:\n",list_orders,"\n")
	dict_map = dict(zip(list_orders, [i for i in range(1, len(list_orders))]))
	#print("\n","dict_map:\n",dict_map,"\n")
	#print("\n","\n","\n","\n",dict_map,"\n","\n","\n","\n")
	# Order ID mapping
	df_orderlines['OrderID'] = df_orderlines['OrderNumber'].map(dict_map)
	#print("\n","df_orderlines after adding OrderID :\n",df_orderlines,"\n")
	#print("\n","\n","\n","\n",df_orderlines,"\n","\n","\n","\n")
	# Grouping Orders by Wave of orders_number 
	df_orderlines['WaveID'] = (df_orderlines.OrderID%orders_number == 0).shift(1).fillna(0).cumsum()
	#print("\n","df_orderlines after adding WaveID :\n",df_orderlines,"\n")
	#print("\n","\n","\n","\n",df_orderlines,"\n","\n","\n","\n")
	# Counting number of Waves
	waves_number = df_orderlines.WaveID.max() + 1
	return df_orderlines, waves_number

def locations_listing(df_orderlines, wave_id):
	'''Getting storage locations to cover for a wave of orders'''
	df = df_orderlines[df_orderlines.WaveID == wave_id]
	#print("df inside locations_listing:\n ", df)
	# Create coordinates listing
	list_locs = list(df['Coord'].apply(lambda t: literal_eval(t)).values)
	#print("df:","\n","\n","\n","\n",df,"\n","\n","\n","\n")
	#print("list_locs:","\n",list_locs)
	list_locs.sort()
	# List of unique coordinates
	list_locs = list(k for k,_ in itertools.groupby(list_locs))
	n_locs = len(list_locs)
	return list_locs, n_locs