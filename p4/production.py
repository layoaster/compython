#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
$Id$
Description: Representacion de la parte derecha de una producción gramatical.
$Author$ Lionel Aster Mena Garcia, Alejandro Samarin Perez, Sergio Armas Perez
$Date$
$Revision$
"""

class Production:

    def __init__(self, string = None):
        """ Constructor de la clase
            _rule = secuencia de simbolos terminales y no terminales que forma la parte derecha de una producción.
        """
        self._rule = string

    def setProd(self, string):
        """ Setter de la secuencia de simbolos
        """
        self._rule = string

    def getProd(self):
        """ Getter de la secuencia de simbolos
        """
        return self._rule