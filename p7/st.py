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
from token import WrapTk
from idclass import WrapCl

class LocalSymbolTable:
    """Clase para la gestion de la tabla de simbolos"""

    def __init__(self):
        """ Descripción:
                Tabla de Simbolos Local que contiene solo los identificadores
                declarados en un determinado ambito (bloque). Implementada como
                tabla hash haciendo uso de los diccionarios.
            Atributos de Clase:
                _table = tabla hash
            Parametros:
                Ninguno
            Valor de retorno:
                Ninguno
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
                True : si se realizo la insercion
                False: en caso contrario
        """
        if not self.isIn(lex)
            self._table[lex] = attr
            return True
        else:
            return False

    def isIn(self, lex):
        """ Descripción: Determina si el identificador ya esta en la TSL.
            Parametros:
                lex: Lexema del identificador a buscar
            Valor de retorno:
                True: si se encontro;
                False: en caso contrario.
        """
        if lex in self._table
            return True
        else:
            return False



class SymbolTable:

    def __init__(self):
        self._blockstack = Stack()
        self._blocklevel = 0
        self._index = 0
        self._localst = LocalST()
        self.insert("NoName", kind=WrapCl.STANDARD_TYPE)
        self.insert("integer", kind=WrapCl.STANDARD_TYPE)
        self.insert("boolean", kind=WrapCl.STANDARD_TYPE)
        self.insert("false", kind=WrapCl.CONSTANT)
        self.insert("true", kind=WrapCl.CONSTANT)
        self.insert("read", kind=WrapCl.STANDARD_PROC)
        self.insert("write", kind=WrapCl.STANDARD_PROC)
        self.set(self._localst)
        }

    def set(self, localst):
        self._blockstack.push(localst)
        self._blocklevel += 1

    def reset(self):
        self._blockstack.pop()
        #if not self._blocktable.isEmpty():
        self._blocklevel -= 1

    def insert(self, lex, **attr):
        attr["index"] = self._index
        if self._localst.insert(self, lex, attr):
	    self._index += 1
        else:
            print "ERROR: identificador", lex, "repetido."

    def _search(self, lex):
        return self._localst.isIn(lex)

    def lookup(self, lex):
        if not search(self, lex):
            for self._blocklevel in range(self._blocklevel, -1, -1):
                if self._tablestack[self._blocklevel].search(lex):
                    self._blocklevel = len(self._tablestack - 1)
                    return True
        return False
