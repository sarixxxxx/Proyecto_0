
espacios = [" ", "\t", "\n"]
simbolos = ["{", "}", ";", "(", ")", ",", "=", "?"]

inputs = ["EXEC".upper(), "NEW".upper()]
definiciones = ["VAR".upper(), "MACRO".upper()]
direccion_turn = ["left".upper(), "right".upper(), "back".upper()]
orientacion_turn = ["north".upper(), "south".upper(), "east".upper(), "west".upper()]
direccion_move = ["left".upper(), "right".upper(), "forward".upper(), "backwards".upper()]
comandos_repetitivos = ["walk".upper(), "jump".upper(), "drop".upper(), "pick".upper(), "grab".upper(), "letGo".upper(), "pop".upper()]
comandos = ["turnToMy".upper(), "turnToThe".upper(), "moves".upper(), "nop".upper(), "safeExe".upper()] + comandos_repetitivos #variables para asignacion de variables
valores = ["size".upper(), "myX".upper(), "myY".upper(), "myChips".upper(), "myBallons".upper()]
controles = ["if".upper(), "do".upper(), "rep".upper()]
condiciones = ["isBlocked".upper(), "isFacing".upper(), "zero".upper(), "not".upper()]
direccion_condiciones = ["left".upper(), "right".upper(), "front".upper(), "back".upper()]

variables = []
dicc_macros = {}


def lexer(texto):
    tokens = []
    token = ""
    for caracter in texto:
        if caracter in simbolos:
            if token != "":
                tokens.append(token)
            tokens.append(caracter)
            token = ""
        elif caracter in espacios:
            if token != "":
                tokens.append(token)
            token = ""
        else:
            token += caracter  
    return tokens

def syntax_condicion(condicion):
    sintaxis = True
    tokens = condicion
    inicio = tokens[0].upper()
    if inicio in condiciones:
        if inicio != "not".upper() and tokens[1] == "?" and tokens[2] == "(" and tokens[4] == ")":
            if inicio == "isBlocked".upper():
                if tokens[3] in direccion_condiciones and len(tokens) == 5:
                    sintaxis = True
                else:
                    return False
            if inicio == "isFacing".upper():
                if tokens[3] in orientacion_turn and len(tokens) == 5:
                    sintaxis = True
                else:
                    return False
            if inicio == "zero".upper():
                if (tokens[3] in valores or tokens[3].isdigit()) and len(tokens) == 5:
                    sintaxis = True
                else:
                    return False
        else:
            if tokens[1] == "(":
                i = 2
                fin_condicion = None
                while i < len(tokens):
                    if tokens[i] == ")" and fin_condicion == None:
                        fin_condicion = i
                    i += 1
                if fin_condicion != None and len(tokens) == 3 + (fin_condicion - 2):
                    nueva_condicion = tokens[2:fin_condicion]
                    sintaxis = syntax_condicion(nueva_condicion)
                else:
                    print("error con not")
                    sintaxis = False
            else:
                print("error con not: condicion no empieza por parentesis")
                sintaxis = False                  
    else:
        print("la condicion señalada no existe")
        sintaxis = False
    
    return sintaxis
                
    

def syntax_control(tokens):
    sintaxis = True
    inicio = tokens[0].upper()
    
    if inicio == "if".upper():
        if tokens[1] == "(":
            i = 2
            fin_condicion = None
            while i < len(tokens):
                if tokens[i] == ")":
                    fin_condicion = i
                i += 1
            if fin_condicion != None:
                condicion = tokens[2:fin_condicion]
                if syntax_condicion(condicion):
                    if tokens[fin_condicion+1].upper() == "then".upper():
                        fin_bloque1 = None
                        i = fin_condicion+2
                        while i < len(tokens) and fin_bloque1 == None:
                            if tokens[i] == "}":
                                fin_bloque1 = i
                            i += 1
                        if fin_bloque1 != None:
                            bloque1 = tokens[fin_condicion+2:fin_bloque1+1]
                            if syntax_bloque(bloque1):
                                if tokens[fin_bloque1+1].upper() == "else".upper():
                                    fin_bloque2 = None
                                    i = fin_bloque1 + 2
                                    while i < len(tokens) and fin_bloque2 == None:
                                        if tokens[i] == "}":
                                            fin_bloque2 = i
                                        i += 1
                                    if fin_bloque2 != None:
                                        bloque2 = tokens[fin_bloque1+2:fin_bloque2+1]
                                        if not syntax_bloque(bloque2) or tokens[fin_bloque2+1].upper() != "fi".upper() or len(tokens) != fin_bloque2+2:
                                            print("error con el if en algun lado")
                                            sintaxis = False
    elif inicio == "do".upper():
        if tokens[1] == "(":
            i = 2
            fin_condicion = None
            while i < len(tokens):
                if tokens[i] == ")":
                    fin_condicion = i
                i += 1
            if fin_condicion != None:
                condicion = tokens[2:fin_condicion]
                if syntax_condicion(condicion):
                    fin_bloque1 = None
                    i = fin_condicion+1
                    while i < len(tokens) and fin_bloque1 == None:
                        if tokens[i] == "}":
                            fin_bloque1 = i
                        i += 1
                    if fin_bloque1 != None:
                        bloque1 = tokens[fin_condicion+2:fin_bloque1+1]
                        if not syntax_bloque(bloque1) or tokens[fin_bloque1+1].upper() != "od".upper() or len(tokens) != fin_bloque1+2:
                            print("error en algun lado con el do")
                            sintaxis = False
    elif inicio == "rep".upper():
        if tokens[1].isdigit():
            fin_bloque1 = None
            i = 2
            while i < len(tokens) and fin_bloque1 == None:
                if tokens[i] == "}":
                    fin_bloque1 = i
                i += 1
            if fin_bloque1 != None:
                bloque1 = tokens[2:fin_bloque1+1]
                if not syntax_bloque(bloque1) or tokens[fin_bloque1+1].upper() == "per".upper() or len(tokens) != fin_bloque1+2:
                    print("algun error con el repeat en algun lado")
                    sintaxis = False
    return sintaxis          

