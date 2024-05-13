#CASO PRÁCTICO FINAL: María José Nadales Núñez

import json
import os

# Definir colores ANSI
RESET = "\033[0m"
CIAN = "\033[36m"
GREEN = "\033[32m"
YELLOW = "\033[33m"
RED = "\033[31m"

#creamos la clase Task con su constructor y un método para marcarla como completa
class Task:
    def __init__(self, description, complete=False):
        self.description = description
        self.complete = complete

    def mark_as_complete(self):
        self.complete = True


#tenemos que cargar todas las tareas desde nuestro archivo json
def load_tasks_from_json(file_path):
    try:
        #abrir el archivo json como lectura para recuperar todas las tareas que tenemos en el archivo
        with open(file_path, 'r') as file:
            #recuperamos la informacion del archivo json
            tasks_data = json.load(file)
            tasks  = []
           # Recorremos cada elemento en tasks_data (que contiene los datos recuperados de nuestro Json)
            for task_data in tasks_data:
                # Creamos una instancia de la clase Task para cada tarea, para luego añadirla a nuestra lista de tareas
                task = Task(task_data['description'], task_data['complete'])
                tasks.append(task)
          
            return tasks
    except FileNotFoundError:
        return []



#guardamos nuestra lista de tareas en el archivo json
def save_tasks_to_json(tasks, file_path):

    tasks_data = []

    for task in tasks:
        # creamos un diccionario para cada tarea con los datos que tenemos que guardar, lo hacemos asi para poder guardar luego en json.
        task_data = {'description': task.description, 'complete': task.complete}
        # añadir el diccionario de la tarea a la lista tareas que vamos a mandar a nuestro json
        tasks_data.append(task_data)

    try:
        # abrimos el archivo Json en modo escritura.
        with open(file_path, 'w') as file:
            # escribimos los datos de las tareas en el archivo JSON.
            json.dump(tasks_data, file, indent=4)

    except Exception as e:
        print(f"\n{RED}Error al guardar tareas en el archivo JSON: {e}{RESET}")


#mostrar todas las tareas
def show_tasks(tasks):

    if tasks:
        print(f"\n\n{CIAN}______MIS TAREAS______:{RESET}\n")
        
        for i, task in enumerate(tasks, 1):
            # usamos enumerate para obtener el índice (empezando en 1) y la tarea actual
            # mostramos el índice (num de tarea), el estado de la tarea (completa o no) y la descripción de la tarea
            # el color del texto según si la tarea está completa es verde y para las pendientes en amarillo
            color = GREEN if task.complete else YELLOW
            print(f"{i}. [{color}{'Completada' if task.complete else 'Pendiente '}{RESET}]======> {task.description}")
           
    else:
        print(F"\n{RED}No hay tareas en la lista.{RESET}")

#añadir nueva tarea
def add_task(tasks):

    description = input(f"\n{RESET}Introduce la descripción de la tarea: ")
    
    # creamos una instancia de la clase Task con la descripción proporcionada por el usuario, no hace falta dar valor al atributo "complete" porque al crear
    #la tarea por primera vez le decimos que sea false, es decir la tarea se acaba de crear por lo que NO está completada aun.
    new_task = Task(description)
    
    tasks.append(new_task)
    save_tasks_to_json(tasks, 'tasks.json')
    print("\nTarea añadida correctamente.")


#eliminamos una tarea de la lista y además actualizamos el archivo json
def remove_task(tasks):

    show_tasks(tasks)
    
    if tasks:
        try:
            index = int(input("\nIntroduce el número de la tarea que deseas eliminar: "))
            if 1 <= index <= len(tasks):
                confirm = input("¿Estás seguro? Pulsa 's' para confirmar: ").lower()
                if confirm == 's':
                    del tasks[index - 1]
                    save_tasks_to_json(tasks, 'tasks.json')
                    print("\nTarea eliminada correctamente.")
                else:
                    print("\nEliminación de tarea cancelada.")
            else:
                print(f"\n{RED}Número de tarea no válido.{RESET}")
        except ValueError:
            print(f"\n{RED}Por favor, introduce un número válido.{RESET}")
    else:
        print(f"\n{RED}No hay tareas para eliminar.{RESET}")




#confirmamos si queremos salir o no, además da igual si ponemos la respuesta en mayúysculas o minusculas
def confirm_exit():
    response = input(f"{RESET}\n¿Estás seguro de que quieres salir? (s/n): ")
    return response.lower() == 's'


#marcamos una tarea como completada, actualizando la lista de tareas y además el archivo json
def complete_task(tasks):

    show_tasks(tasks)

    if tasks:
        try:
            index = int(input("\nIntroduce el número para completar: "))
            
            # chequear si el índice está dentro del rango válido de tareas
            if 1 <= index <= len(tasks):
                tasks[index - 1].mark_as_complete()
                save_tasks_to_json(tasks, 'tasks.json')
                print("\nTarea completada correctamente.")
            else:
                print(f"\n{RED}Número de tarea no válido.{RESET}")
        except ValueError:
            print(f"\n{RED}Por favor, introduce un número válido.{RESET}")
    else:
        print(f"\n{RED}No hay tareas{RESET}")



# limpiamos la pantalla
def clear_screen():
    # si estamos en windows
    if os.name == 'nt':
        _ = os.system('cls') 
    else:
        #si es otro sistema operativo
        _ = os.system('clear') 


if __name__ == '__main__':
    #lo primero que debemos hacer es cargar las tareas desde nuestro archivo Json, 
    #en este caso como estan en el mismo directorio solo hace falta el nombre del archivo, si está en otro poner la ruta a al json
    tasks = load_tasks_from_json('tasks.json')
      
    clear_screen()

    #bucle que muestra el Menú de opciones hasta que "rompamos" la ejecución del mismo con un break, esto ocurre en el caso de pulsar la opcion 5.
    while True:

        print(f"\n{RESET}{CIAN}______MENÚ______:{RESET}\n")
        print("1. Mostrar tareas")
        print("2. Añadir tarea")
        print("3. Eliminar tarea")
        print("4. Completar tarea")
        print("5. Salir")

        choice = input(F"\n\n{CIAN}Selecciona una opción:{RESET} ")


        if choice == '1':
            clear_screen()
            #mostrar todas las tareas
            show_tasks(tasks)   
            input("\nPulsa Enter para regresar al menú")
            clear_screen()
        elif choice == '2':
            clear_screen()
            #añadir nueva tarea
            add_task(tasks)
            input("\nPulsa Enter para regresar al menú")
            clear_screen()
        elif choice == '3':
            clear_screen()
            #eliminar tarea
            remove_task(tasks)
            input("\nPulsa Enter para regresar al menú")
            clear_screen()
        elif choice == '4':
            clear_screen()
            #marcar tarea como completa
            complete_task(tasks)
            input("\nPulsa Enter para regresar al menú")
            clear_screen()
        elif choice == '5':
            clear_screen()
            #salir y terminar
            if confirm_exit():
                break
        else:
            clear_screen()
            print(f"{RED}Opción no válida.{RESET}")
            input("\nPulsa Enter para regresar al menú")
            clear_screen()

