#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
        $Id$
Description: Analizador Lexico para Pascal-.
    $Author$ Lionel Aster Mena Garcia, Alejandro Samarin Perez, Sergio Armas Perez
      $Date$
  $Revision$
"""

class STStats:

    def __init__(self):
        """ Inicializa las estadisticas
            Atributos:
                _stsize = tamaño maximo que alcanzo la tabla de simbolos
                _defid = numero de identificadores declarados
                _refid = numero de identificadores que se han referenciado alguna vez en el programa
                _refids = almacena el numero de referencias que tiene un identificador, distinguiendo ambitos
        """
        self._stsize = 0
        self._defid = 0
        self._refid = 0
        self._totalref = {}

    def setSize(self, size):
        """ Establece el tamaño maximo de la tabla de simbolos
        """
        self._stsize = size

    def addDefined(self):
        """ Incrementa contador de identificadores definidos
        """
        self._defid += 1

    def addReferenced(self):
        """ Incrementa contador de identificadores referenciados alguna vez
        """
        self._refid += 1

    def addIdReference(self, lex, scopename):
        """ Incrementa el contador de las referencias a un identificador
            Parametros:
                lex: identificador a contar
        """
        if scopename not in self._totalref.keys():
            tmp = [[lex, 1]]
            self._totalref[scopename] = tmp
        else:
            flag = False
            tmp = self._totalref[scopename]
            for i in tmp:
                if i[0] == lex:
                    i[1] += 1
                    flag = True
            if not flag:
                tmp.append([lex, 1])
            self._totalref[scopename] = tmp

    def getSize(self):
        """ Obtiene el tamaño maximo de la tabla de simbolos
        """
        return self._stsize

    def getDefined(self):
        """ Obtiene el numero de identificadores definidos
        """
        return self._defid

    def getReferenced(self):
        """ Obtiene el numero de identificadores referenciados alguna vez
        """
        return self._refid

    def dumpGnuPlot(self, basedir='./stats/', outimg='img.png', plotfile='symbols.plot'):
        """ Genera un fichero de sentencias en formato GNUPlot para crear un fichero svg con la informacion
            de los identificadores del programa, con estadisticas sobre el numero de referencias que tiene
            cada uno, diferenciando ademas los distintos ambitos en los que se producen dichas referencias
        """
#""" + str(self._defid) + """]
        count = 1
        sentences = """
set xrange [0:*] 
set yrange [0:*]
set boxwidth 0.6 
set xlabel "Identifiers"
set ylabel "References"
set term png size 800,600
set out '""" + str(outimg) + """'
set xtics rotate by -45
set xtics ("""
        for ambito in self._totalref.keys():
            try:
                file = open(basedir + ambito + ".data", "w")
                for id in self._totalref[ambito]:
                    sentences += "\"" + id[0] + "\"" + "  " + str(count) + ","
                    file.write(str(count) + "  " + str(id[1]) + "\n")
                    count += 1
                file.close()
            except IOError:
                raise

        count = 1
        sentences = sentences[:-1]  # Quitar ultima coma de los xtics
        sentences += """)
plot """
        for ambito in self._totalref.keys():
            sentences += "'" + basedir + ambito + ".data" + """' using 1:2 with boxes fs solid 0.6 title '""" + ambito + """' lt """ + str(count) + ","
            count += 1

        sentences = sentences[:-1] # Quitar ultima coma del plot
        try:
            file = open(plotfile, "w")
            file.write(sentences)
        except IOError:
            raise

    def prueba(self):
        for lex in self._totalref.keys():
            print "Ambito:", lex
            for ref in self._totalref[lex]:
                print ref[0], "-", ref[1]


