#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
$Id$
Description: Representacion de los Simbolos No Terminales.
$Author$ Lionel Aster Mena Garcia, Alejandro Samarin Perez, Sergio Armas Perez
$Date$
$Revision$
"""


class NoTerm:

    def __init__(self, nt = None):
        """ Constructor de la clase
            _name = nombre del simbolo no terminal
        """
        self._name = nt


    def setName(self, nt):
        """ Setter del nombre del simbolo no terminal
        """
        self._name = nt

    def getName(self):
        """ Getter del nombre del simbolo no terminal
        """
        return self._name

    def __eq__(self, nt):
        """ Sobrecarga del operador de comparacion "igual que", para establecer las comparaciones entre objetos NoTerm
            tambien necesaria para utilizarlo como clave en los diccionarios
        """
        if self._name == nt.getName():
            return True
        else:
            return False

    def __hash__ (self):
        """ Sobrecarga de la funcion hash (identificando el objeto NoTerm de manera unica) necesaria para utilizarlo
            como clave en los diccionarios
        """
        return hash(self._name)
