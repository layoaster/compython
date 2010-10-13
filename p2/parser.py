#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
        $Id$
Description: Analizador Lexico para Pascal-.
    $Author$ Lionel Aster Mena Garcia, Alejandro Samarin Perez, Sergio Armas Perez
      $Date$
  $Revision$
"""

from lexan import LexAn
from token import *
from error import *
import st


class SynAn:

    def __init__(self):
        _lookahead = None

    def start(self, fin):
        self._scanner = LexAn()
        try:
            self._scanner.openFile(fin)
        except IOError:
            raise
        self._lookahead = self._scanner.yyLex()
        self._program()

    def _match(self, tok):
        if self._lookahead == tok:
            self._lookahead = self._scanner.yyLex()
        else:
            print "Syntax Error"
            exit(1)

    def _program(self):
        self._match(WrapTk.PROGRAM)
        self._match(WrapTk.ID)
        self._match(WrapTk.SEMICOLON)
        self._blockBody()
        self._match(WrapTk.PERIOD)
        self._match(WrapTk.ENDTEXT)

    def _blockBody(self):
        self._match(WrapTk.BEGIN)
        self._match(WrapTk.END)
