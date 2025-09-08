"""
Módulo de utilidades para la aplicación TODO List.
Contiene funciones de ayuda para validaciones, colores y formato.
"""
from datetime import datetime
import os
import sys

# Constantes para colores y estilos
class Colors:
    RESET = '\033[0m'
    BOLD = '\033[1m'
    UNDERLINE = '\033[4m'
    RED = '\033[91m'
    GREEN = '\033[92m'
    YELLOW = '\033[93m'
    BLUE = '\033[94m'
    PURPLE = '\033[95m'
    CYAN = '\033[96m'

# Emojis
EMOJIS = {
    'check': '✅',
    'edit': '✏️',
    'delete': '🗑️',
    'add': '➕',
    'search': '🔍',
    'warning': '⚠️',
    'error': '❌',
    'info': 'ℹ️',
    'clock': '⏰'
}

def limpiar_pantalla():
    """Limpia la pantalla de la consola."""
    os.system('cls' if os.name == 'nt' else 'clear')

def obtener_fecha_actual():
    """Devuelve la fecha y hora actual formateada."""
    return datetime.now().strftime("%Y-%m-%d %H:%M:%S")

def validar_opcion(opcion, min_val, max_val):
    """Valida que la opción ingresada sea un número dentro del rango."""
    try:
        opcion = int(opcion)
        if min_val <= opcion <= max_val:
            return True, opcion
        return False, None
    except ValueError:
        return False, None

def formatear_tabla(tareas):
    """Formatea la lista de tareas en una tabla."""
    if not tareas:
        return "No hay tareas para mostrar."
    
    # Encabezados de la tabla
    tabla = [
        f"{Colors.BOLD}{'ID':<4} | {'TAREA':<30} | {'PRIORIDAD':<8} | {'ESTADO':<12} | ÚLTIMA MODIFICACIÓN{Colors.RESET}",
        "-" * 85
    ]
    
    # Filas de la tabla
    for tarea in tareas:
        # Color según prioridad
        if tarea['prioridad'] == 'ALTA':
            prioridad = f"{Colors.RED}{tarea['prioridad']}{Colors.RESET}"
        elif tarea['prioridad'] == 'MEDIA':
            prioridad = f"{Colors.YELLOW}{tarea['prioridad']}{Colors.RESET}"
        else:
            prioridad = f"{Colors.GREEN}{tarea['prioridad']}{Colors.RESET}"
        
        # Estado con emoji
        if tarea['estado'] == 'FINALIZADA':
            estado = f"{EMOJIS['check']} {tarea['estado']}"
        else:
            estado = tarea['estado']
        
        fila = f"{tarea['id']:<4} | {tarea['nombre']:<30} | {prioridad:<8} | {estado:<12} | {tarea['fecha']}"
        tabla.append(fila)
    
    return '\n'.join(tabla)

def pausa():
    """Muestra un mensaje y espera a que el usuario presione Enter."""
    input(f"\n{Colors.BLUE}Presiona Enter para continuar...{Colors.RESET}")
