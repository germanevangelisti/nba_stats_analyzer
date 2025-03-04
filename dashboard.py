#!/usr/bin/env python
# -*- coding: utf-8 -*-

import dash
from dash import dcc, html, Input, Output, callback
import plotly.express as px
import plotly.graph_objects as go
import pandas as pd
import os
import base64
from urllib.request import urlopen, Request
import io
import time
import random
from PIL import Image
from svglib.svglib import svg2rlg
from reportlab.graphics import renderPM
import numpy as np
import glob
import json
import datetime
import matplotlib.pyplot as plt
import seaborn as sns
import requests
from io import BytesIO
from bs4 import BeautifulSoup

# Verificar si existe la carpeta visualizaciones y crearla si no existe
if not os.path.exists('visualizaciones'):
    os.makedirs('visualizaciones')

# Crear un directorio para almacenar los logos localmente
if not os.path.exists('logos'):
    os.makedirs('logos')

# Mapeo de equipos de la NBA a sus abreviaturas para obtener logos
team_to_abbr = {
    'Atlanta Hawks': 'ATL',
    'Boston Celtics': 'BOS',
    'Brooklyn Nets': 'BKN',
    'Charlotte Hornets': 'CHA',
    'Chicago Bulls': 'CHI',
    'Cleveland Cavaliers': 'CLE',
    'Dallas Mavericks': 'DAL',
    'Denver Nuggets': 'DEN',
    'Detroit Pistons': 'DET',
    'Golden State Warriors': 'GSW',
    'Houston Rockets': 'HOU',
    'Indiana Pacers': 'IND',
    'LA Clippers': 'LAC',
    'Los Angeles Lakers': 'LAL',
    'Memphis Grizzlies': 'MEM',
    'Miami Heat': 'MIA',
    'Milwaukee Bucks': 'MIL',
    'Minnesota Timberwolves': 'MIN',
    'New Orleans Pelicans': 'NOP',
    'New York Knicks': 'NYK',
    'Oklahoma City Thunder': 'OKC',
    'Orlando Magic': 'ORL',
    'Philadelphia 76ers': 'PHI',
    'Phoenix Suns': 'PHX',
    'Portland Trail Blazers': 'POR',
    'Sacramento Kings': 'SAC',
    'San Antonio Spurs': 'SAS',
    'Toronto Raptors': 'TOR',
    'Utah Jazz': 'UTA',
    'Washington Wizards': 'WAS'
}

# Colores primarios de equipos para gráficos
team_colors = {
    'Atlanta Hawks': '#E03A3E',
    'Boston Celtics': '#007A33',
    'Brooklyn Nets': '#000000',
    'Charlotte Hornets': '#1D1160',
    'Chicago Bulls': '#CE1141',
    'Cleveland Cavaliers': '#860038',
    'Dallas Mavericks': '#00538C',
    'Denver Nuggets': '#0E2240',
    'Detroit Pistons': '#C8102E',
    'Golden State Warriors': '#1D428A',
    'Houston Rockets': '#CE1141',
    'Indiana Pacers': '#002D62',
    'LA Clippers': '#C8102E',
    'Los Angeles Lakers': '#552583',
    'Memphis Grizzlies': '#5D76A9',
    'Miami Heat': '#98002E',
    'Milwaukee Bucks': '#00471B',
    'Minnesota Timberwolves': '#0C2340',
    'New Orleans Pelicans': '#0C2340',
    'New York Knicks': '#006BB6',
    'Oklahoma City Thunder': '#007AC1',
    'Orlando Magic': '#0077C0',
    'Philadelphia 76ers': '#006BB6',
    'Phoenix Suns': '#1D1160',
    'Portland Trail Blazers': '#E03A3E',
    'Sacramento Kings': '#5A2D81',
    'San Antonio Spurs': '#C4CED4',
    'Toronto Raptors': '#CE1141',
    'Utah Jazz': '#002B5C',
    'Washington Wizards': '#002B5C'
}

# Fuentes alternativas de logos
logo_sources = [
    lambda abbr, team_id: f'https://cdn.nba.com/logos/nba/{team_id}/primary/L/logo.svg',
]

# Función para obtener el ID del equipo a partir de la abreviatura
def get_team_id_from_abbr(abbr):
    team_id_map = {
        'ATL': 1610612737,
        'BOS': 1610612738,
        'BKN': 1610612751,
        'CHA': 1610612766,
        'CHI': 1610612741,
        'CLE': 1610612739,
        'DAL': 1610612742,
        'DEN': 1610612743,
        'DET': 1610612765,
        'GSW': 1610612744,
        'HOU': 1610612745,
        'IND': 1610612754,
        'LAC': 1610612746,
        'LAL': 1610612747,
        'MEM': 1610612763,
        'MIA': 1610612748,
        'MIL': 1610612749,
        'MIN': 1610612750,
        'NOP': 1610612740,
        'NYK': 1610612752,
        'OKC': 1610612760,
        'ORL': 1610612753,
        'PHI': 1610612755,
        'PHX': 1610612756,
        'POR': 1610612757,
        'SAC': 1610612758,
        'SAS': 1610612759,
        'TOR': 1610612761,
        'UTA': 1610612762,
        'WAS': 1610612764
    }
    return team_id_map.get(abbr, "")

# Función para obtener el logo de un equipo
def get_team_logo(team_name):
    try:
        abbr = team_to_abbr.get(team_name)
        if not abbr:
            print(f"No se encontró abreviatura para {team_name}")
            return None
        
        # Obtener el ID del equipo
        team_id = get_team_id_from_abbr(abbr)
        
        # Verificar si ya hemos guardado el logo localmente
        logo_path = f'logos/{abbr}.svg'
        if os.path.exists(logo_path) and os.path.getsize(logo_path) > 0:
            try:
                with open(logo_path, 'rb') as f:
                    logo_data = f.read()
                # Codificar SVG para uso en plotly
                encoded_image = base64.b64encode(logo_data).decode('ascii')
                return f"data:image/svg+xml;base64,{encoded_image}"
            except Exception as e:
                print(f"Error con logo local {abbr}: {e}, intentando descargar de nuevo")
                # Si hay un error, eliminar el archivo corrupto y continuar
                os.remove(logo_path)
        
        # Usar la URL oficial de la NBA
        logo_url = f'https://cdn.nba.com/logos/nba/{team_id}/primary/L/logo.svg'
        
        try:
            print(f"Descargando logo desde: {logo_url}")
            
            headers = {
                'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
            }
            
            req = Request(url=logo_url, headers=headers)
            response = urlopen(req, timeout=10)
            logo_data = response.read()
            
            # Guardar el SVG localmente
            with open(logo_path, 'wb') as f:
                f.write(logo_data)
            
            # Codificar SVG para uso en plotly
            encoded_image = base64.b64encode(logo_data).decode('ascii')
            return f"data:image/svg+xml;base64,{encoded_image}"
            
        except Exception as e:
            print(f"Error al obtener logo para {team_name}: {e}")
            return None
    
    except Exception as e:
        print(f"Error general al obtener el logo para {team_name}: {e}")
        return None

# Obtener el color del equipo
def get_team_color(team_name):
    return team_colors.get(team_name, '#1D428A')  # Color predeterminado NBA azul

# Función para obtener el ID del equipo a partir del nombre
def get_team_id(team_name):
    # Mapeo de nombres de equipos a IDs oficiales de la NBA
    team_ids = {
        'Atlanta Hawks': 1610612737,
        'Boston Celtics': 1610612738,
        'Brooklyn Nets': 1610612751,
        'Charlotte Hornets': 1610612766,
        'Chicago Bulls': 1610612741,
        'Cleveland Cavaliers': 1610612739,
        'Dallas Mavericks': 1610612742,
        'Denver Nuggets': 1610612743,
        'Detroit Pistons': 1610612765,
        'Golden State Warriors': 1610612744,
        'Houston Rockets': 1610612745,
        'Indiana Pacers': 1610612754,
        'LA Clippers': 1610612746,
        'Los Angeles Lakers': 1610612747,
        'Memphis Grizzlies': 1610612763,
        'Miami Heat': 1610612748,
        'Milwaukee Bucks': 1610612749,
        'Minnesota Timberwolves': 1610612750,
        'New Orleans Pelicans': 1610612740,
        'New York Knicks': 1610612752,
        'Oklahoma City Thunder': 1610612760,
        'Orlando Magic': 1610612753,
        'Philadelphia 76ers': 1610612755,
        'Phoenix Suns': 1610612756,
        'Portland Trail Blazers': 1610612757,
        'Sacramento Kings': 1610612758,
        'San Antonio Spurs': 1610612759,
        'Toronto Raptors': 1610612761,
        'Utah Jazz': 1610612762,
        'Washington Wizards': 1610612764
    }
    return team_ids.get(team_name)

# Cargar los datos
try:
    df = pd.read_csv('nba_team_complete_stats_2024_25.csv')
    # Limpiar nombres de columnas para evitar confusiones
    # Mostrar los nombres de las columnas para debug
    print("Columnas en el CSV:")
    print(df.columns.tolist())
except FileNotFoundError:
    print("Archivo CSV no encontrado. Ejecuta main.py y advanced_stats.py primero.")
    df = pd.DataFrame()  # DataFrame vacío como fallback

