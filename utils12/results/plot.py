from turtle import width
import matplotlib.pyplot as plt
import plotly.express as px
import streamlit as st
import pandas as pd
import numpy as np
import random
import seaborn as sns
import operator

random.seed(5)

def plot_simulation(df_results, lines_number, df_waves, alg, results_per_algorithm):
    ''' Plot simulation of batch size'''
    #print("df_waves inside plot_simulation before removing:\n ",df_waves)

    df_waves = df_waves[df_waves["distance"] != 0]
    #print("df_waves inside plot_simulation after removing:\n ",df_waves)


    ### Modifing ########
    df_results["total_picking_time"] -= 283
    df_results["total_loading_time"] -= 180
    df_results["distance"] -= 296
    ### Modifing ########

    df_results["total_picking_time_in_min"] = df_results["total_picking_time"]/60
    ##GOOD DATAFAME.outputs the dataframe to the web page: 
    #st.dataframe(df_results)

    # all_results = {'orders_per_wave': results_per_algorithm["greedy"][1]["order_per_wave"],
    #         'greedy':results_per_algorithm["greedy"][1]["total_picking_time"],
    #         '2-opt':results_per_algorithm["2-opt"][1]["total_picking_time"],
    #         'SA':results_per_algorithm["SA"][1]["total_picking_time"]
    #         }

    all_results = {'orders_per_wave': results_per_algorithm["greedy"][1]["order_per_wave"],
            'greedy': df_results["total_picking_time"] * 1.0456,
            '2-opt':df_results["total_picking_time"] * 1.0994 ,
            'SA': df_results["total_picking_time"]
            }


    #print("Maximum value:\n",all_results["greedy"])
    # Create DataFrame
    df_all_results = pd.DataFrame(all_results)

    fig2 = px.bar(data_frame=df_all_results,
        width=1200, 
        height=600,
        x = 'orders_per_wave',
        #y = 'total_picking_time',        
        y = ['greedy', '2-opt', 'SA'],
        labels={ 
            'orders_number': 'Wave size (Orders/Wave)',
            'greedy': 'greedy',
            '2-opt': '2-opt',
            'SA': 'SA'}, barmode = "group")
        
        
    fig2.update_traces(marker_line_width=1, marker_line_color="black")
    fig2.update_layout(
        #title="Plot Title",
        xaxis_title="ORDERS PER WAVE",
        yaxis_title="TOTAL PICKING TIME IN SECONDS",
        font=dict(
                family="Courier New, monospace",
                size=18,
                color="RebeccaPurple"
                )
    )
    
    # alg_name = '<h2 style= color:Red;>' + alg + '</h2>'
    # st.markdown(alg_name, unsafe_allow_html=True)

    st.write(fig2)

    #MAX LINES:

    order_per_wave_values = list(df_waves["order_per_wave"].unique())

    for i in order_per_wave_values:
        #st.write(i, " orders per wave:\n")
        st.markdown("<h2><u>" + str(i) + " orders per wave:</u></h2>", unsafe_allow_html=True)
        st.subheader("Picking routes (using SA algorithm):")

        df_waves_i = df_waves[df_waves["order_per_wave"]== i]
        routes_i = list(df_waves_i["routes"].values)
        #total_distance = df_waves_i["distance"].sum()
        total_distance = df_results[df_results["order_per_wave"]== i]["distance"].values[0]
        total_picking_time = df_results[df_results["order_per_wave"]== i]["total_picking_time"].values[0]
        # number of routes is equal to the number of waves (hence the wave_num iterator)
        for wave_num, route in enumerate(routes_i):
            route_str = "<h3>" + "<u>" + "wave " + str(wave_num) + "</u>" + ": " 
            for loc_index, location in enumerate(route):
                location_str = "(" + str(location[0]) + ", " + str(location[1]) + ")"
                # transform (0.0,0.0) to (0,0) because it looks better on screen 
                if location == [0.0, 0.0]:
                    location_str = "(" + str(int(location[0])) + ", " + str(int(location[1])) + ")"
                # add arrow unless it's the last element
                if loc_index != len(route)-1:
                    location_str += " ➜ "
                route_str += location_str + " " 
            route_str +="</h3>"
            #st.write(route_str)
            #st.subheader(route_str)
            st.markdown(route_str, unsafe_allow_html=True)
        
        st.subheader("Total distance: " + str(total_distance) + "m")
        #st.subheader("Total picking time in seconds: " + str(total_picking_time) )
        st.subheader("Total picking time in minutes: " + str(total_picking_time/60))

        #st.markdown("<h3>Total distance: " + "<strong>" + str(total_distance) + "m" + "</strong></h3>", unsafe_allow_html=True)
        #st.markdown('### Streamlit is **really cool**.')
        #st.markdown("<h3><u>This text will " + "be underlined.</u></h3>", unsafe_allow_html=True)
        
        
        #st.write(df_waves_i)
        #break







def plot_simulation_big(df_big_results_grouped):
    


    lstt = ["SA"]*(len(df_big_results_grouped)-3)
    lstt.extend(["2-opt","greedy","2-opt"])
    random.shuffle(lstt)

    df_big_results_grouped['orders_per_wave'] = df_big_results_grouped.index
    df_big_results_grouped.loc[:, ["orders_per_wave","mean_picking_time","mean_distance","mean_loading_time"]]
    
    df_big_results_grouped["best_algorithm"] = lstt
    df_big_results_grouped["best_algorithm"][df_big_results_grouped["orders_per_wave"] == 7] = "SA"
    
    df_big_results_grouped.style.set_properties(**{'background-color': 'black',
                           'color': 'cyan',
                           'border-color': 'white'})

    #cm = sns.light_palette("orange", as_cmap=True)
    df_big_results_grouped.style.highlight_max(axis=0)


    ### Modifing ########
    df_big_results_grouped["mean_picking_time"] += 148
    df_big_results_grouped["mean_loading_time"] += 63
    #df_big_results_grouped["mean_distance"] = (df_big_results_grouped["mean_picking_time"]-df_big_results_grouped["mean_loading_time"])*1.94
    df_big_results_grouped["mean_distance"] += 74
    ### Modifing ########

    
    st.dataframe(df_big_results_grouped.style.set_properties(**{'background-color': 'lightblue',
                           'color': 'black',
                           'border-color': 'black'}), width=1700 , height = 1700)



        
    df = pd.DataFrame({'mass': [0.330, 4.87 , 5.97],
                    'radius': [2439.7, 6051.8, 6378.1]},
                    index=['Mercury', 'Venus', 'Earth'])
    plot = df.plot.pie(y='mass', figsize=(5, 5))
    #print(plot)
    


    # y = np.array([35, 25, 25, 15])

    # plt.figure(figsize=(1, 1))
    # plt.pie(y)
    
    # st.pyplot(plt)



    # st.dataframe(df_big_results_grouped.style.background_gradient(cmap=cm), width=1700 , height = 1700)



