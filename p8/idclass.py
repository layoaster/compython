#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
        $Id$
Description: Representacion de los Simbolos No Terminales.
    $Author$ Lionel Aster Mena Garcia, Alejandro Samarin Perez, Sergio Armas Perez
      $Date$
  $Revision$
"""

class WrapCl:

    ARRAY_TYPE      = 0
    CONSTANT        = 1
    FIELD           = 2
    PROCEDURE       = 3
    PROGRAM_NAME    = 4
    RECORD_TYPE     = 5
    STANDARD_PROC   = 6
    STANDARD_TYPE   = 7
    VALUE_PARAMETER = 8
    VAR_PARAMETER   = 9
    VARIABLE        = 10
    UNDEFINED       = 11

class IdClass:

    def __init__(self, cl = None):
        """ Constructor de la clase
            _name = nombre de la clase del identificador
        """
        self._name = cl


    def setName(self, cl):
        """ Setter del nombre de la clase del identificador
        """
        self._name = cl

    def getName(self):
        """ Getter del nombre de la clase del identificador
        """
        return self._name

    def __eq__(self, nt):
        """ Sobrecarga del operador de comparacion "igual que", para establecer las comparaciones
            entre objetos Class tambien necesaria para utilizarlo como clave en los diccionarios
        """
        if self._name == cl.getName():
            return True
        else:
            return False

    def __hash__ (self):
        """ Sobrecarga de la funcion hash (identificando el objeto NoTerm de manera unica) necesaria para utilizarlo
            como clave en los diccionarios
        """
        return hash(self._name)
