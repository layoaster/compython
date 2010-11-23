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
from tc import *
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
    argparser.add_argument('fin', metavar='regex_file', type=str, action='store', help='fichero de expresion regular')
    argparser.add_argument('fout', metavar='image_file', type=str, action='store', help='fichero de imagen')
    argparser.add_argument('-t', action='store_true', dest="format", help='imprime el recorrido del AST resultante en pre, in y post orden')

    # Parametros insuficientes -> mostrar por pantalla el modo de uso
    if (len(sys.argv) < 3):
        argparser.print_help()
    else:
        args = argparser.parse_args()
        parser = SynAn()
        try:
            parser.start(args.fin)
            print Colors.OKGREEN + "All OK" + Colors.ENDC
        except Error as e:
            e.printError()
            exit(1)
        except IOError as e:
            print Colors.WARNING + e.filename + Colors.FAIL + " [I/O ERROR] " + Colors.ENDC + e.strerror
            exit(2)
        finally:
            tc = ThompsonConstruction(parser.getASTSequence())
            tc.createGraph()
            tc.drawGraph(args.fout)
