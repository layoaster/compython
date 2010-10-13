#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
        $Id$
Description: Contiene clase que envuelve la representacion interna de los tokens y la propia clase token (con el par componente lexico, valor (identificadores y numerales)).
    $Author$ Lionel Aster Mena Garcia, Alejandro Samarin Perez, Sergio Armas Perez
      $Date$
  $Revision$
"""

class WrapTk:

    AND               = 1
    ARRAY             = 2
    ASTERISK          = 3
    BECOMES           = 4
    BEGIN             = 5
    COLON             = 6
    COMMA             = 7
    CONST             = 8
    DIV               = 9
    DO                = 10
    DOUBLEDOT         = 11
    ELSE              = 12
    END               = 13
    ENDTEXT           = 14
    EQUAL             = 15
    GREATER           = 16
    ID                = 17
    IF                = 18
    LEFTBRACKET       = 19
    LEFTPARENTHESIS   = 20
    LESS              = 21
    MINUS             = 22
    MOD               = 23
    NOT               = 24
    NOTEQUAL          = 25
    NOTGREATER        = 26
    NOTLESS           = 27
    NUMERAL           = 28
    OF                = 29
    OR                = 30
    PERIOD            = 31
    PLUS              = 32
    PROCEDURE         = 33
    PROGRAM           = 34
    RECORD            = 35
    RIGHTBRACKET      = 36
    RIGHTPARENTHESIS  = 37
    SEMICOLON         = 38
    THEN              = 39
    TYPE              = 40
    TOKEN_ERROR       = 41
    VAR               = 42
    WHILE             = 43
    COMMENT           = 44

    TokStrings = ("AND", "ARRAY", "ASTERISK", "BECOMES", "BEGIN", "COLON", "COMMA", "CONST", "DIV",
                  "DO", "DOUBLEDOT", "ELSE", "END", "ENDTEXT", "EQUAL", "GREATER", "ID", "IF", "LEFTBRACKET",
                  "LEFTPARENTHESIS", "LESS", "MINUS", "MOD", "NOT", "NOTEQUAL", "NOTGREATER", "NOTLESS",
                  "NUMERAL", "OF", "OR", "PERIOD", "PLUS", "PROCEDURE", "PROGRAM", "RECORD", "RIGHTBRACKET",
                  "RIGHTPARENTHESIS", "SEMICOLON", "THEN", "TYPE", "TOKEN_ERROR", "VAR", "WHILE", "COMMENT")

    @classmethod
    def toStr(self, token):
        return "_" + str(token)

    @classmethod
    def toToken(self, string):
        token = string[1:]
        return int(token)

class Token:

    def __init__(self, token, value=None):
        """ Constructor de la clase
            _token = token que representa
            _value = lexema o numero para los tokens ID y NUMERAL, para ID este valor hacer de apuntador en la tabla de simbolos
        """
        self._token = token
        self._value = value

    def setToken(self, token):
        self._token = token

    def setValue(self, value):
        self._value = value

    def getToken(self):
        return self._token

    def getValue(self):
        return self._value

    def __eq__(self, token):
        if self._token == token:
            return True
        else:
            return False
