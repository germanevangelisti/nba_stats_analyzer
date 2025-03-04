import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import os
import numpy as np  # Añadir numpy para operaciones de ángulos

# Cargar los datos combinados
combined_stats = pd.read_csv("nba_team_complete_stats_2024_25.csv")

def mostrar_equipos():
    """Muestra la lista de equipos disponibles para consulta"""
    print("\nEquipos disponibles:")
    # Ordenar equipos alfabéticamente para mejor visualización
    teams = sorted(combined_stats['TEAM_NAME_x'].tolist())
    # Mostrar en formato de columnas para mejor visualización
    for i in range(0, len(teams), 3):
        row = teams[i:i+3]
        print("  ".join(f"{team:<25}" for team in row))
    print()

def buscar_equipo(nombre_parcial):
    """Busca equipos que coincidan parcialmente con el nombre proporcionado"""
    matches = combined_stats[combined_stats['TEAM_NAME_x'].str.contains(nombre_parcial, case=False)]
    if len(matches) == 0:
        print(f"No se encontraron equipos con '{nombre_parcial}' en su nombre.")
        return None
    elif len(matches) == 1:
        # Si hay una única coincidencia, devolver esa
        return matches.iloc[0]
    else:
        # Mostrar las opciones y pedir selección
        print(f"Se encontraron {len(matches)} equipos:")
        for i, team in enumerate(matches['TEAM_NAME_x']):
            print(f"{i+1}. {team}")
        try:
            choice = int(input("Seleccione un número: ")) - 1
            if 0 <= choice < len(matches):
                return matches.iloc[choice]
            else:
                print("Selección no válida.")
                return None
        except ValueError:
            print("Por favor, ingrese un número válido.")
            return None

def mostrar_estadisticas(equipo):
    """Muestra estadísticas detalladas del equipo seleccionado"""
    if equipo is None:
        return
    
    # Estadísticas básicas
    print(f"\n===== Estadísticas de {equipo['TEAM_NAME_x']} =====")
    print(f"Record: {int(equipo['W_x'])}-{int(equipo['L_x'])} ({equipo['W_PCT_x']:.3f})")
    print(f"Puntos por partido: {equipo['PTS']:.1f} (Ranking: {int(equipo['PTS_RANK'])})")
    
    # Estadísticas de tiro
    print("\n----- Estadísticas de Tiro -----")
    print(f"Tiros de campo: {equipo['FGM']:.1f}/{equipo['FGA']:.1f} ({equipo['FG_PCT']:.3f})")
    print(f"Triples: {equipo['FG3M']:.1f}/{equipo['FG3A']:.1f} ({equipo['FG3_PCT']:.3f})")
    print(f"Tiros libres: {equipo['FTM']:.1f}/{equipo['FTA']:.1f} ({equipo['FT_PCT']:.3f})")
    
    # Estadísticas avanzadas
    print("\n----- Estadísticas Avanzadas -----")
    print(f"Rating Ofensivo: {equipo['E_OFF_RATING']:.1f} (Ranking: {int(equipo['E_OFF_RATING_RANK'])})")
    print(f"Rating Defensivo: {equipo['E_DEF_RATING']:.1f} (Ranking: {int(equipo['E_DEF_RATING_RANK'])})")
    print(f"Rating Neto: {equipo['E_NET_RATING']:.1f} (Ranking: {int(equipo['E_NET_RATING_RANK'])})")
    print(f"Ritmo (PACE): {equipo['E_PACE']:.1f} (Ranking: {int(equipo['E_PACE_RANK'])})")
    
    # Otras estadísticas
    print("\n----- Otras Estadísticas -----")
    print(f"Rebotes: {equipo['REB']:.1f} (O: {equipo['OREB']:.1f}, D: {equipo['DREB']:.1f})")
    print(f"Asistencias: {equipo['AST']:.1f} (Ranking: {int(equipo['AST_RANK'])})")
    print(f"Robos: {equipo['STL']:.1f} (Ranking: {int(equipo['STL_RANK'])})")
    print(f"Bloqueos: {equipo['BLK']:.1f} (Ranking: {int(equipo['BLK_RANK'])})")
    print(f"Pérdidas: {equipo['TOV']:.1f} (Ranking: {int(equipo['TOV_RANK'])})")
    
    # Gráfica de Radar para visualizar las fortalezas y debilidades del equipo
    crear_grafica_radar(equipo)

