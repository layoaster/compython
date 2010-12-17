#!/usr/bin/env python
# -*- coding: utf-8 -*-

class WrapOp:

    ADD        = 0
    AND        = 1
    ASSING     = 2
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

    OpLexemes = ("ADD", "AND", "ASSING", "CONSTANT", "DIVIDE", "END_PROC",
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
        temp = open("temp.$$$", "w")
        code = open(self._fout + ".eje", "w")
        list = open(self._fout + ".inf", "w")

    def emit(opcode, *args):
        if self._asmbool:
            if self._emitting:
                code.write(opcode + '\n')
                for i in args:
                    code.write(i + '\n')
                list.write(WrapOp.OpLexemes[opcode].rjust(6) + ':')
                list.write(WrapOp.OpLexemes[opcode].rjust(12))
                for i in args:
                    list.write(i.rjust(6))
            self._address += len(args)
        else:
            temp.write(opcode + '\n')
            for i in args:
                temp.write(i + '\n')
            list.write(WrapOp.OpLexemes[opcode].rjust(12))
            for i in args:
                list.write(i.rjust(6))

    def setAsmBool(self):
        if not self._asmbool:
            self._asmbool = True
            list.close()
            list = open(self._fout + ".asm", "w")

    def resetAsmBool(self):
        if self._asmbool:
            self._asmbool = False

    def setEmitting(self):
        if not self._asmbool:
            self._asmbool = True

    def resetEmitting(self):
        if self._asmbool:
            self._asmbool = False
