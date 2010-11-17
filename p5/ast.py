#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
        $Id$
Description: Contiene clase AST que representa un Arbol Sintactico Abstracto y clase Node que representa los nodos de dicho arbol
    $Author$ Lionel Aster Mena Garcia, Alejandro Samarin Perez, Sergio Armas Perez
      $Date$
  $Revision$
"""
import string
from error import Colors

class AbstractSyntaxTree:
    _seqStrings = ('Pre-order:', 'In-order:', 'Post-order:')

    def __init__(self, root = None):
        """ Constructor de la clase con los atributos
            _root = nodo raiz del AST
        """
        self._root = root
        self._strtree = ""
        self._sequences = [[], [], []]

    def mkNode(self, label, *children):
        """ Crea un nodo intermedio con n hijos y una etiqueta
        """
        return Node(label, *children)

    def mkLeaf(self, label):
        """ Crea un nodo hoja con su etiqueta
        """
        return Node(label)

    def preOrder(self, node):
        """ Recorrido en Pre-Orden del AST
        """
        self._sequences[0].append(node.getLabel())
        self._strtree += "[" + str(node.getLabel())
        for n in node.getChildren():
            self.preOrder(n)
        self._strtree += "]"

    def inOrder(self, node):
        """ Recorrido en In-Orden del AST. Notese que para arboles no binarios, este recorrido solo puede
            realizarse en arboles cuyo grado sea par; de otro modo no puede saberse que hijos corresponden
            a la descendencia izquierda del nodo padre y cuales a la descendencia derecha
        """
        for n in range(0, len(node.getChildren()) / 2):
            self.inOrder(node.getChildren()[n])
        self._sequences[1].append(node.getLabel())
        for n in range(len(node.getChildren()) / 2, len(node.getChildren())):
	    self.inOrder(node.getChildren()[n])

    def postOrder(self, node):
        """ Recorrido en Post-Orden del AST
        """
        for n in node.getChildren():
            self.postOrder(n)
        self._sequences[2].append(node.getLabel())

    def setRoot(self, root):
        """ Setter del nodo raiz del arbol
        """
        self._root = root

    def getRoot(self):
        """ Getter del nodo raiz del arbol
        """
        return self._root

    def printSequences(self):
        self._sequences = [[], [], []]
        self.preOrder(self.getRoot())
        self.inOrder(self.getRoot())
        self.postOrder(self.getRoot())
        print ''
        for i in range(0, len(self._sequences)):
            print self._seqStrings[i].ljust(12),
            for j in range(0, len(self._sequences[i])):
                if str(self._sequences[i][j]) in string.punctuation:
                    print Colors.WARNING + str(self._sequences[i][j]) + Colors.ENDC,
                else:
                    print Colors.FAIL + str(self._sequences[i][j]) + Colors.ENDC,
            print ''
        
    def getAST(self):
        """ Retorna la cadena de descripcion del arbol sintactico para su representacion web
        """
        self._sequences = [[], [], []]
        self.preOrder(self.getRoot())
        self.inOrder(self.getRoot())
        self.postOrder(self.getRoot())
        return self._strtree, self._sequences


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

