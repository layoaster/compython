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
      
lineas = fichero.readlines()
num_linea = 1
for linea in lineas:
    print num_linea, linea[:-1] # (*)
    num_linea = num_linea + 1

fichero.close()
