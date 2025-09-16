# Documentación - Módulo de Simulación y Gráficos

## 📌 Resumen Ejecutivo

En esta segunda etapa se amplió la aplicación de TODO List para incluir un **módulo de simulación**. La funcionalidad permite generar registros simulados sin afectar los datos reales, y además visualizar gráficos estadísticos con librerías como **pandas**, **matplotlib** y **seaborn**. Se mantuvo la impronta de un **desarrollador junior**, con código separado en archivos simples y responsabilidades claras.

---

## 📝 Historial de Conversaciones

### 🗣️ Intercambio 1: Requisitos Iniciales

**Usuario**:
> Quiero agregar una función para simular más registros. Se agregará una nueva opción "Simulación" la cual llevará a un submenú, donde podremos elegir cuantos registros se agregarán. Esto se guardará en un nuevo archivo para no afectar el json con registros reales. Ese debe permanecer sin cambios por esta operación de simulación.
> 
> El nuevo documento se llamará simulado-yyyyMMdd.json
> 
> Si el json original tuviese registros, se tomará una copia del mismo como punto de partida para agregar los registros simulados. De lo contrario, se generará el archivo simulado de cero (todos los registros simulados).
> 
> Una vez en el submenú, el usuario podrá elegir un número de registros a simular (por default serán 100).
> 
> Otras opciones serán generar 4 gráficos independientes y una última opción para mostrar los 4 juntos.
> 
> Para eso se usarán librerías como:
> - pandas 
> - matplotlib.pyplot 
> - seaborn

**Asistente**:
Se aclaró que el módulo se implementará en un archivo independiente (`simulador.py`), con:
- Submenú propio con opciones de simulación y gráficos.
- Uso de archivos JSON separados, sin afectar los datos reales.
- Posibilidad de generar múltiples gráficos, incluyendo barras, histogramas, pie charts y heatmaps.
- Validaciones independientes, sin modificar el código existente.

---

### 🗣️ Intercambio 2: Detalles de Implementación

**Usuario**:
> 1.1 Si, usamos los mismos campos de los registros reales. El nombre de las tareas me gustarían que sean simulados (que no superen los 35 o 40 caracteres). Como no pueden tener el mismo nombre, si es necesario repetir alguno podemos poner uno en finalizado o sino agregarle un número al final incremental.
> 
> 1.2 Prioridad y estado asignados de forma aleatoria. No importa el porcentaje de cada uno. Fechas aleatorias entre 9/sep/2025 al 15/sep/2025
> 
> 2. Opciones esperadas:
>    - Generar N registros simulados (default 100)
>    - Generar gráfico <nombre grafico A>
>    - Generar gráfico <nombre grafico B>
>    - Generar gráfico <nombre grafico C>
>    - Generar gráfico <nombre grafico D>
>    - Mostrar los 4 gráficos juntos
>    - Volver al menú principal
> 
> 4. Si, usemos esas librerías
> 
> 5. Así es. Esto debe guardarse en forma independiente. El archivo todo_list.json con los registros reales no debe ser afectado por esta nueva funcionalidad. Si el archivo simulado existe con la fecha de hoy, crear uno nuevo con (1) al final. Y si se siguen generando, incrementar ese número.

**Asistente**:
Se confirmaron los puntos y se sugirió la siguiente lista de gráficos:
1. **Tareas por Prioridad** (barras verticales)
2. **Tareas por Estado** (barras horizontales)
3. **Distribución Temporal de Tareas** (histograma)
4. **Relación Prioridad vs Estado** (heatmap)
5. **Proporción de Tareas por Prioridad** (pie chart)
6. **Proporción de Tareas por Estado** (pie chart)
7. **Tendencia de Estados en el Tiempo** (stackplot)

---

### 🗣️ Intercambio 3: Ajustes Finales

**Usuario**:
> Podemos repetir algunos por ejemplo el de barras por estado y prioridad. Pero la idea es tener al menos 4 gráficos distintos. Si se agregan más de 4 opciones no hay problema, solo que deberemos agregar una pregunta en la opción de mostrar 4 gráficos juntos, para saber cuáles tomar.
> 
> Las opciones de gráficos deben tener un nombre claro que las identifique (no dejes gráfico A B C)

