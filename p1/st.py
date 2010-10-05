#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
        $Id$
Description: Analizador Lexico para Pascal-.
    $Author$ Lionel Aster Mena Garcia, Alejandro Samarin Perez, Sergio Armas Perez
      $Date$
  $Revision$
"""

from token import WrapTk

class SymbolTable:
    """Clase para la gestion de la tabla de simbolos"""
    def __init__(self):
        self._table = {}
        self._index = 1
        # Insertamos las palabras reservadas
        self._table["and"] = [True, WrapTk.AND]
        self._table["array"] = [True, WrapTk.ARRAY]
        self._table["begin"] = [True, WrapTk.BEGIN]
        self._table["const"] = [True, WrapTk.CONST]
        self._table["div"] = [True, WrapTk.DIV]
        self._table["do"] = [True, WrapTk.DO]
        self._table["else"] = [True, WrapTk.ELSE]
        self._table["end"] = [True, WrapTk.END]
        self._table["if"] = [True, WrapTk.IF]
        self._table["mod"] = [True, WrapTk.MOD]
        self._table["not"] = [True, WrapTk.NOT]
        self._table["of"] = [True, WrapTk.OF]
        self._table["or"] = [True, WrapTk.OR]
        self._table["procedure"] = [True, WrapTk.PROCEDURE]
        self._table["program"] = [True, WrapTk.PROGRAM]
        self._table["record"] = [True, WrapTk.RECORD]
        self._table["then"] = [True, WrapTk.THEN]
        self._table["type"] = [True, WrapTk.TYPE]
        self._table["var"] = [True, WrapTk.VAR]
        self._table["while"] = [True, WrapTk.WHILE]
        # Insertamos los identificadores estandar
        self.insert("integer")
        self.insert("boolean")
        self.insert("false")
        self.insert("true")
        self.insert("read")
        self.insert("write")

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

    def printTable(self):
        for i in self._table:
            print i + "\t\t",
            for j in self._table[i]:
                print j, "\t",
            print ""

st = SymbolTable()
