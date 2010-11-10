#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
        $Id$
Description: Clase que almacena first y follow de cada uno de los simbolos no terminales de la gramatica de Pascal-
    $Author$ Lionel Aster Mena Garcia, Alejandro Samarin Perez, Sergio Armas Perez
      $Date$
  $Revision$
"""

from token import *

class FFSets:

    def __init__(self):
        self._ffs = {}

        self._ffs["expr"]   = ((WrapTk.LEFTPARENTHESIS, WrapTk.MINUS, WrapTk.ID, WrapTk.NUMERAL),
                               (WrapTk.ENDTEXT, WrapTk.RIGHTPARENTHESIS))

        self._ffs["expr2"]  = ((WrapTk.PLUS, WrapTk.MINUS),
                               (WrapTk.ENDTEXT, WrapTk.RIGHTPARENTHESIS))

        self._ffs["term"]   = ((WrapTk.LEFTPARENTHESIS, WrapTk.MINUS, WrapTk.ID, WrapTk.NUMERAL),
                               (WrapTk.PLUS, WrapTk.MINUS, WrapTk.ENDTEXT, WrapTk.RIGHTPARENTHESIS))

        self._ffs["term2"]  = ((WrapTk.ASTERISK, WrapTk.SLASH),
                               (WrapTk.PLUS, WrapTk.MINUS, WrapTk.ENDTEXT, WrapTk.RIGHTPARENTHESIS))

        self._ffs["factor"] = ((WrapTk.LEFTPARENTHESIS, WrapTk.MINUS, WrapTk.ID, WrapTk.NUMERAL),
                               (WrapTk.ASTERISK, WrapTk.SLASH, WrapTk.PLUS, WrapTk.MINUS, WrapTk.ENDTEXT, WrapTk.RIGHTPARENTHESIS))

    def first(self, noterm):
        """ Devuelve el conjunto FIRST de un simbolo no terminal de la gramatica
        """
        self._tkset = frozenset(self._ffs[noterm][0])
        return self._tkset

    def follow(self, noterm):
        """ Devuelve el conjunto FOLLOW de un simbolo no terminal de la gramatica
        """
        self._tkset = frozenset(self._ffs[noterm][1])
        return self._tkset