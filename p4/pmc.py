#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
        $Id$
Description: Main del Analizador Sintáctico de Pascal-.
    $Author$ Lionel Aster Mena Garcia, Alejandro Samarin Perez, Sergio Armas Perez
      $Date$
  $Revision$
"""

import sys
import argparse
from error import *
from parser import SynAn
from html import generateStackTrace

def webTree(tree):
    """Crea el archivo html que genera el el Árbol de Análisis Sintático correspondiente al codigo fuente parseado
    """
    fout = open(tree, "w")
    fout.write(generatePHPSyntaxTree(args.fin, parser.getAST()))
    fout.close()

def stackTrace(trace):
    fout = open(trace, "w")
    fout.write(generateStackTrace(parser.getTokens(), parser.getTrace()))
    fout.close()

if __name__ == '__main__':
    # Especificacion del parseado de argumentos por linea de comandos
    parser = argparse.ArgumentParser(description='Realiza el Analisis Sintactico de ficheros de codigo fuente en Pascal-')
    parser.add_argument('fin', metavar='fich_texto.p', type=str, action='store', help='fichero de codigo fuente')
    parser.add_argument('-t', metavar='fich_trace.html', type=str, dest="trace", help='genera fichero html la traza')
    parser.add_argument('-v', action='store_true', dest="verbose", help='imprimir traza del analizador sintactico')
    parser.add_argument('-s', metavar='fich_stack.html', type=str, dest="stack", help='genera fichero html con la pila')

    # Parametros insuficientes -> mostrar por pantalla el modo de uso
    if (len(sys.argv) < 2):
        parser.print_help()
    else:
        args = parser.parse_args()

        parser = SynAn(args.verbose)
        try:
            parser.start(args.fin)
            print Colors.OKGREEN + "All OK" + Colors.ENDC
        except Error as e:
            e.printError();
            exit(1)
        except IOError as e:
            print Colors.WARNING + e.filename + Colors.FAIL + " [I/O ERROR] " + Colors.ENDC + e.strerror
            exit(2)
        finally:
            if args.trace:
                webTree(args.trace)
                print "\n" + Colors.OKBLUE + "[INFO]" + Colors.ENDC + " WebAST written to '" + args.tree + "'"
            if args.stack:
                stackTrace(args.stack)
                print "\n" + Colors.OKBLUE + "[INFO]" + Colors.ENDC + " Stack trace written to '" + args.stack + "'"

