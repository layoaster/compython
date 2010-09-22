import sys

if (len(sys.argv) != 2):
    print "Uso: prueba.py + nombre_fichero"
else:
    try:
        fichero = open(sys.argv[1], "r")
        print "Abriendo " + sys.argv[1]
    except IOError:
        print "ERROR: No se pudo abrir el fichero."
        exit()

# readlines devuelve un array con todas las lineas del fichero
# incluyendo el caracter de salto de linea. Aun no se si existe
# alguna funcion para devolver el indice del array (supongo que no)
        
lineas = fichero.readlines()
num_linea = 1
for linea in lineas:
    print num_linea, linea[:-1] # (*)
    num_linea = num_linea + 1

fichero.close()

# (*) linea[:-1] equivale a linea[0:-1] y muestra el array desde
# desde la posicion inicial hasta una menos de la final donde
# esta el caracter de salto de linea. Si se quita, dejando unicamente
# unicamente lista, lista[:] o lista[::] (todo es lo mismo), tambien
# se imprime el salto de linea, aparte del que pone la funcion print,
# quedando una linea en blanco entre cada linea del fichero de entrada.
# Problema: si al final no hay un salto de linea, se come el ultimo caracter.
