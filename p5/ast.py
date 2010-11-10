#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
        $Id$
Description: Contiene clase AST que representa un Arbol Sintactico Abstracto y clase Node que representa los nodos de dicho arbol
    $Author$ Lionel Aster Mena Garcia, Alejandro Samarin Perez, Sergio Armas Perez
      $Date$
  $Revision$
"""

class AST:

    def __init__(self, root = None):
        self._root = root

    def mkNode(self, label, *children):

        return Node(label, *children)

    def mkLeaf(self, label):
        return Node(label)


    def setRoot(self, root):
        """ Setter del nodo raiz del arbol
        """
        self._root = root


    def getRoot(self):
        """ Getter del nodo raiz del arbol
        """
        return self._root


class Node:

    def __init__(self, label = "", *children):
        """ Constructor de la clase con los atributos:
            _label = etiqueta del nodo
            _children = lista de "punteros" a nodos hijos
        """
        self._label = label
        self._children = []
        for p in children:
            self._children.append(p)

    def setLabel(self, label):
        """ Setter de la etiqueta del nodo
        """
        self._label = label

    def setLeafs(self, *children):
        """ Setter para establecer los "punteros" a nodos hijos, eliminando si hubiese punteros almacenados previamente
        """
        self._children = []
        for p in children:
            self._children.append(p)

    def addLeafs(self, *children):
        """ Setter para añadir "punteros" a nodos hijos, conservando si hubiese punteros almacenados previamente
        """
        for p in children:
            self._children.append(p)

    def getLabel(self):
        """ Getter de la etiqueta del nodo
        """
        return self._label

    def getLeafs(self):
        """ Getter de la lista de "punteros" a nodos hijos
        """
        return self._children

