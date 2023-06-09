# Daily Report Potensi Kepadatan BMS

# import package
from dash import Dash, dcc, html
from dash import dash_table

from flask import Flask
from werkzeug.middleware.dispatcher import DispatcherMiddleware

import datetime
import locale

import functions


# = start code = #

server = Flask(__name__)

app1 = Dash(__name__, server=server, url_base_pathname='/app1/')
app2 = Dash(__name__, server=server, url_base_pathname='/app2/')
app3 = Dash(__name__, server=server, url_base_pathname='/app3/')

app1.title = "Daily Report BMS T1"
app2.title = "Daily Report BMS T2"
app3.title = "Daily Report BMS T3"


## Get today's date
today = datetime.datetime.today().strftime('%Y-%m-%d')

# Set the locale to Indonesian
locale.setlocale(locale.LC_ALL, 'id_ID.utf8')
# Format the date as per Indonesian locale
hari_ini = datetime.date.today().strftime("%A, %d %B %Y")


# Collecting data
data_t1, df_t1, time_t1, list_ovtime_t1, meanT1, mean_plusT1, mean_minT1 = functions.collect_data(today, 1)
data_t2, df_t2, time_t2, list_ovtime_t2, meanT2, mean_plusT2, mean_minT2 = functions.collect_data(today, 2)
data_t3, df_t3, time_t3, list_ovtime_t3, meanT3, mean_plusT3, mean_minT3 = functions.collect_data(today, 3)

## Generating graph
image_t1 = functions.generate_graph(df_t1, 1, today, hari_ini)
image_t2 = functions.generate_graph(df_t2, 2, today, hari_ini)
image_t3 = functions.generate_graph(df_t3, 3, today, hari_ini)

## generating text
text_t1 = functions.generate_text(list_ovtime_t1)
text_t2 = functions.generate_text(list_ovtime_t2)
text_t3 = functions.generate_text(list_ovtime_t3)


# Layout T1
app1.layout = html.Div(
    style={
        "background-image": "url('assets/BG_T1.png')",
        "background-repeat": "no-repeat",
        "background-size": "cover",
        "height": "3020px",
        "width": "100%"
    },
    children=[
       html.Div(
           style={               
                'display': 'flex',
                'justify-content': 'center',
                'align-items': 'center',
           },
           children=[
                html.Div(
                    style={
                        "position": "absolute",                 
                        "top": "510px",
                            },
                    children=[
                        html.H1(
                            children="Hari "+hari_ini, className="header-title", 
                            style={
                            "text-align": "center",
                            'fontSize': '72px',
                            'font-family': 'Raleway',
                            'fontWeight': 'bold',
                            'color' : 'black',
                            }
                        ),

                    ]
        ),
        ]
       ),

        ### TEXT
        html.Div(
            style={
                'display': 'flex',
                'justify-content': 'center',
                'align-items': 'center',
            },
            children=[
                 html.P(
                    style={"position": "absolute", 
                            "top": "1750px", 
                            'fontSize': '46px',
                            'font-family': 'Raleway',
                            'fontWeight': 'bold',
                            "text-align": "center",
                                        },
                        children=[
                            'Pada pukul ',
                            html.Span(time_t1[0]+' – '+time_t1[-1], style={'color': 'red', 'fontSize': '46px',}),
                            ' memiliki jumlah scheduled arrival flight',
                            html.Br(),
                            ' yang lebih dari rata-rata, ',
                            html.Span('sehingga perlu disiapkan antisipasi', style={'color': 'red', 'fontSize': '46px',}),
                            html.Br(),
                            ' pada rentang waktu tersebut.'
                        ]
                    ),
                    ]
        ),
      
    
        html.Div(
            style={"position": "absolute", 
                    "top": "2070px",
                    "right": "180px" 
                    },
            children=[                
                html.P(
                    style={
                        'fontSize': '42px',
                        'font-family': 'Raleway',
                        'fontWeight': 'bold'
                                },
                    children=[
                        'Estimasi lonjakan penumpang ',
                    html.Br(),
                        'terjadi pada pukul: ',
                    dcc.Markdown(children=text_t1,
                                style={
                                    'fontSize': '42px',
                                    'font-family': 'Roboto',
                                    'fontWeight': 'bold',
                                    'color': 'red',
                                    }),      
                    'Di Terminal 1 pada rentang waktu tersebut',
                    html.Br(),
                    'memerlukan perhatian khusus oleh ',
                    html.Br(),
                    'tim yang bertugas.']),
                ]
        ),### TEXT TERMINAL 1 - END

    
        ### DESIGN TERMINAL 1 - START
        html.Div(
            style={"display": "flex"},
            children=[
                html.Img(
                    src='data:image/png;base64,{}'.format(image_t1),
                    style={"position": "absolute",
                            "top": "1000px", 
                            "left": "100px",
                            'height': '750px', 
                            'width': '1900px'
                            }
                           ),        
                html.Div(
                    style={"position": "absolute", 
                           "top": "2070px", 
                            "left": "20%",
                           },
                    children=[
                        dash_table.DataTable(
                            id='table',
                            columns=[{'name': col, 'id': col} for col in data_t1[0].keys()],
                            data=data_t1,
                            style_data_conditional=[
                                {
                                    'if': {
                                        'column_id': 'ARRIVAL FLIGHT',
                                        'filter_query': f'{{ARRIVAL FLIGHT}} < {meanT1}'
                                    },
                                    'backgroundColor': 'lightgreen',
                                    'color': 'black'
                                },
                                {
                                    'if': {
                                        'column_id': 'ARRIVAL FLIGHT',
                                        'filter_query': f'{{ARRIVAL FLIGHT}} >= {meanT1} && {{ARRIVAL FLIGHT}} < {mean_plusT1}'
                                    },
                                    'backgroundColor': 'lemonchiffon',
                                    'color': 'black'
                                },
                                {
                                    'if': {
                                        'column_id': 'ARRIVAL FLIGHT',
                                        'filter_query': f'{{ARRIVAL FLIGHT}} >= {mean_plusT1}'
                                    },
                                    'backgroundColor': 'lightcoral',
                                    'color': 'black'
                                },
                                {
                                    'if': {
                                        'column_id': 'TIME',
                                        'filter_query': f'{{ARRIVAL FLIGHT}} < {meanT1}'
                                    },
                                    'backgroundColor': 'lightgreen',
                                    'color': 'black'
                                },
                                {
                                    'if': {
                                        'column_id': 'TIME',
                                        'filter_query': f'{{ARRIVAL FLIGHT}} >= {meanT1} && {{ARRIVAL FLIGHT}} < {mean_plusT1}'
                                    },
                                    'backgroundColor': 'lemonchiffon',
                                    'color': 'black'
                                },
                                {
                                    'if': {
                                        'column_id': 'TIME',
                                        'filter_query': f'{{ARRIVAL FLIGHT}} >= {mean_plusT1}'
                                    },
                                    'backgroundColor': 'lightcoral',
                                    'color': 'black'
                                },
                            ],
                            style_data={'backgroundColor': '#f2f2f2', 'color': 'black'},
                            style_header={'backgroundColor': 'black', 'fontWeight': 'bold', 'color': 'white', 'width': '20px'},
                            style_cell={
                                        'textAlign': 'center',
                                        'fontSize': '28px',
                                        'height': '45px',
                                        'width': '125px'
                                        }
                        )
        
                    ]
                ),
            ],
            className="wrapper",
        ), ### DESIGN TERMINAL 1 - END

    ]
)

