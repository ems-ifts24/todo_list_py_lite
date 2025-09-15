import os
import json
from datetime import datetime
from typing import Dict, List, Any
import generar_aleatorios
import graficos
from utils import limpiar_pantalla, pausa as pausar, Colors

def mostrar_menu_simulacion() -> None:
    """
    Muestra el menú de simulación con las opciones disponibles.
    """
    limpiar_pantalla()
    print(f"\n{Colors.BLUE}{'='*50}{Colors.RESET}")
    print(f"{Colors.BOLD}{' '*15}📊 SIMULACIÓN DE DATOS {' '*15}{Colors.RESET}")
    print(f"{Colors.BLUE}{'='*50}{Colors.RESET}\n")
    print(f"{Colors.CYAN}1. 🆕 Generar N registros simulados (default = 100)")
    print(f"2. 📊 Generar gráfico: Tareas por Prioridad")
    print(f"3. 📈 Generar gráfico: Tareas por Estado")
    print(f"4. 📅 Generar gráfico: Distribución Temporal de Tareas")
    print(f"5. 🔥 Generar gráfico: Relación Prioridad vs Estado (heatmap)")
    print(f"6. 🍕 Generar gráfico: Proporción de Tareas por Prioridad (pie chart)")
    print(f"7. 🍰 Generar gráfico: Proporción de Tareas por Estado (pie chart)")
    print(f"8. 📉 Generar gráfico: Tendencia de Estados en el Tiempo (stackplot)")
    print(f"9. 🖼️  Mostrar 4 gráficos juntos")
    print(f"{Colors.YELLOW}10. ↩️  Volver al menú principal{Colors.RESET}\n")

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
            print(f"{Colors.YELLOW}⚠️ No se encontraron archivos de simulación. Genere datos primero.{Colors.RESET}")
            return []
        archivo = max(archivos, key=os.path.getmtime)
    
    try:
        with open(archivo, 'r', encoding='utf-8') as f:
            return json.load(f)
    except FileNotFoundError:
        print(f"{Colors.RED}❌ No se pudo encontrar el archivo: {archivo}{Colors.RESET}")
        return []
    except json.JSONDecodeError:
        print(f"{Colors.RED}❌ Error al leer el archivo JSON: {archivo}{Colors.RESET}")
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
                print(f"{Colors.RED}❌ Opción inválida. Intente de nuevo.{Colors.RESET}")
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
                    print(f"{Colors.RED}❌ No se pudieron generar los datos simulados.{Colors.RESET}")
                
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
