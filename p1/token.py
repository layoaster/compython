#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
        $Id$
Description: Contiene clase que envuelve la representacion interna de los tokens y la propia clase token (con el par componente lexico, valor (identificadores y numerales)).
    $Author$ Lionel Aster Mena Garcia, Alejandro Samarin Perez, Sergio Armas Perez
      $Date$
  $Revision$
"""

class WrapTk

    AND = 1
    ARRAY = 2
    ASTERISK = 3
    BECOMES = 4
    BEGIN = 5
    COLON = 6
    COMMA = 7
    CONST = 8
    DIV = 9
    DO = 10
    DOUBLEDOT = 11
    ELSE = 12
    END = 13
    ENDTEXT = 14
    EQUAL = 15
    GREATER = 16
    ID = 17
    IF = 18
    LEFTBRACKET = 19
    LEFTPARENTHESIS = 20
    LESS = 21
    MINUS = 22
    MOD = 23
    NOT = 24
    NOTEQUAL = 25
    NOTGREATER = 26
    NOTLESS = 27
    NUMERAL = 28
    OF = 29
    OR = 30
    PERIOD = 31
    PLUS = 32
    PROCEDURE = 33
    PROGRAM = 34
    RECORD = 35
    RIGHTBRACKET = 36
    RIGHTPARENTHESIS = 37
    SEMICOLON = 38
    THEN = 39
    TYPE = 40
    TOKEN_ERROR = 41
    VAR = 42
    WHILE = 43

class Token:

    def __init__(self):
        """ Constructor de la clase
        """
        self._token = None
        self._value = None

    def setToken(self, token):
        self._token = token

    def setValue(self, value):
        self._value = value

    def getToken():
        return self._token

    def getValue():
        return self._value