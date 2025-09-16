# Prompt para Windsurf — Extender la App con Simulador y Gráficos

Quiero extender la aplicación original que administra tareas usando menús y JSON, pero esta vez desde la perspectiva de un desarrollador junior. La idea es mantener el código simple y entendible, con archivos separados para responsabilidades claras.

## Contexto del proyecto actual

- El proyecto original maneja una lista de tareas en un archivo JSON (`todo_list.json`).
- Hay un menú principal que permite listar, agregar, actualizar y eliminar tareas.
- Existen archivos separados para:
  - `main.py` → contiene la lógica del menú principal.
  - `utils.py` → validaciones y utilidades.
  - `services.py` → lógica de negocio para CRUD.

**Importante**: Todo lo que funcione actualmente no debe modificarse.

## Nueva funcionalidad: Simulación de registros y gráficos

### 1. Nuevo submenú de simulación

En el menú principal se agrega una nueva opción:  
"Simulación" → abrirá un submenú independiente.

Este submenú tendrá las siguientes opciones:

```
--- Simulación ---
1. Generar N registros simulados (default = 100)
2. Generar gráfico: Tareas por Prioridad
3. Generar gráfico: Tareas por Estado
4. Generar gráfico: Distribución Temporal de Tareas
5. Generar gráfico: Relación Prioridad vs Estado (heatmap)
6. Generar gráfico: Proporción de Tareas por Prioridad (pie chart)
7. Generar gráfico: Proporción de Tareas por Estado (pie chart)
8. Generar gráfico: Tendencia de Estados en el Tiempo (stackplot)
9. Mostrar 4 gráficos juntos (preguntar cuáles)
10. Volver al menú principal
```

### 2. Archivos nuevos

#### a) `simulador.py`

Contendrá la lógica del submenú de simulación.

Se encarga de:
- Mostrar el submenú.
- Llamar a las funciones de generación de datos simulados.
- Llamar a las funciones de generación de gráficos.
- Manejar el archivo JSON de simulaciones.

#### b) `generar_aleatorios.py`

Contendrá la lógica para crear registros simulados.

**Detalles**:
- Si el archivo `todo_list.json` (real) tiene registros, se copia como base.
- Si no hay registros, se arranca desde cero.
- Se crean N registros simulados (default 100).
- Los nombres de las tareas serán simulados y únicos:
  - Lista base de nombres + combinación aleatoria.
  - Si se repite un nombre, agregar un número incremental al final.
- La prioridad y el estado se asignan aleatoriamente.
- Las fechas serán aleatorias dentro de todo septiembre 2025.

**Guardado**:
- El archivo resultante se guardará como: `todo_list_simulador_YYYYMMDD.json`
- Si el archivo ya existe, generar: `todo_list_simulador_YYYYMMDD(1).json` y así sucesivamente.

#### c) `graficos.py`

Contendrá todas las funciones para generar gráficos.

**Librerías a usar**:
```python
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
```

Cada gráfico será una función separada.

**Requisitos de los gráficos**:
- Ser claros y legibles.
- Mostrar título y etiquetas.
- Usar colores diferenciados para estados y prioridades.

**Tipos de gráficos**:
1. Barras verticales → Tareas por Prioridad.
2. Barras horizontales → Tareas por Estado.
3. Histograma → Distribución Temporal de Tareas.
4. Heatmap → Prioridad vs Estado.
5. Pie chart → Proporción de Tareas por Prioridad.
6. Pie chart → Proporción de Tareas por Estado.
7. Stackplot → Tendencia de Estados en el Tiempo.
8. Función adicional para mostrar 4 gráficos juntos.

### 3. Validaciones y utilidades

- Si necesitamos validaciones nuevas, agregarlas en `utils.py` sin modificar las existentes.
- Si podemos reutilizar funciones como `validar_opcion(opcion, min_val, max_val)`, usarlas tal cual.

### 4. Estilo del código

Enfocado a un desarrollador junior:
- Código sencillo y fácil de leer.
- Muchas funciones pequeñas, con docstrings explicativos.
- Comentarios claros en cada paso importante.
- Nombres de funciones y variables descriptivos.
- Mantener el uso de emojis y colores en los menús y mensajes, como en la app original.

## Resumen de entregables

- `main.py` → menú principal, se agrega opción para abrir simulador.
- `simulador.py` → submenú de simulación y coordinación.
- `generar_aleatorios.py` → creación de registros simulados.
- `graficos.py` → generación de gráficos.
- `utils.py` → nuevas validaciones, solo si son necesarias.

## Objetivo del prompt

Generar un código simple, modular, documentado y extensible, pero escrito como si lo desarrollara un junior. Los archivos deben ser fáciles de mantener y las funciones cortas, claras y comentadas.