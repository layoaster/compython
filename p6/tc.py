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

class ThompsonConstruction:
    _EPSILON = "&#949;"

    def __init__(self, seq):
        self._seq = seq
        self._graph = pgv.AGraph(strict = False, directed = True, rankdir = 'LR', size = "14.0, 6.0")
        self._graph.node_attr['shape'] = 'circle'
        self._count = 1
        self._start = None
        self._end = None

    def createGraph(self):
        nodes = Stack()
        for symbol in self._seq:
            if symbol in ('+', '?'): # Positive closure or zero or one
                if symbol == '+':
                    self._positiveClosure(nodes.top())
                else:
                    self._zeroOrOne(nodes.top())
            elif symbol == '·': # Concatenation
                lastpair2 = nodes.pop()
                lastpair1 = nodes.pop()
                self._concatenation(lastpair1, lastpair2)

                nodes.push((lastpair1[0], lastpair2[0]))
                self._count -= 1
            else: # Disjunction, Kleene closure or symbol
                newpair = (self._count, self._count + 1)
                if symbol == '*':
                    lastpair = nodes.pop()
                    self._kClosure(newpair, lastpair)
                elif symbol == '|':
                    while not nodes.isEmpty():
                        lastpair = nodes.pop()
                        self._disjunction(newpair,lastpair)
                else:
                    self._graph.add_edge(newpair[0], newpair[1], label = symbol, fontcolor='red')

                nodes.push(newpair)
                self._count += 2

        lastpair = nodes.pop()
        # Creamos estado de arranque
        self._graph.add_node(0, shape = 'point', width = 0, height = 0)
        self._graph.add_edge(0, lastpair[0])
        # Creamos estado de aceptacion
        self._graph.get_node(lastpair[1]).attr['shape'] = "doublecircle"
        # Guardamos los estados de arranque y aceptacion del NFA
        self._start = 0
        self._end = lastpair[1]

    def _positiveClosure(self, topair):
        self._graph.add_edge(topair[1], topair[0], label = self._EPSILON)
    def _zeroOrOne(self, topair):
        self._graph.add_edge(topair[0], topair[1], label = self._EPSILON)

    def _concatenation(self, lastpair1, lastpair2):
        # Obteniendo nodos predecesores del nodo que se elimina, y asignando sus transiciones al nodo inicial del segundo subgrafo
        for n in self._graph.predecessors(lastpair2[1]):
            label = self._graph.get_edge(n, lastpair2[1]).attr["label"]
            color = self._graph.get_edge(n, lastpair2[1]).attr["fontcolor"]
            self._graph.add_edge(n, lastpair2[0], label = label, fontcolor = color)
            self._graph.delete_edge(n, lastpair2[1])
        # Obteniendo nodos sucesores del nodo que se preserva, y asignando sus transiciones al nodo final del primer subgrafo
        for n in self._graph.successors(lastpair2[0]):
            label = self._graph.get_edge(lastpair2[0], n).attr["label"]
            color = self._graph.get_edge(lastpair2[0], n).attr["fontcolor"]
            self._graph.add_edge(lastpair1[1], n, label = label, fontcolor = color)
            self._graph.delete_edge(lastpair2[0], n)
        # Eliminando el nodo sobrante
        self._graph.delete_node(lastpair2[1])

    def _kClosure(self, newpair, lastpair):
        self._graph.add_edge(newpair[0], lastpair[0], label = self._EPSILON)
        self._graph.add_edge(lastpair[1], newpair[1], label = self._EPSILON)
        self._graph.add_edge(lastpair[1], lastpair[0], label = self._EPSILON)
        self._graph.add_edge(newpair[0], newpair[1], label = self._EPSILON)

    def _disjunction(self, newpair, lastpair):
        self._graph.add_edge(newpair[0], lastpair[0], label = self._EPSILON)
        self._graph.add_edge(lastpair[1], newpair[1], label = self._EPSILON)

    def writeDOT(self, filename = "graph.dot"):
        self._graph.write(filename)

    def drawGraph(self, filename = "graph.svg"):
        self._graph.draw(filename, format = filename.partition('.')[2], prog = 'dot')
