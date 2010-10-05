#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
        $Id$
Description: Analizador Lexico para Pascal-.
    $Author$ Lionel Aster Mena Garcia, Alejandro Samarin Perez, Sergio Armas Perez
      $Date$
  $Revision$
"""

import lexan
import sys

if (len(sys.argv) != 2):
    print "Usage: parser.py + source_code"
    exit()
else:
    scanner = LexAn()
    scanner.openFile(argv[1])
#    while True:
#        if scanner.nextToken()
#            pass
#        else:
#            break
