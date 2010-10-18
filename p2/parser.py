#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
        $Id$
Description: Analizador Sintáctico para Pascal-.
    $Author$ Lionel Aster Mena Garcia, Alejandro Samarin Perez, Sergio Armas Perez
      $Date$
  $Revision$
"""

from lexan import LexAn
from token import *
from error import *


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
        if _lookahead == WrapTk.CONST:
            self._constantDefinitionPart()
        if _lookahead == WrapTk.TYPE:
            self._typeDefinitionPart()
        if _lookahead == WrapTk.VAR:
            self._varDefinitionPart()
        while _lookahead == WrapTk.PROCEDURE:
            self._procedureDefinition()
        self._compoundStatement()

    def _constantDefinitionPart(self):
        self._match(WrapTk.CONST):
        self._constantDefinition()
        while _lookahead == WrapTk.ID:
            self._constantDefinition()

    def _constantDefinition(self):
        self._match(WrapTk.ID)
        self._match(WrapTk.EQUAL)
        self._constant()
        self._match(WrapTk.SEMICOLON)

    def _typeDefinitionPart(self):
        self._match(WrapTk.TYPE)
        self._typeDefinition()
        while _lookahead == WrapTk.ID:
            self._typeDefinition()

    def _typeDefinition(self):
        self._match(WrapTk.ID)
        self._match(WrapTk.EQUAL)
        self._newType()
        self._match(WrapTk.SEMICOLON)

    def _newType(self):
        if _lookahead == WrapTk.ARRAY:
            self._newArrayType()
        elif _lookahead == WrapTk.RECORD:
            self._newRecordType()
        else
            self._syntaxError()

    def _newArrayType(self):
        self._match(WrapTk.ARRAY)
        self._match(WrapTk.LEFTBRACKET)
        self._indexRange()
        self._match(WrapTk.RIGHTBRACKET)
        self._match(WrapTk.OF)
        self._match(WrapTk.ID)

    def _indexRange(self):
        self._constant()
        self._match(WrapTk.DOUBLEDOT)
        self._constant()

    def _newRecordType(self):
        self._match(WrapTk.RECORD)
        self._fieldList()
        self._match(WrapTk.END)

    def _fieldList(self):
        self._recordSection()
        while _lookahead == WrapTk.SEMICOLON:
            self._match(WrapTk.SEMICOLON)
            self._recordSection()

    def _recordSection(self):
        self._match(WrapTk.ID)
        while _lookahead == WrapTk.COMMA:
            self._match(WrapTk.COMMA)
            self._match(WrapTk.ID)
        self._match(WrapTk.COLON)
        self._match(WrapTk.ID)

    def _variableDefinitionPart(self):
        self._match(WrapTk.VAR)
        self._variableDefinition()
        while _lookahead == WrapTk.ID:
            self._variableDefinition()




    def _compoundStatement(self):
        self._match(WrapTk.BEGIN)
        self._match(WrapTk.END)