def create_dashboard(df):
    app = dash.Dash(__name__, suppress_callback_exceptions=True)
    
    # Estilos CSS personalizados
    app.index_string = '''
    <!DOCTYPE html>
    <html>
        <head>
            {%metas%}
            <title>{%title%}</title>
            {%favicon%}
            {%css%}
            <style>
                .full-width-charts {
                    width: 100%;
                    padding: 15px;
                    background-color: white;
                    border-radius: 5px;
                    box-shadow: 0 2px 5px rgba(0,0,0,0.1);
                    margin-bottom: 20px;
                }
                .container {
                    max-width: 1200px;
                    margin: 0 auto;
                    padding: 15px;
                }
                .chart-container {
                    margin-bottom: 40px;
                    border-bottom: 1px solid #eee;
                    padding-bottom: 20px;
                }
                h3 {
                    color: #1D428A;
                    border-bottom: 2px solid #CE1141;
                    padding-bottom: 10px;
                    margin-top: 30px;
                }
                .card {
                    background-color: white;
                    border-radius: 5px;
                    padding: 15px;
                    box-shadow: 0 2px 5px rgba(0,0,0,0.1);
                    margin-bottom: 20px;
                }
            </style>
        </head>
        <body>
            {%app_entry%}
            <footer>
                {%config%}
                {%scripts%}
                {%renderer%}
            </footer>
        </body>
    </html>
    '''
    
    # Definir el diseño del panel
    app.layout = html.Div([
        html.H1("Dashboard de Estadísticas NBA 2024-2025", style={'textAlign': 'center'}),
        
        # Botón para limpiar caché de logos
        html.Div([
            html.Button('Limpiar caché de logos', id='clear-cache-button', n_clicks=0,
                     style={
                         'marginBottom': '10px',
                         'backgroundColor': '#1D428A',
                         'color': 'white',
                         'border': 'none',
                         'padding': '10px 15px',
                         'borderRadius': '5px',
                         'cursor': 'pointer'
                     }),
            html.Div(id='clear-cache-output', style={'marginBottom': '10px', 'color': '#CE1141'})
        ], style={'textAlign': 'center', 'marginBottom': '20px'}),
        
        dcc.Tabs(id='tabs', children=[
            # Tab de Vista General
            dcc.Tab(label='Vista General', value='tab-general', children=[
                html.Div([
                    # Contenedor para todos los gráficos en una sola columna
                    html.Div([
                        # Gráfico 1: Gráfico de Dispersión de Equipos
                        html.H3("Gráfico de Dispersión de Equipos", style={'textAlign': 'center', 'marginTop': '20px'}),
                        html.Div([
                            html.Div([
                                html.Label("Eje X:"),
                                dcc.Dropdown(
                                    id='x-axis',
                                    options=[
                                        {'label': 'Puntos por Partido', 'value': 'PTS'},
                                        {'label': 'Asistencias por Partido', 'value': 'AST'},
                                        {'label': 'Rebotes por Partido', 'value': 'REB'},
                                        {'label': 'Robos por Partido', 'value': 'STL'},
                                        {'label': 'Tapones por Partido', 'value': 'BLK'},
                                        {'label': 'Porcentaje de Tiro', 'value': 'FG_PCT'},
                                        {'label': 'Porcentaje de Triples', 'value': 'FG3_PCT'},
                                        {'label': 'Rating Ofensivo', 'value': 'E_OFF_RATING'},
                                        {'label': 'Rating Defensivo', 'value': 'E_DEF_RATING'},
                                        {'label': 'Net Rating', 'value': 'E_NET_RATING'},
                                        {'label': 'Victorias', 'value': 'W_x'},
                                        {'label': 'Derrotas', 'value': 'L_x'},
                                    ],
                                    value='PTS'
                                ),
                            ], style={'width': '48%', 'display': 'inline-block'}),
                            
                            html.Div([
                                html.Label("Eje Y:"),
                                dcc.Dropdown(
                                    id='y-axis',
                                    options=[
                                        {'label': 'Puntos por Partido', 'value': 'PTS'},
                                        {'label': 'Asistencias por Partido', 'value': 'AST'},
                                        {'label': 'Rebotes por Partido', 'value': 'REB'},
                                        {'label': 'Robos por Partido', 'value': 'STL'},
                                        {'label': 'Tapones por Partido', 'value': 'BLK'},
                                        {'label': 'Porcentaje de Tiro', 'value': 'FG_PCT'},
                                        {'label': 'Porcentaje de Triples', 'value': 'FG3_PCT'},
                                        {'label': 'Rating Ofensivo', 'value': 'E_OFF_RATING'},
                                        {'label': 'Rating Defensivo', 'value': 'E_DEF_RATING'},
                                        {'label': 'Net Rating', 'value': 'E_NET_RATING'},
                                        {'label': 'Victorias', 'value': 'W_x'},
                                        {'label': 'Derrotas', 'value': 'L_x'},
                                    ],
                                    value='E_OFF_RATING'
                                ),
                            ], style={'width': '48%', 'display': 'inline-block', 'float': 'right'}),
                        ]),
                        dcc.Graph(id='scatter-plot'),
                        
                        # Gráfico 2: Asistencias vs Victorias
                        html.H3("Asistencias vs Victorias", style={'textAlign': 'center', 'marginTop': '30px'}),
                        dcc.Graph(id='ast-win-chart'),
                        
                        # Gráfico 3: Top 10 Anotadores
                        html.H3("Top 10 Equipos por Puntos", style={'textAlign': 'center', 'marginTop': '30px'}),
                        dcc.Graph(id='top10-points-chart'),
                        
                        # Gráfico 4: Ofensiva vs Defensiva
                        html.H3("Ofensiva vs Defensiva", style={'textAlign': 'center', 'marginTop': '30px'}),
                        dcc.Graph(id='off-def-chart'),
                        
                        # Gráfico 5: Ritmo vs Ofensiva
                        html.H3("Ritmo vs Ofensiva", style={'textAlign': 'center', 'marginTop': '30px'}),
                        dcc.Graph(id='pace-off-chart'),
                        
                        # Gráfico 6: Correlación entre Estadísticas
                        html.H3("Correlación entre Estadísticas", style={'textAlign': 'center', 'marginTop': '30px'}),
                        dcc.Graph(id='correlation-chart'),
                        
                    ], className='full-width-charts')
                ], className='container'),
            ]),
            
            # Tab de Análisis de Equipo Individual
            dcc.Tab(label='Análisis de Equipo', value='tab-team-analysis', children=[
                html.Div([
                    html.Div([
                        html.H3("Selecciona un Equipo"),
                        dcc.Dropdown(
                            id='team-selector',
                            options=[{'label': team, 'value': team} for team in sorted(df['TEAM_NAME_x'].unique())],
                            value=None
                        ),
                        html.Div(id='team-logo-container', style={'textAlign': 'center', 'margin': '20px 0'}),
                        html.H3(id='team-stats-title'),
                        html.Div(id='team-stats-table'),
                        dcc.Graph(id='team-radar-chart'),
                    ], className='card'),
                ], className='container'),
            ]),
            
            # Tab de Comparación de Equipos
            dcc.Tab(label='Comparación de Equipos', value='tab-team-comparison', children=[
                html.Div([
                    html.Div([
                        html.Div([
                            html.H3("Equipo 1"),
                            dcc.Dropdown(
                                id='team1-selector',
                                options=[{'label': team, 'value': team} for team in sorted(df['TEAM_NAME_x'].unique())],
                                value=None
                            ),
                            html.Div(id='team1-logo-container', style={'textAlign': 'center', 'margin': '20px 0'}),
                        ], style={'width': '48%', 'display': 'inline-block'}),
                        
                        html.Div([
                            html.H3("Equipo 2"),
                            dcc.Dropdown(
                                id='team2-selector',
                                options=[{'label': team, 'value': team} for team in sorted(df['TEAM_NAME_x'].unique())],
                                value=None
                            ),
                            html.Div(id='team2-logo-container', style={'textAlign': 'center', 'margin': '20px 0'}),
                        ], style={'width': '48%', 'display': 'inline-block', 'float': 'right'}),
                        
                        dcc.Graph(id='teams-comparison-chart'),
                    ], className='card'),
                ], className='container'),
            ]),
            
            # Tab de Calendario y Predicciones
            dcc.Tab(label='Calendario y Predicciones', value='tab-schedule', children=[
                html.Div([
                    html.H3("Calendario de Partidos NBA", style={'textAlign': 'center', 'marginTop': '20px'}),
                    html.P("Vista de próximos partidos con análisis estadístico y predicciones", 
                           style={'textAlign': 'center', 'marginBottom': '20px', 'color': '#666'}),
                    
                    # Botón para actualizar caché del calendario
                    html.Div([
                        html.Button('Actualizar datos del calendario', id='refresh-schedule-button', n_clicks=0,
                                 style={
                                     'marginBottom': '10px',
                                     'backgroundColor': '#1D428A',
                                     'color': 'white',
                                     'border': 'none',
                                     'padding': '10px 15px',
                                     'borderRadius': '5px',
                                     'cursor': 'pointer'
                                 }),
                        html.Div(id='refresh-schedule-output', style={'marginBottom': '10px', 'color': '#CE1141'})
                    ], style={'textAlign': 'center', 'marginBottom': '20px'}),
                    
                    # Selección de fecha
                    html.Div([
                        html.H4("Selecciona una fecha:"),
                        dcc.DatePickerSingle(
                            id='date-picker',
                            min_date_allowed=datetime.datetime(2024, 10, 1).date(),
                            max_date_allowed=datetime.datetime(2025, 6, 30).date(),
                            initial_visible_month=datetime.datetime.now().date(),
                            date=datetime.datetime.now().date(),
                            display_format='YYYY-MM-DD',
                            style={'marginBottom': '15px'}
                        ),
                    ], style={'textAlign': 'center', 'marginBottom': '20px'}),
                    
                    # Contenedor para la lista de partidos
                    html.Div(id='games-container', className='card')
                    
                ], className='container'),
            ]),
        ]),
        
        html.Footer([
            html.P("Dashboard de Estadísticas NBA 2024-2025 | Desarrollado con Dash y Python"),
        ], style={'textAlign': 'center', 'padding': '20px', 'marginTop': '50px'})
    ])

    # Callback para actualizar el gráfico de dispersión
    @app.callback(
        Output('scatter-plot', 'figure'),
        [Input('x-axis', 'value'),
         Input('y-axis', 'value')]
    )
    def update_scatter(x_axis, y_axis):
        if not x_axis or not y_axis:
            return go.Figure()
        
        # Crear figura base
        fig = go.Figure()
        
        # Agregar puntos para cada equipo con imágenes de logo
        for team_name in df['TEAM_NAME_x'].unique():
            team_data = df[df['TEAM_NAME_x'] == team_name]
            
            # Obtener URL del logo y color del equipo
            logo_url = get_team_logo(team_name)
            team_color = get_team_color(team_name)
            
            if logo_url:
                # Agregar equipo con logo
                fig.add_trace(go.Scatter(
                    x=team_data[x_axis],
                    y=team_data[y_axis],
                    mode='markers',
                    name=team_name,
                    marker=dict(
                        size=40,
                        opacity=0.8,
                        color=team_color,
                        line=dict(color='white', width=2)
                    ),
                    text=team_name,
                    hovertemplate=f"<b>{team_name}</b><br>{x_axis}: %{{x:.2f}}<br>{y_axis}: %{{y:.2f}}<extra></extra>"
                ))
                
                # Agregar logo como imagen
                fig.add_layout_image(
                    dict(
                        source=logo_url,
                        xref="x",
                        yref="y",
                        x=team_data[x_axis].values[0],
                        y=team_data[y_axis].values[0],
                        sizex=3,
                        sizey=3,
                        xanchor="center",
                        yanchor="middle",
                        sizing="contain",
                        opacity=0.9,
                        layer="above"
                    )
                )
            else:
                # Fallback sin logo
                fig.add_trace(go.Scatter(
                    x=team_data[x_axis],
                    y=team_data[y_axis],
                    mode='markers+text',
                    name=team_name,
                    text=team_name,
                    textposition="top center",
                    marker=dict(
                        size=30,
                        color=team_color
                    )
                ))
        
        # Ajustar layout
        fig.update_layout(
            title=f"Relación entre {x_axis} y {y_axis}",
            xaxis_title=x_axis,
            yaxis_title=y_axis,
            showlegend=False,
            hovermode='closest',
            plot_bgcolor='rgba(240, 240, 240, 0.5)',
            paper_bgcolor='white',
            height=600,  # Altura fija para mejor visualización
            margin=dict(l=40, r=40, t=60, b=40)
        )
        
        return fig
    
    # Callback para actualizar el análisis de equipo
    @app.callback(
        [Output('team-radar-chart', 'figure'),
         Output('team-stats-title', 'children'),
         Output('team-stats-table', 'children'),
         Output('team-logo-container', 'children')],
        [Input('team-selector', 'value')]
    )
    def update_team_analysis(team):
        if not team:
            return go.Figure(), "Estadísticas del Equipo", html.Div(), html.Div()
        
        # Filtrar datos para el equipo seleccionado
        team_data = df[df['TEAM_NAME_x'] == team].iloc[0]
        
        # Crear gráfico de radar
        categories = ['PTS', 'AST', 'REB', 'STL', 'BLK', 'TOV']
        values = [team_data[cat] for cat in categories]
        
        # Normalizar valores para mejor visualización
        max_vals = df[categories].max()
        normalized_values = [(val / max_val) * 100 for val, max_val in zip(values, max_vals)]
        
        fig = go.Figure()
        
        # Obtener colores del equipo
        team_color = get_team_color(team)
        
        fig.add_trace(go.Scatterpolar(
            r=normalized_values,
            theta=categories,
            fill='toself',
            name=team,
            line=dict(color=team_color)
        ))
        
        # Crear tabla de estadísticas
        stats_to_show = {
            'Record': f"{int(team_data['W_x'])}-{int(team_data['L_x'])}",
            'Puntos por Partido': f"{team_data['PTS']:.1f}",
            'Asistencias por Partido': f"{team_data['AST']:.1f}",
            'Rebotes por Partido': f"{team_data['REB']:.1f}",
            'Porcentaje de Tiro': f"{team_data['FG_PCT']*100:.1f}%",
            'Porcentaje de Triples': f"{team_data['FG3_PCT']*100:.1f}%",
            'Rating Ofensivo': f"{team_data['E_OFF_RATING']:.1f}",
            'Rating Defensivo': f"{team_data['E_DEF_RATING']:.1f}",
            'Net Rating': f"{team_data['E_NET_RATING']:.1f}"
        }
        
        table = html.Table([
            html.Tr([html.Th("Estadística"), html.Th("Valor")])
        ] + [
            html.Tr([html.Td(k), html.Td(v)]) for k, v in stats_to_show.items()
        ], style={'width': '100%', 'textAlign': 'left'})
        
        # Obtener URL del logo del equipo
        logo_url = get_team_logo(team)
        
        if logo_url:
            logo_component = html.Img(
                src=logo_url,
                style={'height': '120px', 'margin': '10px auto', 'display': 'block', 'max-width': '100%'}
            )
        else:
            # Si no hay logo, mostrar un texto
            logo_component = html.Div(
                team,
                style={
                    'height': '120px', 
                    'margin': '10px auto', 
                    'background-color': team_color,
                    'color': 'white',
                    'display': 'flex',
                    'align-items': 'center',
                    'justify-content': 'center',
                    'border-radius': '5px',
                    'font-weight': 'bold',
                    'font-size': '18px'
                }
            )
        
        fig.update_layout(
            polar=dict(
                radialaxis=dict(
                    visible=True,
                    range=[0, 100]
                )
            ),
            showlegend=False,
            paper_bgcolor='rgba(0,0,0,0)',
            plot_bgcolor='rgba(0,0,0,0)',
            margin=dict(l=80, r=80, t=20, b=20)
        )
        
        return fig, f"Estadísticas de {team}", table, logo_component
    
    # Callback para comparar equipos
    @app.callback(
        [Output('teams-comparison-chart', 'figure'),
         Output('team1-logo-container', 'children'),
         Output('team2-logo-container', 'children')],
        [Input('team1-selector', 'value'),
         Input('team2-selector', 'value')]
    )
    def update_comparison(team1, team2):
        if not team1 or not team2:
            return go.Figure(), html.Div(), html.Div()
        
        # Filtrar datos para los equipos seleccionados
        team1_data = df[df['TEAM_NAME_x'] == team1].iloc[0]
        team2_data = df[df['TEAM_NAME_x'] == team2].iloc[0]
        
        categories = ['PTS', 'AST', 'REB', 'STL', 'BLK', 'FG_PCT', 'FG3_PCT', 'E_OFF_RATING', 'E_DEF_RATING']
        team1_values = [team1_data[cat] for cat in categories]
        team2_values = [team2_data[cat] for cat in categories]
        
        # Normalizar FG_PCT y FG3_PCT multiplicándolos por 100
        categories_display = ['Puntos', 'Asistencias', 'Rebotes', 'Robos', 'Tapones', '% Tiro ×100', '% Triple ×100', 'Rating Of.', 'Rating Def.']
        
        # Normalizar valores para mejor visualización
        normalized_values1 = []
        normalized_values2 = []
        
        for i, (val1, val2) in enumerate(zip(team1_values, team2_values)):
            if categories[i] in ['FG_PCT', 'FG3_PCT']:
                normalized_values1.append(val1 * 100)
                normalized_values2.append(val2 * 100)
            else:
                max_val = max(df[categories[i]])
                normalized_values1.append((val1 / max_val) * 100)
                normalized_values2.append((val2 / max_val) * 100)
        
        # Obtener colores de los equipos
        team1_color = get_team_color(team1)
        team2_color = get_team_color(team2)
        
        fig = go.Figure()
        
        fig.add_trace(go.Scatterpolar(
            r=normalized_values1,
            theta=categories_display,
            fill='toself',
            name=team1,
            line=dict(color=team1_color)
        ))
        
        fig.add_trace(go.Scatterpolar(
            r=normalized_values2,
            theta=categories_display,
            fill='toself',
            name=team2,
            line=dict(color=team2_color)
        ))
        
        # Obtener URL de los logos
        logo_url1 = get_team_logo(team1)
        logo_url2 = get_team_logo(team2)
        
        # Crear componentes de logos
        if logo_url1:
            logo_component1 = html.Img(
                src=logo_url1,
                style={'height': '120px', 'margin': '10px auto', 'display': 'block', 'max-width': '100%'}
            )
        else:
            logo_component1 = html.Div(
                team1,
                style={
                    'height': '120px', 
                    'margin': '10px auto', 
                    'background-color': team1_color,
                    'color': 'white',
                    'display': 'flex',
                    'align-items': 'center',
                    'justify-content': 'center',
                    'border-radius': '5px',
                    'font-weight': 'bold',
                    'font-size': '18px'
                }
            )
            
        if logo_url2:
            logo_component2 = html.Img(
                src=logo_url2,
                style={'height': '120px', 'margin': '10px auto', 'display': 'block', 'max-width': '100%'}
            )
        else:
            logo_component2 = html.Div(
                team2,
                style={
                    'height': '120px', 
                    'margin': '10px auto', 
                    'background-color': team2_color,
                    'color': 'white',
                    'display': 'flex',
                    'align-items': 'center',
                    'justify-content': 'center',
                    'border-radius': '5px',
                    'font-weight': 'bold',
                    'font-size': '18px'
                }
            )
        
        fig.update_layout(
            polar=dict(
                radialaxis=dict(
                    visible=True,
                    range=[0, 100]
                )
            ),
            title=f"Comparación: {team1} vs {team2}",
            showlegend=True
        )
        
        return fig, logo_component1, logo_component2
    
    # Callback para limpiar caché de logos
    @app.callback(
        Output('clear-cache-output', 'children'),
        [Input('clear-cache-button', 'n_clicks')]
    )
    def clear_logo_cache(n_clicks):
        if n_clicks > 0:
            try:
                for filename in os.listdir('logos'):
                    file_path = os.path.join('logos', filename)
                    if os.path.isfile(file_path):
                        os.remove(file_path)
                return html.Div("✅ Caché de logos eliminado correctamente!", style={'color': 'green'})
            except Exception as e:
                return html.Div(f"❌ Error al limpiar el caché: {str(e)}", style={'color': 'red'})
        return ""
    
    # Callbacks para los nuevos gráficos dinámicos
    @app.callback(
        Output('ast-win-chart', 'figure'),
        [Input('tabs', 'value')]
    )
    def update_ast_win_chart(_):
        # Gráfico de Asistencias vs Victorias
        fig = go.Figure()
        
        # Agregar puntos para cada equipo con imágenes de logo
        for team_name in df['TEAM_NAME_x'].unique():
            team_data = df[df['TEAM_NAME_x'] == team_name]
            
            # Obtener URL del logo y color del equipo
            logo_url = get_team_logo(team_name)
            team_color = get_team_color(team_name)
            
            # Agregar punto para el equipo
            fig.add_trace(go.Scatter(
                x=team_data['AST'],
                y=team_data['W_x'],
                mode='markers',
                name=team_name,
                marker=dict(
                    size=25,
                    opacity=0.8,
                    color=team_color,
                    line=dict(color='white', width=1.5)
                ),
                text=team_name,
                hovertemplate=f"<b>{team_name}</b><br>Asistencias: %{{x:.2f}}<br>Victorias: %{{y:.0f}}<extra></extra>"
            ))
            
            # Si tenemos logo, agregarlo
            if logo_url:
                fig.add_layout_image(
                    dict(
                        source=logo_url,
                        xref="x",
                        yref="y",
                        x=team_data['AST'].values[0],
                        y=team_data['W_x'].values[0],
                        sizex=2.2,
                        sizey=2.2,
                        xanchor="center",
                        yanchor="middle",
                        sizing="contain",
                        opacity=0.9,
                        layer="above"
                    )
                )
        
        # Añadir línea de tendencia
        x_range = np.linspace(df['AST'].min() - 0.5, df['AST'].max() + 0.5, 100)
        y_trend = x_range * df['AST'].corr(df['W_x']) + (df['W_x'].mean() - df['AST'].corr(df['W_x']) * df['AST'].mean())
        
        fig.add_trace(go.Scatter(
            x=x_range,
            y=y_trend,
            mode='lines',
            name='Tendencia',
            line=dict(color='rgba(0, 0, 0, 0.5)', width=2, dash='dash')
        ))
        
        # Personalizar el diseño
        fig.update_layout(
            title='Relación entre Asistencias y Victorias',
            xaxis_title='Asistencias por Partido',
            yaxis_title='Victorias',
            showlegend=False,
            plot_bgcolor='rgba(240, 240, 240, 0.5)',
            paper_bgcolor='white',
            height=550,
            margin=dict(l=40, r=40, t=60, b=40)
        )
        
        return fig
        
    @app.callback(
        Output('top10-points-chart', 'figure'),
        [Input('tabs', 'value')]
    )
    def update_top10_points_chart(_):
        # Top 10 equipos por puntos
        top10_pts = df.sort_values('PTS', ascending=False).head(10)
        
        fig = go.Figure()
        
        # Para cada equipo, crear una barra con el valor de puntos
        for i, team in enumerate(top10_pts['TEAM_NAME_x']):
            team_data = top10_pts[top10_pts['TEAM_NAME_x'] == team]
            team_color = get_team_color(team)
            points = team_data['PTS'].values[0]
            
            # Agregar barra para el equipo
            fig.add_trace(go.Bar(
                x=[team],
                y=[points],
                name=team,
                marker_color=team_color,
                text=[f"{points:.1f}"],
                textposition='outside',
                hovertemplate=f"<b>{team}</b><br>Puntos: {points:.1f}<extra></extra>"
            ))
            
            # Obtener logo del equipo
            logo_url = get_team_logo(team)
            if logo_url:
                # Calcular posición Y para el logo (en el medio de la barra)
                y_pos = points / 2
                
                # Añadir logo como imagen
                fig.add_layout_image(
                    dict(
                        source=logo_url,
                        xref="x",
                        yref="y",
                        x=team,
                        y=y_pos,
                        sizex=0.9,
                        sizey=points * 0.5,  # Tamaño proporcional a la altura de la barra
                        xanchor="center",
                        yanchor="middle",
                        sizing="contain",
                        opacity=0.9,
                        layer="above"
                    )
                )
        
        # Personalizar el diseño
        fig.update_layout(
            title='Top 10 Equipos por Puntos por Partido',
            xaxis_title='',
            yaxis_title='Puntos por Partido',
            showlegend=False,
            plot_bgcolor='rgba(240, 240, 240, 0.5)',
            paper_bgcolor='white',
            height=550,
            margin=dict(l=40, r=40, t=60, b=80)
        )
        
        # Ajustar etiquetas del eje X para mejor visualización
        fig.update_xaxes(tickangle=45)
        
        return fig
    
    @app.callback(
        Output('off-def-chart', 'figure'),
        [Input('tabs', 'value')]
    )
    def update_off_def_chart(_):
        # Gráfico de Rating Ofensivo vs Rating Defensivo
        fig = go.Figure()
        
        # Agregar puntos para cada equipo con imágenes de logo
        for team_name in df['TEAM_NAME_x'].unique():
            team_data = df[df['TEAM_NAME_x'] == team_name]
            
            # Obtener URL del logo y color del equipo
            logo_url = get_team_logo(team_name)
            team_color = get_team_color(team_name)
            
            # Calcular tamaño basado en porcentaje de victorias
            size = 15 + (team_data['W_PCT_x'].values[0] * 20)
            
            # Agregar punto para el equipo
            fig.add_trace(go.Scatter(
                x=team_data['E_OFF_RATING'],
                y=team_data['E_DEF_RATING'],
                mode='markers',
                name=team_name,
                marker=dict(
                    size=size,
                    opacity=0.8,
                    color=team_color,
                    line=dict(color='white', width=1.5)
                ),
                text=team_name,
                hovertemplate=f"<b>{team_name}</b><br>Rating Ofensivo: %{{x:.1f}}<br>Rating Defensivo: %{{y:.1f}}<br>Net Rating: {team_data['E_NET_RATING'].values[0]:.1f}<extra></extra>"
            ))
            
            # Si tenemos logo, agregarlo
            if logo_url:
                fig.add_layout_image(
                    dict(
                        source=logo_url,
                        xref="x",
                        yref="y",
                        x=team_data['E_OFF_RATING'].values[0],
                        y=team_data['E_DEF_RATING'].values[0],
                        sizex=2.5,
                        sizey=2.5,
                        xanchor="center",
                        yanchor="middle",
                        sizing="contain",
                        opacity=0.9,
                        layer="above"
                    )
                )
        
        # Personalizar el diseño
        fig.update_layout(
            title='Rating Ofensivo vs Rating Defensivo',
            xaxis_title='Rating Ofensivo',
            yaxis_title='Rating Defensivo (menor es mejor)',
            showlegend=False,
            plot_bgcolor='rgba(240, 240, 240, 0.5)',
            paper_bgcolor='white',
            height=550,
            margin=dict(l=40, r=40, t=60, b=40)
        )
        
        # Añadir líneas de referencia para promedios
        fig.add_hline(y=df['E_DEF_RATING'].mean(), line_dash="dash", line_color="gray", annotation_text="Media Liga")
        fig.add_vline(x=df['E_OFF_RATING'].mean(), line_dash="dash", line_color="gray", annotation_text="Media Liga")
        
        # Añadir anotaciones para los cuadrantes
        fig.add_annotation(
            x=df['E_OFF_RATING'].max() - 1,
            y=df['E_DEF_RATING'].min() + 1,
            text="ELITE",
            showarrow=False,
            font=dict(size=14, color="green")
        )
        fig.add_annotation(
            x=df['E_OFF_RATING'].min() + 1,
            y=df['E_DEF_RATING'].max() - 1,
            text="DÉBIL",
            showarrow=False,
            font=dict(size=14, color="red")
        )
        
        return fig
    
    @app.callback(
        Output('pace-off-chart', 'figure'),
        [Input('tabs', 'value')]
    )
    def update_pace_off_chart(_):
        # Gráfico de Ritmo vs Rating Ofensivo
        fig = go.Figure()
        
        # Agregar puntos para cada equipo con imágenes de logo
        for team_name in df['TEAM_NAME_x'].unique():
            team_data = df[df['TEAM_NAME_x'] == team_name]
            
            # Obtener URL del logo y color del equipo
            logo_url = get_team_logo(team_name)
            team_color = get_team_color(team_name)
            
            # Calcular tamaño basado en puntos por partido
            pts_norm = (team_data['PTS'].values[0] - df['PTS'].min()) / (df['PTS'].max() - df['PTS'].min())
            size = 15 + (pts_norm * 25)
            
            # Agregar punto para el equipo
            fig.add_trace(go.Scatter(
                x=team_data['E_PACE'],
                y=team_data['E_OFF_RATING'],
                mode='markers',
                name=team_name,
                marker=dict(
                    size=size,
                    opacity=0.8,
                    color=team_color,
                    line=dict(color='white', width=1.5)
                ),
                text=team_name,
                hovertemplate=f"<b>{team_name}</b><br>Ritmo: %{{x:.1f}}<br>Rating Ofensivo: %{{y:.1f}}<br>Puntos: {team_data['PTS'].values[0]:.1f}<extra></extra>"
            ))
            
            # Si tenemos logo, agregarlo
            if logo_url:
                fig.add_layout_image(
                    dict(
                        source=logo_url,
                        xref="x",
                        yref="y",
                        x=team_data['E_PACE'].values[0],
                        y=team_data['E_OFF_RATING'].values[0],
                        sizex=2.3,
                        sizey=2.3,
                        xanchor="center",
                        yanchor="middle",
                        sizing="contain",
                        opacity=0.9,
                        layer="above"
                    )
                )
        
        # Personalizar el diseño
        fig.update_layout(
            title='Ritmo vs Rating Ofensivo',
            xaxis_title='Ritmo (posesiones por 48 minutos)',
            yaxis_title='Rating Ofensivo',
            showlegend=False,
            plot_bgcolor='rgba(240, 240, 240, 0.5)',
            paper_bgcolor='white',
            height=550,
            margin=dict(l=40, r=40, t=60, b=40)
        )
        
        # Añadir líneas de referencia para promedios
        fig.add_hline(y=df['E_OFF_RATING'].mean(), line_dash="dash", line_color="gray", annotation_text="Media Liga")
        fig.add_vline(x=df['E_PACE'].mean(), line_dash="dash", line_color="gray", annotation_text="Media Liga")
        
        # Añadir anotaciones para los cuadrantes
        fig.add_annotation(
            x=df['E_PACE'].max() - 0.5,
            y=df['E_OFF_RATING'].max() - 0.5,
            text="RÁPIDO Y EFECTIVO",
            showarrow=False,
            font=dict(size=12, color="green")
        )
        fig.add_annotation(
            x=df['E_PACE'].min() + 0.5,
            y=df['E_OFF_RATING'].max() - 0.5,
            text="LENTO Y EFECTIVO",
            showarrow=False,
            font=dict(size=12, color="blue")
        )
        
        return fig
    
    @app.callback(
        Output('correlation-chart', 'figure'),
        [Input('tabs', 'value')]
    )
    def update_correlation_chart(_):
        # Seleccionar columnas numéricas relevantes para la correlación
        numeric_cols = ['PTS', 'AST', 'REB', 'STL', 'BLK', 'FG_PCT', 'FG3_PCT', 
                        'E_OFF_RATING', 'E_DEF_RATING', 'E_NET_RATING', 'E_PACE', 
                        'W_x', 'L_x', 'W_PCT_x']
        
        # Calcular matriz de correlación
        corr_matrix = df[numeric_cols].corr()
        
        # Crear mapa de calor
        fig = px.imshow(corr_matrix,
                       labels=dict(x="Variable", y="Variable", color="Correlación"),
                       x=numeric_cols,
                       y=numeric_cols,
                       color_continuous_scale='RdBu_r',
                       title='Matriz de Correlación de Estadísticas')
        
        # Añadir anotaciones con los valores de correlación
        for i, row in enumerate(corr_matrix.values):
            for j, val in enumerate(row):
                fig.add_annotation(
                    x=j, y=i,
                    text=f"{val:.2f}",
                    showarrow=False,
                    font_size=9,
                    font_color='black' if abs(val) < 0.7 else 'white'
                )
        
        # Personalizar el diseño
        fig.update_layout(
            height=700,
            margin=dict(l=40, r=40, t=60, b=40),
            plot_bgcolor='rgba(240, 240, 240, 0.5)',
            paper_bgcolor='white'
        )
        
        return fig
        
    # Callback para mostrar los partidos del día seleccionado y sus predicciones
    @app.callback(
        Output('games-container', 'children'),
        [Input('date-picker', 'date')]
    )
    def update_schedule_view(selected_date):
        if not selected_date:
            return html.Div("Selecciona una fecha para ver los partidos programados.")
        
        # Convertir la fecha seleccionada al formato correcto
        selected_date = datetime.datetime.strptime(selected_date.split('T')[0], "%Y-%m-%d").strftime("%Y-%m-%d")
        
        # Obtener datos del calendario
        schedule_data = get_schedule_data()
        
        # Imprimir para depuración
        print(f"Fecha seleccionada: {selected_date}")
        for game in schedule_data[:2]:
            print(f"Juego disponible: {game['gameDate']} - {game['homeTeam']} vs {game['awayTeam']}")
        
        # Filtrar juegos para la fecha seleccionada
        games_for_date = [game for game in schedule_data if game['gameDate'] == selected_date]
        
        if not games_for_date:
            return html.Div("No hay partidos programados para esta fecha.", 
                           style={'textAlign': 'center', 'padding': '20px', 'color': '#666'})
        
        # Crear tarjetas para cada partido
        game_cards = []
        for game in games_for_date:
            home_team = game['homeTeam']
            away_team = game['awayTeam']
            
            # Analizar el enfrentamiento
            matchup_analysis = analyze_matchup(home_team, away_team, df)
            
            if matchup_analysis:
                # Obtener logos y colores
                home_logo = get_team_logo(home_team)
                away_logo = get_team_logo(away_team)
                home_color = get_team_color(home_team)
                away_color = get_team_color(away_team)
                
                # Formatear la hora del partido
                time_str = game.get('time', 'TBD')
                
                # Datos para el radar chart
                radar_categories = ['PTS', 'AST', 'REB', 'STL', 'BLK', 'E_OFF_RATING', 'E_DEF_RATING', 'E_NET_RATING']
                radar_display_names = ['Puntos', 'Asistencias', 'Rebotes', 'Robos', 'Tapones', 'Rating Of.', 'Rating Def.', 'Net Rating']
                
                home_values = []
                away_values = []
                
                for stat_key in radar_categories:
                    if stat_key in matchup_analysis['comparison']:
                        stat_data = matchup_analysis['comparison'][stat_key]
                        home_value = stat_data['team1_value']
                        away_value = stat_data['team2_value']
                        
                        # Normalizar para el radar chart si es necesario
                        if stat_key in ['E_DEF_RATING']:
                            # Para rating defensivo (menor es mejor), invertimos la normalización
                            max_val_def = max(df[stat_key])
                            min_val_def = min(df[stat_key])
                            range_def = max_val_def - min_val_def
                            
                            # Normalizar e invertir para que menor rating defensivo = mayor valor en el gráfico
                            home_normalized = (max_val_def - home_value) / range_def * 100
                            away_normalized = (max_val_def - away_value) / range_def * 100
                            
                            home_values.append(home_normalized)
                            away_values.append(away_normalized)
                        else:
                            # Para el resto de estadísticas (mayor es mejor)
                            max_val = max(df[stat_key])
                            min_val = min(df[stat_key])
                            range_val = max_val - min_val
                            
                            if range_val > 0:  # Evitar división por cero
                                home_normalized = (home_value - min_val) / range_val * 100
                                away_normalized = (away_value - min_val) / range_val * 100
                                home_values.append(home_normalized)
                                away_values.append(away_normalized)
                            else:
                                home_values.append(50)
                                away_values.append(50)
                
                # Crear radar chart para comparación visual
                radar_fig = go.Figure()
                
                radar_fig.add_trace(go.Scatterpolar(
                    r=home_values,
                    theta=radar_display_names,
                    fill='toself',
                    name=home_team,
                    line=dict(color=home_color)
                ))
                
                radar_fig.add_trace(go.Scatterpolar(
                    r=away_values,
                    theta=radar_display_names,
                    fill='toself',
                    name=away_team,
                    line=dict(color=away_color)
                ))
                
                radar_fig.update_layout(
                    polar=dict(
                        radialaxis=dict(
                            visible=True,
                            range=[0, 100]
                        )
                    ),
                    showlegend=True,
                    legend=dict(
                        orientation="h",
                        yanchor="bottom",
                        y=1.02,
                        xanchor="center",
                        x=0.5
                    ),
                    height=350,
                    margin=dict(l=30, r=30, t=30, b=30)
                )
                
                # Crear contenedor principal del partido
                game_card = html.Div([
                    html.Div([
                        # Encabezado con información del partido
                        html.Div([
                            html.H4(f"{game.get('gameLabel', 'Partido regular')}",
                                  style={'textAlign': 'center', 'margin': '10px 0', 'color': '#555'}),
                            html.Div(f"{game.get('arena', 'Arena NBA')} - {game.get('city', '')}",
                                    style={'textAlign': 'center', 'fontSize': '14px', 'color': '#777', 'marginBottom': '10px'})
                        ]),
                        
                        # Información de equipos y puntuación
                        html.Div([
                            # Equipo visitante
                            html.Div([
                                html.Div([
                                    html.Img(src=away_logo, height='80px', style={'display': 'block', 'margin': '0 auto 10px auto'}),
                                    html.H4(away_team, style={'textAlign': 'center', 'color': away_color, 'margin': '5px 0'}),
                                    html.H3(
                                        "-" if game.get('status', '') == '' and (game.get('awayScore', 0) == 0 or game.get('awayScore', '') == '') else str(game.get('awayScore', '')), 
                                        style={'textAlign': 'center', 'fontSize': '24px', 'fontWeight': 'bold', 'margin': '5px 0'}
                                    )
                                ], style={'display': 'flex', 'flexDirection': 'column', 'alignItems': 'center'})
                            ], style={'width': '40%', 'display': 'inline-block', 'verticalAlign': 'middle'}),
                            
                            # Información central (VS y hora)
                            html.Div([
                                html.H3("VS", style={'textAlign': 'center', 'margin': '10px 0'}),
                                html.Div(time_str, style={'textAlign': 'center', 'fontSize': '18px'}),
                                html.Div(game.get('status', ''), 
                                        style={'textAlign': 'center', 'fontSize': '16px', 
                                              'color': '#CE1141' if game.get('status') == 'Final' else '#333'})
                            ], style={'width': '20%', 'display': 'inline-block', 'verticalAlign': 'middle'}),
                            
                            # Equipo local
                            html.Div([
                                html.Div([
                                    html.Img(src=home_logo, height='80px', style={'display': 'block', 'margin': '0 auto 10px auto'}),
                                    html.H4(home_team, style={'textAlign': 'center', 'color': home_color, 'margin': '5px 0'}),
                                    html.H3(
                                        "-" if game.get('status', '') == '' and (game.get('homeScore', 0) == 0 or game.get('homeScore', '') == '') else str(game.get('homeScore', '')), 
                                        style={'textAlign': 'center', 'fontSize': '24px', 'fontWeight': 'bold', 'margin': '5px 0'}
                                    )
                                ], style={'display': 'flex', 'flexDirection': 'column', 'alignItems': 'center'})
                            ], style={'width': '40%', 'display': 'inline-block', 'verticalAlign': 'middle'})
                        ], style={'marginBottom': '20px'}),
                        
                        # Gráfico radar
                        html.Div([
                            html.H4("Comparación Visual", style={'textAlign': 'center', 'marginBottom': '15px'}),
                            dcc.Graph(figure=radar_fig, config={'displayModeBar': False})
                        ], style={'marginBottom': '20px'}),
                        
                        # Análisis del partido
                        html.Div([
                            html.H4("Análisis Estadístico", style={'textAlign': 'center', 'borderBottom': '1px solid #ddd', 'paddingBottom': '10px'}),
                            
                            # Pronóstico de Victoria
                            html.Div([
                                html.H5("Pronóstico:", style={'textAlign': 'center', 'margin': '10px 0'}),
                                html.Div([
                                    html.Div(f"{away_team}: {matchup_analysis['win_probability']['team2']}%", 
                                           style={'width': '45%', 'display': 'inline-block', 'textAlign': 'center'}),
                                    html.Div(f"{home_team}: {matchup_analysis['win_probability']['team1']}%", 
                                           style={'width': '45%', 'display': 'inline-block', 'textAlign': 'center'})
                                ]),
                                
                                # Barra de progreso para visualizar probabilidad
                                html.Div(style={
                                    'height': '10px',
                                    'marginTop': '5px',
                                    'marginBottom': '15px',
                                    'background': f'linear-gradient(to right, {away_color} 0%, {away_color} {matchup_analysis["win_probability"]["team2"]}%, {home_color} {matchup_analysis["win_probability"]["team2"]}%, {home_color} 100%)',
                                    'borderRadius': '5px'
                                })
                            ]),
                            
                            # Estadísticas clave
                            html.Div([
                                html.H5("Estadísticas Clave:", style={'margin': '15px 0 10px 0'}),
                                html.Table([
                                    html.Thead(
                                        html.Tr([
                                            html.Th(away_team, style={'width': '30%', 'textAlign': 'center'}),
                                            html.Th("Estadística", style={'width': '40%', 'textAlign': 'center'}),
                                            html.Th(home_team, style={'width': '30%', 'textAlign': 'center'})
                                        ])
                                    ),
                                    html.Tbody([
                                        html.Tr([
                                            html.Td(f"{stat_data['team2_value']:.1f}", 
                                                  style={
                                                      'textAlign': 'center',
                                                      'color': '#CE1141' if stat_data['advantage'] == 'team1' else '#008348',
                                                      'fontWeight': 'bold' if stat_data['advantage'] == 'team2' else 'normal'
                                                  }),
                                            html.Td(stat_name, style={'textAlign': 'center'}),
                                            html.Td(f"{stat_data['team1_value']:.1f}", 
                                                  style={
                                                      'textAlign': 'center', 
                                                      'color': '#CE1141' if stat_data['advantage'] == 'team2' else '#008348',
                                                      'fontWeight': 'bold' if stat_data['advantage'] == 'team1' else 'normal'
                                                  })
                                        ], style={'backgroundColor': '#f9f9f9' if i % 2 == 0 else 'white'})
                                        for i, (stat_key, stat_data, stat_name) in enumerate(zip(
                                            matchup_analysis['key_stats_for_display'],
                                            [matchup_analysis['comparison'][key] for key in matchup_analysis['key_stats_for_display']],
                                            matchup_analysis['stat_display_names']
                                        ))
                                    ])
                                ], style={'width': '100%', 'borderCollapse': 'collapse'})
                            ]),
                            
                            # Factores completos de análisis
                            html.Div([
                                html.H5("Análisis completo por categorías:", style={'margin': '30px 0 10px 0', 'textAlign': 'center'}),
                                
                                # Iteramos por cada categoría usando componentes nativos de Dash
                                html.Div([
                                    # Para cada categoría creamos un panel colapsable
                                    html.Div([
                                        # Encabezado que siempre está visible
                                        html.Div([
                                            html.Button(
                                                category,
                                                id={'type': 'category-button', 'index': f"{game.get('gameId', '')}-{i}"},
                                                n_clicks=0,
                                                style={
                                                    'backgroundColor': '#f1f1f1',
                                                    'color': '#444',
                                                    'padding': '10px 15px',
                                                    'width': '100%',
                                                    'textAlign': 'left',
                                                    'border': 'none',
                                                    'outline': 'none',
                                                    'cursor': 'pointer',
                                                    'fontWeight': 'bold',
                                                    'borderRadius': '3px',
                                                    'marginBottom': '2px'
                                                }
                                            ),
                                        ]),
                                        
                                        # Contenido visible directamente sin colapsar
                                        html.Div([
                                            # Tabla de estadísticas para esta categoría
                                            html.Table([
                                                # Encabezado de la tabla
                                                html.Thead(
                                                    html.Tr([
                                                        html.Th(away_team, style={'width': '25%', 'textAlign': 'center'}),
                                                        html.Th("Estadística", style={'width': '40%', 'textAlign': 'center'}),
                                                        html.Th("Peso", style={'width': '10%', 'textAlign': 'center'}),
                                                        html.Th(home_team, style={'width': '25%', 'textAlign': 'center'})
                                                    ])
                                                ),
                                                # Cuerpo de la tabla con las estadísticas de esta categoría
                                                html.Tbody([
                                                    html.Tr([
                                                        # Valor equipo visitante
                                                        html.Td(f"{matchup_analysis['comparison'][key]['team2_value']:.1f}", 
                                                              style={
                                                                  'textAlign': 'center',
                                                                  'color': '#CE1141' if matchup_analysis['comparison'][key]['advantage'] == 'team1' else '#008348',
                                                                  'fontWeight': 'bold' if matchup_analysis['comparison'][key]['advantage'] == 'team2' else 'normal'
                                                              }),
                                                        # Nombre de la estadística
                                                        html.Td(name, style={'textAlign': 'center'}),
                                                        # Peso de la estadística
                                                        html.Td(f"{weight}", style={'textAlign': 'center', 'fontSize': '0.9em'}),
                                                        # Valor equipo local
                                                        html.Td(f"{matchup_analysis['comparison'][key]['team1_value']:.1f}", 
                                                              style={
                                                                  'textAlign': 'center', 
                                                                  'color': '#CE1141' if matchup_analysis['comparison'][key]['advantage'] == 'team2' else '#008348',
                                                                  'fontWeight': 'bold' if matchup_analysis['comparison'][key]['advantage'] == 'team1' else 'normal'
                                                              })
                                                    ], style={'backgroundColor': '#f9f9f9' if i % 2 == 0 else 'white'})
                                                    for i, (key, name, weight) in enumerate(stats)
                                                ]),
                                            ], style={'width': '100%', 'borderCollapse': 'collapse', 'marginBottom': '15px'})
                                        ], style={'padding': '10px', 'backgroundColor': 'white', 'border': '1px solid #ddd', 'borderRadius': '0 0 4px 4px', 'marginBottom': '10px'})
                                    ])
                                    for i, (category, stats) in enumerate(matchup_analysis['stat_categories'].items())
                                ]),
                                
                                # Panel para los factores contextuales
                                html.Div([
                                    # Encabezado que siempre es visible
                                    html.Div([
                                        html.Button(
                                            "Factores Contextuales",
                                            id={'type': 'category-button', 'index': f"{game.get('gameId', '')}-factors"},
                                            n_clicks=0,
                                            style={
                                                'backgroundColor': '#e8f5e9',
                                                'color': '#444',
                                                'padding': '10px 15px',
                                                'width': '100%',
                                                'textAlign': 'left',
                                                'border': 'none',
                                                'outline': 'none',
                                                'cursor': 'pointer',
                                                'fontWeight': 'bold',
                                                'borderRadius': '3px',
                                                'marginBottom': '2px',
                                                'marginTop': '10px'
                                            }
                                        ),
                                    ]),
                                    
                                    # Contenido siempre visible
                                    html.Div([
                                        # Tabla de factores adicionales
                                        html.Table([
                                            # Encabezado de la tabla
                                            html.Thead(
                                                html.Tr([
                                                    html.Th("Factor", style={'width': '25%', 'textAlign': 'center'}),
                                                    html.Th("Descripción", style={'width': '50%', 'textAlign': 'center'}),
                                                    html.Th("Impacto", style={'width': '25%', 'textAlign': 'center'})
                                                ])
                                            ),
                                            # Cuerpo de la tabla con los factores adicionales
                                            html.Tbody([
                                                html.Tr([
                                                    # Nombre del factor
                                                    html.Td(factor["name"], style={'textAlign': 'center'}),
                                                    # Descripción del factor
                                                    html.Td(factor["description"], style={'textAlign': 'center'}),
                                                    # Impacto del factor (con color según beneficiario)
                                                    html.Td(
                                                        [
                                                            # Si el impacto es positivo para team1 (local)
                                                            html.Span(f"+{factor['impact']:.1f}% ", 
                                                                     style={'color': home_color, 'fontWeight': 'bold'}) if factor['beneficiary'] == 'team1' and factor['impact'] > 0 else "",
                                                            
                                                            # Si el impacto es positivo para team2 (visitante)
                                                            html.Span(f"+{abs(factor['impact']):.1f}% ", 
                                                                     style={'color': away_color, 'fontWeight': 'bold'}) if factor['beneficiary'] == 'team2' and factor['impact'] < 0 else "",
                                                            
                                                            # Si el impacto es neutral
                                                            html.Span("Neutral", style={'color': '#888'}) if factor['beneficiary'] == 'neutral' or factor['impact'] == 0 else ""
                                                        ], style={'textAlign': 'center'}
                                                    )
                                                ], style={'backgroundColor': '#f9f9f9' if i % 2 == 0 else 'white'})
                                                for i, factor in enumerate(matchup_analysis['additional_factors']['Factores Adicionales'])
                                            ])
                                        ], style={'width': '100%', 'borderCollapse': 'collapse', 'marginBottom': '15px'})
                                    ], style={'padding': '10px', 'backgroundColor': 'white', 'border': '1px solid #ddd', 'borderRadius': '0 0 4px 4px', 'marginBottom': '10px'})
                                ])
                            ], style={'marginTop': '20px', 'backgroundColor': '#fafafa', 'padding': '15px', 'borderRadius': '5px'})
                        ], style={'backgroundColor': '#f5f5f5', 'padding': '15px', 'borderRadius': '5px'})
                    ], style={'padding': '20px', 'borderRadius': '5px', 'boxShadow': '0 2px 5px rgba(0,0,0,0.1)'})
                ], className='card', style={'marginBottom': '30px', 'backgroundColor': 'white'})
                
                game_cards.append(game_card)
        
        # Organizar tarjetas en la página
        return html.Div([
            # Tarjetas de partidos
            html.Div(game_cards)
        ])

    # Callback para actualizar caché del calendario
    @app.callback(
        Output('refresh-schedule-output', 'children'),
        [Input('refresh-schedule-button', 'n_clicks')]
    )
    def refresh_schedule_cache(n_clicks):
        if n_clicks is None or n_clicks == 0:
            return ""
        
        try:
            # Eliminar caché de calendario
            cache_file = os.path.join("cache", "nba_schedule.json")
            if os.path.exists(cache_file):
                os.remove(cache_file)
            
            # Obtener datos actualizados
            get_schedule_data()
            
            return html.Div([
                html.I(className="fas fa-check-circle", style={'color': 'green', 'marginRight': '5px'}),
                "¡Calendario actualizado correctamente! Usando endpoint oficial de la NBA."
            ])
        except Exception as e:
            return html.Div([
                html.I(className="fas fa-exclamation-circle", style={'color': 'red', 'marginRight': '5px'}),
                f"Error al actualizar calendario: {str(e)}"
            ])

    return app

