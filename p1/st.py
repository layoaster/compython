#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
        $Id$
Description: Analizador Lexico para Pascal-.
    $Author$ Lionel Aster Mena Garcia, Alejandro Samarin Perez, Sergio Armas Perez
      $Date$
  $Revision$
"""

class SymbolTable:
    """Clase para la gestion de la tabla de simbolos"""
    def __init__(self):
        self._table = {}
        self._index = 1
        # Insertamos las palabras reservadas
        self._table["and"] = [True]
        self._table["array"] = [True]
        self._table["begin"] = [True]
        self._table["const"] = [True]
        self._table["div"] = [True]
        self._table["do"] = [True]
        self._table["else"] = [True]
        self._table["end"] = [True]
        self._table["if"] = [True]
        self._table["mod"] = [True]
        self._table["not"] = [True]
        self._table["of"] = [True]
        self._table["or"] = [True]
        self._table["procedure"] = [True]
        self._table["program"] = [True]
        self._table["record"] = [True]
        self._table["then"] = [True]
        self._table["type"] = [True]
        self._table["var"] = [True]
        self._table["while"] = [True]
        # Insertamos los identificadores estandar
        self.insertST("integer")
        self.insertST("boolean")
        self.insertST("false")
        self.insertST("true")
        self.insertST("read")
        self.insertST("write")

    def insert(self, lex, reserved = False):
        atributes = [reserved, self._index]
        self._table[lex] = atributes
        self._index += 1

    def isIn(self, lex):
        return self._table.has_key(lex)

    def isReserved(self, lex):
        try:
            return self._table[lex][0]
        except KeyError:
            return None

    def getIndex(self, lex):
        try:
            return self._table[lex][1]
        except KeyError:
            return None
        except IndexError:
            return None

    def print(self):
        for i in self._table:
            print i + "\t\t",
            for j in self._table[i]:
                print j, "\t",
            print ""
