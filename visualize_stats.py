import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import os
import numpy as np

# Configuración de estilo para las visualizaciones
plt.style.use('fivethirtyeight')
sns.set(font_scale=1.2)

# Cargar los datos de estadísticas combinadas
combined_stats = pd.read_csv("nba_team_complete_stats_2024_25.csv")

# Crear carpeta para guardar las visualizaciones
if not os.path.exists("visualizaciones"):
    os.makedirs("visualizaciones")

print(f"Se han cargado datos de {len(combined_stats)} equipos de la NBA")

# 1. Visualización de la correlación entre Ofensiva y Defensiva
plt.figure(figsize=(12, 10))
plt.scatter(combined_stats['E_OFF_RATING'], combined_stats['E_DEF_RATING'], 
           s=100, alpha=0.7, c=combined_stats['W_PCT_x'], cmap='viridis')

# Añadir nombres de los equipos como etiquetas
for i, txt in enumerate(combined_stats['TEAM_NAME_x']):
    plt.annotate(txt, (combined_stats['E_OFF_RATING'].iloc[i], combined_stats['E_DEF_RATING'].iloc[i]),
                fontsize=9)

plt.colorbar(label='Porcentaje de Victorias')
plt.title('Relación entre Rating Ofensivo y Defensivo', fontsize=16)
plt.xlabel('Rating Ofensivo (E_OFF_RATING)', fontsize=14)
plt.ylabel('Rating Defensivo (E_DEF_RATING)', fontsize=14)
# Invertir el eje Y para que los mejores equipos defensivos estén arriba
plt.gca().invert_yaxis()
plt.tight_layout()
plt.savefig('visualizaciones/ofensiva_vs_defensiva.png', dpi=300)
plt.close()

# 2. Top 10 equipos por puntos por partido
top_pts = combined_stats.sort_values('PTS', ascending=False).head(10)
plt.figure(figsize=(14, 8))
sns.barplot(x='TEAM_NAME_x', y='PTS', data=top_pts, palette='viridis')
plt.title('Top 10 Equipos por Puntos por Partido', fontsize=16)
plt.xticks(rotation=45, ha='right')
plt.ylabel('Puntos por partido')
plt.tight_layout()
plt.savefig('visualizaciones/top10_puntos.png', dpi=300)
plt.close()

# 3. Relación entre asistencias y victorias
plt.figure(figsize=(12, 8))
sns.regplot(x='AST', y='W_PCT_x', data=combined_stats, scatter_kws={'s':100, 'alpha':0.7})

# Añadir nombres de los equipos
for i, txt in enumerate(combined_stats['TEAM_NAME_x']):
    plt.annotate(txt, (combined_stats['AST'].iloc[i], combined_stats['W_PCT_x'].iloc[i]),
                fontsize=9)

plt.title('Relación entre Asistencias y Porcentaje de Victorias', fontsize=16)
plt.xlabel('Asistencias por Partido', fontsize=14)
plt.ylabel('Porcentaje de Victorias', fontsize=14)
plt.tight_layout()
plt.savefig('visualizaciones/asistencias_vs_victorias.png', dpi=300)
plt.close()

# 4. Mapa de calor de correlaciones
plt.figure(figsize=(18, 16))
stats_corr = combined_stats[['PTS', 'FG_PCT', 'FG3_PCT', 'FT_PCT', 'AST', 'REB',
                           'STL', 'BLK', 'TOV', 'E_OFF_RATING', 'E_DEF_RATING',
                           'E_PACE', 'E_AST_RATIO', 'W_PCT_x']].corr()
mask = np.triu(np.ones_like(stats_corr, dtype=bool))
heatmap = sns.heatmap(stats_corr, mask=mask, annot=True, fmt='.2f', cmap='viridis',
                     vmin=-1, vmax=1, square=True, linewidths=.5)
plt.title('Correlación entre Estadísticas de Equipos', fontsize=18)
plt.tight_layout()
plt.savefig('visualizaciones/correlacion_estadisticas.png', dpi=300)
plt.close()

# 5. Comparar ritmo de juego (PACE) y efectividad ofensiva
plt.figure(figsize=(12, 8))
sns.scatterplot(x='E_PACE', y='E_OFF_RATING', size='PTS', sizes=(50, 400),
               hue='W_PCT_x', palette='viridis', data=combined_stats)

# Añadir nombres de los equipos
for i, txt in enumerate(combined_stats['TEAM_NAME_x']):
    plt.annotate(txt, (combined_stats['E_PACE'].iloc[i], combined_stats['E_OFF_RATING'].iloc[i]),
                fontsize=9)

plt.title('Ritmo de Juego vs Eficiencia Ofensiva', fontsize=16)
plt.xlabel('Ritmo (Posesiones por 48 min)', fontsize=14)
plt.ylabel('Rating Ofensivo', fontsize=14)
plt.tight_layout()
plt.savefig('visualizaciones/ritmo_vs_ofensiva.png', dpi=300)
plt.close()

print("Visualizaciones generadas con éxito en la carpeta 'visualizaciones'")

# 6. Tabla de líderes en diferentes categorías
leaders = pd.DataFrame({
    'Categoría': ['Puntos por partido', 'Eficiencia Ofensiva', 'Eficiencia Defensiva', 
                 'Rebotes por partido', 'Asistencias por partido', 'Robos por partido'],
    'Equipo Líder': [
        combined_stats.loc[combined_stats['PTS'].idxmax(), 'TEAM_NAME_x'],
        combined_stats.loc[combined_stats['E_OFF_RATING'].idxmax(), 'TEAM_NAME_x'],
        combined_stats.loc[combined_stats['E_DEF_RATING'].idxmin(), 'TEAM_NAME_x'],
        combined_stats.loc[combined_stats['REB'].idxmax(), 'TEAM_NAME_x'],
        combined_stats.loc[combined_stats['AST'].idxmax(), 'TEAM_NAME_x'],
        combined_stats.loc[combined_stats['STL'].idxmax(), 'TEAM_NAME_x']
    ],
    'Valor': [
        combined_stats['PTS'].max(),
        combined_stats['E_OFF_RATING'].max(),
        combined_stats['E_DEF_RATING'].min(),
        combined_stats['REB'].max(),
        combined_stats['AST'].max(),
        combined_stats['STL'].max()
    ]
})

print("\nLíderes de la liga por categoría:")
print(leaders) 