# Layout T2
app2.layout = html.Div(
    style={
        "background-image": "url('assets/BG_T2.png')",
        "background-repeat": "no-repeat",
        "background-size": "cover",
        "height": "3020px",
        "width": "100%"
    },
    children=[
       html.Div(
           style={               
                'display': 'flex',
                'justify-content': 'center',
                'align-items': 'center',
           },
           children=[
                html.Div(
                    style={
                        "position": "absolute",                 
                        "top": "510px",
                            },
                    children=[
                        html.H1(
                            children="Hari "+hari_ini, className="header-title", 
                            style={
                            "text-align": "center",
                            'fontSize': '72px',
                            'font-family': 'Raleway',
                            'fontWeight': 'bold',
                            'color' : 'black',
                            }
                        ),

                    ]
        ),
        ]
       ),

        ### TEXT - START
        html.Div(
            style={
                'display': 'flex',
                'justify-content': 'center',
                'align-items': 'center',
            },
            children=[
                 html.P(
                    style={"position": "absolute", 
                            "top": "1750px", 
                            'fontSize': '46px',
                            'font-family': 'Raleway',
                            'fontWeight': 'bold',
                            "text-align": "center",
                                        },
                        children=[
                            'Pada pukul ',
                            html.Span(time_t2[0]+' – '+time_t2[-1], style={'color': 'red', 'fontSize': '46px',}),
                            ' memiliki jumlah scheduled arrival flight',
                            html.Br(),
                            ' yang lebih dari rata-rata, ',
                            html.Span('sehingga perlu disiapkan antisipasi', style={'color': 'red', 'fontSize': '46px',}),
                            html.Br(),
                            ' pada rentang waktu tersebut.'
                        ]
                    ),
                    ]
        ),
      
    
        html.Div(
            style={"position": "absolute", 
                    "top": "2070px",
                    "right": "180px" 
                    },
            children=[                
                html.P(
                    style={
                        'fontSize': '42px',
                        'font-family': 'Raleway',
                        'fontWeight': 'bold'
                                },
                    children=[
                        'Estimasi lonjakan penumpang ',
                    html.Br(),
                        'terjadi pada pukul: ',
                    dcc.Markdown(children=text_t2,
                                style={
                                    'fontSize': '42px',
                                    'font-family': 'Roboto',
                                    'fontWeight': 'bold',
                                    'color': 'red',
                                    }),      
                    'Di Terminal 2 pada rentang waktu tersebut',
                    html.Br(),
                    'memerlukan perhatian khusus oleh ',
                    html.Br(),
                    'tim yang bertugas.']),
                ]
        ),### TEXT - END

    
        ### DESIGN - START
        html.Div(
            style={"display": "flex"},
            children=[
                html.Img(
                    src='data:image/png;base64,{}'.format(image_t2),
                    style={"position": "absolute",
                            "top": "1000px", 
                            "left": "100px",
                            'height': '750px', 
                            'width': '1900px'
                            }
                           ),        
                html.Div(
                    style={"position": "absolute", 
                           "top": "2070px", 
                            "left": "20%",
                           },
                    children=[
                        dash_table.DataTable(
                            id='table',
                            columns=[{'name': col, 'id': col} for col in data_t2[0].keys()],
                            data=data_t2,
                            style_data_conditional=[
                                {
                                    'if': {
                                        'column_id': 'ARRIVAL FLIGHT',
                                        'filter_query': f'{{ARRIVAL FLIGHT}} < {meanT2}'
                                    },
                                    'backgroundColor': 'lightgreen',
                                    'color': 'black'
                                },
                                {
                                    'if': {
                                        'column_id': 'ARRIVAL FLIGHT',
                                        'filter_query': f'{{ARRIVAL FLIGHT}} >= {meanT2} && {{ARRIVAL FLIGHT}} < {mean_plusT2}'
                                    },
                                    'backgroundColor': 'lemonchiffon',
                                    'color': 'black'
                                },
                                {
                                    'if': {
                                        'column_id': 'ARRIVAL FLIGHT',
                                        'filter_query': f'{{ARRIVAL FLIGHT}} >= {mean_plusT2}'
                                    },
                                    'backgroundColor': 'lightcoral',
                                    'color': 'black'
                                },
                                {
                                    'if': {
                                        'column_id': 'TIME',
                                        'filter_query': f'{{ARRIVAL FLIGHT}} < {meanT2}'
                                    },
                                    'backgroundColor': 'lightgreen',
                                    'color': 'black'
                                },
                                {
                                    'if': {
                                        'column_id': 'TIME',
                                        'filter_query': f'{{ARRIVAL FLIGHT}} >= {meanT2} && {{ARRIVAL FLIGHT}} < {mean_plusT2}'
                                    },
                                    'backgroundColor': 'lemonchiffon',
                                    'color': 'black'
                                },
                                {
                                    'if': {
                                        'column_id': 'TIME',
                                        'filter_query': f'{{ARRIVAL FLIGHT}} >= {mean_plusT2}'
                                    },
                                    'backgroundColor': 'lightcoral',
                                    'color': 'black'
                                },
                            ],
                            style_data={'backgroundColor': '#f2f2f2', 'color': 'black'},
                            style_header={'backgroundColor': 'black', 'fontWeight': 'bold', 'color': 'white', 'width': '20px'},
                            style_cell={
                                        'textAlign': 'center',
                                        'fontSize': '28px',
                                        'height': '45px',
                                        'width': '125px'
                                        }
                        )
        
                    ]
                ),
            ],
            className="wrapper",
        ), ### DESIGN - END

    ]
)

