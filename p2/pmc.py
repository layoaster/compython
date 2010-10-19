#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
        $Id$
Description: Main del Analizador Sintactico de Pascal-.
    $Author$ Lionel Aster Mena Garcia, Alejandro Samarin Perez, Sergio Armas Perez
      $Date$
  $Revision$
"""

import sys
import argparse
from error import *
from parser import SynAn
from html import generatePHPSyntaxTree

def webTree():
    fout = open("webtree.html", "w")
    fout.write(generatePHPSyntaxTree(args.fin, parser.getAST()[:-8] + "]"))

if __name__ == '__main__':
    # Especificacion del parseado de argumentos por linea de comandos
    parser = argparse.ArgumentParser(description='Indexa las palabras de un texto y genera un indice en texto plano y/o en html.')
    parser.add_argument('fin',  metavar='fich_texto.pas', type=str, action='store', help='fichero de codigo fuente')

    # Parametros insuficientes -> mostrar por pantalla el modo de uso
    if (len(sys.argv) != 2):
        parser.print_help()
    else:
        args = parser.parse_args()

        parser = SynAn()
        try:
            parser.start(args.fin)
        except LexicalError as e:
            e._printError();
            print "I/O failure"
            exit()

        print "All Ok."
        webTree()