# Función principal para iniciar el dashboard
def main():
    try:
        # Cargar datos
        csv_path = 'nba_team_complete_stats_2024_25.csv'
        if not os.path.exists(csv_path):
            print(f"Error: No se encontró el archivo {csv_path}")
            return
        
        df = pd.read_csv(csv_path)
        print("Columnas en el CSV:")
        print(list(df.columns))
        
        # Crear y lanzar el dashboard
        app = create_dashboard(df)
        
        print("Iniciando el Dashboard NBA...")
        print("Navega a http://127.0.0.1:8050/ en tu navegador para ver el dashboard.")
        app.run_server(debug=True)
    
    except Exception as e:
        print(f"Error al iniciar el dashboard: {e}")

def normalize_team_name(api_team_name, df_team_names):
    """
    Normaliza el nombre del equipo de la API para que coincida con nuestro DataFrame.
    
    Args:
        api_team_name: Nombre del equipo obtenido de la API
        df_team_names: Lista de nombres de equipos en nuestro DataFrame
    
    Returns:
        Nombre normalizado que coincide con el DataFrame o el nombre original
    """
    # Mapeo de nombres conocidos que pueden diferir
    name_mapping = {
        'LA Clippers': 'Los Angeles Clippers',
        'Portland Trail Blazers': 'Portland Trailblazers',  # Posible diferencia
        'Brooklyn Nets': 'Brooklyn Nets',
        'Phoenix Suns': 'Phoenix Suns',
        'Oklahoma City Thunder': 'Oklahoma City Thunder',
        'Utah Jazz': 'Utah Jazz',
        'Los Angeles Lakers': 'Los Angeles Lakers',
        'Denver Nuggets': 'Denver Nuggets',
        'Boston Celtics': 'Boston Celtics',
        'Milwaukee Bucks': 'Milwaukee Bucks',
        'Minnesota Timberwolves': 'Minnesota Timberwolves',
        'Cleveland Cavaliers': 'Cleveland Cavaliers',
        'New York Knicks': 'New York Knicks',
        'Orlando Magic': 'Orlando Magic',
        'Indiana Pacers': 'Indiana Pacers',
        'Philadelphia 76ers': 'Philadelphia 76ers',
        'New Orleans Pelicans': 'New Orleans Pelicans',
        'Dallas Mavericks': 'Dallas Mavericks',
        'Sacramento Kings': 'Sacramento Kings',
        'Houston Rockets': 'Houston Rockets',
        'Miami Heat': 'Miami Heat',
        'Golden State Warriors': 'Golden State Warriors',
        'Atlanta Hawks': 'Atlanta Hawks',
        'Chicago Bulls': 'Chicago Bulls',
        'Toronto Raptors': 'Toronto Raptors',
        'Memphis Grizzlies': 'Memphis Grizzlies',
        'Charlotte Hornets': 'Charlotte Hornets',
        'San Antonio Spurs': 'San Antonio Spurs',
        'Detroit Pistons': 'Detroit Pistons',
        'Washington Wizards': 'Washington Wizards'
    }
    
    # Mostrar información de diagnóstico si es la primera vez
    if not hasattr(normalize_team_name, 'shown_diagnosis'):
        normalize_team_name.shown_diagnosis = True
        print("Nombres de equipos en el DataFrame:")
        for name in sorted(df_team_names):
            print(f"  - {name}")
    
    # Primero, verificar si hay un mapeo directo
    if api_team_name in name_mapping:
        normalized_name = name_mapping[api_team_name]
    else:
        normalized_name = api_team_name
    
    # Verificar si el nombre normalizado está en el DataFrame
    if normalized_name in df_team_names:
        return normalized_name
    
    # Si no coincide exactamente, buscar coincidencias parciales
    for df_name in df_team_names:
        # Eliminar espacios y convertir a minúsculas para comparación
        api_name_clean = normalized_name.lower().replace(' ', '')
        df_name_clean = df_name.lower().replace(' ', '')
        
        # Verificar si el nombre limpio está contenido o es similar
        if api_name_clean in df_name_clean or df_name_clean in api_name_clean:
            print(f"Coincidencia aproximada: '{api_team_name}' -> '{df_name}'")
            return df_name
    
    # Si no se encuentra coincidencia, devolver el nombre original
    print(f"No se encontró coincidencia para el equipo: '{api_team_name}'")
    return api_team_name

