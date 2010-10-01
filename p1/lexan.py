#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
        $Id$
Description: Analizador Lexico para Pascal-.
    $Author$ Lionel Aster Mena Garcia, Alejandro Samarin Perez, Sergio Armas Perez
      $Date$
  $Revision$
"""

import sys
import string

class LexAn:
    """Clase General de Analizador Lexico"""
    __fin
    __nline
    __ncol
    __line

    def __init__(self):
    """
    """
        self.__nline = 1
        self.__ncol = 1
        self.__line = []

    def openFile(self, fin):
        error = False
        try:
            self.__fin = open(fin, "rU")
        except IOError:
            error = True
        return error

    def yyLex():


