#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
        $Id$
Description: Implementacion de una Pila mediante una lista.
    $Author$ Lionel Aster Mena Garcia, Alejandro Samarin Perez, Sergio Armas Perez
      $Date$
  $Revision$
"""

class Stack:

    def __init__(self):
        """ Constructor de la clase
            _st = pila
        """
        self._st = []

    def push(self, t):
        """ Inserta el elemento t en la pila
        """
        self._st.append(t)

    def pop(self):
        """ Extrae elemento de la cima de la pila
        """
        return self._st.pop()

    def top(self):
        """ Retorna elemento de la cima de la pila
        """
        return self._st[-1]

    def isEmpty(self):
        """ Retorna False = si la pila no esta vacía
                     True = si la pila esta vacía
        """
        return (len(self._st) == 0)

    def printStack(self):
        """ Imprime el contenido de la pila (util en trazas)
        """
        print self._st