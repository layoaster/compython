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
        if lex not in self._totalref.keys():
            tmp = [[scopename, 1]]
            self._totalref[lex] = tmp
        else:
            flag = False
            tmp = self._totalref[lex]
            for i in tmp:
                if i[0] == scopename:
                    i[1] += 1
                    flag = True
            if not flag:
                tmp.append([scopename, 1])
            self._totalref[lex] = tmp

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

    def prueba(self):
        for lex in self._totalref.keys():
            print "ID:", lex
            for ref in self._totalref[lex]:
                print ref[0], "-", ref[1]


