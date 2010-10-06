#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
        $Id$
Description: Analizador Lexico para Pascal-.
    $Author$ Lionel Aster Mena Garcia, Alejandro Samarin Perez, Sergio Armas Perez
      $Date$
  $Revision$
"""

from lexan import LexAn
from token import WrapTk
import st
import sys
import argparse

if __name__ == '__main__':
    # Especificacion del parseado de argumentos por linea de comandos
    parser = argparse.ArgumentParser(description='Indexa las palabras de un texto y genera un indice en texto plano y/o en html.')
    parser.add_argument('fin',  metavar='fich_texto.pas', type=str, action='store', help='fichero de codigo fuente')

    # Parametros insuficientes -> mostrar por pantalla el modo de uso
    if (len(sys.argv) != 2):
        parser.print_help()
    else:
        args = parser.parse_args()

        scanner = LexAn()
        scanner.openFile(args.fin)
        tok = scanner.yyLex()
        cline = 0
        while tok.getToken() != WrapTk.ENDTEXT[0]:
            if scanner.getPos()[0] == cline:
                print "  ", scanner.getPos()[1],
            else:
                cline = scanner.getPos()[0]
                print cline, scanner.getPos()[1],
            
            print "<" + str(tok.getToken()) + ",", str(tok.getValue()) + ">",
            
            # Si es un identificador, mostramos su indice de la ST
            if (tok.getValue() != None and tok.getToken() != WrapTk.NUMERAL[0]):
                print "ST INDEX:", st.st.getIndex(tok.getValue()),
            tok = scanner.yyLex()
            print ""

        print "-- ENDTEXT --"
