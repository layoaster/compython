#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
        $Id: lexan.py 74 2010-10-01 13:42:48Z lionelmena@gmail.com $
Description: Analizador Lexico para Pascal-.
    $Author: lionelmena@gmail.com $ Lionel Aster Mena Garcia, Alejandro Samarin Perez, Sergio Armas Perez
      $Date: 2010-10-01 14:42:48 +0100 (vie, 01 oct 2010) $
  $Revision: 74 $
"""

import lexan

if (len(sys.argv) != 2):
    print "Usage: parser.py + source_code"
    exit()
else:
    scanner = LexAn(argv[1])
