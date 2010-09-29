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


def readFile(dict, file, coding = "utf-8"):
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

def writeFile(dict, file, coding = "utf-8"):
    """Escritura del diccionario a un archivo"""
    try:
        fout = open(file, mode='w')
        print "Escribiendo fichero:" , file

        sorted = dict.keys()
        sorted.sort()
        for word in sorted:
            fout.write(("%-25s" % word).encode(coding))
            for num in dict[word]:
                fout.write(str(num))
                if dict[word].index(num) != len(dict[word]) - 1:
                    fout.write(", ")
            fout.write("\n")
        fout.close()
    except IOError:
        print "ERROR: No se pudo abrir el fichero."
        exit(-1)

def writeHTML(dict, file, coding = "utf-8"):
    """Escritura del diccionario a un archivo"""
    try:
        fout = open(file, "w")
        print "Escribiendo fichero HTML:" , file
        fout.write(unicode(html.head("Diccionario Online - " + fout.name, coding) + html.body(dict) + html.tail()).encode(coding))

        fout.close()
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
            if dict[word].index(num) != len(dict[word]) - 1:
                print str(num) + ",",
            else:
                print str(num)


#Programa Principal
parser = argparse.ArgumentParser(description='Indexa las palabras de un texto y genera un indice en texto plano y/o en html.')
parser.add_argument('fin',  metavar='fich_texto.in', type=str, action='store', help='nombre del fichero a indexar')
parser.add_argument('fout', metavar='fich_dicc.out', type=str, help='nombre del fichero que almacena el diccionario')
parser.add_argument('-w', metavar='fich_web.html', type=str, dest="fweb", help='nombre del fichero html a crear')
parser.add_argument('-i', metavar='cod_entrada', type=str, default= "utf-8", dest="codin", help='codificacion del fichero a indexar')
parser.add_argument('-o', metavar='cod_salida', type=str, default = "utf-8", dest="codout", help='codificacion del fichero indice')
parser.add_argument('-p', action='store_true', dest="print_screen", help='imprimir por pantalla el indice generado')

if (len(sys.argv) < 3):
    parser.print_help()
else:
    args = parser.parse_args()

    dict = {}
    readFile(dict,  args.fin, args.codin)
    if args.print_screen:
        dictPrint(dict)
    writeFile(dict, args.fout, args.codout)
    if args.fweb:
        writeHTML(dict, args.fweb, args.codout)


