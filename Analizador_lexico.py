import sys
operadores = {
    "NOT": "token_neg",
    "=": "token_igual",
    "<>": "token_dif",
    "<": "token_menor",
    ">": "token_mayor",
    "<=": "token_menor_igual",
    ">=": "token_mayor_igual",
    "+": "token_mas",
    "-": "token_menos",
    "/": "token_div",
    "*": "token_mul",
    "MOD": "token_mod",
    "(": "token_par_izq",
    ")": "token_par_der",
    "OR": "token_o",
    "AND": "token_y",
    "XOR": "token_xor",
    ";": "token_pyc",
    ",": "token_coma",
    "^": "token_pot",
    "%": "token_porcentaje",
    "&": "token_ampersand",
    "!": "token_admiracion",
    "#": "token_numeral",
    "$": "token_pesos"
}
palabras_reservadas = {
    "STRING": "string",
    "DIM": "dim",
    "INTEGER": "integer",
    "AS": "as",
    "LONG": "long",
    "SINGLE": "single",
    "DOUBLE": "double",
    "INPUT": "input",
    "PRINT": "print",
    "IF": "if",
    "THEN": "then",
    "ELSEIF": "elseif",
    "ELSE": "else",
    "END": "end",
    "SELECT": "select",
    "CASE": "case",
    "WHILE": "while",
    "WEND": "wend",
    "DO": "do",
    "LOOP": "loop",
    "UNTIL": "until",
    "FOR": "for",
    "NEXT": "next",
    "TO": "to",
    "SUB": "sub",
    "SHARED": "shared",
    "FUNCTION": "function",
    "LEN": "len",
    "LEFT$": "left$",
    "RIGHT$": "rigth$",
    "MID$": "mid$",
    "INFINITY": "infinity",
    "STEP": "step"
}


def verificacion_palabra(palabra, fila, columna):
    mayuscula = palabra.upper()

    if mayuscula in palabras_reservadas:
        tipo_token = palabras_reservadas[mayuscula]
        print("<" + tipo_token + "," +
              str(fila) + "," + str(columna) + ">")
        return True

    elif mayuscula in operadores:
        nombre_token = operadores[mayuscula]
        print("<" + nombre_token + "," +
              str(fila) + "," + str(columna) + ">")
        return True

    elif palabra.isdigit():
        if int(palabra) <= 32767:
            print("<token_integer," + palabra + "," +
                  str(fila) + "," + str(columna) + ">")
            return True
        elif int(palabra) > 32767:
            print("<token_long," + palabra + "," +
                  str(fila) + "," + str(columna) + ">")
            return True

    elif palabra[0] == '"' and palabra[len(palabra) - 1] == '"' and len(palabra) > 1:
        _string_ = palabra.strip('"')
        print("<token_string," + _string_ + "," +
              str(fila) + "," + str(columna) + ">")
        return True

    elif palabra.isalpha():
        print("<id," + palabra.lower() + "," +
              str(fila) + "," + str(columna) + ">")
        return True

    return False


