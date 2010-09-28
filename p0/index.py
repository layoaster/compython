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
import html
import codecs

def readFile(dict, file):
    try:
        fin = open(file, "rU")
        print "Fichero abierto:" , file

        line_c = 1
        line = fin.readline()
        while line:
            if len(line) > 1:
                words = re.split('\W+', line.strip(string.punctuation + string.whitespace), re.UNICODE)
                dictAdd(dict, words, line_c)

            line_c = line_c + 1
            line = fin.readline()
        fin.close()

    except IOError:
        print "ERROR: No se pudo abrir el fichero."
        exit(-1)

def dictAdd(dict, words, act_line):
    """Añade las palabras de una linea al diccionario"""
    for wd in words:
        if not wd.isdigit() and not wd == '':
            wd = wd.lower()
            if (wd in dict):
                if act_line not in dict[wd]:
                    dict[wd].append(act_line)
            else:
                dict[wd] = [act_line]


def dictPrint(dict):
    """Listado del diccionario por pantalla"""
    sorted = dict.keys()
    sorted.sort()
    for word in sorted:
        #print '{0:20}'.format(word), dict[word]
        print "%-25s" % word,

        for num in dict[word]:
            print str(num) + ",",
        print ""

def writeFile(dict, file):
    """Escritura del diccionario a un archivo"""
    try:
        fout = open(file, "w")
        print "Escribiendo fichero:" , file

        sorted = dict.keys()
        sorted.sort()
        for word in sorted:
            fout.write("%-25s" % word)
            for num in dict[word]:
                fout.write(str(num) + ", ")
            fout.write("\n")

    except IOError:
        print "ERROR: No se pudo abrir el fichero."
        exit(-1)

def writeHTML(dict, file):
    """Escritura del diccionario a un archivo"""
    try:
        fout = open(file, "w")
        print "Escribiendo fichero HTML:" , file
        fout.write(html.head() + html.body(dict) + html.tail())

    except IOError:
        print "ERROR: No se pudo abrir el fichero."
        exit(-1)

if (len(sys.argv) < 3):
    print "ERROR: No se indica el fichero de entrada y/o salida"
    print "USO: index.py texto.in diccionario.out"
    print "USO: index.py texto.in diccionario.out pagina.html"
else:
    dict = {}
    readFile(dict, sys.argv[1])
    #dictPrint(dict)
    writeFile(dict, sys.argv[2])
    if (len(sys.argv) == 4)
        writeHTML(dict, sys.argv[3])

