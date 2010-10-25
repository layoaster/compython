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
    """ Clase Analizador Sintactico:
        Comprueba que la secuencia de tokens de entrada sea acorde con las
        especificaciones de la gramatica de Pascal-
    """
    def __init__(self):
        """ Constructor de la clase. Atributos:
            _lookahead = token o simbolo de preanalisis
            _scanner = instancia de la clase analizador lexico
            _strTree = cadena que describe el arbol de analisis sintactico obtenido en notacion phpSyntaxTree
        """
        self._lookahead = None
        self._scanner = None
        self._strTree = ""

    def start(self, fin):
        """ Comienzo del analizador sintactico. Se encarga de inicializar el lexico, ordenarle abrir el
            fichero y recoger el primer token de entrada para comenzar el analisis
        """
        self._scanner = LexAn()
        try:
            self._scanner.openFile(fin)
        except IOError:
            raise
        self._lookahead = self._scanner.yyLex()
        self._program()

    def _syntaxError(self, expected=None):
        """ Administra los errores que se hayan podido producir durante esta etapa. Crea una excepcion que es
            capturada en el modulo 'pmc', con toda la informacion necesaria acerca del error
        """
        self._strTree += "[TOKEN-ERROR]"
        # Si el error vino desde 'match', podemos saber que token esperariamos encontrar
        if expected is not None:
            raise SynError(SynError.UNEXPECTED_SYM, self._scanner.getPos(),
                  " - Found '" + self._lookahead.getLexeme() + "', expected '" + Token(expected).getLexeme() + "'")
        else:
            raise SynError(SynError.UNEXPECTED_SYM, self._scanner.getPos(),
                  " - Found '" + self._lookahead.getLexeme() + "'")

    def getAST(self):
        """ Retorna la cadena de descripcion del arbol de analisis sintactico para su representacion web """
        return self._strTree

    def _match(self, tok):
        """ Trata de emparejar el token leido con el token que espera encontrar en cada momento. Si el matching
            tuvo exito, se lee el siguiente token (a la vez que se adjunta la descripcion del terminal en strTree).
            En caso contrario, se llama al metodo syntaxError que se encargara de la gestion del error. Ademas,
            comprueba si el analizador lexico ha obtenido algun error durante la obtencion del token y, en tal caso,
            eleva la excepcion que este ultimo genera hacia el modulo 'pmc'.
        """
        try:
            if self._lookahead == tok:
                self._strTree += "[" + self._lookahead.getLexeme() + "]"
                self._lookahead = self._scanner.yyLex()
            else:
                self._syntaxError(tok)
        except LexError:
            raise

    def _program(self):
        self._strTree += "[<Program>"
        self._match(WrapTk.PROGRAM)
        self._match(WrapTk.ID)
        self._match(WrapTk.SEMICOLON)
        self._blockBody()
        self._match(WrapTk.PERIOD)
        #self._match(WrapTk.ENDTEXT)
        self._strTree += "]"

    def _blockBody(self):
        self._strTree += "[<BlockBody>"
        if self._lookahead == WrapTk.CONST:
            self._constantDefinitionPart()
        if self._lookahead == WrapTk.TYPE:
            self._typeDefinitionPart()
        if self._lookahead == WrapTk.VAR:
            self._variableDefinitionPart()
        while self._lookahead == WrapTk.PROCEDURE:
            self._procedureDefinition()
        self._compoundStatement()
        self._strTree += "]"

    def _constantDefinitionPart(self):
        self._strTree += "[<ConstantDefinitionPart>"
        self._match(WrapTk.CONST)
        self._constantDefinition()
        while self._lookahead == WrapTk.ID:
            self._constantDefinition()
        self._strTree += "]"

    def _constantDefinition(self):
        self._strTree += "[<ConstantDefinition>"
        self._match(WrapTk.ID)
        self._match(WrapTk.EQUAL)
        self._constant()
        self._match(WrapTk.SEMICOLON)
        self._strTree += "]"

    def _typeDefinitionPart(self):
        self._strTree += "[<TypeDefinitionPart>"
        self._match(WrapTk.TYPE)
        self._typeDefinition()
        while self._lookahead == WrapTk.ID:
            self._typeDefinition()
        self._strTree += "]"

    def _typeDefinition(self):
        self._strTree += "[<TypeDefinition>"
        self._match(WrapTk.ID)
        self._match(WrapTk.EQUAL)
        self._newType()
        self._match(WrapTk.SEMICOLON)
        self._strTree += "]"

    def _newType(self):
        self._strTree += "[<NewType>"
        if self._lookahead == WrapTk.ARRAY:
            self._newArrayType()
        elif self._lookahead == WrapTk.RECORD:
            self._newRecordType()
        else:
            self._syntaxError()
        self._strTree += "]"

    def _newArrayType(self):
        self._strTree += "[<NewArrayType>"
        self._match(WrapTk.ARRAY)
        self._match(WrapTk.LEFTBRACKET)
        self._indexRange()
        self._match(WrapTk.RIGHTBRACKET)
        self._match(WrapTk.OF)
        self._match(WrapTk.ID)
        self._strTree += "]"

    def _indexRange(self):
        self._strTree += "[<IndexRange>"
        self._constant()
        self._match(WrapTk.DOUBLEDOT)
        self._constant()
        self._strTree += "]"

    def _newRecordType(self):
        self._strTree += "[<NewRecordType>"
        self._match(WrapTk.RECORD)
        self._fieldList()
        self._match(WrapTk.END)
        self._strTree += "]"

    def _fieldList(self):
        self._strTree += "[<FieldList>"
        self._recordSection()
        while self._lookahead == WrapTk.SEMICOLON:
            self._match(WrapTk.SEMICOLON)
            self._recordSection()
        self._strTree += "]"

    def _recordSection(self):
        self._strTree += "[<RecordSection>"
        self._match(WrapTk.ID)
        while self._lookahead == WrapTk.COMMA:
            self._match(WrapTk.COMMA)
            self._match(WrapTk.ID)
        self._match(WrapTk.COLON)
        self._match(WrapTk.ID)
        self._strTree += "]"

    def _variableDefinitionPart(self):
        self._strTree += "[<VariableDefinitionPart>"
        self._match(WrapTk.VAR)
        self._variableDefinition()
        while self._lookahead == WrapTk.ID:
            self._variableDefinition()
        self._strTree += "]"

    def _variableDefinition(self):
        self._strTree += "[<VariableDefinition>"
        self._variableGroup()
        self._match(WrapTk.SEMICOLON)
        self._strTree += "]"

    def _variableGroup(self):
        self._strTree += "[<VariableGroup>"
        self._match(WrapTk.ID)
        while self._lookahead == WrapTk.COMMA:
            self._match(WrapTk.COMMA)
            self._match(WrapTk.ID)
        self._match(WrapTk.COLON)
        self._match(WrapTk.ID)
        self._strTree += "]"

    def _procedureDefinition(self):
        self._strTree += "[<ProcedureDefinition>"
        self._match(WrapTk.PROCEDURE)
        self._match(WrapTk.ID)
        self._procedureBlock()
        self._match(WrapTk.SEMICOLON)
        self._strTree += "]"

    def _procedureBlock(self):
        self._strTree += "[<ProcedureBlock>"
        if self._lookahead == WrapTk.LEFTPARENTHESIS:
            self._match(WrapTk.LEFTPARENTHESIS)
            self._formalParameterList()
            self._match(WrapTk.RIGHTPARENTHESIS)
        self._match(WrapTk.SEMICOLON)
        self._blockBody()
        self._strTree += "]"

    def _formalParameterList(self):
        self._strTree += "[<FormalParameterList>"
        self._parameterDefinition()
        while self._lookahead == WrapTk.SEMICOLON:
            self._match(WrapTk.SEMICOLON)
            self._parameterDefinition()
        self._strTree += "]"

    def _parameterDefinition(self):
        self._strTree += "[<ParameterDefinition>"
        if self._lookahead == WrapTk.VAR:
            self._match(WrapTk.VAR)
        self._variableGroup()
        self._strTree += "]"

    def _statement(self):
        self._strTree += "[<Statement>"
        if self._lookahead == WrapTk.ID:
            self._match(WrapTk.ID)
            self._statementGroup()
        elif self._lookahead == WrapTk.IF:
            self._ifStatement()
        elif self._lookahead == WrapTk.WHILE:
            self._whileStatement()
        elif self._lookahead == WrapTk.BEGIN:
            self._compoundStatement()
        self._strTree += "]"

    def _statementGroup(self):
        self._strTree += "[<StatementGroup>"
        if self._lookahead in [WrapTk.LEFTBRACKET, WrapTk.PERIOD, WrapTk.BECOMES]:
            while self._lookahead in [WrapTk.LEFTBRACKET, WrapTk.PERIOD]:
                self._selector()
            self._match(WrapTk.BECOMES)
            self._expression()
        elif self._lookahead == WrapTk.LEFTPARENTHESIS:
            self._procedureStatement()
        else:
            self._syntaxError()
        self._strTree += "]"

    def _procedureStatement(self):
        self._strTree += "[<ProcedureStatement>"
        if self._lookahead == WrapTk.LEFTPARENTHESIS:
            self._match(WrapTk.LEFTPARENTHESIS)
            self._actualParameterList()
            self._match(WrapTk.RIGHTPARENTHESIS)
        self._strTree += "]"

    def _actualParameterList(self):
        self._strTree += "[<ActualParameterList>"
        self._expression()
        while self._lookahead == WrapTk.COMMA:
            self._match(WrapTk.COMMA)
            self._expression()
        self._strTree += "]"

    def _ifStatement(self):
        self._strTree += "[<IfStatement>"
        self._match(WrapTk.IF)
        self._expression()
        self._match(WrapTk.THEN)
        self._statement()
        if self._lookahead == WrapTk.ELSE:
            self._match(WrapTk.ELSE)
            self._statement()
        self._strTree += "]"

    def _whileStatement(self):
        self._strTree += "[<WhileStatement>"
        self._match(WrapTk.WHILE)
        self._expression()
        self._match(WrapTk.DO)
        self._statement()
        self._strTree += "]"

    def _compoundStatement(self):
        self._strTree += "[<CompoundStatement>"
        self._match(WrapTk.BEGIN)
        self._statement()
        while self._lookahead == WrapTk.SEMICOLON:
            self._match(WrapTk.SEMICOLON)
            self._statement()
        self._match(WrapTk.END)
        self._strTree += "]"

    def _expression(self):
        self._strTree += "[<Expression>"
        self._simpleExpression()
        if self._lookahead in [WrapTk.LESS, WrapTk.EQUAL, WrapTk.GREATER, WrapTk.NOTGREATER, WrapTk.NOTEQUAL, WrapTk.NOTLESS]:
            self._relationalOperator()
            self._simpleExpression()
        self._strTree += "]"

    def _relationalOperator(self):
        self._strTree += "[<RelationalOperator>"
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
        self._strTree += "]"

    def _simpleExpression(self):
        self._strTree += "[<SimpleExpression>"
        if self._lookahead in [WrapTk.PLUS, WrapTk.MINUS]:
            self._signOperator()
        self._term()
        while self._lookahead in [WrapTk.PLUS, WrapTk.MINUS, WrapTk.OR]:
            self._additiveOperator()
            self._term()
        self._strTree += "]"

    def _signOperator(self):
        self._strTree += "[<SignOperator>"
        if self._lookahead == WrapTk.PLUS:
            self._match(WrapTk.PLUS)
        elif self._lookahead == WrapTk.MINUS:
            self._match(WrapTk.MINUS)
        else:
            self._syntaxError()
        self._strTree += "]"

    def _additiveOperator(self):
        self._strTree += "[<AdditiveOperator>"
        if self._lookahead == WrapTk.PLUS:
            self._match(WrapTk.PLUS)
        elif self._lookahead == WrapTk.MINUS:
            self._match(WrapTk.MINUS)
        elif self._lookahead == WrapTk.OR:
            self._match(WrapTk.OR)
        else:
            self._syntaxError()
        self._strTree += "]"

    def _term(self):
        self._strTree += "[<Term>"
        self._factor()
        while self._lookahead in [WrapTk.ASTERISK, WrapTk.DIV, WrapTk.MOD, WrapTk.AND]:
           self._multiplyingOperator()
           self._factor()
        self._strTree += "]"

    def _multiplyingOperator(self):
        self._strTree += "[<MultiplyingOperator>"
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
        self._strTree += "]"

    def _factor(self):
        self._strTree += "[<Factor>"
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
        self._strTree += "]"

    def _selector(self):
        self._strTree += "[<Selector>"
        if self._lookahead == WrapTk.LEFTBRACKET:
            self._indexSelector()
        elif self._lookahead == WrapTk.PERIOD:
            self._fieldSelector()
        else:
            self._syntaxError()
        self._strTree += "]"

    def _indexSelector(self):
        self._strTree += "[<IndexSelector>"
        self._match(WrapTk.LEFTBRACKET)
        self._expression()
        self._match(WrapTk.RIGHTBRACKET)
        self._strTree += "]"

    def _fieldSelector(self):
        self._strTree += "[<FieldSelector>"
        self._match(WrapTk.PERIOD)
        self._match(WrapTk.ID)
        self._strTree += "]"

    def _constant(self):
        self._strTree += "[<Constant>"
        if self._lookahead == WrapTk.NUMERAL:
            self._match(WrapTk.NUMERAL)
        elif self._lookahead == WrapTk.ID:
            self._match(WrapTk.ID)
        else:
            self._syntaxError()
        self._strTree += "]"
