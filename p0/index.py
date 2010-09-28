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
import argparse


def readFile(dict, file, coding="iso-8859-1"):
    try:
        fin = open(file, mode='rU')
        print "Fichero abierto:" , file

        line_c = 1
        line = fin.readline().decode(coding)
        while line:
            if len(line) > 1:
                words = re.split('(?u)\W+', line.strip(string.punctuation + string.whitespace))
                dictAdd(dict, words, line_c)

            line_c = line_c + 1
            line = fin.readline().decode(coding)

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
        print "%-25s" % word,

        for num in dict[word]:
            print str(num) + ",",
        print ""

def writeFile(dict, file, coding="iso-8859-1"):
    """Escritura del diccionario a un archivo"""
    try:
        fout = open(file, mode='w')
        print "Escribiendo fichero:" , file

        sorted = dict.keys()
        sorted.sort()
        for word in sorted:
            fout.write(("%-25s" % word).encode(coding))
            for num in dict[word]:
                fout.write(str(num) + ", ")
            fout.write("\n")

        fout.close()
    except IOError:
        print "ERROR: No se pudo abrir el fichero."
        exit(-1)

def writeHTML(dict, file):
    """Escritura del diccionario a un archivo"""
    try:
        fout = open(file, "w")
        print "Escribiendo fichero HTML:" , file
        fout.write(html.head("Diccionario Online - " + fout.name) + html.body(dict) + html.tail())

        fout.close()
    except IOError:
        print "ERROR: No se pudo abrir el fichero."
        exit(-1)

parser = argparse.ArgumentParser(description='Procesa nombres de fichero.')
parser.add_argument('fin',  metavar='fichero_texto.in', type=str, action='store', help='nombre del fichero a indexar')
parser.add_argument('fout', metavar='fichero_diccionario.out', type=str, help='nombre del fichero que almacena el diccionario')
parser.add_argument('-w', metavar='fichero_web.html', type=str, dest="fweb", help='nombre del fichero html a crear')
parser.add_argument('-i', metavar='codificacion_entrada', type=str, default= "iso-8859-1", dest="codin", help='codificacion del fichero a indexar')

parser.add_argument('-o', metavar='codificacion_salida', type=str, default = "iso-8859-1", dest="codout", help='codificacion del fichero indice')

args = parser.parse_args()
print args


if (len(sys.argv) < 3):

    print "ERROR: No se indica el fichero de entrada y/o salida"
    print "USO: index.py texto.in diccionario.out"
    print "USO: index.py texto.in diccionario.out pagina.html"
else:
    dict = {}
    readFile(dict,  args.fin, args.codin)
    writeFile(dict, args.fout, args.codout)
    if (len(sys.argv) > 3):
        writeHTML(dict, args.fweb)


