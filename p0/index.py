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
    """ Descripcion:
            Lectura del fichero de entrada introducido por linea de comandos; lee linea a linea
            y separa las palabras clave utilizando una expresion regular
        
        Parametros:
            - dict: Diccionario donde se cargara el indice del fichero
            - file: Ruta del fichero a leer
            - coding: Codificacion de los caracteres de 'file'; por defecto se considera Unicode
    
        Valor de retorno:
            Nada (sale del programa en caso de que haya ocurrido un error de lectura del fichero)
    """
    try:
        fin = open(file, mode='rU')
        print "Fichero abierto:" , file

        line_count = 1
        line = " "
        while line:
            line = fin.readline().decode(coding)
            if len(line) > 1:
                words = re.split('(?u)\W+', line.strip(string.punctuation + string.whitespace))
                dictAdd(dict, words, line_count)

            line_count += 1

        fin.close()
    except IOError:
        print "ERROR: No se pudo abrir el fichero."
        exit(-1)

def writeFile(dict, file, coding = "utf-8"):
    """ Descripcion:
            Escritura en texto plano del indice generado a partir del fichero de entrada
        
        Parametros:
            - dict: Diccionario donde se encuentra el indice del fichero
            - file: Ruta del fichero a volcar el contenido del diccionario
            - coding: Codificacion de los caracteres de 'file'; por defecto se considera Unicode
    
        Valor de retorno:
            Nada (sale del programa en caso de que haya ocurrido un error de escritura del fichero)
    """
    try:
        fout = open(file, mode='w')
        print "Escribiendo fichero:" , file

        sorted = dict.keys()
        sorted.sort()
        for word in sorted:
            # Formato de salida del fichero y codificacion deseada
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
    """ Descripcion:
            Escribe en un fichero HTML el indice generado a partir del fichero de entrada,
            utilizando HTML estandar + hoja de estilos CSS
        
        Parametros:
            - dict: Diccionario donde se encuentra el indice del fichero
            - file: Ruta del fichero HTML a volcar el contenido del diccionario
            - coding: Codificacion de los caracteres de 'file'; por defecto se considera Unicode
    
        Valor de retorno:
            Nada (sale del programa en caso de que haya ocurrido un error de escritura del fichero)
    """
    try:
        fout = open(file, "w")
        print "Escribiendo fichero HTML:" , file
        fout.write(unicode(html.head("Diccionario Online - " + fout.name, coding) + html.body(dict) + html.tail()).encode(coding))

        fout.close()
    except IOError:
        print "ERROR: No se pudo abrir el fichero."
        exit(-1)

def dictAdd(dict, words, act_line):
    """ Descripcion:
            Anyade las palabras de una linea al diccionario junto con su numero de linea correspondiente
        
        Parametros:
            - dict: Diccionario donde se encuentra el indice del fichero
            - words: Lista de palabras de una linea
            - act_line: Numero de la linea a procesar
        
        Valor de retorno:
            Nada 
    """
    for wd in words:
        # Comprobar que la palabra actual no sea un numero y que tampoco sea vacia (casos especiales que el parseado previo no detecto)
        if not wd.isdigit() and not wd == '':
            # Eliminar sensibilidad a capitalizacion
            wd = wd.lower()
            if (wd in dict):
                if act_line not in dict[wd]:
                    dict[wd].append(act_line)
            else:
                dict[wd] = [act_line]


def dictPrint(dict):
    """ Descripcion:
            Imprime el contenido del diccionario por pantalla
        
        Parametros:
            - dict: Diccionario donde se encuentra el indice del fichero

        Valor de retorno:
            Nada 
    """
    sorted = dict.keys()
    sorted.sort()
    for word in sorted:
        # Formato de salida: columna de 25 caracteres para la palabra, alineacion a la izquierda
        print "%-25s" % word,

        for num in dict[word]:
            # Evitar imprimir una coma despues del ultumo numero de linea
            if dict[word].index(num) != len(dict[word]) - 1:
                print str(num) + ",",
            else:
                print str(num)


# --- Programa Principal ---

if __name__ == '__main__':
    # Especificacion del parseado de argumentos por linea de comandos
    parser = argparse.ArgumentParser(description='Indexa las palabras de un texto y genera un indice en texto plano y/o en html.')
    parser.add_argument('fin',  metavar='fich_texto.in', type=str, action='store', help='nombre del fichero a indexar')
    parser.add_argument('fout', metavar='fich_dicc.out', type=str, help='nombre del fichero que almacena el diccionario')
    parser.add_argument('-w', metavar='fich_web.html', type=str, dest="fweb", help='nombre del fichero html a crear')
    parser.add_argument('-i', metavar='cod_entrada', type=str, default= "utf-8", dest="codin", help='codificacion del fichero a indexar')
    parser.add_argument('-o', metavar='cod_salida', type=str, default = "utf-8", dest="codout", help='codificacion del fichero indice')
    parser.add_argument('-p', action='store_true', dest="print_screen", help='imprimir por pantalla el indice generado')

    # Parametros insuficientes -> mostrar por pantalla el modo de uso
    if (len(sys.argv) < 3):
        parser.print_help()
    else:
        args = parser.parse_args()
    dictPrint(dict)

        dict = {}   # Creacion del indice
        readFile(dict, args.fin, args.codin)
        if args.print_screen:   # Si se especifico el flag '-p'
            dictPrint(dict)
        writeFile(dict, args.fout, args.codout)
        if args.fweb:           # Si se especifico el flag '-w'
            writeHTML(dict, args.fweb, args.codout)