# Layout T3
app3.layout = html.Div(
    style={
        "background-image": "url('assets/BG_T3.png')",
        "background-repeat": "no-repeat",
        "background-size": "cover",
        "height": "3020px",
        "width": "100%"
    },
    children=[
       html.Div(
           style={               
                'display': 'flex',
                'justify-content': 'center',
                'align-items': 'center',
           },
           children=[
                html.Div(
                    style={
                        "position": "absolute",                 
                        "top": "510px",
                            },
                    children=[
                        html.H1(
                            children="Hari "+hari_ini, className="header-title", 
                            style={
                            "text-align": "center",
                            'fontSize': '72px',
                            'font-family': 'Raleway',
                            'fontWeight': 'bold',
                            'color' : 'black',
                            }
                        ),

                    ]
        ),
        ]
       ),

        ### TEXT - START
        html.Div(
            style={
                'display': 'flex',
                'justify-content': 'center',
                'align-items': 'center',
            },
            children=[
                 html.P(
                    style={"position": "absolute", 
                            "top": "1750px", 
                            'fontSize': '46px',
                            'font-family': 'Raleway',
                            'fontWeight': 'bold',
                            "text-align": "center",
                                        },
                        children=[
                            'Pada pukul ',
                            html.Span(time_t3[0]+' – '+time_t3[-1], style={'color': 'red', 'fontSize': '46px',}),
                            ' memiliki jumlah scheduled arrival flight',
                            html.Br(),
                            ' yang lebih dari rata-rata, ',
                            html.Span('sehingga perlu disiapkan antisipasi', style={'color': 'red', 'fontSize': '46px',}),
                            html.Br(),
                            ' pada rentang waktu tersebut.'
                        ]
                    ),
                    ]
        ),
      
    
        html.Div(
            style={"position": "absolute", 
                    "top": "2070px",
                    "right": "180px" 
                    },
            children=[                
                html.P(
                    style={
                        'fontSize': '42px',
                        'font-family': 'Raleway',
                        'fontWeight': 'bold'
                                },
                    children=[
                        'Estimasi lonjakan penumpang ',
                    html.Br(),
                        'terjadi pada pukul: ',
                    dcc.Markdown(children=text_t3,
                                style={
                                    'fontSize': '42px',
                                    'font-family': 'Roboto',
                                    'fontWeight': 'bold',
                                    'color': 'red',
                                    }),      
                    'Di Terminal 3 pada rentang waktu tersebut',
                    html.Br(),
                    'memerlukan perhatian khusus oleh ',
                    html.Br(),
                    'tim yang bertugas.']),
                ]
        ),### TEXT - END

    
        ### DESIGN - START
        html.Div(
            style={"display": "flex"},
            children=[
                html.Img(
                    src='data:image/png;base64,{}'.format(image_t3),
                    style={"position": "absolute",
                            "top": "1000px", 
                            "left": "100px",
                            'height': '750px', 
                            'width': '1900px'
                            }
                           ),        
                html.Div(
                    style={"position": "absolute", 
                           "top": "2070px", 
                            "left": "20%",
                           },
                    children=[
                        dash_table.DataTable(
                            id='table',
                            columns=[{'name': col, 'id': col} for col in data_t3[0].keys()],
                            data=data_t3,
                            style_data_conditional=[
                                {
                                    'if': {
                                        'column_id': 'ARRIVAL FLIGHT',
                                        'filter_query': f'{{ARRIVAL FLIGHT}} < {meanT3}'
                                    },
                                    'backgroundColor': 'lightgreen',
                                    'color': 'black'
                                },
                                {
                                    'if': {
                                        'column_id': 'ARRIVAL FLIGHT',
                                        'filter_query': f'{{ARRIVAL FLIGHT}} >= {meanT3} && {{ARRIVAL FLIGHT}} < {mean_plusT3}'
                                    },
                                    'backgroundColor': 'lemonchiffon',
                                    'color': 'black'
                                },
                                {
                                    'if': {
                                        'column_id': 'ARRIVAL FLIGHT',
                                        'filter_query': f'{{ARRIVAL FLIGHT}} >= {mean_plusT3}'
                                    },
                                    'backgroundColor': 'lightcoral',
                                    'color': 'black'
                                },
                                {
                                    'if': {
                                        'column_id': 'TIME',
                                        'filter_query': f'{{ARRIVAL FLIGHT}} < {meanT3}'
                                    },
                                    'backgroundColor': 'lightgreen',
                                    'color': 'black'
                                },
                                {
                                    'if': {
                                        'column_id': 'TIME',
                                        'filter_query': f'{{ARRIVAL FLIGHT}} >= {meanT3} && {{ARRIVAL FLIGHT}} < {mean_plusT3}'
                                    },
                                    'backgroundColor': 'lemonchiffon',
                                    'color': 'black'
                                },
                                {
                                    'if': {
                                        'column_id': 'TIME',
                                        'filter_query': f'{{ARRIVAL FLIGHT}} >= {mean_plusT3}'
                                    },
                                    'backgroundColor': 'lightcoral',
                                    'color': 'black'
                                },
                            ],
                            style_data={'backgroundColor': '#f2f2f2', 'color': 'black'},
                            style_header={'backgroundColor': 'black', 'fontWeight': 'bold', 'color': 'white', 'width': '20px'},
                            style_cell={
                                        'textAlign': 'center',
                                        'fontSize': '28px',
                                        'height': '45px',
                                        'width': '125px'
                                        }
                        )
        
                    ]
                ),
            ],
            className="wrapper",
        ), ### DESIGN - END
    ]
)


# Create the DispatcherMiddleware to combine multiple apps
application = DispatcherMiddleware(server, {
    '/app1': app1.server,
    '/app2': app2.server,
    '/app3': app3.server,
})

if __name__ == '__main__':
    server.run(debug=True)


