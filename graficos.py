import matplotlib.pyplot as plt
import seaborn as sns
import pandas as pd
from typing import List, Dict, Any

# Configuración de estilo para los gráficos
sns.set_theme(style="whitegrid")
plt.rcParams['figure.figsize'] = (12, 6)
plt.rcParams['font.size'] = 10

# Paleta de colores consistente
COLORES_PRIORIDAD = {
    'baja': '#4CAF50',     # Verde
    'media': '#FFC107',    # Amarillo
    'alta': '#FF9800',     # Naranja
    'crítica': '#F44336'   # Rojo
}

COLORES_ESTADO = {
    'pendiente': '#9E9E9E',    # Gris
    'en progreso': '#2196F3',  # Azul
    'completada': '#4CAF50',   # Verde
    'en revisión': '#9C27B0',  # Púrpura
    'bloqueada': '#F44336'     # Rojo
}

def configurar_grafico(titulo: str, xlabel: str = '', ylabel: str = '') -> None:
    """
    Configura los aspectos básicos de un gráfico.
    
    Args:
        titulo: Título del gráfico
        xlabel: Etiqueta del eje X
        ylabel: Etiqueta del eje Y
    """
    plt.title(titulo, fontsize=14, fontweight='bold', pad=20)
    plt.xlabel(xlabel, fontsize=10)
    plt.ylabel(ylabel, fontsize=10)
    plt.tight_layout()

def grafico_tareas_por_prioridad(tareas: List[Dict[str, Any]]) -> None:
    """
    Genera un gráfico de barras mostrando la cantidad de tareas por prioridad.
    
    Args:
        tareas: Lista de tareas
    """
    # Crear DataFrame
    df = pd.DataFrame(tareas)
    
    # Contar tareas por prioridad
    conteo = df['prioridad'].value_counts().sort_index()
    
    # Ordenar por prioridad (personalizado)
    orden_prioridad = ['baja', 'media', 'alta', 'crítica']
    conteo = conteo.reindex(orden_prioridad, fill_value=0)
    
    # Crear gráfico
    plt.figure(figsize=(10, 6))
    barras = sns.barplot(x=conteo.index, y=conteo.values, 
                        palette=COLORES_PRIORIDAD.values())
    
    # Agregar etiquetas
    for i, valor in enumerate(conteo.values):
        plt.text(i, valor + 0.5, str(valor), ha='center', va='bottom')
    
    # Configurar gráfico
    configurar_grafico("Tareas por Prioridad", "Prioridad", "Cantidad de Tareas")
    plt.xticks(rotation=45)
    plt.show()

def grafico_tareas_por_estado(tareas: List[Dict[str, Any]]) -> None:
    """
    Genera un gráfico de barras horizontales mostrando la cantidad de tareas por estado.
    
    Args:
        tareas: Lista de tareas
    """
    # Crear DataFrame
    df = pd.DataFrame(tareas)
    
    # Contar tareas por estado
    conteo = df['estado'].value_counts()
    
    # Crear gráfico
    plt.figure(figsize=(10, 6))
    barras = sns.barplot(x=conteo.values, y=conteo.index, 
                        palette=[COLORES_ESTADO.get(estado, '#CCCCCC') for estado in conteo.index])
    
    # Agregar etiquetas
    for i, valor in enumerate(conteo.values):
        plt.text(valor + 0.5, i, str(valor), va='center')
    
    # Configurar gráfico
    configurar_grafico("Tareas por Estado", "Cantidad de Tareas", "Estado")
    plt.tight_layout()
    plt.show()

def grafico_distribucion_temporal(tareas: List[Dict[str, Any]]) -> None:
    """
    Genera un histograma mostrando la distribución de fechas de creación de tareas.
    
    Args:
        tareas: Lista de tareas
    """
    # Crear DataFrame
    df = pd.DataFrame(tareas)
    
    # Convertir fechas a datetime
    df['fecha_creacion'] = pd.to_datetime(df['fecha_creacion'])
    
    # Crear gráfico
    plt.figure(figsize=(12, 6))
    sns.histplot(data=df, x='fecha_creacion', bins=30, kde=True, 
                color='#2196F3', alpha=0.7)
    
    # Configurar formato de fechas
    plt.gcf().autofmt_xdate()
    
    # Configurar gráfico
    configurar_grafico("Distribución Temporal de Tareas", 
                      "Fecha de Creación", 
                      "Cantidad de Tareas")
    plt.show()

