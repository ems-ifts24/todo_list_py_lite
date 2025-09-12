import os
import json
import random
from datetime import datetime, timedelta
from typing import List, Dict, Any

def generar_nombre_tarea() -> str:
    """
    Genera un nombre de tarea aleatorio combinando verbos, sustantivos y adjetivos.
    
    Returns:
        str: Nombre de tarea generado aleatoriamente
    """
    verbos = ["Completar", "Revisar", "Actualizar", "Corregir", "Mejorar", 
              "Optimizar", "Implementar", "Diseñar", "Probar", "Documentar"]
    
    adjetivos = ["importante", "urgente", "crítico", "menor", "prioritario",
                "complejo", "sencillo", "recurrente", "mensual", "semanal"]
    
    sustantivos = ["informe", "código", "interfaz", "base de datos", "API",
                  "documentación", "pruebas", "diseño", "seguridad", "rendimiento"]
    
    # Generar combinación aleatoria
    verbo = random.choice(verbos)
    adjetivo = random.choice(adjetivos)
    sustantivo = random.choice(sustantivos)
    
    return f"{verbo} {adjetivo} {sustantivo}"

def generar_fecha_aleatoria() -> str:
    """
    Genera una fecha y hora aleatoria dentro de septiembre de 2025.
    
    Returns:
        str: Fecha y hora en formato 'YYYY-MM-DD HH:MM:SS'
    """
    # Rango de fechas: 01/09/2025 - 30/09/2025
    inicio = datetime(2025, 9, 1)
    fin = datetime(2025, 9, 30)
    
    # Generar un número aleatorio de segundos dentro del rango
    delta = fin - inicio
    segundos_totales = delta.days * 24 * 60 * 60  # Convertir días a segundos
    segundos_aleatorios = random.randrange(segundos_totales)
    fecha = inicio + timedelta(seconds=segundos_aleatorios)
    
    # Redondear a minutos para tener una hora más realista
    fecha = fecha.replace(second=0)
    
    return fecha.strftime("%Y-%m-%d %H:%M:%S")

def generar_estado() -> str:
    """
    Genera un estado aleatorio para una tarea.
    
    Returns:
        str: Estado de la tarea (PENDIENTE, EN CURSO, FINALIZADA)
    """
    estados = ["PENDIENTE", "EN CURSO", "FINALIZADA"]
    return random.choice(estados)

def generar_prioridad() -> str:
    """
    Genera una prioridad aleatoria para una tarea.
    
    Returns:
        str: Prioridad de la tarea (ALTA, MEDIA, BAJA)
    """
    prioridades = ["ALTA", "MEDIA", "BAJA"]
    return random.choice(prioridades)

def generar_tarea_unica(tareas_existentes: List[Dict[str, Any]]) -> Dict[str, Any]:
    """
    Genera una tarea con nombre único.
    
    Args:
        tareas_existentes: Lista de tareas existentes para verificar duplicados
        
    Returns:
        Dict[str, Any]: Tarea generada con la estructura: 
        {
            "id": int,
            "nombre": str,
            "prioridad": str,
            "estado": str,
            "fecha": str
        }
    """
    # Obtener el próximo ID disponible
    if tareas_existentes:
        ultimo_id = max(int(tarea.get('id', 0)) for tarea in tareas_existentes)
        nuevo_id = ultimo_id + 1
    else:
        nuevo_id = 1
    
    # Obtener todos los nombres de tareas existentes
    nombres_existentes = {tarea.get('nombre', '') for tarea in tareas_existentes}
    
    # Generar un nombre único
    while True:
        nombre_base = generar_nombre_tarea()
        if nombre_base not in nombres_existentes:
            break
        
        # Si el nombre ya existe, agregar un sufijo numérico
        contador = 1
        while f"{nombre_base} ({contador})" in nombres_existentes:
            contador += 1
        nombre_base = f"{nombre_base} ({contador})"
        break
    
    # Crear la tarea con la estructura exacta requerida
    tarea = {
        "id": nuevo_id,
        "nombre": nombre_base,
        "prioridad": generar_prioridad(),
        "estado": generar_estado(),
        "fecha": generar_fecha_aleatoria()
    }
    
    return tarea

def generar_datos_simulados(n_registros: int = 100) -> str:
    """
    Genera un archivo JSON con tareas simuladas.
    
    Args:
        n_registros: Cantidad de tareas a generar
        
    Returns:
        str: Ruta del archivo generado, o cadena vacía en caso de error
    """
    try:
        # Intentar cargar tareas existentes si el archivo existe
        tareas = []
        if os.path.exists('todo_list.json'):
            try:
                with open('todo_list.json', 'r', encoding='utf-8') as f:
                    tareas = json.load(f)
                print(f"Se cargaron {len(tareas)} tareas existentes.")
            except (json.JSONDecodeError, FileNotFoundError):
                print("No se pudieron cargar tareas existentes. Se creará una lista nueva.")
        
        # Generar nuevas tareas
        print(f"\nGenerando {n_registros} tareas simuladas...")
        for _ in range(n_registros):
            tarea = generar_tarea_unica(tareas)
            tareas.append(tarea)
        
        # Generar nombre de archivo con timestamp
        timestamp = datetime.now().strftime("%Y%m%d")
        nombre_archivo = f"todo_list_simulador_{timestamp}.json"
        
        # Si el archivo ya existe, agregar un número al final
        contador = 1
        while os.path.exists(nombre_archivo):
            nombre_base = f"todo_list_simulador_{timestamp}({contador}).json"
            contador += 1
            nombre_archivo = nombre_base
        
        # Guardar el archivo
        with open(nombre_archivo, 'w', encoding='utf-8') as f:
            json.dump(tareas, f, indent=2, ensure_ascii=False)
        
        print(f"Se generaron {n_registros} tareas simuladas.")
        print(f"Archivo guardado como: {nombre_archivo}")
        
        return nombre_archivo
        
    except Exception as e:
        print(f"Error al generar datos simulados: {str(e)}")
        return ""

if __name__ == "__main__":
    # Ejemplo de uso
    print("🔹 Generador de datos simulados para la lista de tareas")
    print("=" * 50)
    
    n = input("\n🔹 Ingrese la cantidad de tareas a generar (ENTER para 100): ")
    n = int(n) if n.isdigit() else 100
    
    generar_datos_simulados(n)
