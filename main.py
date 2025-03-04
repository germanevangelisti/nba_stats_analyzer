from nba_api.stats.endpoints import leaguedashteamstats
from nba_api.stats.static import teams
import pandas as pd

# Obtener la lista de todos los equipos de la NBA
all_teams = teams.get_teams()
print(f"Total de equipos en la NBA: {len(all_teams)}")

# Obtener estadísticas de todos los equipos para la temporada actual (2024-25)
team_stats = leaguedashteamstats.LeagueDashTeamStats(
    season="2024-25",
    season_type_all_star="Regular Season",
    per_mode_detailed="PerGame",
    measure_type_detailed_defense="Base",
    plus_minus="N",
    pace_adjust="N",
    rank="N",
    shot_clock_range_nullable="",
    period=0,
    last_n_games=0,
    month=0
)

# Obtener los datos como un DataFrame de pandas
stats_df = team_stats.get_data_frames()[0]

# Mostrar los nombres de las columnas disponibles
print("\nColumnas de estadísticas disponibles:")
print(list(stats_df.columns))

# Mostrar las estadísticas de todos los equipos
print("\nEstadísticas de equipos para la temporada 2024-25:")
pd.set_option('display.max_columns', None)  # Mostrar todas las columnas
pd.set_option('display.width', 1000)  # Ampliar el ancho de visualización
print(stats_df)

# Guardar estadísticas en un archivo CSV
stats_df.to_csv("nba_team_stats_2024_25.csv", index=False)
print("\nEstadísticas guardadas en 'nba_team_stats_2024_25.csv'")