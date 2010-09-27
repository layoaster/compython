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
import re


def dictAdd(dict, words, act_line):
    """Añade las palabras de una linea al diccionario"""
    for wd in words:
        if not wd.isdigit():
            if (wd in dict):
                numl = dict[wd]
                if act_line not in numl:
                    numl.append(act_line)
            else:
                dict[wd] = [act_line]


def dictWrite(dict, fout):
    """Listado del diccionario en orden alfabetico"""
    sorted = dict.keys()
    sorted.sort()

    for word in sorted:
        #print '{0:20}'.format(word), dict[word]
        print word, "\t\t\t\t",dict[word]

if (len(sys.argv) != 3):
    print "ERROR: No se indica el fichero de entrada y/o salida"
    print "USO: index.py texto.in diccionario.out"
else:
    try:
        fin = open(sys.argv[1], "r")
        print "Fichero abierto:" , sys.argv[1]

        dict = {}
        line_c = 1
        line = fin.readline()
        while line:
            if len(line) > 1:
                words = re.split('\W+', line.strip(string.punctuation + string.whitespace), re.UNICODE)
                dictAdd(dict, words, line_c)

            line_c = line_c + 1
            line = fin.readline()
        fin.close()

        dictWrite(dict, sys.argv[2])
    except IOError:
        print "ERROR: No se pudo abrir el fichero."
        exit()