def grafico_heatmap_prioridad_estado(tareas: List[Dict[str, Any]]) -> None:
    """
    Genera un heatmap mostrando la relación entre prioridad y estado de las tareas.
    
    Args:
        tareas: Lista de tareas
    """
    # Crear DataFrame
    df = pd.DataFrame(tareas)
    
    # Crear tabla de contingencia
    tabla = pd.crosstab(df['prioridad'], df['estado'])
    
    # Ordenar prioridades
    orden_prioridad = ['baja', 'media', 'alta', 'crítica']
    tabla = tabla.reindex(orden_prioridad)
    
    # Crear heatmap
    plt.figure(figsize=(10, 6))
    sns.heatmap(tabla, annot=True, fmt='d', cmap='YlOrRd', 
                linewidths=0.5, cbar_kws={'label': 'Cantidad de Tareas'})
    
    # Configurar gráfico
    configurar_grafico("Relación entre Prioridad y Estado de Tareas")
    plt.tight_layout()
    plt.show()

def grafico_pie_prioridad(tareas: List[Dict[str, Any]]) -> None:
    """
    Genera un gráfico de pastel mostrando la proporción de tareas por prioridad.
    
    Args:
        tareas: Lista de tareas
    """
    # Crear DataFrame
    df = pd.DataFrame(tareas)
    
    # Contar tareas por prioridad
    conteo = df['prioridad'].value_counts()
    
    # Ordenar por prioridad
    orden_prioridad = ['baja', 'media', 'alta', 'crítica']
    conteo = conteo.reindex(orden_prioridad, fill_value=0)
    
    # Crear gráfico de pastel
    plt.figure(figsize=(8, 8))
    colores = [COLORES_PRIORIDAD.get(p, '#CCCCCC') for p in conteo.index]
    
    # Asegurar que no haya valores cero
    etiquetas = [f"{p} ({v})" if v > 0 else '' for p, v in zip(conteo.index, conteo.values)]
    
    plt.pie(conteo.values, labels=etiquetas, colors=colores,
           autopct='%1.1f%%', startangle=90, wedgeprops={'edgecolor': 'white'})
    
    # Configurar gráfico
    configurar_grafico("Proporción de Tareas por Prioridad")
    plt.axis('equal')
    plt.tight_layout()
    plt.show()

def grafico_pie_estado(tareas: List[Dict[str, Any]]) -> None:
    """
    Genera un gráfico de pastel mostrando la proporción de tareas por estado.
    
    Args:
        tareas: Lista de tareas
    """
    # Crear DataFrame
    df = pd.DataFrame(tareas)
    
    # Contar tareas por estado
    conteo = df['estado'].value_counts()
    
    # Crear gráfico de pastel
    plt.figure(figsize=(8, 8))
    colores = [COLORES_ESTADO.get(e, '#CCCCCC') for e in conteo.index]
    
    plt.pie(conteo.values, labels=conteo.index, colors=colores,
           autopct='%1.1f%%', startangle=90, wedgeprops={'edgecolor': 'white'})
    
    # Configurar gráfico
    configurar_grafico("Proporción de Tareas por Estado")
    plt.axis('equal')
    plt.tight_layout()
    plt.show()

def grafico_tendencia_estados(tareas: List[Dict[str, Any]]) -> None:
    """
    Genera un stackplot mostrando la tendencia de estados a lo largo del tiempo.
    
    Args:
        tareas: Lista de tareas
    """
    # Crear DataFrame
    df = pd.DataFrame(tareas)
    
    # Convertir fechas a datetime
    df['fecha_creacion'] = pd.to_datetime(df['fecha_creacion'])
    
    # Ordenar por fecha
    df = df.sort_values('fecha_creacion')
    
    # Crear tabla de frecuencias acumuladas por fecha y estado
    df['fecha_str'] = df['fecha_creacion'].dt.strftime('%Y-%m-%d')
    tabla = pd.crosstab(df['fecha_str'], df['estado']).cumsum()
    
    # Reordenar columnas para mejor visualización
    if 'completada' in tabla.columns:
        columnas_orden = ['pendiente', 'en progreso', 'en revisión', 'bloqueada', 'completada']
    else:
        columnas_orden = sorted(tabla.columns)
    
    # Filtrar solo las columnas existentes
    columnas_orden = [c for c in columnas_orden if c in tabla.columns]
    tabla = tabla[columnas_orden]
    
    # Obtener colores para los estados
    colores = [COLORES_ESTADO.get(estado, '#CCCCCC') for estado in tabla.columns]
    
    # Crear stackplot
    plt.figure(figsize=(12, 6))
    plt.stackplot(tabla.index, [tabla[col] for col in tabla.columns],
                 labels=tabla.columns, colors=colores, alpha=0.8)
    
    # Configurar ejes y leyenda
    plt.xticks(rotation=45, ha='right')
    plt.legend(loc='upper left')
    
    # Configurar gráfico
    configurar_grafico("Tendencia de Estados a lo Largo del Tiempo",
                      "Fecha",
                      "Cantidad de Tareas")
    plt.tight_layout()
    plt.show()

