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

if (len(sys.argv) != 2):
    print "Usage: parser.py + source_code"
    exit()
else:
    scanner = LexAn()
    scanner.openFile(sys.argv[1])
    tok = scanner.yyLex()
    while tok != WrapTk.ENDTEXT:
        print tok
        tok = scanner.yyLex()
