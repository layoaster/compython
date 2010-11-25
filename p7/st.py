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
from idclass import WrapCl

class SymbolTable:
    """Clase para la gestion de la tabla de simbolos"""

    def __init__(self):
        """ Descripción:
                El constructor inicializa la tabla de simbolos insertando
                las palabras reservadas y los identificadores estandar,
                haciendo uso de la clase Dictionary, que implementa una
                tabla hash. La clave de busqueda es una cadena de caracteres
                y el valor una lista de 2 elementos: 1 valor boolean que
                indica si la cadena es una palabra reservadas y 1 indice
                para los identificadores que se utilizara en sucesivas etapas
                del compilador. Las palabras reservadas no tienen indice,
                pero utilizamos ese espacio para almacenar su token_ID.
            Parametros:
                Ninguno

            Valor de retorno:
                Ninguno
	"""
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
        self.insert("integer", WrapCl.STANDARD_TYPE)
        self.insert("boolean", WrapCl.STANDARD_TYPE)
        self.insert("false", WrapCl.CONSTANT)
        self.insert("true", WrapCl.CONSTANT)
        self.insert("read", WrapCl.STANDARD_PROC)
        self.insert("write", WrapCl.STANDARD_PROC)

    def insert(self, lex, kind = None, reserved = False):
        """ Descripción:
                Inserta los identificadores en la tabla de simbolos que
                detecta el analizador lexico. Al no ser palabras reservadas,
                por defecto se toma False para el primer elemento del valor.
                Como indice se utiliza el valor actual de self._index, el cual
                se incrementa para dejarlo preparado para la siguiente entrada.

            Parametros:
                - lex: Cadena de caracteres que se inserta como identificador.
                - reserved: Boolean que indica si el identificador es una
                            palabra reservada o no. Por defecto, False.

            Valor de retorno:
                Ninguno
        """
        atributes = [reserved, self._index]
        self._table[lex] = atributes
        self._index += 1

    def isIn(self, lex):
        """ Descripción:
                Comprueba si una cadena de caracteres esta en la tabla.

            Parametros:
                - lex: Cadena de caracteres que se buscara.

            Valor de retorno:
                True si se encontro; False en caso contrario.
        """
        return lex in self._table

    def isReserved(self, lex):
        """ Descripción:
                Comprueba si una cadena de caracteres es palabra reservada.

            Parametros:
                - lex: Cadena de caracteres que se buscara.

            Valor de retorno:
                True si es palabra reservada; False en caso contrario.
        """
        try:
            return self._table[lex][0]
        except KeyError:
            return None

    def getIndex(self, lex):
        """ Descripción:
                Devuelve el indice asociado a una cadena de caracteres.
            Parametros:
                - lex: Cadena de caracteres que se buscara.

            Valor de retorno:
                Indice asociado a la cadena de caracteres.
        """
        try:
            return self._table[lex][1]
        except KeyError:
            return None
        except IndexError:
            return None

    def printTable(self):
        """ Descripción:
                Imprime la tabla de simbolos por pantalla a efectos de
                comprobacion. No forma parte del proceso de compilacion.
.
            Parametros:
                Ninguno.

            Valor de retorno:
                Nada.
        """

        for i in self._table:
            print i + "\t\t",
            for j in self._table[i]:
                print j, "\t",
            print ""

# Objeto de la clase SymbolTable que se utilizara como tabla de simbolos
# del compilador. El hecho de que se instancie en este modulo obedece a
# que debe estar accesible durante todo el proceso de compilacion, para
# que otras fases accedan y/o escriban en ella.
st = SymbolTable()
