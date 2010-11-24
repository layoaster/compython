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
from html import generateWebOutput

def webOutput(output):
    """Crea el archivo html que genera el Árbol de Análisis Sintático correspondiente al codigo fuente parseado
    """
    fin = open(args.fin, "rU")
    generateWebOutput(output, fin.readline(), parser.getAST()[0], parser.getAST()[2], args.fout)
    fin.close()

if __name__ == '__main__':
    # Especificacion del parseado de argumentos por linea de comandos
    argparser = argparse.ArgumentParser(description='Realiza la construccion de thompson de una expresion regular, generando a la salida una imagen o un fichero DOT')
    argparser.add_argument('fin', metavar='regex_file', type=str, action='store', help='fichero de expresion regular')
    argparser.add_argument('fout', metavar='output_file', type=str, action='store', nargs='?', help='fichero DOT | fichero de imagen (‘gif’, ‘jpe’, ‘jpeg’, ‘jpg’, ‘pdf’, ‘pic’, ‘png’, ‘ps’, ‘ps2’, ‘svg’, ‘svgz’, ‘wbmp’, ‘xdot’, ‘xlib’)')
    argparser.add_argument('-w', metavar='file.html', type=str, dest="web", help='genera fichero html con el AST de la expresion y su construccion de Thompson')

    # Parametros insuficientes -> mostrar por pantalla el modo de uso
    if (len(sys.argv) < 2):
        argparser.print_help()
    else:
        args = argparser.parse_args()
        parser = SynAn()
        try:
            parser.start(args.fin)
            print Colors.OKGREEN + "[ALL OK]" + Colors.ENDC + " Well-formed regular expression"
        except Error as e:
            e.printError()
            exit(1)
        except IOError as e:
            print Colors.WARNING + e.filename + Colors.FAIL + " [I/O ERROR] " + Colors.ENDC + e.strerror
            exit(2)

        if args.fout:
            tc = ThompsonConstruction(parser.getASTSequence())
            tc.createGraph()
            if args.fout.partition('.')[2] == "dot":
                tc.writeDOT(args.fout)
                print Colors.OKBLUE + "[INFO]" + Colors.ENDC + " DOT file written to '" + args.fout + "'"
            else:
                tc.drawGraph(args.fout)
                print Colors.OKBLUE + "[INFO]" + Colors.ENDC + " Thompson Construction graph written to '" + args.fout + "'"

        if args.web and args.fout:
            webOutput(args.web)
            print Colors.OKBLUE + "[INFO]" + Colors.ENDC + " WebThompson written to '" + args.web + "'"
