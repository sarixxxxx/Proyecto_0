import parser as ps

def ConsolaInteractiva():
    control={
        "variables":{},
        "macros":{},
        "tokens": []
    }
    return control

def inicio(control):
    print("Bienvenido a la consola interactiva. \n Si desea salir de la consola ingrese SALIR. \n Ingrese el código a analizar:")
    seguir=True
    while seguir:
        try:
            entrada=input(">>> ")
            if entrada.upper() in ["EXIT", "SALIR", "0", "OUT"]:
                print("Saliendo de la consola...")
                seguir=False
            else:
                control["tokens"]= ps.lexer(entrada)
                
        except Exception as e:
            print(f"Error: {e}")
        