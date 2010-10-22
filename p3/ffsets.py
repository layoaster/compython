#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
        $Id$
Description: Clase que almacena first y follow de cada uno de los simbolos no terminales de la gramatica de Pascal-
    $Author$ Lionel Aster Mena Garcia, Alejandro Samarin Perez, Sergio Armas Perez
      $Date$
  $Revision$
"""

class FFSets:

    def __init__(self):
        self.ffs["program"] = (("PROGRAM"), ())