def get_schedule_data():
    """
    Obtiene datos de partidos de la NBA utilizando el endpoint oficial de la NBA.
    Implementa caché para evitar llamadas excesivas al endpoint.
    """
    cache_dir = "cache"
    cache_file = os.path.join(cache_dir, "nba_schedule.json")
    
    # Obtener la lista de nombres de equipos del DataFrame
    df_team_names = list(df['TEAM_NAME_x'].unique()) if 'df' in globals() and isinstance(df, pd.DataFrame) and 'TEAM_NAME_x' in df.columns else []
    
    # Crear directorio de caché si no existe
    if not os.path.exists(cache_dir):
        os.makedirs(cache_dir)
    
    # Verificar si hay datos en caché y si son recientes (menos de 3 horas)
    if os.path.exists(cache_file):
        file_timestamp = os.path.getmtime(cache_file)
        current_timestamp = time.time()
        # Si el archivo fue modificado en las últimas 3 horas
        if (current_timestamp - file_timestamp) < 10800:  # 3 horas en segundos
            try:
                with open(cache_file, 'r') as f:
                    return json.load(f)
            except Exception as e:
                print(f"Error leyendo caché de calendario: {e}")
    
    try:
        import requests
        import datetime
        
        print("Obteniendo datos del calendario de la NBA usando el endpoint oficial...")
        
        # URL del endpoint oficial de la NBA
        url = "https://cdn.nba.com/static/json/staticData/scheduleLeagueV2.json"
        
        # Realizar la solicitud HTTP
        response = requests.get(url)
        response.raise_for_status()  # Verificar si hubo errores en la solicitud
        
        # Obtener los datos JSON
        nba_data = response.json()
        
        # Obtener la fecha actual
        current_date = datetime.datetime.now()
        
        # Procesar los datos para obtener los partidos
        schedule = []
        
        # Obtener todas las fechas de juegos
        game_dates = nba_data.get('leagueSchedule', {}).get('gameDates', [])
        
        print(f"Se encontraron {len(game_dates)} fechas con partidos")
        
        for date_data in game_dates:
            # Convertir formato de fecha "MM/DD/YYYY 00:00:00" a "YYYY-MM-DD"
            try:
                game_date_str = date_data.get('gameDate', '')
                game_date = datetime.datetime.strptime(game_date_str, "%m/%d/%Y %H:%M:%S")
                formatted_date = game_date.strftime("%Y-%m-%d")
            except Exception as e:
                print(f"Error al procesar fecha: {game_date_str} - {e}")
                continue
            
            for game in date_data.get('games', []):
                home_team_data = game.get('homeTeam', {})
                away_team_data = game.get('awayTeam', {})
                
                # Obtener nombres completos de los equipos
                home_team = f"{home_team_data.get('teamCity', '')} {home_team_data.get('teamName', '')}"
                away_team = f"{away_team_data.get('teamCity', '')} {away_team_data.get('teamName', '')}"
                
                # Normalizar nombres de equipos para que coincidan con nuestro dataset
                home_team = normalize_team_name(home_team, df_team_names)
                away_team = normalize_team_name(away_team, df_team_names)
                
                # Obtener hora del partido en UTC y convertir a formato local
                game_time_utc = game.get('gameDateTimeUTC', '')
                
                try:
                    # Intentar extraer solo la hora del partido
                    if game_time_utc:
                        game_time = datetime.datetime.strptime(game_time_utc, "%Y-%m-%dT%H:%M:%SZ")
                        # Convertir a formato de 24 horas
                        time_str = game_time.strftime("%H:%M")
                    else:
                        time_str = "19:30"  # Hora por defecto
                except Exception as e:
                    print(f"Error procesando hora del partido: {e}")
                    time_str = "19:30"  # Hora por defecto
                
                # Crear entrada para el partido con información adicional
                game_entry = {
                    'gameDate': formatted_date,
                    'time': time_str,
                    'homeTeam': home_team,
                    'awayTeam': away_team,
                    'game_id': game.get('gameId', ''),
                    'status': game.get('gameStatusText', ''),
                    'arena': game.get('arenaName', ''),
                    'city': game.get('arenaCity', ''),
                    'gameLabel': game.get('gameLabel', ''),
                    'homeScore': home_team_data.get('score', 0),
                    'awayScore': away_team_data.get('score', 0)
                }
                
                schedule.append(game_entry)
        
        # Si no se encontraron partidos, generar datos de muestra
        if not schedule:
            print("No se encontraron partidos. Generando datos de muestra...")
            schedule = generate_sample_schedule(df_team_names)
        else:
            print(f"Se encontraron {len(schedule)} partidos.")
        
        # Guardar en caché
        with open(cache_file, 'w') as f:
            json.dump(schedule, f)
        
        return schedule
    
    except Exception as e:
        print(f"Error obteniendo datos del calendario: {e}")
        print("Generando datos de muestra como fallback...")
        
        # Generar datos de muestra como fallback
        schedule = generate_sample_schedule(df_team_names)
        
        # Guardar en caché
        with open(cache_file, 'w') as f:
            json.dump(schedule, f)
        
        return schedule

