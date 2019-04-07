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
from EC_Objects import *
import dash_table as dt


app.layout = html.Div(children =
	[
	html.Div(id='output-data-upload', hidden  = True),
	html.Div(children = 
		[
		html.H1('e-commerce Dashboard', className = 'five columns'),
	    ], className = 'twelve columns'),
	html.Div(children = 
		[
		dcc.Tabs(id="tabs", value='tab-1', children=[
			dcc.Tab(label='Overall Summaries', value='tab-1'),
			dcc.Tab(label='Order Traffic Stats', value='tab-2'),
			dcc.Tab(label='Location Information', value='tab-3'),
			dcc.Tab(label='Category Information', value='tab-4')]),
		html.Div(id='tabs-content'),
		],className = 'twelve columns'),
	html.Div(id='intermediate-value', style={'display': 'none'}),
	html.Div(id='intermediate-value-full', style={'display': 'none'}),
	], className = 'row', style = {'marginRight': 50, 'marginLeft': 100, 'marginBottom': 50, 'marginTop': 25, 'fontSize': 12})

##########################################################################################
########################## The Tabs Callback #############################################
##########################################################################################

@app.callback(Output('tabs-content', 'children'),
              [Input('tabs', 'value')])
def render_content(tab):
    if tab == 'tab-1':
        return html.Div([
            # html.H3('Overall Summaries'),
            # Pie Charts for payment types, pie charts for categories, pie charts for time series earnings
            dcc.Graph(
                id='pie-2-tab-1',
                figure={
                    'data': [{
                        'values': payment_contrib['payment_value'],
                        'labels': payment_contrib['payment_type'],
                        'type': 'pie'
                    }],
                    'layout' : {
    					'height':700,
                    	}
                },
                className = 'twelve columns'
            ),
            dcc.Graph(
                id='pie-1-tab-1',
                figure={
                    'data': [{
                        'values': category_contrib['price'],
                        'labels': category_contrib['product_category_name_english'],
                        'type': 'pie'
                    }],
                    'layout' : {
    					'height':700,
                    	}
                },
                className = 'twelve columns'
            ),
            dcc.Graph(
                id='line-1-tab-1',
                figure={
                    'data': [{
                        'x': orders_per_day['order_purchase_timestamp'],
                        'y': orders_per_day['price'],
                        'type': 'line'
                    }]
                },
                className = 'twelve columns'
            )

        ])
    elif tab == 'tab-2':
        return html.Div([
            # html.H3('Order Traffic Stats'),
            # Bar Charts for hourly and weekly traffic
            dcc.Graph(
                id='bar-1-tab-2',
                figure={
                    'data': [{
                        'x': purchase_time_stats_1['Hour'],
                        'y': purchase_time_stats_1['price'],
                        'type': 'bar'
                    }]
                }
            ),
            dcc.Graph(
                id='bar-2-tab-2',
                figure={
                    'data': [{
                        'x': purchase_time_stats['Weekday'],
                        'y': purchase_time_stats['price'],
                        'type': 'bar'
                    }]
                }
            )
        ])
    elif tab == 'tab-3':
        return html.Div([
            # html.H3('Location Information'),
            # Maps Stuff with dropdowns for different kinds of categories
            dcc.Dropdown(
			    options=[
			        {'label': 'Customer Locations', 'value': 'Customer Locations'},
			        {'label': 'Seller Locations', 'value': 'Seller Locations'}
			    ],
			    value='Customer Locations',
			    id = 'drop-1-tab-3'),
            html.Div(children = [
            	dcc.Graph(
				figure = go.Figure(
					data = graph_data,
					layout = graph_layout
					),
			id = 'map-1-tab-3'),
            	]),
            dcc.Graph(
                id='bar-1-tab-3',
                figure={
                    'data': [{
                        'x': [1, 2, 3],
                        'y': [15, 10, 12],
                        'type': 'bar'
                    }]
                }
            )])
    elif tab == 'tab-4':

        return html.Div([
            # html.H3('Categories Information'),
            # Maps stuff with dropdowns for different categories
            dcc.Dropdown(
			    options=[
			        {'label': 'Most Proffitable', 'value': 'Most Proffitable'},
			        {'label': 'Most Proffitable Per Item', 'value': 'Most Proffitable Per Item'},
			        {'label': 'Most Ordered', 'value': 'Most Ordered'}
			    ],
			    value='Most Proffitable',
			    id = 'drop-1-tab-4'),

			dt.DataTable(
			    columns=[{"name": i, "id": i} for i in category_for_total_profit_ranking.columns],
			    data=category_for_total_profit_ranking.to_dict("rows"),
			    id = 'table-1-tab-4'),
            dcc.Graph(
                id='bar-1-tab-4',
                figure={
                    'data': [{
                        'x': [1, 2, 3],
                        'y': [5, 8, 1],
                        'type': 'bar'
                    }]
                }
            ),
            dcc.Graph(
				figure = go.Figure(
					data = cat_graph_data,
					layout = cat_graph_layout
					),
			id = 'map-1-tab-4')
        ])



