import json, os, pickle

import numpy as np
import pandas as pd
from collections import namedtuple
from datetime import datetime

import plotly
import plotly.plotly as py
import plotly.graph_objs as go

import dash
import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output, State
import dash_table as dt


Plotly_API_Key = 123##
Google_Maps_API_Key = 123##
Map_Box_Access_Token = 123##
plotly.tools.set_credentials_file(username='User', api_key=Plotly_API_Key)


external_stylesheets = ['https://codepen.io/chriddyp/pen/bWLwgP.css']
app = dash.Dash(__name__, external_stylesheets = external_stylesheets)
app.config['suppress_callback_exceptions'] = True

##################################################################################
############## Importing Preprocessed Pickled Dataset ############################
##################################################################################
variables_dict = pickle.load(open('variables_dict.p', 'rb'))

order_items_time_customer_loc_data = variables_dict['order_items_time_customer_loc_data']
order_items_time_seller_loc_data = variables_dict['order_items_time_seller_loc_data']
order_items_time_data = variables_dict['order_items_time_data']
orders_data = variables_dict['orders_data']
customers_data = variables_dict['customers_data']
geolocation_data = variables_dict['geolocation_data']
order_items_data = variables_dict['order_items_data']
payments_data = variables_dict['payments_data']
reviews_data = variables_dict['reviews_data']
products_data = variables_dict['products_data']
sellers_data = variables_dict['sellers_data']

################### Color Coding of categories in map plots ########################

cat_dict = {'garden_tools' : 'black',
 'electronics' : 'cyan',
 'fashion_bags_accessories' : 'yellow',
 'luggage_accessories' : 'red',
 'office_furniture' : 'black',
 'small_appliances_home_oven_and_coffee' : 'black',
 'bed_bath_table' : 'black',
 'home_construction' : 'black',
 'auto' : 'black',
 'consoles_games' : 'cyan',
 'perfumery' : 'yellow',
 'cool_stuff' : 'cyan',
 'construction_tools_construction' : 'black',
 'sports_leisure' : 'white',
 'health_beauty' : 'white',
 'computers_accessories' : 'cyan',
 'costruction_tools_tools' : 'black',
 'flowers' : 'yellow',
 'furniture_decor' : 'black',
 'computers' : 'cyan',
 'market_place' : 'red',
 'home_appliances' : 'black',
 'housewares' : 'black',
 'telephony' : 'cyan',
 'christmas_supplies' : 'red',
 'fixed_telephony' : 'black',
 'small_appliances' : 'black',
 'baby': 'green',
 'stationery' : 'red',
 'home_appliances_2' : 'black',
 'toys': 'green',
 'pet_shop' : 'red',
 'watches_gifts' : 'cyan',
 'home_confort' : 'black'}


day_dict = {0: 'Monday',
1: 'Tuesday',
2: 'Wednesday',
3: 'Thursday',
4: 'Friday',
5: 'Saturday',
6: 'Sunday'
}

###########################################################
################ Order time pattern analysis ##############
###########################################################

##### Pattern by Hours in the day ######
order_items_purchases = order_items_time_data[['Hour', 'Weekday', 'order_purchase_timestamp','Approval_Time','Purchased_to_Shipped', 'Shipped_to_Delivered', 'price']]
purchase_time_stats_1 = order_items_purchases[['Hour', 'price']].groupby('Hour').count().reset_index()
#purchase_time_stats.plot.bar(x = 'Hour', y = 'price')

payment_contrib = payments_data[['payment_value', 'payment_type']].groupby('payment_type').sum().reset_index()

##### Pattern by weekdays ######
purchase_time_stats = order_items_purchases[['Weekday', 'price']].groupby('Weekday').count().reset_index()
purchase_time_stats['Weekday'] = purchase_time_stats.apply(lambda row : day_dict[row['Weekday']] , axis= 1)

##### Timeseries orders ###########
orders_per_day = order_items_purchases[['order_purchase_timestamp', 'price']].groupby(pd.Grouper(key = 'order_purchase_timestamp', freq = '1M')).count().reset_index()

#############################################################
########## Category Analysis ################################
#############################################################

order_items_frieght = order_items_time_seller_loc_data[['product_id','seller_state','Shipped_to_Delivered', 'price', 'freight_value']]

######### Website earning is calculated as 0.1*(price-frieght value) (Assumption)#######################
order_items_frieght['Website_Earnings (BRL)'] = order_items_frieght.apply(lambda row: 0.1*(row['price'] - row['freight_value']), axis = 1)
seller_earnings_pivot = order_items_frieght[['seller_state', 'Website_Earnings (BRL)']].groupby('seller_state').sum().reset_index()

order_product_info = order_items_frieght.merge(products_data, on = 'product_id')

