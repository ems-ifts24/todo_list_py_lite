"""
Módulo de servicio para la aplicación TODO List.
Contiene la lógica de negocio y manejo de datos.
"""
import json
import os
from datetime import datetime
from utils import Colors, EMOJIS, obtener_fecha_actual

class TodoService:
    """Clase que maneja la lógica de negocio de la aplicación TODO List."""
    
    def __init__(self, archivo_datos='todo_list.json'):
        """
        Inicializa el servicio con la ruta al archivo de datos.
        Si el archivo no existe, crea uno con una lista vacía.
        """
        self.archivo_datos = archivo_datos
        self.tareas = self._cargar_tareas()
        self.proximo_id = self._calcular_proximo_id()
    
    def _cargar_tareas(self):
        """Carga las tareas desde el archivo JSON."""
        try:
            if not os.path.exists(self.archivo_datos):
                with open(self.archivo_datos, 'w', encoding='utf-8') as f:
                    json.dump([], f, indent=2)
                return []
            
            with open(self.archivo_datos, 'r', encoding='utf-8') as f:
                return json.load(f)
        except (json.JSONDecodeError, FileNotFoundError):
            # Si hay un error al leer el archivo, se crea uno nuevo
            with open(self.archivo_datos, 'w', encoding='utf-8') as f:
                json.dump([], f, indent=2)
            return []
    
    def _guardar_tareas(self):
        """Guarda las tareas en el archivo JSON."""
        with open(self.archivo_datos, 'w', encoding='utf-8') as f:
            json.dump(self.tareas, f, indent=2, ensure_ascii=False)
    
    def _calcular_proximo_id(self):
        """Calcula el próximo ID disponible."""
        if not self.tareas:
            return 1
        return max(tarea['id'] for tarea in self.tareas) + 1
    
    def _validar_nombre_unico(self, nombre, tarea_id=None):
        """
        Valida que no exista otra tarea con el mismo nombre (excepto si está finalizada).
        Si se proporciona tarea_id, la ignora en la validación (para edición).
        """
        for tarea in self.tareas:
            if tarea['nombre'].lower() == nombre.lower() and tarea['estado'] != 'FINALIZADA':
                if tarea_id is None or tarea['id'] != tarea_id:
                    return False
        return True
    
    def agregar_tarea(self, nombre, prioridad):
        """Agrega una nueva tarea a la lista."""
        if not nombre or not nombre.strip():
            return False, "El nombre de la tarea no puede estar vacío."
        
        if not self._validar_nombre_unico(nombre):
            return False, f"Ya existe una tarea pendiente o en curso con el nombre: {nombre}"
        
        nueva_tarea = {
            'id': self.proximo_id,
            'nombre': nombre.strip(),
            'prioridad': prioridad,
            'estado': 'PENDIENTE',
            'fecha': obtener_fecha_actual()
        }
        
        self.tareas.append(nueva_tarea)
        self.proximo_id += 1
        self._guardar_tareas()
        
        return True, f"{EMOJIS['add']} Tarea agregada correctamente con ID: {nueva_tarea['id']}"
    
    def listar_tareas(self, filtro_prioridad=None):
        """
        Devuelve la lista de tareas, opcionalmente filtrada por prioridad.
        Si se proporciona filtro_prioridad, solo devuelve las tareas con esa prioridad.
        """
        if filtro_prioridad:
            return [t for t in self.tareas if t['prioridad'] == filtro_prioridad]
        return self.tareas
    
    def buscar_tareas(self, texto_busqueda, prioridad=None):
        """
        Busca tareas que contengan el texto de búsqueda en el nombre.
        Opcionalmente filtra por prioridad.
        """
        texto_busqueda = texto_busqueda.lower()
        resultados = []
        
        for tarea in self.tareas:
            if (texto_busqueda in tarea['nombre'].lower() and 
                (prioridad is None or tarea['prioridad'] == prioridad)):
                resultados.append(tarea)
        
        return resultados
    
    def obtener_tarea_por_id(self, tarea_id):
        """Obtiene una tarea por su ID o None si no existe."""
        for tarea in self.tareas:
            if tarea['id'] == tarea_id:
                return tarea
        return None
    
    def editar_tarea(self, tarea_id, nuevo_nombre=None, nueva_prioridad=None, nuevo_estado=None):
        """Edita una tarea existente."""
        tarea = self.obtener_tarea_por_id(tarea_id)
        if not tarea:
            return False, f"No se encontró ninguna tarea con ID: {tarea_id}"
        
        if tarea['estado'] == 'FINALIZADA':
            return False, "No se puede editar una tarea FINALIZADA. Crea una nueva tarea en su lugar."
        
        cambios = []
        
        if nuevo_nombre and nuevo_nombre.strip() and nuevo_nombre.strip() != tarea['nombre']:
            if not self._validar_nombre_unico(nuevo_nombre, tarea_id):
                return False, f"Ya existe otra tarea con el nombre: {nuevo_nombre}"
            tarea['nombre'] = nuevo_nombre.strip()
            cambios.append("nombre")
        
        if nueva_prioridad and nueva_prioridad != tarea['prioridad']:
            tarea['prioridad'] = nueva_prioridad
            cambios.append("prioridad")
        
        if nuevo_estado and nuevo_estado != tarea['estado']:
            tarea['estado'] = nuevo_estado
            cambios.append("estado")
        
        if cambios:
            tarea['fecha'] = obtener_fecha_actual()
            self._guardar_tareas()
            return True, f"{EMOJIS['edit']} Tarea actualizada correctamente. Campos modificados: {', '.join(cambios)}"
        
        return False, "No se realizaron cambios en la tarea."
    
    def eliminar_tarea(self, tarea_id):
        """Elimina una tarea por su ID."""
        for i, tarea in enumerate(self.tareas):
            if tarea['id'] == tarea_id:
                tarea_eliminada = self.tareas.pop(i)
                self._guardar_tareas()
                return True, f"{EMOJIS['delete']} Tarea eliminada: {tarea_eliminada['nombre']}"
        
        return False, f"No se encontró ninguna tarea con ID: {tarea_id}"