########################### Callbacks for adjusting state charts #########################
#############################################################################################
@app.callback(Output('bar-1-tab-3', 'figure'),
              [Input('drop-1-tab-3', 'value')])
def render_content1(drop_value):

	data_frame_1 = city_contrib_data[drop_value]
	
	if drop_value == 'Customer Locations':
		city_col = 'customer_city'
	else:
		city_col = 'seller_city'
	return {'data': [{
                        'x': data_frame_1[city_col],
                        'y': data_frame_1['price'],
                        'type': 'bar'
                    }]}



########################### Callbacks for adjusting category tables #########################
#############################################################################################
@app.callback(Output('table-1-tab-4', 'data'),
              [Input('drop-1-tab-4', 'value')])
def render_content(drop_value):

	data_frame_1 = category_data[drop_value]

	return data_frame_1.to_dict("rows")

@app.callback(Output('table-1-tab-4', 'columns'),
              [Input('drop-1-tab-4', 'value')])
def render_content(drop_value):

	data_frame_1 = category_data[drop_value]

	return [{"name": i, "id": i} for i in data_frame_1.columns]


####################### Callbacks for adjusting category graphs ################################
################################################################################################
@app.callback(Output('bar-1-tab-4', 'figure'),
              [Input('drop-1-tab-4', 'value')])
def render_tables(drop_value):

	data_frame_1 = category_data[drop_value]

	if drop_value != 'Most Ordered':
		column_value = 'Website_Earnings (BRL)'
	else:
		column_value = 'Numbers Ordered'

	return {'data': [{
                    'x': data_frame_1['product_category_name_english'],
                    'y': data_frame_1[column_value],
                    'type': 'bar'
                }]
            }


####################### Callbacks for adjusting location maps ##################################
################################################################################################

@app.callback(Output('map-1-tab-3', 'figure'),
              [Input('drop-1-tab-3', 'value')])
def render_graph(drop_value):

	data_frame = all_loc_data[drop_value]

	graph_data = [
	    go.Scattermapbox(
	        lat=list(data_frame['geolocation_lat']),
	        lon=list(data_frame['geolocation_lng']),
	        mode='markers',
	        marker=go.scattermapbox.Marker(
	            size=9
	        ))]


	graph_layout = go.Layout(
	    autosize=True,
	    hovermode='closest',
	    mapbox=go.layout.Mapbox(
	        accesstoken=Map_Box_Access_Token,
	        bearing=0,
	        center=go.layout.mapbox.Center(
	            lat=sum(list(data_frame['geolocation_lat']))/len(list(data_frame['geolocation_lat'])),
	            lon=sum(list(data_frame['geolocation_lng']))/len(list(data_frame['geolocation_lng']))
	        ),
	        pitch=0,
	        zoom=3
	    ),)

	return go.Figure(
					data = graph_data,
					layout = graph_layout
					)



if __name__ == '__main__':
	app.run_server(debug = True)