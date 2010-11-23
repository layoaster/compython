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
    _EPSILON = "&#949;"

    def __init__(self, seq):
        self._seq = seq
        self._graph = pgv.AGraph(strict = False, directed = True, rankdir = 'LR', size = "6.0, 2.0")
        self._graph.node_attr['shape'] = 'circle'
        #self._graph.rankdir = "LR"
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
                    self._graph.add_edge(newpair[0], lastpair[0], label = self._EPSILON, fontcolor='red')
                    self._graph.add_edge(lastpair[1], newpair[1], label = self._EPSILON, fontcolor='red')
                    self._graph.add_edge(lastpair[1], lastpair[0], label = self._EPSILON, fontcolor='red')
                    self._graph.add_edge(newpair[0], newpair[1], label = self._EPSILON, fontcolor='red')

                elif symbol == '|':
                    while not nodes.isEmpty():
                        lastpair = nodes.pop()
                        self._graph.add_edge(newpair[0], lastpair[0], label = self._EPSILON, fontcolor='red')
                        self._graph.add_edge(lastpair[1], newpair[1], label = self._EPSILON, fontcolor='red')

                else: #simbolos
                    self._graph.add_edge(newpair[0], newpair[1], label = symbol)

                nodes.push(newpair)
                self._count += 2
            else: #concatenacion
                lastpair2 = nodes.pop()
                lastpair1 = nodes.pop()
                label = self._graph.get_edge(lastpair2[0], lastpair2[1]).attr["label"]
                self._graph.delete_edge(lastpair2[0], lastpair2[1])
                self._graph.add_edge(lastpair1[1], lastpair2[0], label = label)
                self._graph.delete_node(lastpair2[1])
                nodes.push((lastpair1[0], lastpair2[0]))
                self._count -= 1

        lastpair = nodes.pop()
        self._graph.get_node(lastpair[1]).attr['shape'] = "doublecircle"
        self._start = lastpair[0]
        self._end = lastpair[1]
        self._graph.graph_attr['start'] = str(self._start)

    def writeDOT(self, filename = "graph.dot"):
        self._graph.write(filename)

    def drawGraph(self, filename = "graph.svg"):
        self._graph.draw(filename, format = filename.partition('.')[2], prog = 'dot')
