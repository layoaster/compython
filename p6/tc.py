#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
        $Id$
Description: Contiene clase AST que representa un Arbol Sintactico Abstracto y clase Node que representa los nodos de dicho arbol
    $Author$ Lionel Aster Mena Garcia, Alejandro Samarin Perez, Sergio Armas Perez
      $Date$
  $Revision$
"""

import pygraphviz as pgv
from stack import *
import string

class ThompsonConstruction:

    def __init__(self, seq):
        self._seq = seq
        self._graph = AGraph(strict = False, directed = True)
        self._count = 1
        self._start = None
        self._end = None

    def createGraph(self):

        nodes = Stack()
        for symbol in self._seq:
            if symbol != '·':
                newpair = (self._count, self._count + 1)
                if symbol == '*':
                    lastpair = nodes.pop()
                    self._graph.add_edge(newpair[0], lastpair[0], label = "&epsilon")
                    self._graph.add_edge(lastpair[1], newpair[1], label = "&epsilon")
                    self._graph.add_edge(lastpair[1], lastpair[0], label = "&epsilon")
                    self._graph.add_edge(newpair[0], newpair[1], label = "&epsilon")

                elif symbol == '|':
                    while not nodes.isEmpty():
                        lastpair = nodes.pop()
                        self._graph.add_edge(newpair[0], lastpair[0], label = "&epsilon")
                        self._graph.add_edge(lastpair[1], newpair[1], label = "&epsilon")

                else: #simbolos
                    self._graph.add_edge(newpair[0], newpair[1], label = symbol)

                nodes.push(newpair)
                self._count += 2
            else: #concatenacion
                lastpair2 = nodes.pop()
                lastpair1 = nodes.pop()
                label = get_edge(lastpair2[0], lastpair2[1]).attr["label"]
                self._graph.delete_edge(lastpair2[0], lastpair2[1])
                self._graph.add_edge(lastpair1[1], lastpair2[1], label = label)
                self._graph.delete_node(lastpair2[0])
                nodes.push((lastpair1[0], lastpair2[1]))

        lastpair = stack.pop()
        self._start = lastpair[0]
        self._end = lastpair[1]

    def writeDOT(self, filename = "graph.dot"):
        self._graph.write(filename)

    def drawGraph(self, filename = "graph", format = "svg"):
        filepath = ".".join(filename, format)
        self._graph.draw(filepath, format)










