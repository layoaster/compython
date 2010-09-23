#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
        $Id$
Description: Programa que crea un indice de palabras para un texto.
    $Author$ Lionel Aster Mena Garcia, Alejandro Samarin Perez, Sergio Armas Perez
      $Date$
  $Revision$
"""

import sys
import string

"""Limpia la linea de signos de puntuacion y devuelve en una lista
   las palabras que contiene la linea"""
def lclean(line):
    if sys.version_info < (2, 6):
        table = ''.join(chr(i) for i in xrange(256))
    else:
        table = None

    line = line.translate(table, string.punctuation)
    print line
    words = line.split()

    return words

if (len(sys.argv) != 3):
    print "ERROR: No se indica el fichero de entrada y/o salida"
    print "USO: index.py texto.in diccionario.out"
else:
    try:
        fin = open(sys.argv[1], "r")
        print "Fichero abierto:" , sys.argv[1]

        eof = True
        line_c = 1
        while eof:
            line = fin.readline()
            if line:
                print lclean(line)

                line_c = line_c + 1;
            else:
                eof = False

        fin.close()
    except IOError:
        print "ERROR: No se pudo abrir el fichero."
        exit()