def generate_sample_schedule(team_names):
    """
    Genera un calendario de muestra con partidos aleatorios.
    
    Args:
        team_names: Lista de nombres de equipos
    
    Returns:
        Lista de partidos generados
    """
    if not team_names:
        # Si no hay nombres de equipos, usar algunos predeterminados
        team_names = [
            "Atlanta Hawks", "Boston Celtics", "Brooklyn Nets", "Charlotte Hornets",
            "Chicago Bulls", "Cleveland Cavaliers", "Dallas Mavericks", "Denver Nuggets",
            "Detroit Pistons", "Golden State Warriors", "Houston Rockets", "Indiana Pacers",
            "Los Angeles Clippers", "Los Angeles Lakers", "Memphis Grizzlies", "Miami Heat",
            "Milwaukee Bucks", "Minnesota Timberwolves", "New Orleans Pelicans", "New York Knicks",
            "Oklahoma City Thunder", "Orlando Magic", "Philadelphia 76ers", "Phoenix Suns",
            "Portland Trail Blazers", "Sacramento Kings", "San Antonio Spurs", "Toronto Raptors",
            "Utah Jazz", "Washington Wizards"
        ]
    
    schedule = []
    
    # Generar calendario para toda la temporada
    # Desde octubre hasta junio (9 meses)
    start_date = datetime.datetime(2024, 10, 1)
    end_date = datetime.datetime(2025, 6, 30)
    
    # Generar partidos para cada semana de la temporada
    current_date = start_date
    while current_date <= end_date:
        # Saltamos algunos días para no tener partidos todos los días
        # Típicamente se juegan más partidos en días específicos de la semana
        days_with_games = [0, 1, 3, 4, 6]  # Lunes, martes, jueves, viernes, domingo
        
        # Si el día de la semana está en la lista de días con juegos
        if current_date.weekday() in days_with_games:
            game_date_str = current_date.strftime("%Y-%m-%d")
            
            # Generar 4-8 partidos por día de juego
            num_games = random.randint(4, 8)
            teams_used_today = set()
            
            for j in range(num_games):
                # Seleccionar equipos que no hayan jugado hoy
                available_teams = [team for team in team_names if team not in teams_used_today]
                
                if len(available_teams) < 2:
                    break
                
                home_team = random.choice(available_teams)
                teams_used_today.add(home_team)
                available_teams.remove(home_team)
                
                away_team = random.choice(available_teams)
                teams_used_today.add(away_team)
                
                # Generar hora aleatoria (entre 17:00 y 22:00)
                hour = random.randint(17, 22)
                minute = random.choice([0, 30])
                game_time = f"{hour:02d}:{minute:02d}"
                
                game_entry = {
                    'gameDate': game_date_str,
                    'time': game_time,
                    'homeTeam': home_team,
                    'awayTeam': away_team,
                    'game_id': f"sample_{current_date.strftime('%m%d')}_{j}",
                    'status': '',
                    'arena': 'NBA Arena',
                    'city': 'NBA City',
                    'gameLabel': 'Regular Season'
                }
                
                schedule.append(game_entry)
        
        # Avanzar al siguiente día
        current_date += datetime.timedelta(days=1)
    
    return schedule