def syntax_comando(tokens):
    sintaxis = True
    inicio = tokens[0].upper()
    if inicio in dicc_macros:
        comas = dicc_macros[inicio] - 1
        longitud = 3 + dicc_macros[inicio] + comas
        parametros = tokens[2:(2+dicc_macros[inicio]+comas)]
        
        bien_parametros = True
        for parametro in parametros:
            if parametro != ",":
                if (parametro not in valores) and (parametro.isdigit() == False):
                    bien_parametros = False
        if bien_parametros and len(tokens) == longitud and tokens[1] == "(" and tokens[longitud-1] == ")":
            sintaxis = True
        else:
            print("parametros, longitud o parentesis mal")
            sintaxis = False
    elif inicio == "turnToMy".upper():
        if len(tokens) == 4 and tokens[1] == "(" and tokens[2].upper() in direccion_turn and tokens[3] == ")":
            sintaxis = True
        else:
            print(tokens)
            print("fallo turn to my")
            sintaxis = False
    elif inicio == "turnToThe".upper():
        if len(tokens) == 4 and tokens[1] == "(" and tokens[2].upper() in orientacion_turn and tokens[3] == ")":
            sintaxis = True
        else:
            print("fallo turn to the")
            sintaxis = False
    elif inicio in comandos_repetitivos:
        if len(tokens) == 4 and tokens[1] == "(" and (tokens[2].upper() in valores or tokens[2].isdigit()) and tokens[3] == ")":
            sintaxis = True
        else:
            print("fallo comandos repetitivos")
            sintaxis = False
    elif inicio == "moves".upper():
        if tokens[1] == "(":
            i = 2
            ds = ""
            final = False
            while i < len(tokens) and final == False:
                if tokens[i] == ")":
                    final = True
                else:
                    ds += tokens[i]
                i += 1
            if ds != "":
                direcciones_bien = True
                ds.split(",")
                for direccion in ds:
                    if direccion.upper() not in direccion_move:
                        direcciones_bien = False
                longitud = 3 + 2*len(ds) - 1 #comas es len(ds) - 1
                if not direcciones_bien or (len(tokens) != longitud) or tokens[1] != "(" or tokens[longitud-1] != ")":
                    sintaxis = False
            else:
                print("la secuencia de instrucciones de move esta vacia")
                sintaxis = False
        else:
            print("moves no empieza con parentesis")
    elif inicio == "nop".upper():
        if len(tokens) != 1:
            sintaxis = False
    elif inicio == "SafeExe".upper():
        if len(tokens) == 7:
            nuevo_comando = tokens[2:6]
            sintaxis = syntax_comando(nuevo_comando)
        else:
            print("el safeexe esta mal")
            sintaxis = False
    else:
        if tokens[0] in variables and len(tokens) == 3 and tokens[1] == "=" and (tokens[2] in valores or tokens[2].isdigit()):
            sintaxis = True
        else:
            print("el comando de asignacion de valor a variable esta mal")
            sintaxis = False
    return sintaxis
        
def syntax_instruccion(instruccion):
    sintaxis = True
    if instruccion[-1] != ";":
        print("La instruccion no termina con ;")
        return False
    
    tokens = instruccion[0:-1]
    inicio = tokens[0].upper()
    
    if inicio in comandos:
        sintaxis = syntax_comando(tokens)
        if not sintaxis:
            print("Error en syntax comando")
    elif inicio in controles:
        sintaxis = syntax_control(tokens)
        if not sintaxis:
            print("Error en syntax control")
    else:
        print("No se encontro la instruccion", inicio)
        sintaxis = False
    return sintaxis

