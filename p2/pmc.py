#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
        $Id: parser.py 137 2010-10-13 17:07:37Z lionelmena@gmail.com $
Description: Analizador Lexico para Pascal-.
    $Author: lionelmena@gmail.com $ Lionel Aster Mena Garcia, Alejandro Samarin Perez, Sergio Armas Perez
      $Date: 2010-10-13 18:07:37 +0100 (mié 13 de oct de 2010) $
  $Revision: 137 $
"""

from lexan import LexAn
from token import *
from error import *
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
        print "ROW\tPOS\tTOKEN\t\t\tSYMBOL TABLE"
        print "---\t---\t-----\t\t\t------------"
        while tok.getToken() != WrapTk.ENDTEXT:
            # Imprimimos linea y posicion
            if scanner.getPos()[0] == cline:
                print "\t", scanner.getPos()[1],
            else:
                cline = scanner.getPos()[0]
                print cline, "\t", scanner.getPos()[1],

            # Imprimimos el tokenID y su valor, si es el caso
            print "\t<" + WrapTk.TokStrings[tok.getToken() - 1] + ",",
            print str(tok.getValue()) + ">",

            # Si es un identificador, mostramos su indice de la ST
            if (tok.getValue() != None and tok.getToken() != WrapTk.NUMERAL):
                print "\t\tST INDEX:", st.st.getIndex(tok.getValue()),
            try:
                tok = scanner.yyLex()
            except LexicalError as e:
                e._printError()
                tok = Token(WrapTk.TOKEN_ERROR)
            print ""

        print "--- ENDTEXT ---"
