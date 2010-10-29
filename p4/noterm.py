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
        self._name = nt

    def getName(self):
        return self._name

    def __eq__(self, nt):
        """ Sobrecarga del operador de comparacion "igual que", para establecer las comparaciones con un enteros
            tambien es necesario para insertar el objeto en un set/frozenset
        """
        if self._name == nt.getName():
            return True
        else:
            return False

    def __hash__ (self):
        """ Sobrecarga de la funcion hash (identificando el objeto token de manera unica) necesaria para insertar
        el objeto en un set/frozenset
        """
        return hash(self._name)