def mostrar_cuatro_graficos(tareas: List[Dict[str, Any]]) -> None:
    """
    Muestra 4 gráficos juntos en una sola figura.
    
    Args:
        tareas: Lista de tareas
    """
    # Crear figura con 2x2 subplots
    fig, axs = plt.subplots(2, 2, figsize=(16, 12))
    
    # 1. Gráfico de barras por prioridad
    df = pd.DataFrame(tareas)
    conteo_prioridad = df['prioridad'].value_counts()
    orden_prioridad = ['baja', 'media', 'alta', 'crítica']
    conteo_prioridad = conteo_prioridad.reindex(orden_prioridad, fill_value=0)
    
    axs[0, 0].bar(conteo_prioridad.index, conteo_prioridad.values, 
                 color=[COLORES_PRIORIDAD.get(p, '#CCCCCC') for p in conteo_prioridad.index])
    axs[0, 0].set_title('Tareas por Prioridad', fontweight='bold')
    axs[0, 0].set_xlabel('Prioridad')
    axs[0, 0].set_ylabel('Cantidad de Tareas')
    
    # 2. Gráfico de pastel por estado
    conteo_estado = df['estado'].value_counts()
    colores_estado = [COLORES_ESTADO.get(e, '#CCCCCC') for e in conteo_estado.index]
    
    axs[0, 1].pie(conteo_estado, labels=conteo_estado.index, 
                 autopct='%1.1f%%', startangle=90, colors=colores_estado,
                 wedgeprops={'edgecolor': 'white'})
    axs[0, 1].set_title('Proporción por Estado', fontweight='bold')
    axs[0, 1].axis('equal')
    
    # 3. Heatmap de prioridad vs estado
    tabla = pd.crosstab(df['prioridad'], df['estado'])
    tabla = tabla.reindex(orden_prioridad)
    
    sns.heatmap(tabla, annot=True, fmt='d', cmap='YlOrRd', 
                linewidths=0.5, cbar_kws={'label': 'Cantidad'},
                ax=axs[1, 0])
    axs[1, 0].set_title('Relación Prioridad vs Estado', fontweight='bold')
    
    # 4. Gráfico de tendencia de estados
    df['fecha_creacion'] = pd.to_datetime(df['fecha_creacion'])
    df = df.sort_values('fecha_creacion')
    df['fecha_str'] = df['fecha_creacion'].dt.strftime('%Y-%m-%d')
    
    # Tomar solo las últimas 10 fechas para mejor visualización
    ultimas_fechas = df['fecha_str'].drop_duplicates().sort_values().tail(10)
    df_filtrado = df[df['fecha_str'].isin(ultimas_fechas)]
    
    if not df_filtrado.empty:
        tabla_tendencia = pd.crosstab(df_filtrado['fecha_str'], df_filtrado['estado']).cumsum()
        
        # Ordenar columnas para mejor visualización
        if 'completada' in tabla_tendencia.columns:
            columnas_orden = ['pendiente', 'en progreso', 'en revisión', 'bloqueada', 'completada']
            columnas_orden = [c for c in columnas_orden if c in tabla_tendencia.columns]
            tabla_tendencia = tabla_tendencia[columnas_orden]
        
        colores_tendencia = [COLORES_ESTADO.get(e, '#CCCCCC') for e in tabla_tendencia.columns]
        
        axs[1, 1].stackplot(tabla_tendencia.index, 
                           [tabla_tendencia[col] for col in tabla_tendencia.columns],
                           labels=tabla_tendencia.columns,
                           colors=colores_tendencia,
                           alpha=0.8)
        
        axs[1, 1].set_title('Tendencia de Estados (Últimas 10 fechas)', fontweight='bold')
        axs[1, 1].set_xlabel('Fecha')
        axs[1, 1].set_ylabel('Cantidad de Tareas')
        axs[1, 1].legend(loc='upper left')
        axs[1, 1].tick_params(axis='x', rotation=45)
    
    # Ajustar espaciado
    plt.tight_layout()
    plt.suptitle('Resumen de Tareas', fontsize=16, fontweight='bold', y=1.02)
    plt.show()

# Función auxiliar para guardar los gráficos
guardar_grafico = lambda nombre: plt.savefig(f"grafico_{nombre.lower().replace(' ', '_')}.png", 
                                           bbox_inches='tight', dpi=300)

if __name__ == "__main__":
    # Ejemplo de uso
    print("🔹 Módulo de visualización de datos")
    print("=" * 50)
    print("\nEste módulo contiene funciones para generar gráficos a partir de datos de tareas.")
    print("Para usarlo, importa las funciones necesarias en tu script principal.")
    print("\nEjemplo:")
    print("from graficos import grafico_tareas_por_prioridad")
    print("grafico_tareas_por_prioridad(lista_de_tareas)")
