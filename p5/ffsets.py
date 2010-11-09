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

        self._ffs["expr"]   = (WrapTk.LEFTPARENTHESIS, WrapTk.MINUS, WrapTk.ID, WrapTk.NUMERAL)

        self._ffs["expr2"]  = (WrapTk.PLUS, WrapTk.MINUS)

        self._ffs["term"]   = (WrapTk.LEFTPARENTHESIS, WrapTk.MINUS, WrapTk.ID, WrapTk.NUMERAL)

        self._ffs["term2"]  = (WrapTk.ASTERISK, WrapTk.SLASH)

        self._ffs["factor"] = (WrapTk.LEFTPARENTHESIS, WrapTk.MINUS, WrapTk.ID, WrapTk.NUMERAL)

    def first(self, noterm):
        """ Devuelve el conjunto FIRST de un simbolo no terminal de la gramatica
        """
        self._tkset = frozenset(self._ffs[noterm])
        return self._tkset
