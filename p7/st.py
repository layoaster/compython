#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
        $Id$
Description: Analizador Lexico para Pascal-.
    $Author$ Lionel Aster Mena Garcia, Alejandro Samarin Perez, Sergio Armas Perez
      $Date$
  $Revision$
"""

from stack import *
from error import *
from token import WrapTk
from idclass import WrapCl
from stats import *

class SymbolTable:

    def __init__(self):
        self._stats = STStats()
        self._blockstack = Stack()
        self._blocklevel = -1
        self._index = 0
        self.set()
        self.insert("NoName", kind=WrapCl.STANDARD_TYPE)
        self.insert("integer", kind=WrapCl.STANDARD_TYPE)
        self.insert("boolean", kind=WrapCl.STANDARD_TYPE)
        self.insert("false", kind=WrapCl.CONSTANT)
        self.insert("true", kind=WrapCl.CONSTANT)
        self.insert("read", kind=WrapCl.STANDARD_PROC)
        self.insert("write", kind=WrapCl.STANDARD_PROC)

    def set(self):
        localst = LocalSymbolTable()
        self._blockstack.push(localst)
        self._blocklevel += 1

    def reset(self):
        lst = self._blockstack.pop()
        # Comprobacion de indetificadores declarados pero no usados y estadisticas
        for i in lst.getIdentifiers():
            if (not lst.getAttr(i, "ref")) and (lst.getAttr(i, "kind") == WrapCl.VARIABLE):
                print "Identificador declarado, pero nunca usado:", lst.getAttr(i, "pos"), i
            if (lst.getAttr(i, "ref")) and (lst.getAttr(i, "kind") == WrapCl.VARIABLE):
                print "Identificador referenciado:", lst.getAttr(i, "pos"), i
                self._stats.addReferenced()
        self._blocklevel -= 1

    def insert(self, lex, **attr):
        attr["index"] = self._index
        if self._blockstack.top().insert(lex, attr):
            self._index += 1
            self._stats.incSize()
            if attr["kind"] == WrapCl.VARIABLE:
                self._stats.addDefined()
                print "Identificador declarado:", self._blockstack.top().getAttr(lex, "pos"), lex
            return True
        else:
            return False

    def _search(self, lex):
        return self._blockstack.top().isIn(lex)

    def lookup(self, lex):
        for i in range(self._blocklevel, -1, -1):
            if self._blockstack[i].isIn(lex):
                self._blockstack[i].setAttr(lex, "ref", True)
                return True
        self.insert(lex, kind=WrapCl.UNDEFINED)
        return False

    def printTable(self):
        for i in self._blockstack:
            print i

    def printStats(self):
        """ Imprime por la pantalla las estadisticas de la tabla de simbolos
        """
        print "Symbol Table Size:     ", self._stats.getSize()
        print "Declared identifiers:  ", self._stats.getDefined()
        print "Referenced identifiers:", self._stats.getReferenced()


class LocalSymbolTable:
    """Clase para la gestion de la tabla de simbolos Local"""

    def __init__(self):
        """ Descripción:
                Tabla de Simbolos Local que contiene solo los identificadores
                declarados en un determinado ambito (bloque). Implementada como
                tabla hash haciendo uso de los diccionarios.
            Atributos de Clase:
                _table = tabla hash
        """
        self._table = {}

    def insert(self, lex, attr):
        """ Descripción:
                Inserta los identificadores y sus atributos en la TSL, comprueba
                que el identificador no este en la tabla para poder insertarlo,
                en cas contrario notificara que ya estaba insertado,
            Parametros:
                - lex: Lexema del identificador que hara de clave primaria
                - attr: diccionario de atributos variable que acompañan al
                        identificador, los unicos atributos estaticos son el
                        "index" y el "kind"
            Valor de retorno:
                True : si se realizo la inercion
                False: en caso contrario
        """
        if not self.isIn(lex):
            if "ref" not in attr.keys():
                attr["ref"] = False
            self._table[lex] = attr
            return True
        else:
            if self._table[lex]["kind"] == WrapCl.FIELD:
                return True
            return False

    def isIn(self, lex):
        """ Descripción: Determina si el identificador ya esta en la TSL.
            Parametros:
                lex: Lexema del identificador a buscar
            Valor de retorno:
                True: si se encontro;
                False: en caso contrario.
        """
        if lex in self._table:
            return True
        else:
            return False


    def setAttr(self, lex, attr, value):
        """ Añade o redefine un atributo dado un valor
            Parametros:
                lex: identificador del que se desea añadir o redefinir un atributo
                attr: atributo a añadir o redefinir
                value: valor del atributo
        """
        self._table[lex][attr] = value

    def getAttr(self, lex, attr):
        """ Obtiene el atributo de un identificador en la tabla
            Parametros:
                lex: identificador del que se desea añadir o redefinir un atributo
                attr: atributo a obtener
        """
        return self._table[lex][attr]

    def getIdentifiers(self):
        """ Retorna la lista de identififcadores que contiene la tabla
        """
        return self._table.keys()

    def __str__(self):
        string = ""
        for i in self._table:
            string = string + i + " "
        return string