def crear_grafica_radar(equipo):
    """Crea una gráfica de radar para visualizar las fortalezas y debilidades del equipo"""
    # Crear carpeta si no existe
    if not os.path.exists("visualizaciones"):
        os.makedirs("visualizaciones")
    
    # Categorías para el radar chart
    categories = ['Puntos', 'Eficiencia\nOfensiva', 'Eficiencia\nDefensiva', 
                 'Rebotes', 'Asistencias', 'Robos', 'Bloqueos']
    
    # Convertir rankings a valores (30-ranking+1 para que valores más altos sean mejores)
    values = [
        31 - equipo['PTS_RANK'],
        31 - equipo['E_OFF_RATING_RANK'],
        31 - equipo['E_DEF_RATING_RANK'],
        31 - equipo['REB_RANK'],
        31 - equipo['AST_RANK'],
        31 - equipo['STL_RANK'],
        31 - equipo['BLK_RANK']
    ]
    
    # Crear figura
    plt.figure(figsize=(10, 10))
    
    # Calcular ángulos para cada categoría (en radianes)
    angles = np.linspace(0, 2*np.pi, len(categories), endpoint=False).tolist()
    
    # Cerrar el polígono repitiendo el primer valor y ángulo
    values.append(values[0])
    angles.append(angles[0])
    
    # Configurar el radar
    ax = plt.subplot(111, polar=True)
    ax.set_theta_offset(np.pi / 2)  # Rotar para que el primer eje esté arriba
    ax.set_theta_direction(-1)  # Sentido horario
    
    # Dibujar líneas desde el centro a cada punto
    plt.plot(angles, values, 'o-', linewidth=2)
    plt.fill(angles, values, alpha=0.25)
    
    # Configurar etiquetas y límites
    ax.set_xticks(angles[:-1])  # Excluir el último ángulo duplicado
    ax.set_xticklabels(categories)
    
    # Configurar escala de valores
    ax.set_yticks([5, 10, 15, 20, 25, 30])
    ax.set_yticklabels(['5', '10', '15', '20', '25', '30'])
    ax.set_ylim(0, 30)
    
    # Añadir título
    plt.title(f"Perfil de {equipo['TEAM_NAME_x']} - Temporada 2024-25", size=16, y=1.05)
    
    # Guardar la figura
    plt.tight_layout()
    plt.savefig(f"visualizaciones/{equipo['TEAM_NAME_x'].replace(' ', '_')}_radar.png", dpi=300)
    print(f"\nGráfica de radar creada en visualizaciones/{equipo['TEAM_NAME_x'].replace(' ', '_')}_radar.png")
    plt.close()

def comparar_equipos():
    """Permite comparar dos equipos seleccionados"""
    print("\n===== COMPARACIÓN DE EQUIPOS =====")
    
    # Seleccionar primer equipo
    print("\nSeleccione el primer equipo:")
    mostrar_equipos()
    nombre1 = input("Nombre del primer equipo (o parte del nombre): ")
    equipo1 = buscar_equipo(nombre1)
    if equipo1 is None:
        return
    
    # Seleccionar segundo equipo
    print("\nSeleccione el segundo equipo:")
    nombre2 = input("Nombre del segundo equipo (o parte del nombre): ")
    equipo2 = buscar_equipo(nombre2)
    if equipo2 is None:
        return
    
    # Crear tabla comparativa
    print(f"\n===== {equipo1['TEAM_NAME_x']} vs {equipo2['TEAM_NAME_x']} =====")
    
    metricas = [
        ("Record", f"{int(equipo1['W_x'])}-{int(equipo1['L_x'])}", f"{int(equipo2['W_x'])}-{int(equipo2['L_x'])}"),
        ("W%", f"{equipo1['W_PCT_x']:.3f}", f"{equipo2['W_PCT_x']:.3f}"),
        ("Puntos/Partido", f"{equipo1['PTS']:.1f}", f"{equipo2['PTS']:.1f}"),
        ("FG%", f"{equipo1['FG_PCT']:.3f}", f"{equipo2['FG_PCT']:.3f}"),
        ("3P%", f"{equipo1['FG3_PCT']:.3f}", f"{equipo2['FG3_PCT']:.3f}"),
        ("Rating Ofensivo", f"{equipo1['E_OFF_RATING']:.1f}", f"{equipo2['E_OFF_RATING']:.1f}"),
        ("Rating Defensivo", f"{equipo1['E_DEF_RATING']:.1f}", f"{equipo2['E_DEF_RATING']:.1f}"),
        ("Rebotes", f"{equipo1['REB']:.1f}", f"{equipo2['REB']:.1f}"),
        ("Asistencias", f"{equipo1['AST']:.1f}", f"{equipo2['AST']:.1f}"),
        ("Robos", f"{equipo1['STL']:.1f}", f"{equipo2['STL']:.1f}"),
        ("Bloqueos", f"{equipo1['BLK']:.1f}", f"{equipo2['BLK']:.1f}"),
        ("Pérdidas", f"{equipo1['TOV']:.1f}", f"{equipo2['TOV']:.1f}"),
        ("Ritmo (PACE)", f"{equipo1['E_PACE']:.1f}", f"{equipo2['E_PACE']:.1f}")
    ]
    
    print(f"{'Métrica':<20} {equipo1['TEAM_NAME_x']:<15} {equipo2['TEAM_NAME_x']:<15}")
    print("="*60)
    for metrica, valor1, valor2 in metricas:
        print(f"{metrica:<20} {valor1:<15} {valor2:<15}")
    
    # Crear gráfica comparativa de barras
    crear_grafica_comparativa(equipo1, equipo2)

