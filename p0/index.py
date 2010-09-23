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

if (len(sys.argv) != 3):
    print "ERROR: No se indica el fichero de entrada y/o salida"
    print "USO: index.py texto.in diccionario.out"
else:
    try:
        fin = open(sys.argv[1], "r")
        print "Fichero abierto:" , sys.argv[1]

        eof = True
        while eof:
            line = fin.readline()
            if line:
                print line
            else:
                eof = False

        fin.close()
    except IOError:
        print "ERROR: No se pudo abrir el fichero."
        exit()