def analyze_matchup(team1_name, team2_name, df):
    """
    Analiza un enfrentamiento entre dos equipos y calcula la probabilidad de victoria.
    Retorna un diccionario con estadísticas comparativas y predicciones.
    
    Modelo avanzado que considera múltiples factores con pesos diferenciados:
    - Eficiencia ofensiva (tiros de campo, triples, tiros libres)
    - Defensa (rating defensivo, bloqueos, robos)
    - Tendencias de juego (rebotes, asistencias, ritmo)
    - Factores contextuales (victorias recientes, rendimiento histórico)
    """
    if team1_name not in df['TEAM_NAME_x'].values or team2_name not in df['TEAM_NAME_x'].values:
        return None
    
    team1_data = df[df['TEAM_NAME_x'] == team1_name].iloc[0]
    team2_data = df[df['TEAM_NAME_x'] == team2_name].iloc[0]
    
    # Agrupar estadísticas por categorías con sus respectivos pesos
    stat_categories = {
        "Ofensiva": [
            ('PTS', 'Puntos por partido', 1.0),
            ('E_OFF_RATING', 'Rating Ofensivo', 1.2),
            ('FG_PCT', 'Porcentaje tiros campo', 0.9),
            ('FG3_PCT', 'Porcentaje triples', 0.8),
            ('FT_PCT', 'Porcentaje tiros libres', 0.7),
            ('AST', 'Asistencias', 0.8),
            ('E_AST_RATIO', 'Ratio de asistencias', 0.7),
            ('FGM', 'Canastas anotadas', 0.6),
            ('FG3M', 'Triples anotados', 0.6)
        ],
        "Defensa": [
            ('E_DEF_RATING', 'Rating Defensivo', 1.2),
            ('STL', 'Robos', 0.8),
            ('BLK', 'Tapones', 0.7),
            ('BLKA', 'Tapones recibidos', 0.6),
            ('PF', 'Faltas cometidas', 0.6)
        ],
        "Rebotes y Posesiones": [
            ('REB', 'Rebotes totales', 0.9),
            ('OREB', 'Rebotes ofensivos', 0.8),
            ('DREB', 'Rebotes defensivos', 0.7),
            ('E_OREB_PCT', 'Porcentaje rebotes ofensivos', 0.7),
            ('E_DREB_PCT', 'Porcentaje rebotes defensivos', 0.7),
            ('TOV', 'Pérdidas', 0.8),
            ('E_TM_TOV_PCT', 'Porcentaje pérdidas', 0.7),
            ('E_PACE', 'Ritmo de juego', 0.5)
        ],
        "Factores de victoria": [
            ('W_PCT_x', 'Porcentaje victorias', 1.5),
            ('E_NET_RATING', 'Rating Neto', 1.3),
            ('PLUS_MINUS', 'Diferencial puntos', 1.0)
        ]
    }
    
    # Inicializar comparación y contadores de ventajas ponderadas
    comparison = {}
    advantage_points = {"team1": 0, "team2": 0}
    total_weight = 0
    
    # Analizar cada categoría y estadística
    for category, stats in stat_categories.items():
        for key, name, weight in stats:
            if key in team1_data and key in team2_data:
                total_weight += weight
                advantage = "team1"  # Por defecto
                
                # Estadísticas donde menor es mejor (invertir comparación)
                if key in ['E_DEF_RATING', 'TOV', 'E_TM_TOV_PCT', 'BLKA', 'PF']:
                    if team1_data[key] < team2_data[key]:
                        advantage_points["team1"] += weight
                        advantage = "team1"
                    else:
                        advantage_points["team2"] += weight
                        advantage = "team2"
                # Para todas las demás estadísticas, mayor es mejor
                else:
                    if team1_data[key] > team2_data[key]:
                        advantage_points["team1"] += weight
                        advantage = "team1"
                    else:
                        advantage_points["team2"] += weight
                        advantage = "team2"
                
                # Guardar comparación para mostrar en la interfaz
                comparison[key] = {
                    "name": name,
                    "category": category,
                    "team1_value": team1_data[key],
                    "team2_value": team2_data[key],
                    "advantage": advantage,
                    "weight": weight
                }
    
    # Calcular probabilidades basadas en puntos ponderados
    team1_win_prob = (advantage_points["team1"] / total_weight) * 100
    team2_win_prob = (advantage_points["team2"] / total_weight) * 100
    
    # Factores de ajuste adicionales
    
    # 1. Factor de momentum (ventaja al equipo con mejor racha reciente)
    # Simulamos este factor con el porcentaje de victorias, ya que no tenemos datos de rachas
    momentum_factor = 5  # Ajuste de hasta 5%
    if team1_data['W_PCT_x'] > team2_data['W_PCT_x'] * 1.2:  # 20% mejor
        team1_win_prob += momentum_factor
        team2_win_prob -= momentum_factor
    elif team2_data['W_PCT_x'] > team1_data['W_PCT_x'] * 1.2:
        team1_win_prob -= momentum_factor
        team2_win_prob += momentum_factor
    
    # 2. Factor de estilo de juego (equipos de ritmo alto vs equipos de ritmo bajo)
    pace_factor = 3  # Ajuste de hasta 3%
    if team1_data['E_PACE'] > team2_data['E_PACE'] * 1.1:  # Equipo 1 juega a un ritmo 10% más alto
        high_pace_team = "team1"
        low_pace_team = "team2"
    elif team2_data['E_PACE'] > team1_data['E_PACE'] * 1.1:
        high_pace_team = "team2"
        low_pace_team = "team1"
    else:
        high_pace_team = None
        low_pace_team = None
    
    # Si hay diferencia significativa en ritmo, el equipo de ritmo alto tiene ventaja si es mejor ofensivamente
    # El equipo de ritmo bajo tiene ventaja si es mejor defensivamente
    if high_pace_team and low_pace_team:
        if high_pace_team == "team1" and team1_data['E_OFF_RATING'] > team2_data['E_OFF_RATING']:
            team1_win_prob += pace_factor
            team2_win_prob -= pace_factor
        elif high_pace_team == "team2" and team2_data['E_OFF_RATING'] > team1_data['E_OFF_RATING']:
            team1_win_prob -= pace_factor
            team2_win_prob += pace_factor
        elif low_pace_team == "team1" and team1_data['E_DEF_RATING'] < team2_data['E_DEF_RATING']:
            team1_win_prob += pace_factor
            team2_win_prob -= pace_factor
        elif low_pace_team == "team2" and team2_data['E_DEF_RATING'] < team1_data['E_DEF_RATING']:
            team1_win_prob -= pace_factor
            team2_win_prob += pace_factor
    
    # 3. Factor de eficiencia de tiro y defensa contra tiros
    shooting_factor = 4  # Ajuste de hasta 4%
    if team1_data['FG_PCT'] > team2_data['FG_PCT'] * 1.1 and team1_data['FG3_PCT'] > team2_data['FG3_PCT'] * 1.1:
        team1_win_prob += shooting_factor
        team2_win_prob -= shooting_factor
    elif team2_data['FG_PCT'] > team1_data['FG_PCT'] * 1.1 and team2_data['FG3_PCT'] > team1_data['FG3_PCT'] * 1.1:
        team1_win_prob -= shooting_factor
        team2_win_prob += shooting_factor
    
    # 4. Factor de localía (Home-Court Advantage)
    # En la NBA, históricamente, jugar en casa proporciona aproximadamente un 60% de probabilidad de victoria
    # En nuestro modelo, team1 es siempre el equipo local
    home_court_advantage = 6.0  # Ajuste de 6% por jugar en casa
    team1_win_prob += home_court_advantage  # Beneficia al equipo local (team1)
    team2_win_prob -= home_court_advantage  # Penaliza al equipo visitante (team2)
    
    # Si el equipo visitante tiene un porcentaje de victorias mucho mayor que el local,
    # se reduce ligeramente el factor de localía
    if team2_data['W_PCT_x'] > team1_data['W_PCT_x'] * 1.3:  # Visitante 30% mejor
        neutralizing_factor = 2.0
        team1_win_prob -= neutralizing_factor
        team2_win_prob += neutralizing_factor
    
    # Asegurar que las probabilidades estén en el rango 0-100%
    team1_win_prob = max(0, min(100, team1_win_prob))
    team2_win_prob = max(0, min(100, team2_win_prob))
    
    # Asegurar que las probabilidades sumen exactamente 100%
    total_prob = team1_win_prob + team2_win_prob
    if total_prob > 0:  # Evitar división por cero
        team1_win_prob = (team1_win_prob / total_prob) * 100
        team2_win_prob = (team2_win_prob / total_prob) * 100
    else:
        # Si ambas probabilidades son 0, distribuir equitativamente
        team1_win_prob = 50
        team2_win_prob = 50
    
    # Calcular nivel de confianza basado en la diferencia de probabilidad
    confidence_level = abs(team1_win_prob - team2_win_prob)
    
    # Definir estadísticas clave para mostrar en la interfaz
    key_stats_for_display = ['PTS', 'AST', 'REB', 'E_OFF_RATING', 'E_DEF_RATING']
    stat_display_names = ['Puntos', 'Asistencias', 'Rebotes', 'Rating Of.', 'Rating Def.']
    
    # Añadir los factores adicionales al diccionario de comparación
    additional_factors = {
        "Factores Adicionales": [
            {
                "key": "home_court",
                "name": "Factor Localía",
                "description": f"Ventaja del equipo local: +{home_court_advantage}%",
                "impact": home_court_advantage,
                "beneficiary": "team1"
            },
            {
                "key": "momentum",
                "name": "Momentum",
                "description": "Ventaja por mejor racha reciente",
                "impact": momentum_factor if team1_data['W_PCT_x'] > team2_data['W_PCT_x'] * 1.2 else 
                         -momentum_factor if team2_data['W_PCT_x'] > team1_data['W_PCT_x'] * 1.2 else 0,
                "beneficiary": "team1" if team1_data['W_PCT_x'] > team2_data['W_PCT_x'] * 1.2 else 
                             "team2" if team2_data['W_PCT_x'] > team1_data['W_PCT_x'] * 1.2 else "neutral"
            },
            {
                "key": "pace",
                "name": "Estilo de Juego",
                "description": "Ventaja por ritmo de juego",
                "impact": pace_factor if high_pace_team and 
                          ((high_pace_team == "team1" and team1_data['E_OFF_RATING'] > team2_data['E_OFF_RATING']) or
                           (low_pace_team == "team1" and team1_data['E_DEF_RATING'] < team2_data['E_DEF_RATING'])) else
                         -pace_factor if high_pace_team and 
                          ((high_pace_team == "team2" and team2_data['E_OFF_RATING'] > team1_data['E_OFF_RATING']) or
                           (low_pace_team == "team2" and team2_data['E_DEF_RATING'] < team1_data['E_DEF_RATING'])) else 0,
                "beneficiary": "team1" if high_pace_team and 
                               ((high_pace_team == "team1" and team1_data['E_OFF_RATING'] > team2_data['E_OFF_RATING']) or
                                (low_pace_team == "team1" and team1_data['E_DEF_RATING'] < team2_data['E_DEF_RATING'])) else
                              "team2" if high_pace_team and 
                               ((high_pace_team == "team2" and team2_data['E_OFF_RATING'] > team1_data['E_OFF_RATING']) or
                                (low_pace_team == "team2" and team2_data['E_DEF_RATING'] < team1_data['E_DEF_RATING'])) else "neutral"
            },
            {
                "key": "shooting",
                "name": "Eficiencia de Tiro",
                "description": "Ventaja por mejor eficiencia en tiros",
                "impact": shooting_factor if team1_data['FG_PCT'] > team2_data['FG_PCT'] * 1.1 and team1_data['FG3_PCT'] > team2_data['FG3_PCT'] * 1.1 else
                         -shooting_factor if team2_data['FG_PCT'] > team1_data['FG_PCT'] * 1.1 and team2_data['FG3_PCT'] > team1_data['FG3_PCT'] * 1.1 else 0,
                "beneficiary": "team1" if team1_data['FG_PCT'] > team2_data['FG_PCT'] * 1.1 and team1_data['FG3_PCT'] > team2_data['FG3_PCT'] * 1.1 else
                              "team2" if team2_data['FG_PCT'] > team1_data['FG_PCT'] * 1.1 and team2_data['FG3_PCT'] > team1_data['FG3_PCT'] * 1.1 else "neutral"
            }
        ]
    }
    
    return {
        "comparison": comparison,
        "win_probability": {
            "team1": round(team1_win_prob, 1),
            "team2": round(team2_win_prob, 1)
        },
        "prediction": team1_name if team1_win_prob > team2_win_prob else team2_name,
        "confidence": confidence_level,  # Nivel de confianza basado en la diferencia
        "key_stats_for_display": key_stats_for_display,
        "stat_display_names": stat_display_names,
        "stat_categories": stat_categories,  # Enviamos las categorías completas
        "additional_factors": additional_factors  # Enviamos los factores adicionales
    }

if __name__ == '__main__':
    main() 