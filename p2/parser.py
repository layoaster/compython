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

    def _syntaxError(self):
        print "Syntax Error: ", self._scanner.getPos()
        exit(1)

    def _match(self, tok):
        if self._lookahead == tok:
            self._lookahead = self._scanner.yyLex()
        else:
            self._syntaxError()

    def _program(self):
        self._match(WrapTk.PROGRAM)
        self._match(WrapTk.ID)
        self._match(WrapTk.SEMICOLON)
        self._blockBody()
        self._match(WrapTk.PERIOD)
        self._match(WrapTk.ENDTEXT)

    def _blockBody(self):
        if self._lookahead == WrapTk.CONST:
            self._constantDefinitionPart()
        if self._lookahead == WrapTk.TYPE:
            self._typeDefinitionPart()
        if self._lookahead == WrapTk.VAR:
            self._variableDefinitionPart()
        while self._lookahead == WrapTk.PROCEDURE:
            self._procedureDefinition()
        self._compoundStatement()

    def _constantDefinitionPart(self):
        self._match(WrapTk.CONST)
        self._constantDefinition()
        while self._lookahead == WrapTk.ID:
            self._constantDefinition()

    def _constantDefinition(self):
        self._match(WrapTk.ID)
        self._match(WrapTk.EQUAL)
        self._constant()
        self._match(WrapTk.SEMICOLON)

    def _typeDefinitionPart(self):
        self._match(WrapTk.TYPE)
        self._typeDefinition()
        while self._lookahead == WrapTk.ID:
            self._typeDefinition()

    def _typeDefinition(self):
        self._match(WrapTk.ID)
        self._match(WrapTk.EQUAL)
        self._newType()
        self._match(WrapTk.SEMICOLON)

    def _newType(self):
        if self._lookahead == WrapTk.ARRAY:
            self._newArrayType()
        elif self._lookahead == WrapTk.RECORD:
            self._newRecordType()
        else:
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
        while self._lookahead == WrapTk.SEMICOLON:
            self._match(WrapTk.SEMICOLON)
            self._recordSection()

    def _recordSection(self):
        self._match(WrapTk.ID)
        while self._lookahead == WrapTk.COMMA:
            self._match(WrapTk.COMMA)
            self._match(WrapTk.ID)
        self._match(WrapTk.COLON)
        self._match(WrapTk.ID)

    def _variableDefinitionPart(self):
        self._match(WrapTk.VAR)
        self._variableDefinition()
        while self._lookahead == WrapTk.ID:
            self._variableDefinition()

    def _variableDefinition(self):
        self._variableGroup()
        self._match(WrapTk.SEMICOLON)

    def _variableGroup(self):
        self._match(WrapTk.ID)
        while self._lookahead == WrapTk.COMMA:
            self._match(WrapTk.COMMA)
            self._match(WrapTk.ID)
        self._match(WrapTk.COLON)
        self._match(WrapTk.ID)

    def _procedureDefinition(self):
        self._match(WrapTk.PROCEDURE)
        self._match(WrapTk.ID)
        self._procedureBlock()
        self._match(WrapTk.SEMICOLON)

    def _procedureBlock(self):
        if self._lookahead == WrapTk.LEFTPARENTHESIS:
            self._match(WrapTk.LEFTPARENTHESIS)
            self._formalParameterList()
            self._match(WrapTk.RIGHTPARENTHESIS)
        self._match(WrapTk.SEMICOLON)
        self._blockBody()

    def _formalParameterList(self):
        self._parameterDefinition()
        while self._lookahead == WrapTk.SEMICOLON:
            self._match(WrapTk.SEMICOLON)
            self._parameterDefinition()

    def _parameterDefinition(self):
        if self._lookahead == WrapTk.VAR:
            self._match(WrapTk.VAR)
        self._variableGroup()

    def _statement(self):
        if self._lookahead == WrapTk.ID:
            self._match(WrapTk.ID)
            self._statementGroup()
        elif self._lookahead == WrapTk.IF:
            self._ifStatement()
        elif self._lookahead == WrapTk.WHILE:
            self._whileStatement()
        elif self._lookahead == WrapTk.BEGIN:
            self._compoundStatement()

    def _statementGroup(self):
        if self._lookahead in [WrapTk.LEFTBRACKET, WrapTk.PERIOD, WrapTk.BECOMES]:
            while self._lookahead in [WrapTk.LEFTBRACKET, WrapTk.PERIOD]:
                self._selector()
            self._match(WrapTk.BECOMES)
            self._expression()
        elif self._lookahead == WrapTk.LEFTPARENTHESIS:
            self._procedureStatement()

    def _procedureStatement(self):
        if self._lookahead == WrapTk.LEFTPARENTHESIS:
            self._match(WrapTk.LEFTPARENTHESIS)
            self._actualParameterList()
            self._match(WrapTk.RIGHTPARENTHESIS)

    def _actualParameterList(self):
        self._expression()
        while self._lookahead == WrapTk.COMMA:
            self._match(WrapTk.COMMA)
            self._expression()

    def _ifStatement(self):
        self._match(WrapTk.IF)
        self._expression()
        self._match(WrapTk.THEN)
        self._statement()
        if self._lookahead == WrapTk.ELSE:
            self._match(WrapTk.ELSE)
            self._statement()

    def _whileStatement(self):
        self._match(WrapTk.WHILE)
        self._expression()
        self._match(WrapTk.DO)
        self._statement()

    def _compoundStatement(self):
        self._match(WrapTk.BEGIN)
        self._statement()
        while self._lookahead == WrapTk.SEMICOLON:
            self._match(WrapTk.SEMICOLON)
            self._statement()
        self._match(WrapTk.END)

    def _expression(self):
        self._simpleExpression()
        if self._lookahead in [WrapTk.LESS, WrapTk.EQUAL, WrapTk.GREATER, WrapTk.NOTGREATER, WrapTk.NOTEQUAL, WrapTk.NOTLESS]:
            self._relationalOperator()
            self._simpleExpression()

    def _relationalOperator(self):
        if self._lookahead == WrapTk.LESS:
            self._match(WrapTk.LESS)
        elif self._lookahead == WrapTk.EQUAL:
            self._match(WrapTk.EQUAL)
        elif self._lookahead == WrapTk.GREATER:
            self._match(WrapTk.GREATER)
        elif self._lookahead == WrapTk.NOTGREATER:
            self._match(WrapTk.NOTGREATER)
        elif self._lookahead == WrapTk.NOTEQUAL:
            self._match(WrapTk.NOTEQUAL)
        elif self._lookahead == WrapTk.NOTLESS:
            self._match(WrapTk.NOTLESS)
        else:
            self._syntaxError()

    def _simpleExpression(self):
        if self._lookahead in [WrapTk.PLUS, WrapTk.MINUS]:
            self._signOperator()
        self._term()
        while self._lookahead in [WrapTk.PLUS, WrapTk.MINUS, WrapTk.OR]:
            self._additiveOperator()
            self._term()

    def _signOperator(self):
        if self._lookahead == WrapTk.PLUS:
            self._match(WrapTk.PLUS)
        elif self._lookahead == WrapTk.MINUS:
            self._match(WrapTk.MINUS)
        else:
            self._syntaxError()

    def _additiveOperator(self):
        if self._lookahead == WrapTk.PLUS:
            self._match(WrapTk.PLUS)
        elif self._lookahead == WrapTk.MINUS:
            self._match(WrapTk.MINUS)
        elif self._lookahead == WrapTk.OR:
            self._match(WrapTk.OR)
        else:
            self._syntaxError()

    def _term(self):
        self._factor()
        while self._lookahead in [WrapTk.ASTERISK, WrapTk.DIV, WrapTk.MOD, WrapTk.AND]:
           self._multiplyingOperator()
           self._factor()

    def _multiplyingOperator(self):
        if self._lookahead == WrapTk.ASTERISK:
            self._match(WrapTk.ASTERISK)
        elif self._lookahead == WrapTk.DIV:
            self._match(WrapTk.DIV)
        elif self._lookahead == WrapTk.MOD:
            self._match(WrapTk.MOD)
        elif self._lookahead == WrapTk.AND:
            self._match(WrapTk.AND)
        else:
            self._syntaxError()

    def _factor(self):
        if self._lookahead == WrapTk.NUMERAL:
            self._match(WrapTk.NUMERAL)
        elif self._lookahead == WrapTk.ID:
            self._match(WrapTk.ID)
            while self._lookahead in [WrapTk.LEFTBRACKET, WrapTk.PERIOD]:
                self._selector()
        elif self._lookahead == WrapTk.LEFTPARENTHESIS:
            self._match(WrapTk.LEFTPARENTHESIS)
            self._expression()
            self._match(WrapTk.RIGHTPARENTHESIS)
        elif self._lookahead == WrapTk.NOT:
            self._match(WrapTk.NOT)
            self._factor()
        else:
            self._syntaxError()

    def _selector(self):
        if self._lookahead == WrapTk.LEFTBRACKET:
            self._indexSelector()
        elif self._lookahead == WrapTk.PERIOD:
            self._fieldSelector()
        else:
            self._syntaxError()

    def _indexSelector(self):
        self._match(WrapTk.LEFTBRACKET)
        self._expression()
        self._match(WrapTk.RIGHTBRACKET)

    def _fieldSelector(self):
        self._match(WrapTk.PERIOD)
        self._match(WrapTk.ID)

    def _constant(self):
        if self._lookahead == WrapTk.NUMERAL:
            self._match(WrapTk.NUMERAL)
        elif self._lookahead == WrapTk.ID:
            self._match(WrapTk.ID)
        else:
            self._syntaxError()
