#!/usr/bin/python
# -*- coding: utf-8 -*-
"""
        $Id$
Description: Programa que crea un indice de palabras para un texto.
    $Author$ Lionel Aster Mena Garcia, Alejandro Samarin Perez, Sergio Armas Perez
      $Date$
  $Revision$
"""

import sys

if (len(sys.argv) > 2):
    print "Abriendo " + sys.argv[1] + " y escribiendo en " + sys.argv[2]
else:
    print "No se indica el fichero de entrada y/o salida"

