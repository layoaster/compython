#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
        $Id$
Description: Contiene clase AST que representa un Arbol Sintactico Abstracto y clase Node que representa los nodos de dicho arbol
    $Author$ Lionel Aster Mena Garcia, Alejandro Samarin Perez, Sergio Armas Perez
      $Date$
  $Revision$
"""

class AbstractSyntaxTree:

    def __init__(self, root = None):
        """ Constructor de la clase con los atributos
            _root = nodo raiz del AST
        """
        self._root = root
        self._strtree = ""

    def mkNode(self, label, *children):
        """ Crea un nodo intermedio con n hijos y una etiqueta
        """
        return Node(label, *children)

    def mkLeaf(self, label):
        """ Crea un nodo hoja con su etiqueta
        """
        return Node(label)

    def preOrder(self, node):
        """ Reccorido en Pre-Orden del AST
        """
        print node.getLabel()
        self._strtree += "[" + str(node.getLabel())
        for n in node.getChildren():
            self.preOrder(n)
        self._strtree += "]"

    def inOrder(self, node):
        for n in range(0, len(node.getChildren()) / 2):
            self.inOrder(node.getChildren()[n])
        print node.getLabel()
        for n in range(len(node.getChildren()) / 2, len(node.getChildren())):
	    self.inOrder(node.getChildren()[n])

    def postOrder(self, node):
        """ Reccorido en Post-Orden del AST
        """
        for n in node.getChildren():
            self.postOrder(n)
        print node.getLabel()

    def setRoot(self, root):
        """ Setter del nodo raiz del arbol
        """
        self._root = root


    def getRoot(self):
        """ Getter del nodo raiz del arbol
        """
        return self._root

    def getAST(self):
        """ Retorna la cadena de descripcion del arbol sintactico para su representacion web
        """
        return self._strtree


class Node:

    def __init__(self, label = "~", *children):
        """ Constructor de la clase con los atributos:
            _label    = etiqueta del nodo
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

    def setChildren(self, *children):
        """ Setter para establecer los "punteros" a nodos hijos, eliminando si hubiese punteros almacenados previamente
        """
        self._children = []
        for p in children:
            self._children.append(p)

    def addChildren(self, *children):
        """ Setter para añadir "punteros" a nodos hijos, conservando si hubiese punteros almacenados previamente
        """
        for p in children:
            self._children.append(p)

    def getLabel(self):
        """ Getter de la etiqueta del nodo
        """
        return self._label

    def getChildren(self):
        """ Getter de la lista de "punteros" a nodos hijos
        """
        return self._children

    def __str__(self):
        """ Representacion string del objeto nodo, que se traduce en su etiqueta
        """
        return str(self._label)

