import pandas as pd

# Cargar el archivo CSV
combined_stats = pd.read_csv("nba_team_complete_stats_2024_25.csv")

# Imprimir las columnas disponibles
print("Columnas disponibles en el archivo CSV:")
print(combined_stats.columns.tolist())

# Imprimir las primeras filas para ver la estructura
print("\nPrimeras filas del conjunto de datos:")
print(combined_stats.head(2)) 