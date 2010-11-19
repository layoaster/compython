#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
        $Id$
Description: Compilador del legunaje de expresiones aritmeticas (+, -, *, /, - (unario)) parentizadas.
    $Author$ Lionel Aster Mena Garcia, Alejandro Samarin Perez, Sergio Armas Perez
      $Date$
  $Revision$
"""

import sys
import argparse
from error import *
from parser import SynAn
#from html import generatePHPSyntaxTree

def webTree(tree):
    """Crea el archivo html que genera el Árbol de Análisis Sintático correspondiente al codigo fuente parseado
    """
    fout = open(tree, "w")
    fout.write(generatePHPSyntaxTree(args.fin, parser.getAST()[0], parser.getAST()[1], parser.getDPT()))
    fout.close()

if __name__ == '__main__':
    # Especificacion del parseado de argumentos por linea de comandos
    argparser = argparse.ArgumentParser(description='Realiza el Analisis Sintactico de ficheros de codigo fuente en Pascal-')
    argparser.add_argument('fin', metavar='fich_texto.p', type=str, action='store', help='fichero de codigo fuente')
    argparser.add_argument('-w', metavar='fich_tree.html', type=str, dest="tree", help='genera fichero html con el AAS del codigo fuente')
    argparser.add_argument('-t', action='store_true', dest="traverse", help='imprime el recorrido del AST resultante en pre, in y post orden')
    argparser.add_argument('-r', action='store_true', dest="result", help='muestra el resultado de evaluar una expresion que no contenga identificadores')

    # Parametros insuficientes -> mostrar por pantalla el modo de uso
    if (len(sys.argv) < 2):
        argparser.print_help()
    else:
        args = argparser.parse_args()

        parser = SynAn()
        error = None
        try:
            error = parser.start(args.fin)
            if not isinstance(error, Error):
                print Colors.OKGREEN + "All OK" + Colors.ENDC
        except IOError as e:
            error = e
            print Colors.WARNING + e.filename + Colors.FAIL + " [I/O ERROR] " + Colors.ENDC + e.strerror
            exit(2)
        finally:
            if not error:
                if args.tree:
                    webTree(args.tree)
                    print "\n" + Colors.OKBLUE + "[INFO]" + Colors.ENDC + " WebAST written to '" + args.tree + "'"
                if args.traverse:
                    parser.printAST()
                if args.result:
                    print "Resultado: ", parser.getResult()
