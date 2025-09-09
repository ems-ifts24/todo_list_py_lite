import os
import json
from datetime import datetime
from typing import Dict, List, Any
import generar_aleatorios
import graficos
from utils import limpiar_pantalla, pausa as pausar

def mostrar_menu_simulacion() -> None:
    """
    Muestra el menú de simulación con las opciones disponibles.
    """
    limpiar_pantalla()
    print("\n" + "="*50)
    print(" "*15 + "SIMULACIÓN" + " "*15)
    print("="*50)
    print("\n1. Generar N registros simulados (default = 100)")
    print("2. Generar gráfico: Tareas por Prioridad")
    print("3. Generar gráfico: Tareas por Estado")
    print("4. Generar gráfico: Distribución Temporal de Tareas")
    print("5. Generar gráfico: Relación Prioridad vs Estado (heatmap)")
    print("6. Generar gráfico: Proporción de Tareas por Prioridad (pie chart)")
    print("7. Generar gráfico: Proporción de Tareas por Estado (pie chart)")
    print("8. Generar gráfico: Tendencia de Estados en el Tiempo (stackplot)")
    print("9. Mostrar 4 gráficos juntos")
    print("10. Volver al menú principal\n")

def cargar_datos_simulados(archivo: str = None) -> List[Dict[str, Any]]:
    """
    Carga los datos del archivo JSON de simulaciones.
    
    Args:
        archivo (str, optional): Ruta al archivo JSON. Si es None, usa el último archivo generado.
        
    Returns:
        List[Dict[str, Any]]: Lista de tareas simuladas
    """
    if archivo is None:
        # Buscar el archivo de simulación más reciente
        archivos = [f for f in os.listdir() if f.startswith('todo_list_simulador_') and f.endswith('.json')]
        if not archivos:
            print("No se encontraron archivos de simulación. Genere datos primero.")
            return []
        archivo = max(archivos, key=os.path.getmtime)
    
    try:
        with open(archivo, 'r', encoding='utf-8') as f:
            return json.load(f)
    except FileNotFoundError:
        print(f"No se pudo encontrar el archivo: {archivo}")
        return []
    except json.JSONDecodeError:
        print(f"Error al leer el archivo JSON: {archivo}")
        return []

def ejecutar_simulacion() -> None:
    """
    Ejecuta el menú de simulación y maneja las opciones seleccionadas.
    """
    datos_simulados = []
    
    while True:
        mostrar_menu_simulacion()
        opcion = input("\n🔹 Seleccione una opción (1-10): ")
        
        try:
            opcion = int(opcion)
            if opcion < 1 or opcion > 10:
                print("Opción inválida. Intente de nuevo.")
                pausar()
                continue
                
            if opcion == 1:
                # Generar N registros simulados
                n_registros = input("\n🔹 Ingrese la cantidad de registros a generar (ENTER para 100): ")
                n_registros = int(n_registros) if n_registros.isdigit() else 100
                
                print(f"\nGenerando {n_registros} tareas simuladas...")
                archivo_generado = generar_aleatorios.generar_datos_simulados(n_registros)
                
                if archivo_generado:
                    print(f"Datos simulados guardados en: {archivo_generado}")
                    datos_simulados = cargar_datos_simulados(archivo_generado)
                else:
                    print("No se pudieron generar los datos simulados.")
                
            elif 2 <= opcion <= 9:
                # Cargar datos si no están cargados
                if not datos_simulados:
                    datos_simulados = cargar_datos_simulados()
                    if not datos_simulados:
                        pausar()
                        continue
                
                # Generar el gráfico correspondiente
                if opcion == 2:
                    graficos.grafico_tareas_por_prioridad(datos_simulados)
                elif opcion == 3:
                    graficos.grafico_tareas_por_estado(datos_simulados)
                elif opcion == 4:
                    graficos.grafico_distribucion_temporal(datos_simulados)
                elif opcion == 5:
                    graficos.grafico_heatmap_prioridad_estado(datos_simulados)
                elif opcion == 6:
                    graficos.grafico_pie_prioridad(datos_simulados)
                elif opcion == 7:
                    graficos.grafico_pie_estado(datos_simulados)
                elif opcion == 8:
                    graficos.grafico_tendencia_estados(datos_simulados)
                elif opcion == 9:
                    graficos.mostrar_cuatro_graficos(datos_simulados)
                
                print("\nGráfico generado correctamente.")
                
            elif opcion == 10:
                print("\nVolviendo al menú principal...")
                break
                
            pausar()
                
        except ValueError:
            print("Por favor ingrese un número válido.")
            pausar()
            continue
        except Exception as e:
            print(f"Ocurrió un error: {str(e)}")
            pausar()
            continue

if __name__ == "__main__":
    ejecutar_simulacion()
