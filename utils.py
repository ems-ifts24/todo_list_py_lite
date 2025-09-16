"""
Módulo de utilidades para la aplicación TODO List.
Contiene funciones de ayuda para validaciones, colores y formato.
"""
from datetime import datetime
import os   # Módulo os usado para limpiar pantalla.
import re   # Módulo regex usado para calcular el ancho de la tabla.

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
    'check': '✅',
    'edit': '✏️',
    'delete': '🗑️',
    'add': '📝',
    'search': '🔍',
    'warning': '⚠️',
    'error': '❌',
    'info': 'ℹ️',
    'clock': '⏰',
    'list': '📋',
    'simulacion': '📊',
    'salir': '🚪'
}

def limpiar_pantalla():
    """Limpia la pantalla de la consola."""
    os.system('cls' if os.name == 'nt' else 'clear')

def obtener_fecha_actual():
    """Devuelve la fecha y hora actual formateada en formato DD/MM/YYYY HH:MM:SS."""
    return datetime.now().strftime("%d/%m/%Y %H:%M:%S")

def validar_opcion(opcion, min_val, max_val):
    """Valida que la opción ingresada sea un número dentro del rango."""
    try:
        opcion = int(opcion)    # Valida que sea entero. Si no lo puede parsear, lanza ValueError.
        if min_val <= opcion <= max_val:
            return True, opcion
        return False, None  # Retorna una tupla (bool, int)
    except ValueError:
        return False, None  # Retorna una tupla (bool, None)

def get_display_width(text):
    """
    Calcula el ancho visual real del texto, excluyendo códigos ANSI y ajustando emojis
    """
    # Remover códigos de color ANSI
    # compile compila la expresión regular
    ansi_escape = re.compile(r'\x1B(?:[@-Z\\-_]|\[[0-?]*[ -/]*[@-~])')
    clean_text = ansi_escape.sub('', text)
    
    # Contar caracteres, considerando que los emojis ocupan 2 espacios visuales
    # ord() devuelve el valor Unicode de un carácter
    width = 0
    for char in clean_text:
        # Los emojis y algunos caracteres especiales ocupan 2 espacios
        if ord(char) > 0x1F600:  # Rango básico de emojis
            width += 2
        else:
            width += 1
    
    return width

def pad_text(text, width, align='left'):
    """
    Rellena el texto para alcanzar el ancho deseado, considerando caracteres especiales
    """
    display_width = get_display_width(text)
    padding_needed = width - display_width
    
    if padding_needed <= 0:
        return text
    
    if align == 'center':
        left_pad = padding_needed // 2
        right_pad = padding_needed - left_pad
        return ' ' * left_pad + text + ' ' * right_pad
    elif align == 'right':
        return ' ' * padding_needed + text
    else:  # left
        return text + ' ' * padding_needed

def formatear_tabla(tareas):
    """Formatea la lista de tareas en una tabla con anchos dinámicos."""
    if not tareas:
        return "No hay tareas para mostrar."
    
    # Encabezados
    headers = ['ID', 'TAREA', 'PRIORIDAD', 'ESTADO', 'ÚLTIMA MODIFICACIÓN']
    
    # Inicializar anchos mínimos con los encabezados
    max_widths = {header: get_display_width(header) for header in headers}
    
    # Forzar ancho fijo de 40 caracteres para TAREA
    max_widths['TAREA'] = 40
    
    # Forzar anchos fijos para PRIORIDAD y ESTADO (ancho actual + 1)
    max_widths['PRIORIDAD'] = max(get_display_width('PRIORIDAD'), max_widths.get('PRIORIDAD', 0)) + 1
    max_widths['ESTADO'] = max(get_display_width('ESTADO'), max_widths.get('ESTADO', 0)) + 1
    
    # Preparar datos de filas y calcular anchos máximos
    processed_rows = []
    
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
        elif tarea['estado'] == 'PENDIENTE':
            estado = f"⏳ {tarea['estado']}"
        elif tarea['estado'] == 'EN CURSO':
            estado = f"🔄 {tarea['estado']}"
        else:
            estado = tarea['estado']
        
        # Crear fila con datos procesados
        row_data = [
            str(tarea['id']),
            tarea['nombre'][:40],  # Limitar a 40 caracteres
            prioridad,
            estado,
            tarea['fecha']
        ]
        
        processed_rows.append(row_data)
        
        # Actualizar anchos máximos (excepto para columnas con ancho fijo)
        for i, (header, data) in enumerate(zip(headers, row_data)):
            if header not in ['TAREA', 'PRIORIDAD', 'ESTADO']:  # Saltar columnas con ancho fijo
                width = get_display_width(data)
                if width > max_widths[header]:
                    max_widths[header] = width
    
    # Agregar padding mínimo de 1 espacio a cada lado
    for header in max_widths:
        max_widths[header] += 2
    
    # Crear tabla
    tabla = []
    
    # Encabezado formateado
    header_row = " | ".join(
        pad_text(f"{Colors.BOLD}{header}{Colors.RESET}", max_widths[header], 'left')
        for header in headers
    )
    tabla.append(header_row)
    
    # Línea separadora
    total_width = sum(max_widths.values()) + len(headers) * 3 - 3  # 3 por " | " entre columnas
    tabla.append("-" * total_width)
    
    # Filas de datos
    for row_data in processed_rows:
        fila_formateada = " | ".join(
            pad_text(data, max_widths[header], 'left')
            for header, data in zip(headers, row_data)
        )
        tabla.append(fila_formateada)
    
    return '\n'.join(tabla)


def pausa():
    """Muestra un mensaje y espera a que el usuario presione Enter."""
    input(f"\n{Colors.BLUE}Presiona Enter para continuar...{Colors.RESET}")
