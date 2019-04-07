import dash
import dash_core_components as dcc
import dash_html_components as html
import requests

url = "http://backend-service:8000/hello/hello"

result = requests.get(url)

external_stylesheets = ['https://codepen.io/chriddyp/pen/bWLwgP.css']

app = dash.Dash(__name__, external_stylesheets=external_stylesheets)
app.config.suppress_callback_exceptions = True


app.layout = html.Div(children=[
    html.H3(children=str(result)),

    html.Div(children='''
        Dash: A web application framework for Pyshhon2.
    ''' + str(result.content[1:1000])),

    dcc.Graph(
        id='example-graph',
        figure={
            'data': [
                {'x': [1, 2, 3], 'y': [4, 1, 2], 'type': 'bar', 'name': 'result'},
                {'x': [1, 2, 3], 'y': [2, 4, 5], 'type': 'bar', 'name': 'Montreal'},
            ],
            'layout': {
                'title': 'Dash Data Visualization'
            }
        }
    )
])




if __name__ == '__main__':
    app.run_server(host='0.0.0.0',debug=True, port=8050)