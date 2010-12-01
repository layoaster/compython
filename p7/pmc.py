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
#import traceback
from error import *
from parser import SynAn
from html import generatePHPSyntaxTree

def webTree(tree):
    """Crea el archivo html que genera el el Árbol de Análisis Sintático correspondiente al codigo fuente parseado
    """
    fout = open(tree, "w")
    fout.write(generatePHPSyntaxTree(args.fin, parser.getAST()))
    fout.close()

if __name__ == '__main__':
    # Especificacion del parseado de argumentos por linea de comandos
    parser = argparse.ArgumentParser(description='Compilador (solo front-end) para Pascal-')
    parser.add_argument('fin', metavar='fich_texto.p', type=str, action='store', help='fichero de codigo fuente')
    parser.add_argument('-w', metavar='fich_tree.html', type=str, dest="webstats", help='genera fichero html con las estadisticas y el dumpeo de la TS')
    parser.add_argument('-s', action='store_true', dest="stats", help='imprimir estadisticas de la tabla de simbolos del compilador')

    # Parametros insuficientes -> mostrar por pantalla el modo de uso
    if (len(sys.argv) < 2):
        parser.print_help()
    else:
        args = parser.parse_args()
        parser = SynAn(args.stats)
        try:
            parser.start(args.fin)
            print Colors.OKGREEN + "All OK" + Colors.ENDC
        except Error as e:
            e.printError()
        except IOError as e:
            print Colors.WARNING + e.filename + Colors.FAIL + " [I/O ERROR] " + Colors.ENDC + e.strerror
            exit(2)
        finally:
            if args.webstats:
                parser.dumpGnuPlot()
                #webTree(args.tree)
                #print "\n" + Colors.OKBLUE + "[INFO]" + Colors.ENDC + " WebAST written to '" + args.tree + "'"


