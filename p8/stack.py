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
            _stack = pila
        """
        self._stack = []
        self._n = 0

    def push(self, t):
        """ Inserta el elemento t en la pila
        """
        self._stack.append(t)

    def pop(self):
        """ Extrae elemento de la cima de la pila
        """
        return self._stack.pop()

    def top(self):
        """ Retorna elemento de la cima de la pila
        """
        return self._stack[-1]

    def isEmpty(self):
        """ Retorna False = si la pila no esta vacía
                     True = si la pila esta vacía
        """
        return (len(self._stack) == 0)

    def clear(self):
        """ Vacia la pila
        """
        self._stack = []

    def printStack(self):
        """ Imprime el contenido de la pila (util en trazas)
        """
        for i in self._stack:
            print i, " | ",
        print ""

    def return3Last(self):
        """ Retorna los tres ultimos elementos empezando desde el tope de la pila (para la traza por consola)
        """
        return self._stack[-3:]

    def __getitem__(self, i):
        """ Sobrecarga del operador de indexado devuelve el contenido de la pila del nivel indicador por i
        """
        try:
            return self._stack[i]
        except IndexError:
            raise

    def __len__(self):
        """ Sobrecarga de la funcion que determina la longitud
        """
        return len(self._stack)

    def __str__(self):
        """ Representacion string del objeto pila (util en trazas)
        """
        string = ""
        for i in self._stack:
            string = string + " " + str(i) + " " + " | "
        return string