def syntax_bloque(bloque):
    sintaxis = True
    if bloque[0] != "{":
        print("Syntax Error: inicia instruccion sin llave")
        return False
    if bloque[-1] != "}":
        print("Syntax Error: termina instruccion sin llave")
        return False
    tokens = bloque[1:-1]
    
    # Manejar múltiples instrucciones dentro de un bloque
    instrucciones = []
    instruccion_actual = []
    nivel_bloque = 0

    for token in tokens:
        if token == '{':
            nivel_bloque += 1
        elif token == '}':
            nivel_bloque -= 1
        elif token == ';' and nivel_bloque == 0:
            if instruccion_actual:
                instrucciones.append(instruccion_actual + [token])
                instruccion_actual = []
        else:
            instruccion_actual.append(token)

    if instruccion_actual:
        instrucciones.append(instruccion_actual)

    for instruccion in instrucciones:
        if not syntax_instruccion(instruccion):
            sintaxis = False
    
    return sintaxis
    

#ojo me toca revisar los casos en que esta vacio pa no delvolver false, digamos exect{}
def syntax_definicion(tokens):
    sintaxis = True
    definicion = tokens[0].upper()
    
    if definicion == "VAR":
        if tokens[2] == "=" and (tokens[3] in valores or tokens[3].isdigit()):
            variables.append(tokens[1].upper())
            valores.append(tokens[1].upper())
            comandos.append(tokens[1].upper())
            sintaxis = True
        else:
            print("ERROR EN DEFINICION VAR")
            sintaxis = False
    else:
        if tokens[2] == "(":
            i = 3
            parametros = ""
            indice_final = None
            while i < len(tokens) and indice_final == None:
                if tokens[i] == ")":
                    indice_final = i
                else:
                    parametros += tokens[i]
                i += 1
            if indice_final == None:
                sintaxis = False
            else:
                comandos.append(tokens[1].upper())
                parametros_lista = parametros.split(",")
                for parametro in parametros_lista:
                    valores.append(parametro.upper())
                dicc_macros[tokens[1]] = len(parametros)
                bloque = tokens[indice_final+1:]
                sintaxis = syntax_bloque(bloque)
        else:
            print("ERROR EN DEFINICION MACRO")
            sintaxis = False
    return sintaxis

def parser(texto):
    tokens = lexer(texto)
    sintaxis = True
    
    if tokens[0] not in inputs:
        print("Syntax Error: Invalid input")
        sintaxis = False

    subconjuntos = []
    inicio = None
    for i, token in enumerate(tokens):
        if token in inputs:
            if inicio is not None:
                subconjuntos.append(tokens[inicio:i])
            inicio = i
    if inicio is not None:
        subconjuntos.append(tokens[inicio:])
    
    for subconjunto in subconjuntos:
        inp = subconjunto[0].upper()
        if inp == "EXEC".upper():
            bloque = subconjunto[1:] #dentro revisa que empiece bien
            if not syntax_bloque(bloque):
                print("Syntax Error: Invalid execution block")
                sintaxis = False
        else:
            definicion = subconjunto[1:]
            if not syntax_definicion(definicion):
                print("Syntax Error: Invalid definition block")
                sintaxis = False
    print(sintaxis)
    return sintaxis

#pruebas
texto = '''
EXEC  {	
walk(10);
}
'''

texto2 = '''
NEW VAR speed = 5
EXEC  {	
walk(10);
}
NEW MACRO moveSquare (steps){walk(steps); turnToMy(right); walk(steps); turnToMy(right); walk(steps); turnToMy(right); walk(steps); }
EXEC {walk(10); turnToThe(north); jump(3); }


'''

texto3 = '''
EXEC {
    if(isBlocked?(front)) then {
        turnToMy(right);
        walk(5);
    } else {
        walk(10);
    } fi;
}
EXEC {rep 3 times {walk(2); turnToMy(left); } per}

'''

texto4 = '''
EXEC  { foo (1 ,3) ; }
'''

texto5 = '''
NEW VAR one= 1
NEW MACRO  		goend ()
{
	if not (blocked?(front))
	then  { move(one); goend();  }
	else  { nop; }
    fi;
}
'''

texto6 = '''
NEW MACRO fill ()
  { 
  rep roomForChips times 
  {  if not (zero?(myChips)) { drop(1);}  else { nop; } fi ;} ; 
  }
  
  NEW MACRO fill1 ()
  { 
  while not zero?(rooomForChips)
  {  if not (zero?(myChips)) { drop(1);}  else { nop; } fi ;
  } ; 
  }
'''

texto7 = '''
NEW MACRO grabAll ()
{ grab (balloonsHere);
}
'''

parser(texto)
print("\n")
parser(texto2)
print("\n")
parser(texto3)
print("\n")
parser(texto4)
print("\n")
parser(texto5)
print("\n")
parser(texto6)
print("\n")
parser(texto7)