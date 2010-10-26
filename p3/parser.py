#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
        $Id$
Description: Analizador Sintáctico para Pascal-.
    $Author$ Lionel Aster Mena Garcia, Alejandro Samarin Perez, Sergio Armas Perez
      $Date$
  $Revision$
"""

import traceback
import sys
from lexan import LexAn
from token import *
from error import *
from ffsets import *

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
        self._ff = FFSets()
        self._linerror = 0
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
        self._program(frozenset([WrapTk.ENDTEXT]))

    def _syntaxError(self, stop):
        """ Administra los errores que se hayan podido producir durante esta etapa. Crea una excepcion que es
            capturada en el modulo 'pmc', con toda la informacion necesaria acerca del error
        """
        self._strTree += " [[IGNORED-TOKENS " + self._lookahead.getLexeme()
        if self._scanner.getPos()[0] != self._linerror:
            print "error en la linea:", self._scanner.getPos(), self._lookahead.getLexeme()
            self._linerror = self._scanner.getPos()[0]
        while self._lookahead not in stop:
            self._lookahead = self._scanner.yyLex()
            self._strTree += self._lookahead.getLexeme() + " "
        self._strTree += "]]"
        #self._strTree += "[TOKEN-ERROR]"
        # Si el error vino desde 'match', podemos saber que token esperariamos encontrar
        #if expected is not None:
            #raise SynError(SynError.UNEXPECTED_SYM, self._scanner.getPos(),
                  #" - Found '" + self._lookahead.getLexeme() + "', expected '" + Token(expected).getLexeme() + "'")
        #else:
            #raise SynError(SynError.UNEXPECTED_SYM, self._scanner.getPos(),
                  #" - Found '" + self._lookahead.getLexeme() + "'")

    def _syntaxCheck(self, stop):
        if self._lookahead not in stop:
            self._syntaxError(stop)

    def getAST(self):
        """ Retorna la cadena de descripcion del arbol de analisis sintactico para su representacion web """
        return self._strTree

    def _match(self, tok, stop):
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
                self._syntaxCheck(stop)
            else:
                self._syntaxError(stop)
        except LexError:
            raise

    # <Program> ::= program id ; <BlockBody> .
    def _program(self, stop):
        self._strTree += "[<Program>"
        self._match(WrapTk.PROGRAM, stop.union((WrapTk.ID, WrapTk.SEMICOLON, WrapTk.PERIOD), self._ff.first("blockBody")))
        self._match(WrapTk.ID, stop.union((WrapTk.SEMICOLON,WrapTk.PERIOD), self._ff.first("blockBody")))
        self._match(WrapTk.SEMICOLON, stop.union([WrapTk.PERIOD], self._ff.first("blockBody")))
        self._blockBody(stop.union([WrapTk.PERIOD]))
        self._match(WrapTk.PERIOD, stop)
        #self._match(WrapTk.ENDTEXT)
        self._strTree += "]"

    # <BlockBody> ::= [<ConstantDefinitionPart>] [<TypeDefinitionPart>] [<VariableDefinitionPart>] {<ProcedureDefinition>}
    # <CompoundStatement>
    def _blockBody(self, stop):
        self._strTree += "[<BlockBody>"
        if self._lookahead == WrapTk.CONST:
            self._constantDefinitionPart(stop.union(self._ff.first("typeDefinitionPart"), self._ff.first("variableDefinitionPart"), self._ff.first("procedureDefinition"), self._ff.first("compoundStatement")))
        if self._lookahead == WrapTk.TYPE:
            self._typeDefinitionPart(stop.union(self._ff.first("variableDefinitionPart"), self._ff.first("procedureDefinition"), self._ff.first("compoundStatement")))
        if self._lookahead == WrapTk.VAR:
            self._variableDefinitionPart(stop.union(self._ff.first("procedureDefinition"), self._ff.first("compoundStatement")))
        while self._lookahead == WrapTk.PROCEDURE:
            self._procedureDefinition(stop.union(self._ff.first("procedureDefinition"), self._ff.first("compoundStatement")))
        self._compoundStatement(stop)
        self._strTree += "]"

    # <ConstantDefinitionPart> ::= const <ConstantDefinition> {<ConstantDefinition>}
    def _constantDefinitionPart(self, stop):
        self._strTree += "[<ConstantDefinitionPart>"
        self._match(WrapTk.CONST, stop.union(self._ff.first("constantDefinition")))
        self._constantDefinition(stop.union(self._ff.first("constantDefinition")))
        while self._lookahead == WrapTk.ID:
            self._constantDefinition(stop.union(self._ff.first("constantDefinition")))
        self._strTree += "]"

    # <ConstantDefinition> ::= id = <Constant> ;
    def _constantDefinition(self, stop):
        self._strTree += "[<ConstantDefinition>"
        self._match(WrapTk.ID, stop.union((WrapTk.EQUAL, WrapTk.SEMICOLON), self._ff.first("constant")))
        self._match(WrapTk.EQUAL, stop.union([WrapTk.SEMICOLON], self._ff.first("constant")))
        self._constant(stop.union([WrapTk.SEMICOLON]))
        self._match(WrapTk.SEMICOLON, stop)
        self._strTree += "]"

    # <TypeDefinitionPart> ::= type <TypeDefinition> {<TypeDefinition>}
    def _typeDefinitionPart(self, stop):
        self._strTree += "[<TypeDefinitionPart>"
        self._match(WrapTk.TYPE, stop.union(self._ff.first("typeDefinition")))
        self._typeDefinition(stop.union(self._ff.first("typeDefinition")))
        while self._lookahead == WrapTk.ID:
            self._typeDefinition(stop.union(self._ff.first("typeDefinition")))
        self._strTree += "]"

    # <TypeDefintion> ::= id = <NewType> ;
    def _typeDefinition(self, stop):
        self._strTree += "[<TypeDefinition>"
        self._match(WrapTk.ID, stop.union((WrapTk.EQUAL, WrapTk.SEMICOLON), self._ff.first("newType")))
        self._match(WrapTk.EQUAL, stop.union([WrapTk.SEMICOLON], self._ff.first("newType")))
        self._newType(stop.union([WrapTk.SEMICOLON]))
        self._match(WrapTk.SEMICOLON, stop)
        self._strTree += "]"

    # <NewType> ::= <NewArrayType> | <NewRecordType>
    def _newType(self, stop):
        self._strTree += "[<NewType>"
        if self._lookahead == WrapTk.ARRAY:
            self._newArrayType(stop)
        elif self._lookahead == WrapTk.RECORD:
            self._newRecordType(stop)
        else:
            self._syntaxError(stop)
        self._strTree += "]"

    # <NewArrayType> ::= array [ <IndexRange> ] of id
    def _newArrayType(self, stop):
        self._strTree += "[<NewArrayType>"
        self._match(WrapTk.ARRAY, stop.union((WrapTk.LEFTBRACKET, WrapTk.RIGHTBRACKET, WrapTk.OF, WrapTk.ID), self._ff.first("indexRange")))
        self._match(WrapTk.LEFTBRACKET, stop.union((WrapTk.RIGHTBRACKET, WrapTk.OF, WrapTk.ID), self._ff.first("indexRange")))
        self._indexRange(stop.union((WrapTk.RIGHTBRACKET, WrapTk.OF, WrapTk.ID)))
        self._match(WrapTk.RIGHTBRACKET, stop.union((WrapTk.OF, WrapTk.ID)))
        self._match(WrapTk.OF, stop.union([WrapTk.ID]))
        self._match(WrapTk.ID, stop)
        self._strTree += "]"

    # <IndexRange> ::= <Constant> .. <Constant>
    def _indexRange(self, stop):
        self._strTree += "[<IndexRange>"
        self._constant(stop.union([WrapTk.DOUBLEDOT], self._ff.first("constant")))
        self._match(WrapTk.DOUBLEDOT, stop.union(self._ff.first("constant")))
        self._constant(stop)
        self._strTree += "]"

    # <NewRecordType> ::= record <FieldList> end
    def _newRecordType(self, stop):
        self._strTree += "[<NewRecordType>"
        self._match(WrapTk.RECORD, stop.union([WrapTk.END], self._ff.first("fieldList")))
        self._fieldList(stop.union([WrapTk.END]))
        self._match(WrapTk.END, stop)
        self._strTree += "]"

    # <FieldList> ::= <RecordSection> {; <RecordSection>}
    def _fieldList(self, stop):
        self._strTree += "[<FieldList>"
        self._recordSection(stop.union([WrapTk.SEMICOLON]))
        while self._lookahead == WrapTk.SEMICOLON:
            self._match(WrapTk.SEMICOLON, stop.union([WrapTk.SEMICOLON], self._ff.first("recordSection")))
            self._recordSection(stop.union([WrapTk.SEMICOLON]))
        self._strTree += "]"

    # <RecordSection> ::= id {, id} : id
    def _recordSection(self, stop):
        self._strTree += "[<RecordSection>"
        self._match(WrapTk.ID, stop.union((WrapTk.COMMA, WrapTk.ID, WrapTk.COLON)))
        while self._lookahead == WrapTk.COMMA:
            self._match(WrapTk.COMMA, stop.union((WrapTk.COMMA, WrapTk.ID, WrapTk.COLON)))
            self._match(WrapTk.ID, stop.union((WrapTk.COMMA, WrapTk.ID, WrapTk.COLON)))
        self._match(WrapTk.COLON, stop.union([WrapTk.ID]))
        self._match(WrapTk.ID, stop)
        self._strTree += "]"

    # <VariableDefinitionPart> ::= var <VariableDefinition> {<VariableDefinition>}
    def _variableDefinitionPart(self, stop):
        self._strTree += "[<VariableDefinitionPart>"
        self._match(WrapTk.VAR, stop.union(self._ff.first("variableDefinition")))
        self._variableDefinition(stop.union(self._ff.first("variableDefinition")))
        while self._lookahead == WrapTk.ID:
            self._variableDefinition(stop.union(self._ff.first("variableDefinition")))
        self._strTree += "]"

    # <VariableDefinition> ::= <VariableGroup> ;
    def _variableDefinition(self, stop):
        self._strTree += "[<VariableDefinition>"
        self._variableGroup(stop.union([WrapTk.SEMICOLON]))
        self._match(WrapTk.SEMICOLON, stop)
        self._strTree += "]"


    # <VariableGroup> ::= id {, id} : id
    def _variableGroup(self, stop):
        self._strTree += "[<VariableGroup>"
        self._match(WrapTk.ID, stop.union((WrapTk.COMMA, WrapTk.ID, WrapTk.COLON)))
        while self._lookahead == WrapTk.COMMA:
            self._match(WrapTk.COMMA, stop.union((WrapTk.COMMA, WrapTk.ID, WrapTk.COLON)))
            self._match(WrapTk.ID, stop.union((WrapTk.COMMA, WrapTk.ID, WrapTk.COLON)))
        self._match(WrapTk.COLON, stop.union([WrapTk.ID]))
        self._match(WrapTk.ID, stop)
        self._strTree += "]"

    # <ProcedureDefinition> ::= procedure id <ProcedureBlock> ;
    def _procedureDefinition(self, stop):
        self._strTree += "[<ProcedureDefinition>"
        self._match(WrapTk.PROCEDURE, stop.union((WrapTk.ID, WrapTk.SEMICOLON), self._ff.first("procedureBlock")))
        self._match(WrapTk.ID, stop.union(self._ff.first("procedureBlock"), [WrapTk.SEMICOLON]))
        self._procedureBlock(stop.union([WrapTk.SEMICOLON]))
        self._match(WrapTk.SEMICOLON, stop)
        self._strTree += "]"

    # <ProcedureBlock> ::= [( <FormalParameterList> )] ; <BlockBody>
    def _procedureBlock(self, stop):
        self._strTree += "[<ProcedureBlock>"
        if self._lookahead == WrapTk.LEFTPARENTHESIS:
            self._match(WrapTk.LEFTPARENTHESIS, stop.union((WrapTk.RIGHTPARENTHESIS, WrapTk.SEMICOLON), self._ff.first("formalParameterList"), self._ff.first("blockBody")))
            self._formalParameterList(stop.union((WrapTk.RIGHTPARENTHESIS, WrapTk.SEMICOLON), self._ff.first("blockBody")))
            self._match(WrapTk.RIGHTPARENTHESIS, stop.union([WrapTk.SEMICOLON], self._ff.first("blockBody")))
        self._match(WrapTk.SEMICOLON, stop.union(self._ff.first("blockBody")))
        self._blockBody(stop)
        self._strTree += "]"

    # <FormalParameterList> ::= <ParameterDefinition> {; <ParameterDefinition>}
    def _formalParameterList(self, stop):
        self._strTree += "[<FormalParameterList>"
        self._parameterDefinition(stop.union([WrapTk.SEMICOLON]))
        while self._lookahead == WrapTk.SEMICOLON:
            self._match(WrapTk.SEMICOLON, stop.union([WrapTk.SEMICOLON], self._ff.first("parameterDefinition")))
            self._parameterDefinition(stop.union([WrapTk.SEMICOLON]))
        self._strTree += "]"

    # <ParameterDefinition> ::= [var] <VariableGroup>
    def _parameterDefinition(self, stop):
        self._strTree += "[<ParameterDefinition>"
        if self._lookahead == WrapTk.VAR:
            self._match(WrapTk.VAR, stop.union(self._ff.first("variableGroup")))
        self._variableGroup(stop)
        self._strTree += "]"

    # <Statement> ::= id <StatementGroup> | <IfStatement> | <WhileStatement> | <CompoundStatement> | ~
    def _statement(self, stop):
        self._strTree += "[<Statement>"
        if self._lookahead == WrapTk.ID:
            self._match(WrapTk.ID, stop.union(self._ff.first("statementGroup")))
            self._statementGroup(stop)
        elif self._lookahead == WrapTk.IF:
            self._ifStatement(stop)
        elif self._lookahead == WrapTk.WHILE:
            self._whileStatement(stop)
        elif self._lookahead == WrapTk.BEGIN:
            self._compoundStatement(stop)
        else:
            self._syntaxCheck(stop)
        self._strTree += "]"

    # <StatementGroup> ::= {<Selector>} := <Expression> | <ProcedureStatement>
    def _statementGroup(self, stop):
        self._strTree += "[<StatementGroup>"
        if self._lookahead in [WrapTk.LEFTBRACKET, WrapTk.PERIOD, WrapTk.BECOMES]:
            while self._lookahead in [WrapTk.LEFTBRACKET, WrapTk.PERIOD]:
                self._selector(stop.union([WrapTk.BECOMES], self._ff.first("selector"), self._ff.first("expression")))
            self._match(WrapTk.BECOMES, stop.union(self._ff.first("expression")))
            self._expression(stop)
        elif self._lookahead == WrapTk.LEFTPARENTHESIS:
            self._procedureStatement(stop)
        else:
            self._syntaxCheck(stop)
        self._strTree += "]"

    # <ProcedureStatement> ::= ( <ActualParameterList> )
    def _procedureStatement(self, stop):
        self._strTree += "[<ProcedureStatement>"
        if self._lookahead == WrapTk.LEFTPARENTHESIS:
            self._match(WrapTk.LEFTPARENTHESIS, stop.union([WrapTk.RIGHTPARENTHESIS], self._ff.first("actualParameterList")))
            self._actualParameterList(stop.union([WrapTk.RIGHTPARENTHESIS]))
            self._match(WrapTk.RIGHTPARENTHESIS, stop)
        self._strTree += "]"

    # <ActualParameterList> ::= <Expression> {, <Expression>}
    def _actualParameterList(self, stop):
        self._strTree += "[<ActualParameterList>"
        self._expression(stop.union([WrapTk.COMMA]))
        while self._lookahead == WrapTk.COMMA:
            self._match(WrapTk.COMMA, stop.union([WrapTk.COMMA], self._ff.first("expression")))
            self._expression(stop.union([WrapTk.COMMA]))
        self._strTree += "]"

    # <IfStatement> ::= if <Expression> then <Statement> [else <Statement>]
    def _ifStatement(self, stop):
        self._strTree += "[<IfStatement>"
        self._match(WrapTk.IF, stop.union((WrapTk.THEN, WrapTk.ELSE), self._ff.first("expression"), self._ff.first("statement")))
        self._expression(stop.union((WrapTk.THEN, WrapTk.ELSE), self._ff.first("statement")))
        self._match(WrapTk.THEN, stop.union([WrapTk.ELSE], self._ff.first("statement")))
        self._statement(stop.union([WrapTk.ELSE], self._ff.first("statement")))
        self._syntaxCheck(stop.union([WrapTk.ELSE]))
        if self._lookahead == WrapTk.ELSE:
            self._match(WrapTk.ELSE, stop.union(self._ff.first("statement")))
            self._statement(stop)
        self._strTree += "]"

    # <WhileStatement> ::= while <Expression> do <Statement>
    def _whileStatement(self, stop):
        self._strTree += "[<WhileStatement>"
        self._match(WrapTk.WHILE, stop.union([WrapTk.DO], self._ff.first("expression"), self._ff.first("statement")))
        self._expression(stop.union([WrapTk.DO], self._ff.first("statement")))
        self._match(WrapTk.DO, stop.union(self._ff.first("statement")))
        self._statement(stop)
        self._strTree += "]"

    # <CompoundStatement> ::= begin <Statement> {; <Statement>} end
    def _compoundStatement(self, stop):
        self._strTree += "[<CompoundStatement>"
        self._match(WrapTk.BEGIN, stop.union((WrapTk.SEMICOLON, WrapTk.END), self._ff.first("statement")))
        self._statement(stop.union((WrapTk.SEMICOLON, WrapTk.END)))
        while self._lookahead == WrapTk.SEMICOLON:
            self._match(WrapTk.SEMICOLON, stop.union((WrapTk.SEMICOLON, WrapTk.END), self._ff.first("statement")))
            self._statement(stop.union((WrapTk.SEMICOLON, WrapTk.END)))
        self._match(WrapTk.END, stop)
        self._strTree += "]"

    # <Expression> ::= <SimpleExpression> [<RelationalOperator> <SimpleExpression>]
    def _expression(self, stop):
        self._strTree += "[<Expression>"
        self._simpleExpression(stop.union(self._ff.first("relationalOperator")))
        if self._lookahead in [WrapTk.LESS, WrapTk.EQUAL, WrapTk.GREATER, WrapTk.NOTGREATER, WrapTk.NOTEQUAL, WrapTk.NOTLESS]:
            self._relationalOperator(stop.union(self._ff.first("simpleExpression")))
            self._simpleExpression(stop)
        self._strTree += "]"

    # <RelationalOperator> ::= < | = | > | <= | <> | >=
    def _relationalOperator(self, stop):
        self._strTree += "[<RelationalOperator>"
        if self._lookahead == WrapTk.LESS:
            self._match(WrapTk.LESS, stop)
        elif self._lookahead == WrapTk.EQUAL:
            self._match(WrapTk.EQUAL, stop)
        elif self._lookahead == WrapTk.GREATER:
            self._match(WrapTk.GREATER, stop)
        elif self._lookahead == WrapTk.NOTGREATER:
            self._match(WrapTk.NOTGREATER, stop)
        elif self._lookahead == WrapTk.NOTEQUAL:
            self._match(WrapTk.NOTEQUAL, stop)
        elif self._lookahead == WrapTk.NOTLESS:
            self._match(WrapTk.NOTLESS, stop)
        else:
            self._syntaxError(stop)
        self._strTree += "]"

    # <SimpleExpression> ::= [<SignOperator>] <Term> {<AdditiveOperator> <Term>}
    def _simpleExpression(self, stop):
        self._strTree += "[<SimpleExpression>"
        if self._lookahead in [WrapTk.PLUS, WrapTk.MINUS]:
            self._signOperator(stop.union(self._ff.first("term"), self._ff.first("additiveOperator")))
        self._term(stop.union(self._ff.first("additiveOperator")))
        while self._lookahead in [WrapTk.PLUS, WrapTk.MINUS, WrapTk.OR]:
            self._additiveOperator(stop.union(self._ff.first("additiveOperator"), self._ff.first("term")))
            self._term(stop.union(self._ff.first("additiveOperator")))
        self._strTree += "]"

    # <SignOperator> ::= + | -
    def _signOperator(self, stop):
        self._strTree += "[<SignOperator>"
        if self._lookahead == WrapTk.PLUS:
            self._match(WrapTk.PLUS, stop)
        elif self._lookahead == WrapTk.MINUS:
            self._match(WrapTk.MINUS, stop)
        else:
            self._syntaxError(stop)
        self._strTree += "]"

    # <AdditiveOperator> ::= + | - | or
    def _additiveOperator(self, stop):
        self._strTree += "[<AdditiveOperator>"
        if self._lookahead == WrapTk.PLUS:
            self._match(WrapTk.PLUS, stop)
        elif self._lookahead == WrapTk.MINUS:
            self._match(WrapTk.MINUS, stop)
        elif self._lookahead == WrapTk.OR:
            self._match(WrapTk.OR, stop)
        else:
            self._syntaxError(stop)
        self._strTree += "]"

    # <Term> ::= <Factor> {<MultiplyingOperator> <Factor>}
    def _term(self, stop):
        self._strTree += "[<Term>"
        self._factor(stop.union(self._ff.first("multiplyingOperator")))
        while self._lookahead in [WrapTk.ASTERISK, WrapTk.DIV, WrapTk.MOD, WrapTk.AND]:
           self._multiplyingOperator(stop.union(self._ff.first("multiplyingOperator"), self._ff.first("factor")))
           self._factor(stop.union(self._ff.first("multiplyingOperator")))
        self._strTree += "]"

    # <MultiplyingOperator> ::= * | div | mod | and
    def _multiplyingOperator(self, stop):
        self._strTree += "[<MultiplyingOperator>"
        if self._lookahead == WrapTk.ASTERISK:
            self._match(WrapTk.ASTERISK, stop)
        elif self._lookahead == WrapTk.DIV:
            self._match(WrapTk.DIV, stop)
        elif self._lookahead == WrapTk.MOD:
            self._match(WrapTk.MOD, stop)
        elif self._lookahead == WrapTk.AND:
            self._match(WrapTk.AND, stop)
        else:
            self._syntaxError(stop)
        self._strTree += "]"

    # <Factor> ::= numeral | id {<Selector>} | ( <Expression> ) | not <Factor>
    def _factor(self, stop):
        self._strTree += "[<Factor>"
        if self._lookahead == WrapTk.NUMERAL:
            self._match(WrapTk.NUMERAL, stop)
        elif self._lookahead == WrapTk.ID:
            self._match(WrapTk.ID, stop.union(self._ff.first("selector")))
            while self._lookahead in [WrapTk.LEFTBRACKET, WrapTk.PERIOD]:
                self._selector(stop.union(self._ff.first("selector")))
        elif self._lookahead == WrapTk.LEFTPARENTHESIS:
            self._match(WrapTk.LEFTPARENTHESIS, stop.union([WrapTk.RIGHTPARENTHESIS], self._ff.first("expression")))
            self._expression(stop.union([WrapTk.RIGHTPARENTHESIS]))
            self._match(WrapTk.RIGHTPARENTHESIS, stop)
        elif self._lookahead == WrapTk.NOT:
            self._match(WrapTk.NOT, stop.union(self._ff.first("factor")))
            self._factor(stop)
        else:
            self._syntaxError(stop)
        self._strTree += "]"

    # <Selector> ::= <IndexSelector> | <FieldSelector>
    def _selector(self, stop):
        self._strTree += "[<Selector>"
        if self._lookahead == WrapTk.LEFTBRACKET:
            self._indexSelector(stop)
        elif self._lookahead == WrapTk.PERIOD:
            self._fieldSelector(stop)
        else:
            self._syntaxError(stop)
        self._strTree += "]"

    # <IndexSelector> ::= [ <Expression> ]
    def _indexSelector(self, stop):
        self._strTree += "[<IndexSelector>"
        self._match(WrapTk.LEFTBRACKET, stop.union([WrapTk.RIGHTBRACKET], self._ff.first("expression")))
        self._expression(stop.union([WrapTk.RIGHTBRACKET]))
        self._match(WrapTk.RIGHTBRACKET, stop)
        self._strTree += "]"

    # <FieldSelector> ::= . id
    def _fieldSelector(self, stop):
        self._strTree += "[<FieldSelector>"
        self._match(WrapTk.PERIOD, stop.union([WrapTk.ID]))
        self._match(WrapTk.ID, stop)
        self._strTree += "]"

    # <Constant> ::= numeral | id
    def _constant(self, stop):
        self._strTree += "[<Constant>"
        if self._lookahead == WrapTk.NUMERAL:
            self._match(WrapTk.NUMERAL, stop)
        elif self._lookahead == WrapTk.ID:
            self._match(WrapTk.ID, stop)
        else:
            self._syntaxError(stop)
        self._strTree += "]"