**Usuario**:
> Quiero que continúe con la impronta de un desarrollador junior.
> 
> Pongamos la lógica de generar aleatorios en un archivo (ej generar_aleatorios o generar_registros)
> 
> La lógica de gráficos también pongamosla en un archivo a parte.
> 
> 1. Si, el número de registros por default será 100.
> 2. Ok
> 3. Usemos un mes entero como fechas aleatorias (entre el primer día de septiembre y el último)
> 4. Si, ese menú si podemos modificarlo para agregar la opción del nuevo submenú.
> 
> Con esto arma un nuevo prompt para extender la app original.

**Asistente**:
Se definió la estructura modular para esta segunda parte:
- `simulador.py` → control del submenú de simulación.
- `generar_aleatorios.py` → creación de registros simulados.
- `graficos.py` → generación de gráficos con pandas/matplotlib/seaborn.

---

## ⚙️ Especificaciones Técnicas

### 1. Generación de Registros Simulados
- **Campos**: `id`, `tarea`, `prioridad`, `estado`, `fecha`
- **Nombres de tareas**: Hasta 40 caracteres, únicos (se agrega número incremental si hay duplicados)
- **Prioridades**: ALTA, MEDIA, BAJA (aleatorio)
- **Estados**: PENDIENTE, EN CURSO, FINALIZADA (aleatorio)
- **Fechas**: Aleatorias entre 01/09/2025 y 30/09/2025

### 2. Gestión de Archivos
- **Archivo real**: `todo_list.json` (no se modifica)
- **Archivos de simulación**: 
  - Formato: `todo_list_simulador_YYYYMMDD.json`
  - Si existe: `todo_list_simulador_YYYYMMDD(1).json`, `todo_list_simulador_YYYYMMDD(2).json`, etc.

### 3. Gráficos Disponibles
1. 📊 Tareas por Prioridad (barras verticales)
2. 📈 Tareas por Estado (barras horizontales)
3. 📅 Distribución Temporal (histograma)
4. 🔥 Relación Prioridad vs Estado (heatmap)
5. 🥧 Proporción por Prioridad (pie chart)
6. 🍰 Proporción por Estado (pie chart)
7. 📈 Tendencia de Estados (stackplot)

### 4. Estructura de Archivos
```
/todo_list_py_lite
│── main.py                 # Menú principal (modificado)
│── simulador.py            # Submenú de simulación
│── generar_aleatorios.py   # Generación de datos simulados
│── graficos.py             # Funciones de visualización
│── service.py              # Lógica de negocio (existente)
│── utils.py                # Utilidades (existente)
```

### 5. Flujo de la Aplicación
1. Usuario selecciona "Simulación" en el menú principal
2. Se muestra el submenú de simulación
3. Opciones disponibles:
   - Generar N registros simulados
   - Ver gráficos individuales
   - Ver 4 gráficos juntos (seleccionables)
   - Volver al menú principal

---

## 📋 Prompt Final para la Implementación

```markdown
# Extensión de la Aplicación TODO List - Módulo de Simulación

## Objetivo
Ampliar la aplicación existente con un módulo de simulación que permita:
1. Generar registros de tareas simulados
2. Visualizar estadísticas mediante gráficos
3. Mantener los datos reales inalterados

## Requisitos Técnicos

### 1. Generación de Datos
- Crear `generar_aleatorios.py` con funciones para:
  - Generar N registros con datos aleatorios
  - Manejar nombres de tareas únicos
  - Asignar prioridades y estados aleatorios
  - Generar fechas aleatorias en septiembre 2025

### 2. Visualización
- Crear `graficos.py` con funciones para:
  - Gráfico de barras por prioridad
  - Gráfico de barras por estado
  - Histograma de distribución temporal
  - Heatmap de prioridad vs estado
  - Gráficos de torta para proporciones
  - Stackplot de tendencia
  - Visualización de 4 gráficos juntos

### 3. Interfaz de Usuario
- Modificar `main.py` para incluir opción de Simulación
- Crear `simulador.py` con submenú interactivo
- Mantener consistencia visual con la aplicación existente

### 4. Consideraciones
- No modificar la lógica existente
- Mantener separación de responsabilidades
- Documentar funciones principales
- Manejar errores de forma amigable
- Usar emojis y colores para mejor experiencia
```
