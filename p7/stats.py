#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
        $Id$
Description: Analizador Lexico para Pascal-.
    $Author$ Lionel Aster Mena Garcia, Alejandro Samarin Perez, Sergio Armas Perez
      $Date$
  $Revision$
"""

class STStats:

    def __init__(self):
        self._stsize = 0
        self._defid = 0
        self._refid = 0

    def setSize(self, size):
        self._stsize = size

    def addDefined(self):
        self._defid += 1

    def addReferenced(self):
        self._refid += 1

    def getSize(self):
        return self._stsize

    def getDefined(self):
        return self._defid

    def getReferenced(self):
        return self._refid


