from nba_api.stats.endpoints import teamestimatedmetrics
from nba_api.stats.static import teams
import pandas as pd

# Obtener la lista de todos los equipos de la NBA
all_teams = teams.get_teams()
print(f"Total de equipos en la NBA: {len(all_teams)}")

# Obtener métricas avanzadas estimadas para todos los equipos en la temporada actual
advanced_metrics = teamestimatedmetrics.TeamEstimatedMetrics(
    season="2024-25",
    season_type="Regular Season",
    league_id="00"  # NBA
)

# Obtener los datos como un DataFrame de pandas
metrics_df = advanced_metrics.get_data_frames()[0]

# Mostrar los nombres de las columnas disponibles
print("\nColumnas de métricas avanzadas disponibles:")
print(list(metrics_df.columns))

# Mostrar las métricas avanzadas de todos los equipos
print("\nMétricas avanzadas de equipos para la temporada 2024-25:")
pd.set_option('display.max_columns', None)  # Mostrar todas las columnas
pd.set_option('display.width', 1000)  # Ampliar el ancho de visualización
print(metrics_df)

# Guardar las métricas avanzadas en un archivo CSV
metrics_df.to_csv("nba_team_advanced_metrics_2024_25.csv", index=False)
print("\nMétricas avanzadas guardadas en 'nba_team_advanced_metrics_2024_25.csv'")

# Combinar con estadísticas básicas
try:
    # Cargar las estadísticas básicas guardadas previamente
    basic_stats = pd.read_csv("nba_team_stats_2024_25.csv")
    
    # Unir ambos conjuntos de datos por TEAM_ID
    combined_stats = pd.merge(basic_stats, metrics_df, on="TEAM_ID", how="inner")
    
    # Guardar el conjunto de datos combinado
    combined_stats.to_csv("nba_team_complete_stats_2024_25.csv", index=False)
    print("\nEstadísticas completas guardadas en 'nba_team_complete_stats_2024_25.csv'")
except Exception as e:
    print(f"\nNo se pudieron combinar las estadísticas: {e}") 