def verificacion_caracter(palabra, fila, columna):
    
    token = ""
    lexema = ""
    operador = False
    numero = False
    decimal = False
    letra = False
    decimas = 0
    verificacion_operador = False

    columna_palabra = columna

    i = 0
    while i < len(palabra):
        caracter = palabra[i]
        if caracter in operadores:
            if numero or letra:
                print("<" + token + "," + lexema.lower() + "," +
                      str(fila) + "," + str(columna) + ">")

            columna = columna_palabra + i
            if i + 1 < len(palabra):
                if palabra[i + 1] in operadores:
                    token = caracter + palabra[i + 1]
                    if token in operadores:
                        i += 1
                        print("<" + operadores[token] + "," +
                              str(fila) + "," + str(columna) + ">")
                    else:
                        print("<" + operadores[caracter] + "," +
                              str(fila) + "," + str(columna) + ">")
                else:
                    print("<" + operadores[caracter] + "," +
                          str(fila) + "," + str(columna) + ">")
            else:
                print("<" + operadores[caracter] + "," +
                      str(fila) + "," + str(columna) + ">")
            columna += 1

            token = ""
            lexema = ""
            operador = True
            numero = False
            decimal = False
            letra = False
            decimas = 0

        elif caracter.isdigit():
            operador = False

            if numero == False:
                numero = True
                token = "token_integer"

            elif decimal:
                decimas += 1

            if decimal and decimas <= 6:
                token = "token_single"

            elif decimal and decimas > 6:
                token = "token_double"

            if letra:
                token = "id"
            elif numero and lexema.isdigit():
                if int(lexema) > 32767:
                    token = "token_long"

            lexema = lexema + caracter

        elif caracter == "." and not decimal:
            operador = False
            decimal = True
            lexema = lexema + caracter

        elif caracter == "." and decimal and letra:
            columna = columna_palabra + i
            print(">>> Error lexico (linea:" + str(fila) +
                  ", posicion:" + str(columna) + ")")
            sys.exit()

        elif caracter.isalpha():
            operador = False
            letra = True
            if numero:

                print("<" + token + "," + lexema.lower() + "," +
                      str(fila) + "," + str(columna) + ">")
                columna = columna_palabra + i
                numero = False
                lexema = ""

            if caracter == "N":
                lexema = caracter + palabra[i + 1] + palabra[i + 2]
                if lexema in operadores:
                    i = i + 2
                    verificacion_operador = True
                    operador = True

            elif caracter == "O":
                lexema = caracter + palabra[i + 1]
                if lexema in operadores:
                    i = i + 1
                    verificacion_operador = True
                    operador = True

            elif caracter == "X":
                lexema = caracter + palabra[i + 1] + palabra[i + 2]
                if lexema in operadores:
                    i = i + 2
                    verificacion_operador = True
                    operador = True

            elif caracter == "M":
                lexema = caracter + palabra[i + 1] + palabra[i + 2]
                if lexema in operadores:
                    i = i + 2
                    verificacion_operador = True
                    operador = True

            elif caracter == "A":
                lexema = caracter + palabra[i + 1] + palabra[i + 2]
                if lexema in operadores:
                    i = i + 2
                    verificacion_operador = True
                    operador = True

            if not verificacion_operador:
                token = "id"
                lexema = lexema + caracter
            else:
                print("<" + operadores[lexema] + "," +
                      str(fila) + "," + str(columna) + ">")
                lexema = ""
                token = ""
                letra = False

            verificacion_operador = False
            

        elif caracter not in operadores:

            operador = False
            if caracter == "_":
                lexema = lexema + caracter
            else:
                if numero or letra:
                    print("<" + token + "," + lexema.lower() + "," +
                          str(fila) + "," + str(columna) + ">")

                columna = columna_palabra + i
                print(">>> Error lexico (linea:" +
                      str(fila) + ", posicion:" + str(columna) + ")")
                sys.exit()

        if i + 1 == len(palabra) and not operador:
            print("<" + token + "," + lexema.lower() + "," +
                  str(fila) + "," + str(columna) + ">")

        i += 1


def verificacion_string(i, palabras, fila, columna):
    token = "token_string"
    if palabras[i].count('"') > 1:
        lexema = palabras[i].split('"')
        palabras[i] = lexema[2]
        print("<" + token + "," + lexema[1] + "," +
              str(fila) + "," + str(columna) + ">")
        return i - 1

    lexema = palabras[i].strip('"') + " "
    error = True

    i += 1
    while i < len(palabras):
        palabra = palabras[i]
        if '"' in palabra:
            if palabra[len(palabra) - 1] == '"':
                error = False
                _string_ = palabra.strip('"')
                lexema = lexema + _string_

                print("<" + token + "," + lexema + "," +
                      str(fila) + "," + str(columna) + ">")
                return i
            else:
                error = False
                nueva_palabra = palabra.split('"')
                palabras[i] = nueva_palabra[1]
                lexema = lexema + nueva_palabra[0]
                print("<" + token + "," + lexema + "," +
                      str(fila) + "," + str(columna) + ">")
                return i - 1

        else:
            lexema = lexema + palabra + " "
            i += 1
    if error:
        print(">>> Error lexico (linea:" +
              str(fila) + ", posicion:" + str(columna) + ")")
        sys.exit()


fila = 0
while(True):
    entrada = sys.stdin.readline()
    linea = entrada.strip("\n")
    palabras = linea.split(" ")
    fila += 1
    posicion_final_palabra = 0

    i = 0
    while i < len(palabras):

        palabra = palabras[i]
        columna = linea.find(palabra) + 1

        if posicion_final_palabra > columna:
            columna = linea.find(palabra, posicion_final_palabra) + 1

        posicion_final_palabra = columna + len(palabra) - 1

        if len(palabra) == 0:
            i += 1
            continue

        if palabra[0] == '\'':
            i = len(palabras)
        elif not verificacion_palabra(palabra, fila, columna):
            if palabra[0] == '"':
                i = verificacion_string(i, palabras, fila, columna)
            else:
                verificacion_caracter(palabra, fila, columna)
        i += 1

    if entrada[len(entrada) - 1] != "\n":
        sys.exit()
