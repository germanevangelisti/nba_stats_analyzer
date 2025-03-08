#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os
import pandas as pd
import sys

# Asegurarse de que el directorio actual esté en el path para importaciones
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

# Importaciones locales
from dashboard import create_dashboard

# Verificar directorios necesarios
os.makedirs('visualizations', exist_ok=True)
os.makedirs('visualizaciones', exist_ok=True)
os.makedirs('logos', exist_ok=True)
os.makedirs('cache', exist_ok=True)

# Aplicación principal para Elastic Beanstalk
def create_app():
    try:
        # Intentar cargar los datos
        csv_path = 'nba_team_complete_stats_2024_25.csv'
        if os.path.exists(csv_path):
            df = pd.read_csv(csv_path)
            print(f"Datos cargados correctamente de {csv_path}")
            print(f"Dimensiones del DataFrame: {df.shape}")
        else:
            print(f"No se encontró el archivo {csv_path}. Creando DataFrame vacío.")
            df = pd.DataFrame()
        
        # Crear la aplicación Dash
        app = create_dashboard(df)
        return app
    
    except Exception as e:
        print(f"Error al inicializar la aplicación: {e}")
        # Crear una aplicación con un DataFrame vacío como fallback
        return create_dashboard(pd.DataFrame())

# Crear la aplicación - necesario para Elastic Beanstalk
application = create_app()
# Alias para WSGI
app = application

# Para ejecución local
if __name__ == '__main__':
    host = os.environ.get('HOST', '0.0.0.0')
    port = int(os.environ.get('PORT', 8050))
    debug = os.environ.get('DEBUG', 'False').lower() in ('true', '1', 't')
    
    print(f"Iniciando servidor en {host}:{port} (debug: {debug})")
    application.run_server(host=host, port=port, debug=debug) 