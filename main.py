"""
Aplicación TODO List - Punto de entrada principal
"""
# print(AplicacionTodoList.__doc__)
# Muestra: "Clase principal de la aplicación TODO List."
# Permite acceder desde la terminal a la documentación de la clase.

from service import TodoService
from utils import (
    Colors, EMOJIS, limpiar_pantalla, 
    obtener_fecha_actual, formatear_tabla, pausa, validar_opcion
)

# Constantes
OPCIONES_MENU_PRINCIPAL = [
    "Agregar tarea",
    "Listar tareas",
    "Buscar tareas",
    "Editar tarea",
    "Eliminar tarea",
    "Salir"
]

PRIORIDADES = {
    1: "ALTA",
    2: "MEDIA",
    3: "BAJA"
}

ESTADOS = {
    1: "PENDIENTE",
    2: "EN CURSO",
    3: "FINALIZADA"
}

class AplicacionTodoList:
    """Clase principal de la aplicación TODO List."""
    
    def __init__(self):
        """Inicializa la aplicación con el servicio de tareas."""
        self.servicio = TodoService()
        # Self es una convención en Python que se usa para referirse a la instancia de la clase. (Similar al operador this)
        # Es explícito y obligatorio como primer parámetro de los métodos de la clase.
        # Podría llamarse de otra manera pero es una buena práctica usar self.
    
    def mostrar_encabezado(self):
        """Muestra el encabezado de la aplicación."""
        limpiar_pantalla()
        print(f"\n{Colors.BOLD}{Colors.PURPLE}📝 TODO List App{Colors.RESET}")
        print(f"{'~' * 40}")
        print(f"{Colors.CYAN}Fecha actual: {obtener_fecha_actual()}{Colors.RESET}\n")
    
    def mostrar_menu_principal(self):
        """Muestra el menú principal y obtiene la opción seleccionada."""
        self.mostrar_encabezado()
        print(f"{Colors.BOLD}Menú Principal:{Colors.RESET}")
        
        # Muestra opciones numeradas (1-6)
        for i, opcion in enumerate(OPCIONES_MENU_PRINCIPAL, 1):
            print(f"{i}. {opcion}")
        
        print("\n" + "~" * 40)
        
        # Bucle hasta recibir una opción válida
        while True:
            opcion = input("\nSeleccione una opción (1-6): ")
            valida, opcion_num = validar_opcion(opcion, 1, 6)
            
            # Retorna si la opción es válida
            if valida:
                return opcion_num
                
            # Muestra error y repite el bucle
            print(f"{Colors.RED}Opción inválida. Intente nuevamente.{Colors.RESET}")
    
    def ejecutar(self):
        """Ejecuta el bucle principal de la aplicación."""
        while True:
            try:
                opcion = self.mostrar_menu_principal()
                
                if opcion == 1:  # Agregar tarea
                    self.agregar_tarea()
                elif opcion == 2:  # Listar tareas
                    self.listar_tareas()
                elif opcion == 3:  # Buscar tareas
                    self.buscar_tareas()
                elif opcion == 4:  # Editar tarea
                    self.editar_tarea()
                elif opcion == 5:  # Eliminar tarea
                    self.eliminar_tarea()
                elif opcion == 6:  # Salir
                    print(f"\n{Colors.GREEN}¡Hasta luego! {EMOJIS['check']}{Colors.RESET}\n")
                    break
                
                pausa()
                
            except KeyboardInterrupt:
                print(f"\n\n{Colors.YELLOW}Operación cancelada por el usuario.{Colors.RESET}")
                pausa()
            except Exception as e:
                print(f"\n{Colors.RED}Error: {str(e)}{Colors.RESET}")
                pausa()
    
    def agregar_tarea(self):
        """Interfaz para agregar una nueva tarea."""
        self.mostrar_encabezado()
        print(f"{Colors.BOLD}{EMOJIS['add']} Agregar Nueva Tarea{Colors.RESET}\n")
        
        # Obtener nombre de la tarea
        while True:
            nombre = input("Nombre de la tarea: ").strip()
            if nombre:
                break
            print(f"{Colors.RED}El nombre no puede estar vacío.{Colors.RESET}")
        
        # Obtener prioridad
        print("\nSeleccione la prioridad:")
        for num, prioridad in PRIORIDADES.items():
            print(f"{num}. {prioridad}")
        
        while True:
            opcion = input("\nOpción (1-3): ")
            valida, opcion_num = validar_opcion(opcion, 1, 3)
            if valida:
                prioridad = PRIORIDADES[opcion_num]
                break
            print(f"{Colors.RED}Opción inválida. Intente nuevamente.{Colors.RESET}")
        
        # Agregar la tarea
        exito, mensaje = self.servicio.agregar_tarea(nombre, prioridad)
        if exito:
            print(f"\n{Colors.GREEN}{mensaje}{Colors.RESET}")
        else:
            print(f"\n{Colors.RED}{mensaje}{Colors.RESET}")
    
    def listar_tareas(self, tareas=None, mensaje=None):
        """Muestra la lista de tareas con opción de paginación."""
        self.mostrar_encabezado()
        print(f"{Colors.BOLD}{EMOJIS['info']} Lista de Tareas{Colors.RESET}")
        if mensaje:
            print(f"\n{mensaje}")
        
        # Si no se proporciona una lista de tareas, obtener todas
        if tareas is None:
            tareas = self.servicio.listar_tareas()
        
        if not tareas:
            print(f"\n{Colors.YELLOW}No hay tareas para mostrar.{Colors.RESET}")
            return
        
        # Mostrar tareas por lotes de 15
        total_tareas = len(tareas)
        inicio = 0
        tamano_lote = 15
        
        while inicio < total_tareas:
            lote = tareas[inicio:inicio + tamano_lote]
            print(f"\n{formatear_tabla(lote)}")
            print(f"\nMostrando {inicio + 1}-{min(inicio + len(lote), total_tareas)} de {total_tareas} tareas")
            
            inicio += tamano_lote
            
            if inicio < total_tareas:
                input(f"\n{Colors.BLUE}Presiona Enter para ver más tareas o Ctrl+C para volver al menú...{Colors.RESET}")
                self.mostrar_encabezado()
                print(f"{Colors.BOLD}{EMOJIS['info']} Lista de Tareas (continuación){Colors.RESET}\n")
    
    def buscar_tareas(self):
        """Interfaz para buscar tareas."""
        self.mostrar_encabezado()
        print(f"{Colors.BOLD}{EMOJIS['search']} Buscar Tareas{Colors.RESET}\n")
        
        texto_busqueda = input("Ingrese texto para buscar (dejar en blanco para omitir): ").strip()
        
        # Opción para filtrar por prioridad
        print("\nFiltrar por prioridad:")
        print("1. Todas las prioridades")
        for num, prioridad in PRIORIDADES.items():
            print(f"{num + 1}. {prioridad}")
        
        while True:
            opcion = input("\nOpción (1-4): ")
            valida, opcion_num = validar_opcion(opcion, 1, 4)
            if valida:
                if opcion_num == 1:
                    prioridad = None
                else:
                    prioridad = PRIORIDADES[opcion_num - 1]
                break
            print(f"{Colors.RED}Opción inválida. Intente nuevamente.{Colors.RESET}")
        
        # Realizar la búsqueda
        if texto_busqueda:
            resultados = self.servicio.buscar_tareas(texto_busqueda, prioridad)
            mensaje = f"Resultados para: '{texto_busqueda}'"
            if prioridad:
                mensaje += f" (Prioridad: {prioridad})"
        else:
            resultados = self.servicio.listar_tareas(prioridad) if prioridad else self.servicio.listar_tareas()
            mensaje = f"Todas las tareas" + (f" (Filtradas por prioridad: {prioridad})" if prioridad else "")
        
        self.listar_tareas(resultados, mensaje)
    
    def editar_tarea(self):
        """Interfaz para editar una tarea existente."""
        self.mostrar_encabezado()
        print(f"{Colors.BOLD}{EMOJIS['edit']} Editar Tarea{Colors.RESET}\n")
        
        # Mostrar todas las tareas primero
        tareas = self.servicio.listar_tareas()
        if not tareas:
            print(f"{Colors.YELLOW}No hay tareas para editar.{Colors.RESET}")
            return
        
        print(formatear_tabla(tareas))
        
        # Obtener ID de la tarea a editar
        while True:
            try:
                tarea_id = int(input("\nIngrese el ID de la tarea a editar (0 para cancelar): "))
                if tarea_id == 0:
                    print("Operación cancelada.")
                    return
                
                tarea = self.servicio.obtener_tarea_por_id(tarea_id)
                if tarea:
                    break
                print(f"{Colors.RED}No se encontró ninguna tarea con ID: {tarea_id}{Colors.RESET}")
            except ValueError:
                print(f"{Colors.RED}Por favor ingrese un número de ID válido.{Colors.RESET}")
        
        # Mostrar datos actuales
        print(f"\n{Colors.BOLD}Editando tarea ID: {tarea['id']}{Colors.RESET}")
        print(f"1. Nombre: {tarea['nombre']}")
        print(f"2. Prioridad: {tarea['prioridad']}")
        print(f"3. Estado: {tarea['estado']}")
        
        # Obtener campos a editar
        print("\n¿Qué campo desea editar?")
        print("1. Nombre")
        print("2. Prioridad")
        print("3. Estado")
        print("4. Cancelar")
        
        while True:
            opcion = input("\nSeleccione una opción (1-4): ")
            valida, opcion_num = validar_opcion(opcion, 1, 4)
            if valida:
                break
            print(f"{Colors.RED}Opción inválida. Intente nuevamente.{Colors.RESET}")
        
        if opcion_num == 4:
            print("Operación cancelada.")
            return
        
        # Procesar la edición según el campo seleccionado
        if opcion_num == 1:  # Editar nombre
            nuevo_nombre = input("Nuevo nombre: ").strip()
            if not nuevo_nombre:
                print(f"{Colors.RED}El nombre no puede estar vacío.{Colors.RESET}")
                return
            
            exito, mensaje = self.servicio.editar_tarea(
                tarea_id, 
                nuevo_nombre=nuevo_nombre,
                nueva_prioridad=None,
                nuevo_estado=None
            )
            
        elif opcion_num == 2:  # Editar prioridad
            print("\nSeleccione la nueva prioridad:")
            for num, prioridad in PRIORIDADES.items():
                print(f"{num}. {prioridad}")
            
            while True:
                opcion_prioridad = input("\nOpción (1-3): ")
                valida, prioridad_num = validar_opcion(opcion_prioridad, 1, 3)
                if valida:
                    break
                print(f"{Colors.RED}Opción inválida. Intente nuevamente.{Colors.RESET}")
            
            exito, mensaje = self.servicio.editar_tarea(
                tarea_id,
                nuevo_nombre=None,
                nueva_prioridad=PRIORIDADES[prioridad_num],
                nuevo_estado=None
            )
            
        elif opcion_num == 3:  # Editar estado
            print("\nSeleccione el nuevo estado:")
            for num, estado in ESTADOS.items():
                print(f"{num}. {estado}")
            
            while True:
                opcion_estado = input("\nOpción (1-3): ")
                valida, estado_num = validar_opcion(opcion_estado, 1, 3)
                if valida:
                    break
                print(f"{Colors.RED}Opción inválida. Intente nuevamente.{Colors.RESET}")
            
            exito, mensaje = self.servicio.editar_tarea(
                tarea_id,
                nuevo_nombre=None,
                nueva_prioridad=None,
                nuevo_estado=ESTADOS[estado_num]
            )
        
        if exito:
            print(f"\n{Colors.GREEN}{mensaje}{Colors.RESET}")
        else:
            print(f"\n{Colors.RED}{mensaje}{Colors.RESET}")
    
    def eliminar_tarea(self):
        """Interfaz para eliminar una tarea."""
        self.mostrar_encabezado()
        print(f"{Colors.BOLD}{EMOJIS['delete']} Eliminar Tarea{Colors.RESET}\n")
        
        # Mostrar todas las tareas primero
        tareas = self.servicio.listar_tareas()
        if not tareas:
            print(f"{Colors.YELLOW}No hay tareas para eliminar.{Colors.RESET}")
            return
        
        print(formatear_tabla(tareas))
        
        # Obtener ID de la tarea a eliminar
        while True:
            try:
                tarea_id = int(input("\nIngrese el ID de la tarea a eliminar (0 para cancelar): "))
                if tarea_id == 0:
                    print("Operación cancelada.")
                    return
                
                # Confirmar eliminación
                confirmacion = input(f"¿Está seguro de que desea eliminar la tarea con ID {tarea_id}? (s/n): ").lower()
                if confirmacion == 's':
                    exito, mensaje = self.servicio.eliminar_tarea(tarea_id)
                    if exito:
                        print(f"\n{Colors.GREEN}{mensaje}{Colors.RESET}")
                    else:
                        print(f"\n{Colors.RED}{mensaje}{Colors.RESET}")
                    break
                else:
                    print("Eliminación cancelada.")
                    break
                    
            except ValueError:
                print(f"{Colors.RED}Por favor ingrese un número de ID válido.{Colors.RESET}")

def main():
    """Función principal que inicia la aplicación."""
    try:
        app = AplicacionTodoList()
        app.ejecutar()
    except KeyboardInterrupt:
        print(f"\n\n{Colors.YELLOW}Aplicación finalizada por el usuario.{Colors.RESET}\n")
    except Exception as e:
        print(f"\n{Colors.RED}Error inesperado: {str(e)}{Colors.RESET}")
        print(f"\n{Colors.YELLOW}Por favor, intente nuevamente.{Colors.RESET}")
        pausa()
        main()  # Reiniciar la aplicación en caso de error

if __name__ == "__main__":
    main()
