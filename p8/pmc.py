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
import os
import argparse
from error import *
from parser import SynAn
from html import generateWebStats

if __name__ == '__main__':
    # Especificacion del parseado de argumentos por linea de comandos
    parser = argparse.ArgumentParser(description='Compilador (solo front-end) para Pascal-')
    parser.add_argument('fin', metavar='fich_texto.p', type=str, action='store', help='fichero de codigo fuente')
    parser.add_argument('-w', metavar='fich_stats.html', type=str, dest="wstats", help='genera fichero html con las estadisticas y el dumpeo de la TS')

    # Parametros insuficientes -> mostrar por pantalla el modo de uso
    if (len(sys.argv) < 2):
        parser.print_help()
    else:
        args = parser.parse_args()
        parser = SynAn()
        try:
            parser.start(args.fin)
            print Colors.OKGREEN + "All OK" + Colors.ENDC
        except Error as e:
            e.printError()
        except IOError as e:
            print Colors.WARNING + e.filename + Colors.FAIL + " [I/O ERROR] " + Colors.ENDC + e.strerror
            exit(2)