def crear_grafica_comparativa(equipo1, equipo2):
    """Crea una gráfica comparativa entre dos equipos"""
    # Crear carpeta si no existe
    if not os.path.exists("visualizaciones"):
        os.makedirs("visualizaciones")
    
    # Métricas a comparar
    metricas = ['PTS', 'REB', 'AST', 'STL', 'BLK', 'FG_PCT', 'FG3_PCT']
    nombres = ['Puntos', 'Rebotes', 'Asistencias', 'Robos', 'Bloqueos', 'FG%', '3P%']
    
    # Crear figura
    plt.figure(figsize=(12, 8))
    
    # Configurar barras
    x = range(len(metricas))
    width = 0.35
    
    # Valores para cada equipo
    # Para porcentajes multiplicamos por 100 para mejor visualización
    vals1 = [equipo1[m] if 'PCT' not in m else equipo1[m]*100 for m in metricas]
    vals2 = [equipo2[m] if 'PCT' not in m else equipo2[m]*100 for m in metricas]
    
    # Dibujar barras
    plt.bar([i - width/2 for i in x], vals1, width, label=equipo1['TEAM_NAME_x'], color='skyblue')
    plt.bar([i + width/2 for i in x], vals2, width, label=equipo2['TEAM_NAME_x'], color='orange')
    
    # Etiquetas y título
    plt.xticks(x, nombres)
    plt.title(f"Comparación: {equipo1['TEAM_NAME_x']} vs {equipo2['TEAM_NAME_x']}", fontsize=16)
    plt.legend()
    
    # Añadir valores sobre las barras
    for i, v in enumerate(vals1):
        valor = f"{v:.1f}" if 'PCT' not in metricas[i] else f"{v:.1f}%"
        plt.text(i - width/2, v + 1, valor, ha='center')
    
    for i, v in enumerate(vals2):
        valor = f"{v:.1f}" if 'PCT' not in metricas[i] else f"{v:.1f}%"
        plt.text(i + width/2, v + 1, valor, ha='center')
    
    # Guardar gráfica
    team1 = equipo1['TEAM_NAME_x'].replace(' ', '_')
    team2 = equipo2['TEAM_NAME_x'].replace(' ', '_')
    plt.tight_layout()
    plt.savefig(f"visualizaciones/comparacion_{team1}_vs_{team2}.png", dpi=300)
    print(f"\nGráfica comparativa creada en visualizaciones/comparacion_{team1}_vs_{team2}.png")
    plt.close()

def menu_principal():
    """Muestra el menú principal y maneja la selección del usuario"""
    while True:
        print("\n===== ANALIZADOR DE ESTADÍSTICAS NBA - TEMPORADA 2024-25 =====")
        print("1. Ver lista de equipos")
        print("2. Buscar estadísticas de un equipo")
        print("3. Comparar dos equipos")
        print("4. Salir")
        
        opcion = input("\nSeleccione una opción (1-4): ")
        
        if opcion == '1':
            mostrar_equipos()
        elif opcion == '2':
            mostrar_equipos()
            nombre = input("Nombre del equipo (o parte del nombre): ")
            equipo = buscar_equipo(nombre)
            if equipo is not None:
                mostrar_estadisticas(equipo)
        elif opcion == '3':
            comparar_equipos()
        elif opcion == '4':
            print("Gracias por utilizar el Analizador de Estadísticas NBA.")
            break
        else:
            print("Opción no válida. Por favor, seleccione una opción entre 1 y 4.")

if __name__ == "__main__":
    menu_principal() 