#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os
import pandas as pd
from dashboard import create_dashboard, main

# Punto de entrada para AWS Amplify
if __name__ == '__main__':
    # Verificar directorios necesarios
    os.makedirs('visualizations', exist_ok=True)
    os.makedirs('visualizaciones', exist_ok=True)
    os.makedirs('logos', exist_ok=True)
    os.makedirs('cache', exist_ok=True)
    
    try:
        # Intentar cargar los datos
        df = pd.read_csv('nba_team_complete_stats_2024_25.csv')
        print("Datos cargados correctamente")
    except Exception as e:
        print(f"Error al cargar datos: {e}")
        print("Ejecutando función principal para generar datos...")
        main()
    
    # Ejecutar la función principal
    main() 