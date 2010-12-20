#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
        $Id$
Description: Clase que contiene funciones y datos de la generacion de codigo intermedio para el compilador de Pascal-
    $Author$ Lionel Aster Mena Garcia, Alejandro Samarin Perez, Sergio Armas Perez
      $Date$
  $Revision$
"""

class WrapOp:

    ADD        = 0
    AND        = 1
    ASSIGN     = 2
    CONSTANT   = 3
    DIVIDE     = 4
    ENDPROC    = 5
    ENDPROG    = 6
    EQUAL      = 7
    FIELD      = 8
    GOFALSE    = 9
    GOTO       = 10
    GREATER    = 11
    INDEX      = 12
    LESS       = 13
    MINUS      = 14
    MODULO     = 15
    MULTIPLY   = 16
    NOT        = 17
    NOTEQUAL   = 18
    NOTGREATER = 19
    NOTLESS    = 20
    OR         = 21
    PROCCALL   = 22
    PROCEDURE  = 23
    PROGRAM    = 24
    SUBTRACT   = 25
    VALUE      = 26
    VARIABLE   = 27
    VARPARAM   = 28
    READ       = 29
    WRITE      = 30
    DEFADDR    = 31
    DEFARG     = 32

    OpLexemes = ("ADD", "AND", "ASSIGN", "CONSTANT", "DIVIDE", "END_PROC",
                 "END_PROG", "EQUAL", "FIELD", "GO_FALSE", "GOTO", "GREATER",
                 "INDEX", "LESS", "MINUS", "MODULO", "MULTIPLY", "NOT",
                 "NOT_EQUAL", "NOT_GREATER", "NOT_LESS", "OR", "PROC_CALL",
                 "PROCEDURE", "PROGRAM", "SUBTRACT", "VALUE", "VARIABLE",
                 "VAR_PARAM", "READ", "WRITE", "DEF_ADDR", "DEF_ARG")

class CodeGenerator:

    def __init__(self, fout):
        self._fout = fout
        self._address = 0
        self._asmbool = False
        self._emitting = False
        self._temp = open("temp.$$$", "w")
        self._list = open(self._fout + ".inf", "w")

    def __del__(self):
        self._list.close()
        if not self._temp.closed():
            self._temp.close()
        if not self._code.closed():
            self._code.close()

    def emit(self, opcode, *args):
        if self._asmbool:
            if self._emitting:
                self._code.write(str(opcode) + '\n')
                for i in args:
                    self._code.write(str(i) + '\n')
                self._list.write(WrapOp.OpLexemes[opcode].rjust(6) + ':')
                self._list.write(WrapOp.OpLexemes[opcode].rjust(12))
                for i in args:
                    self._list.write(str(i).rjust(6))
                self._list.write('\n')    
            self._address += len(args)
        else:
            self._temp.write(str(opcode) + '\n')
            for i in args:
                self._temp.write(str(i) + '\n')
            self._list.write(WrapOp.OpLexemes[opcode].rjust(12))
            for i in args:
                self._list.write(str(i).rjust(6))
            self._list.write('\n')    

    def setAsmBool(self):
        if not self._asmbool:
            self._asmbool = True
            self._temp.close()
            self._list.close()
            self._list = open(self._fout + ".asm", "w")
            self._code = open(self._fout + ".exe", "w")

    def resetAsmBool(self):
        if self._asmbool:
            self._asmbool = False

    def setEmitting(self):
        if not self._asmbool:
            self._asmbool = True

    def resetEmitting(self):
        if self._asmbool:
            self._asmbool = False
