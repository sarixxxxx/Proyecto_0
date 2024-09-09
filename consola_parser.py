import parser as ps

def ConsolaInteractiva():
    control={
        "variables":[],
        "macros":{},
        "tokens": []
    }
    return control

def print_menu():
    print("Bienvenido a la consola interactiva. \n ¿Qué desea hacer?")
    print("1. Si desea salir de la consola.")
    print("2. Si desea analizar el archivo code-examples.txt. ")
    print("3. Si desea ingresar un código a analizar.")
    
def inicio(control):
    
    seguir=True
    while seguir:
        print_menu()
        try:
            entrada=input(" Seleccione una opción para continuar >>> ")
            if int(entrada) in ["1", "SALIR", "0", "OUT", "EXIT", 1, 0]:
                print("Saliendo de la consola...")
                seguir=False
            elif int(entrada) == 2:
                control["tokens"]= ps.lexer(contenido)
                print(f"Tokens generados: {control["tokens"]}")
                
                valido= ps.parser(control["tokens"], control["variables"], control["macros"])
                if valido:
                    print("El código ingresado es válido lexicográficamente.")
                else:
                    print("El código ingresado no es válido lexicográficamente.")
            else:
                codigo=input("Ingrese el código a analizar: ")
                control["tokens"]= ps.lexer(codigo)
                print(f"Tokens generados: {control["tokens"]}")
                
                valido= ps.parser(control["tokens"], control["variables"], control["macros"])
                if valido:
                    print("El código ingresado es válido lexicográficamente.")
                else:
                    print("El código ingresado no es válido lexicográficamente.")
        except Exception as e:
            print(f"Error: {e}")
            print("El código ingresado no es válido lexicográficamente.")
            
control=ConsolaInteractiva()
nombre_archivo="code-examples.txt"

with open(nombre_archivo, 'r') as archivo:
            contenido = archivo.read()
            
inicio(control)