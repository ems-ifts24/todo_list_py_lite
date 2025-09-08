# 📝 TODO List App

Una aplicación de lista de tareas (TODO List) desarrollada en Python que se ejecuta en la terminal. Permite gestionar tareas con diferentes prioridades y estados, ofreciendo una interfaz intuitiva y colorida.

## 🚀 Características Principales

- **CRUD completo** de tareas (Crear, Leer, Actualizar, Eliminar)
- Gestión de prioridades (ALTA, MEDIA, BAJA)
- Seguimiento de estados (PENDIENTE, EN CURSO, FINALIZADA)
- Búsqueda y filtrado de tareas
- Interfaz de usuario intuitiva con colores y emojis
- Persistencia de datos en archivo JSON
- Validación de entradas
- Paginación de resultados

## 📁 Estructura del Proyecto

```
todo_list_py_lite/
│
├── main.py          # Punto de entrada principal de la aplicación
├── service.py       # Lógica de negocio y manejo de datos
├── utils.py         # Utilidades, colores y funciones de ayuda
├── todo_list.json   # Archivo de almacenamiento de tareas (se crea automáticamente)
└── README.md        # Este archivo
```

## 🛠️ Archivos y sus Funciones

### 1. `main.py`
Contiene la clase principal `AplicacionTodoList` que maneja la interfaz de usuario:
- Menús interactivos
- Entrada y validación de datos
- Navegación entre funciones
- Manejo de excepciones

### 2. `service.py`
Implementa la clase `TodoService` con la lógica de negocio:
- Gestión de tareas (CRUD)
- Validación de datos
- Persistencia en archivo JSON
- Búsqueda y filtrado

### 3. `utils.py`
Contiene funciones de utilidad:
- Formateo de tablas
- Manejo de colores en consola
- Validación de entradas
- Funciones de ayuda para la interfaz

## 🚀 Cómo Ejecutar

1. Asegúrate de tener Python 3.10 o superior instalado
2. Clona el repositorio o descarga los archivos
3. Navega hasta el directorio del proyecto
4. Ejecuta:
   ```bash
   python main.py
   ```

## 🎯 Ejemplos de Uso

### 1. Agregar una tarea
```
1. Agregar tarea
2. Listar tareas
3. Buscar tareas
4. Editar tarea
5. Eliminar tarea
6. Salir

Seleccione una opción (1-6): 1

📝 Agregar Nueva Tarea

Nombre de la tarea: Comprar leche

Seleccione la prioridad:
1. ALTA
2. MEDIA
3. BAJA

Opción (1-3): 2

✅ Tarea agregada correctamente con ID: 1
```

### 2. Listar tareas
```
📝 TODO List App
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
Fecha actual: 2025-09-08 19:30:00

Menú Principal:
1. Agregar tarea
2. Listar tareas
3. Buscar tareas
4. Editar tarea
5. Eliminar tarea
6. Salir

~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

Seleccione una opción (1-6): 2

📋 Lista de Tareas

ID  | TAREA                         | PRIORIDAD | ESTADO      | ÚLTIMA MODIFICACIÓN
----|-------------------------------|-----------|-------------|-----------------------
1   | Comprar leche                 | MEDIA     | PENDIENTE   | 2025-09-08 19:30:00
2   | Hacer ejercicio               | ALTA      | EN CURSO    | 2025-09-08 20:15:00
3   | Aprender Python               | ALTA      | PENDIENTE   | 2025-09-08 21:00:00
```

### 3. Buscar tareas
```
🔍 Buscar Tareas

Ingrese texto para buscar (dejar en blanco para omitir): python

Filtrar por prioridad:
1. Todas las prioridades
2. ALTA
3. MEDIA
4. BAJA

Opción (1-4): 1

Resultados para: 'python'

ID  | TAREA                         | PRIORIDAD | ESTADO      | ÚLTIMA MODIFICACIÓN
----|-------------------------------|-----------|-------------|-----------------------
3   | Aprender Python               | ALTA      | PENDIENTE   | 2025-09-08 21:00:00
```

## 📝 Notas

- Las tareas se guardan automáticamente en `todo_list.json`
- No se permiten nombres de tareas duplicados (a menos que estén FINALIZADAS)
- Las tareas FINALIZADAS no se pueden editar
- La interfaz usa colores ANSI que funcionan en la mayoría de terminales modernas

## 📄 Licencia

Este proyecto está bajo la Licencia MIT. Ver el archivo [LICENSE](LICENSE) para más detalles.

---

Desarrollado con ChatGPT y Windsurf para la materia de Ingeniería de Software - IFTS24 - 2025
