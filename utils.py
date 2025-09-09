"""
Módulo de utilidades para la aplicación TODO List.
Contiene funciones de ayuda para validaciones, colores y formato.
"""
from datetime import datetime
import os

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

# Emojis reemplazados por caracteres ASCII compatibles
EMOJIS = {
    'check': '[OK]',      # ✅ → [OK]
    'edit': '[EDIT]',     # ✏️ → [EDIT]
    'delete': '[X]',      # 🗑️ → [X]
    'add': '[+]',         # ➕ → [+]
    'search': '[?]',      # 🔍 → [?]
    'warning': '[!]',     # ⚠️ → [!]
    'error': '[ERR]',     # ❌ → [ERR]
    'info': '[i]',        # ℹ️ → [i]
    'clock': '[H]',       # ⏰ → [H]
    'list': '[*]',        # Para listas
    'arrow': '[->]',      # Flecha
    'star': '[*]'         # Para destacar
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
        opcion = int(opcion)    # Valida que sea entero. Si no lo puede parsear, lanza ValueError.
        if min_val <= opcion <= max_val:
            return True, opcion
        return False, None  # Retorna una tupla (bool, int)
    except ValueError:
        return False, None  # Retorna una tupla (bool, None)

# Función que recibe un array de tareas y las formatea en una tabla
def formatear_tabla(tareas):
    """Formatea la lista de tareas en una tabla."""
    if not tareas:
        return "No hay tareas para mostrar."
    
    # Encabezados de la tabla
    # Ancho de columna con :4, :30, :8, :12 y < para alinear los textos a la izquierda
    # "-" * 85 crea una línea horizontal de 85 caracteres
    tabla = [
        f"{Colors.BOLD}{'ID':<4} | {'TAREA':<40} | {'PRIORIDAD':<10} | {'ESTADO':<15} | {'ÚLTIMA MODIFICACIÓN':<20}{Colors.RESET}",
        "-" * 102
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
        
        # Cuando se usan códigos de colores ANSI (como Colors.RED), estos ocupan espacio en la consola pero no se muestran
        # ni cuentan para el ancho de formato. Por ejemplo, \033[91mALTA\033[0m tiene más caracteres que "ALTA",
        # pero en la consola solo muestra "ALTA". Por eso se usa 19 en lugar de 10 para la prioridad.
        fila = f"{tarea['id']:<4} | {tarea['nombre']:<40} | {prioridad:<19} | {estado:<15} | {tarea['fecha']:<20}"
        tabla.append(fila)
    
    return '\n'.join(tabla)

def pausa():
    """Muestra un mensaje y espera a que el usuario presione Enter."""
    input(f"\n{Colors.BLUE}Presiona Enter para continuar...{Colors.RESET}")
