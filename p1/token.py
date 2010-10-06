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

    AND =              ("AND",               1)
    ARRAY =            ("ARRAY",             2)
    ASTERISK =         ("ASTERISK",          3)
    BECOMES =          ("BECOMES",           4)
    BEGIN =            ("BEGIN",             5)
    COLON =            ("COLON",             6)
    COMMA =            ("COMMA",             7)
    CONST =            ("CONST",             8)
    DIV =              ("DIV",               9)
    DO =               ("DO",               10)
    DOUBLEDOT =        ("DOUBLEDOT",        11)
    ELSE =             ("ELSE",             12)
    END =              ("END",              13)
    ENDTEXT =          ("ENDTEXT",          14)
    EQUAL =            ("EQUAL",            15)
    GREATER =          ("GREATER",          16)
    ID =               ("ID",               17)
    IF =               ("IF",               18)
    LEFTBRACKET =      ("LEFTBRACKET",      19)
    LEFTPARENTHESIS =  ("LEFTPARENTHESIS",  20)
    LESS =             ("LESS",             21)
    MINUS =            ("MINUS",            22)
    MOD =              ("MOD",              23)
    NOT =              ("NOT",              24)
    NOTEQUAL =         ("NOTEQUAL",         25)
    NOTGREATER =       ("NOTGREATER",       26)
    NOTLESS =          ("NOTLESS",          27)
    NUMERAL =          ("NUMERAL",          28)
    OF =               ("OF",               29)
    OR =               ("OR",               30)
    PERIOD =           ("PERIOD",           31)
    PLUS =             ("PLUS",             32)
    PROCEDURE =        ("PROCEDURE",        33)
    PROGRAM =          ("PROGRAM",          34)
    RECORD =           ("RECORD",           35)
    RIGHTBRACKET =     ("RIGHTBRACKET",     36)
    RIGHTPARENTHESIS = ("RIGHTPARENTHESIS", 37)
    SEMICOLON =        ("SEMICOLON",        38)
    THEN =             ("THEN",             39)
    TYPE =             ("TYPE",             40)
    TOKEN_ERROR =      ("TOKEN_ERROR",      41)
    VAR =              ("VAR",              42)
    WHILE =            ("WHILE",            43)
    COMMENT =          ("COMMENT",          44)

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