category_for_total_profit_ranking = order_product_info[['product_category_name_english', 'Website_Earnings (BRL)']].groupby('product_category_name_english').sum().sort_values(by = 'Website_Earnings (BRL)', ascending = False).reset_index()[:10]
category_for_profit_per_item_ranking = order_product_info[['product_category_name_english', 'Website_Earnings (BRL)']].groupby('product_category_name_english').mean().sort_values(by = 'Website_Earnings (BRL)', ascending = False).reset_index()[:10]
category_for_number_of_orders_ranking = order_product_info[['product_category_name_english', 'Website_Earnings (BRL)']].groupby('product_category_name_english').count().sort_values(by = 'Website_Earnings (BRL)', ascending = False).reset_index()[:10]

category_for_total_profit_ranking['Website_Earnings (BRL)'] = category_for_total_profit_ranking['Website_Earnings (BRL)'].astype(int)
category_for_profit_per_item_ranking['Website_Earnings (BRL)'] = category_for_profit_per_item_ranking['Website_Earnings (BRL)'].astype(int)
category_for_number_of_orders_ranking['Numbers Ordered'] = category_for_number_of_orders_ranking['Website_Earnings (BRL)'].astype(int)
category_for_number_of_orders_ranking = category_for_number_of_orders_ranking[['product_category_name_english', 'Numbers Ordered']]

product_info = order_items_time_customer_loc_data[['product_id','customer_state', 'price', 'freight_value', 'geolocation_lat', 'geolocation_lng']].merge(products_data, on = 'product_id')[['customer_state', 'price', 'freight_value', 'geolocation_lat', 'geolocation_lng', 'product_category_name_english']]
product_info['Website_Earnings'] = product_info.apply(lambda row: 0.1*(row['price'] - row['freight_value']), axis = 1)

category_contrib = product_info[['product_category_name_english', 'price']].groupby('product_category_name_english').sum().reset_index()

category_loc = product_info[['Website_Earnings', 'product_category_name_english', 'geolocation_lat', 'geolocation_lng']]
category_loc['Cat_Color'] = category_loc.apply(lambda row : cat_dict[row['product_category_name_english']] if row['product_category_name_english'] in cat_dict.keys() else 'grey', axis = 1)


################# Preparing a Dictionary of dataframes for the tables and Maps #######################

category_data = {'category_location' : category_loc,
    'Most Proffitable': category_for_total_profit_ranking,
    'Most Proffitable Per Item' : category_for_profit_per_item_ranking,
    'Most Ordered' : category_for_number_of_orders_ranking}

###############################################################
############## Location Analysis ##############################
###############################################################

##### Customer Locations #############
customer_locations = order_items_time_customer_loc_data[['geolocation_lat', 'geolocation_lng']].values
customer_city_contrib = order_items_time_customer_loc_data[['customer_city', 'price']].groupby('customer_city').sum().reset_index()


######## Seller Locations ########################
seller_locations = order_items_time_seller_loc_data[['geolocation_lat', 'geolocation_lng']].values
seller_city_contrib = order_items_time_seller_loc_data[['seller_city', 'price']].groupby('seller_city').sum().reset_index()

city_contrib_data = {'Customer Locations' : customer_city_contrib,
    'Seller Locations' : seller_city_contrib}


all_loc_data = {'Customer Locations' : order_items_time_customer_loc_data,
	'Seller Locations' : order_items_time_seller_loc_data}




################################################################
################### Mapbox Objects for Plotting ################
################################################################


graph_data = [
    go.Scattermapbox(
        lat=list(order_items_time_customer_loc_data['geolocation_lat']),
        lon=list(order_items_time_customer_loc_data['geolocation_lng']),
        mode='markers',
        marker=go.scattermapbox.Marker(
            size=[x**2/10000 for x in list(order_items_time_customer_loc_data['price'])]
        ))]


graph_layout = go.Layout(
    autosize=True,
    hovermode='closest',
    mapbox=go.layout.Mapbox(
        accesstoken=Map_Box_Access_Token,
        bearing=0,
        center=go.layout.mapbox.Center(
            lat=sum(list(order_items_time_customer_loc_data['geolocation_lat']))/len(list(order_items_time_customer_loc_data['geolocation_lat'])),
            lon=sum(list(order_items_time_customer_loc_data['geolocation_lng']))/len(list(order_items_time_customer_loc_data['geolocation_lng']))
        ),
        pitch=0,
        zoom=10
    ),
)


cat_graph_data = [
    go.Scattermapbox(
        lat=list(category_loc['geolocation_lat']),
        lon=list(category_loc['geolocation_lng']),
        mode='markers',
        marker=go.scattermapbox.Marker(
            size=9,
            color = category_loc['Cat_Color']),
        hovertext = category_loc['product_category_name_english']
        )]


cat_graph_layout = go.Layout(
    autosize=True,
    hovermode='closest',
    mapbox=go.layout.Mapbox(
        accesstoken=Map_Box_Access_Token,
        bearing=0,
        center=go.layout.mapbox.Center(
            lat=sum(list(category_loc['geolocation_lat']))/len(list(category_loc['geolocation_lat'])),
            lon=sum(list(category_loc['geolocation_lng']))/len(list(category_loc['geolocation_lng']))
        ),
        pitch=0,
        zoom=3
    ),
)



