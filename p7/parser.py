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
from ffsets import *
from st import *

class SynAn:
    """ Clase Analizador Sintactico:
        Comprueba que la secuencia de tokens de entrada sea acorde con las
        especificaciones de la gramatica de Pascal-
    """
    def __init__(self, stats = False):
        """ Constructor de la clase. Atributos:
            _lookahead = token o simbolo de preanalisis
            _scanner   = instancia de la clase analizador lexico
            _linerror  = almacena la linea del ultimo error mostrado (para no mostrar errores en la misma linea)
            _ff        = conjuntos de First y Follow de la gramatica de Pascal-
            _st        = Tabla de Simbolos
            _stats     = Flag para imprimir las estadisticas de la Tabla de Simbolos
        """
        self._lookahead = None
        self._idlist = []
        self._idtemp = None
        self._kindtemp = None
        self._scanner = None
        self._ff = FFSets()
        self._linerror = 0
        self._st = SymbolTable()
        self._stats = stats

    def getTrace(self):
        """ Retorna el contenido en cada momento de cada subtabla """
        return self._st.getTrace()

    def getSize(self):
        return self._st.getSize()

    def getStats(self):
        return self._st.getStats()[0], self._st.getStats()[1], self._st.getStats()[2]

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
        if self._stats:
            self._st.printStats()

    def _syntaxError(self, stop, expected=None):
        """ Administra los errores que se hayan podido producir durante esta etapa. Crea una excepcion que es
            capturada en el modulo 'pmc', con toda la informacion necesaria acerca del error
        """
        if self._lookahead == WrapTk.TOKEN_ERROR:
            self._linerror = self._scanner.getPos()[0]

        if self._scanner.getPos()[0] != self._linerror:
            SynError(SynError.UNEXPECTED_SYM, self._scanner.getPos(), self._lookahead, expected)
            self._linerror = self._scanner.getPos()[0]
        while self._lookahead not in stop:
            self._lookahead = self._scanner.yyLex()

    def _syntaxCheck(self, stop):
        """ Comprueba que el token siguiente este dentro de lo que puede esperarse a continuacion (el token
            pertenezca al conjunto de parada)
        """
        if self._lookahead not in stop:
            self._syntaxError(stop)

    def _match(self, tok, stop):
        """ Trata de emparejar el token leido con el token que espera encontrar en cada momento. Si el matching
            tuvo exito, se lee el siguiente token.
            En caso contrario, se llama al metodo syntaxError que se encargara de la gestion del error. Ademas,
            comprueba si el analizador lexico ha obtenido algun error durante la obtencion del token y, en tal caso,
            eleva la excepcion que este ultimo genera hacia el modulo 'pmc'.
        """
        try:
            if self._lookahead == tok:
                self._lookahead = self._scanner.yyLex()
                self._syntaxCheck(stop)
            else:
                self._syntaxError(stop)
        except LexError:
            raise

    # <Program> ::= program id ; <BlockBody> .
    def _program(self, stop):
        self._st.set()
        self._match(WrapTk.PROGRAM, stop.union((WrapTk.ID, WrapTk.SEMICOLON), self._ff.first("blockBody")))
        if self._lookahead == WrapTk.ID:
            if not self._st.insert(self._lookahead.getLexeme(), kind=WrapCl.VARIABLE, pos=self._scanner.getPos(),ref=True):
                SemError(SemError.REDEFINED_ID, self._scanner.getPos(), self._lookahead)
        else:
            if not self._st.insert("NoName", kind=WrapCl.VARIABLE):
                SemError(SemError.REDEFINED_ID, self._scanner.getPos(), self._lookahead)
        self._match(WrapTk.ID, stop.union([WrapTk.SEMICOLON], self._ff.first("blockBody")))
        self._match(WrapTk.SEMICOLON, stop.union(self._ff.first("blockBody")))
        self._blockBody(stop)
        self._match(WrapTk.PERIOD, stop)
        #self._match(WrapTk.ENDTEXT, stop)
        self._st.buildTrace()
        self._st.reset()

    # <BlockBody> ::= [<ConstantDefinitionPart>] [<TypeDefinitionPart>] [<VariableDefinitionPart>] {<ProcedureDefinition>}
    # <CompoundStatement>
    def _blockBody(self, stop):
        if self._lookahead == WrapTk.CONST:
            self._constantDefinitionPart(stop.union(self._ff.first("typeDefinitionPart"), self._ff.first("variableDefinitionPart"), self._ff.first("procedureDefinition"), self._ff.first("compoundStatement")))
        if self._lookahead == WrapTk.TYPE:
            self._typeDefinitionPart(stop.union(self._ff.first("variableDefinitionPart"), self._ff.first("procedureDefinition"), self._ff.first("compoundStatement")))
        if self._lookahead == WrapTk.VAR:
            self._variableDefinitionPart(stop.union(self._ff.first("procedureDefinition"), self._ff.first("compoundStatement")))
        while self._lookahead == WrapTk.PROCEDURE:
            self._procedureDefinition(stop.union(self._ff.first("procedureDefinition"), self._ff.first("compoundStatement")))
        self._compoundStatement(stop)

    # <ConstantDefinitionPart> ::= const <ConstantDefinition> {<ConstantDefinition>}
    def _constantDefinitionPart(self, stop):
        self._match(WrapTk.CONST, stop.union(self._ff.first("constantDefinition")))
        self._constantDefinition(stop.union(self._ff.first("constantDefinition")))
        while self._lookahead == WrapTk.ID:
            self._constantDefinition(stop.union(self._ff.first("constantDefinition")))

    # <ConstantDefinition> ::= id = <Constant> ;
    def _constantDefinition(self, stop):
        self._idlist = []
        # Tener cuidado con las autodefiniciones (a = a;)
        if self._lookahead == WrapTk.ID:
            self._idlist.append(self._lookahead.getLexeme())
            if not self._st.insert(self._lookahead.getLexeme(), kind=WrapCl.CONSTANT, pos=self._scanner.getPos()):
                SemError(SemError.REDEFINED_ID, self._scanner.getPos(), self._lookahead)
        else:
            if not self._st.insert("NoName", kind=CONSTANT):
                SemError(SemError.REDEFINED_ID, self._scanner.getPos(), self._lookahead)
        self._match(WrapTk.ID, stop.union((WrapTk.EQUAL, WrapTk.SEMICOLON), self._ff.first("constant")))
        self._match(WrapTk.EQUAL, stop.union([WrapTk.SEMICOLON], self._ff.first("constant")))
        self._constant(stop.union([WrapTk.SEMICOLON]))
        self._match(WrapTk.SEMICOLON, stop)

    # <TypeDefinitionPart> ::= type <TypeDefinition> {<TypeDefinition>}
    def _typeDefinitionPart(self, stop):
        self._match(WrapTk.TYPE, stop.union(self._ff.first("typeDefinition")))
        self._typeDefinition(stop.union(self._ff.first("typeDefinition")))
        while self._lookahead == WrapTk.ID:
            self._typeDefinition(stop.union(self._ff.first("typeDefinition")))

    # <TypeDefinition> ::= id = <NewType> ;
    def _typeDefinition(self, stop):
        self._idlist = []
        if self._lookahead == WrapTk.ID:
            self._idlist.append(self._lookahead.getLexeme())
            self._idtemp = self._lookahead.getLexeme()
        else:
            self._idtemp = "NoName"
        self._match(WrapTk.ID, stop.union((WrapTk.EQUAL, WrapTk.SEMICOLON), self._ff.first("newType")))
        self._match(WrapTk.EQUAL, stop.union([WrapTk.SEMICOLON], self._ff.first("newType")))
        self._newType(stop.union([WrapTk.SEMICOLON]))
        self._match(WrapTk.SEMICOLON, stop)

    # <NewType> ::= <NewArrayType> | <NewRecordType>
    def _newType(self, stop):
        if self._lookahead == WrapTk.ARRAY:
            if not self._st.insert(self._idtemp, kind=WrapCl.ARRAY_TYPE, pos=self._scanner.getPos()):
                SemError(SemError.REDEFINED_ID, self._scanner.getPos(), self._lookahead)
            self._newArrayType(stop)
        elif self._lookahead == WrapTk.RECORD:
            if not self._st.insert(self._idtemp, kind=WrapCl.RECORD_TYPE, pos=self._scanner.getPos()):
                SemError(SemError.REDEFINED_ID, self._scanner.getPos(), self._lookahead)
            self._newRecordType(stop)
        else:
            self._syntaxError(stop, self._ff.first("newType"))

    # <NewArrayType> ::= array [ <IndexRange> ] of id
    def _newArrayType(self, stop):
        self._match(WrapTk.ARRAY, stop.union((WrapTk.LEFTBRACKET, WrapTk.RIGHTBRACKET, WrapTk.OF, WrapTk.ID), self._ff.first("indexRange")))
        self._match(WrapTk.LEFTBRACKET, stop.union((WrapTk.RIGHTBRACKET, WrapTk.OF, WrapTk.ID), self._ff.first("indexRange")))
        self._indexRange(stop.union((WrapTk.RIGHTBRACKET, WrapTk.OF, WrapTk.ID)))
        self._match(WrapTk.RIGHTBRACKET, stop.union((WrapTk.OF, WrapTk.ID)))
        self._match(WrapTk.OF, stop.union([WrapTk.ID]))
        # Tener cuidado con las autodefiniciones, Ej:
        # pepe = array [1..10] of pepe;
        if self._lookahead == WrapTk.ID:
            if self._lookahead.getLexeme() not in self._idlist:
                if not self._st.lookup(self._lookahead.getLexeme()):
                    SemError(SemError.UNDECLARED_ID, self._scanner.getPos(), self._lookahead)
            else:
                SemError(SemError.REC_DEFINITION, self._scanner.getPos(), self._lookahead)
        self._match(WrapTk.ID, stop)

    # <IndexRange> ::= <Constant> .. <Constant>
    def _indexRange(self, stop):
        self._constant(stop.union([WrapTk.DOUBLEDOT], self._ff.first("constant")))
        self._match(WrapTk.DOUBLEDOT, stop.union(self._ff.first("constant")))
        self._constant(stop)

    # <NewRecordType> ::= record <FieldList> end
    def _newRecordType(self, stop):
        self._match(WrapTk.RECORD, stop.union([WrapTk.END], self._ff.first("fieldList")))
        self._fieldList(stop.union([WrapTk.END]))
        self._match(WrapTk.END, stop)

    # <FieldList> ::= <RecordSection> {; <RecordSection>}
    def _fieldList(self, stop):
        self._recordSection(stop.union([WrapTk.SEMICOLON]))
        while self._lookahead == WrapTk.SEMICOLON:
            self._match(WrapTk.SEMICOLON, stop.union([WrapTk.SEMICOLON], self._ff.first("recordSection")))
            self._recordSection(stop.union([WrapTk.SEMICOLON]))

    # <RecordSection> ::= id {, id} : id
    def _recordSection(self, stop):
        # Tener cuidado con las autodefiniciones, Ej:
        # paco = record
        #           campo1, campo2 : paco;
        #
        #        end;
        if self._lookahead == WrapTk.ID:
            self._idlist.append(self._lookahead.getLexeme())
            if not self._st.insert(self._lookahead.getLexeme(), kind=WrapCl.FIELD, pos=self._scanner.getPos()):
                SemError(SemError.REDEFINED_ID, self._scanner.getPos(), self._lookahead)
        else:
            if not self._st.insert("NoName", kind=WrapCl.FIELD):
                SemError(SemError.REDEFINED_ID, self._scanner.getPos(), self._lookahead)
        self._match(WrapTk.ID, stop.union((WrapTk.COMMA, WrapTk.ID, WrapTk.COLON)))
        while self._lookahead == WrapTk.COMMA:
            self._match(WrapTk.COMMA, stop.union((WrapTk.COMMA, WrapTk.ID, WrapTk.COLON)))
            if self._lookahead == WrapTk.ID:
                self._idlist.append(self._lookahead.getLexeme())
                if not self._st.insert(self._lookahead.getLexeme(), kind=WrapCl.FIELD, pos=self._scanner.getPos()):
                    SemError(SemError.REDEFINED_ID, self._scanner.getPos(), self._lookahead)
            else:
                if not self._st.insert("NoName", kind=WrapCl.FIELD):
                    SemError(SemError.REDEFINED_ID, self._scanner.getPos(), self._lookahead)
            self._match(WrapTk.ID, stop.union((WrapTk.COMMA, WrapTk.ID, WrapTk.COLON)))
        self._match(WrapTk.COLON, stop.union([WrapTk.ID]))
        if self._lookahead == WrapTk.ID:
            if self._lookahead.getLexeme() not in self._idlist:
                if not self._st.lookup(self._lookahead.getLexeme()):
                    SemError(SemError.UNDECLARED_ID, self._scanner.getPos(), self._lookahead)
            else:
                SemError(SemError.REDEFINED_ID, self._scanner.getPos(), self._lookahead)
        self._match(WrapTk.ID, stop)

    # <VariableDefinitionPart> ::= var <VariableDefinition> {<VariableDefinition>}
    def _variableDefinitionPart(self, stop):
        self._match(WrapTk.VAR, stop.union(self._ff.first("variableDefinition")))
        self._variableDefinition(stop.union(self._ff.first("variableDefinition")))
        while self._lookahead == WrapTk.ID:
            self._variableDefinition(stop.union(self._ff.first("variableDefinition")))

    # <VariableDefinition> ::= <VariableGroup> ;
    def _variableDefinition(self, stop):
        self._kindtemp = WrapCl.VARIABLE
        self._variableGroup(stop.union([WrapTk.SEMICOLON]))
        self._match(WrapTk.SEMICOLON, stop)

    # <VariableGroup> ::= id {, id} : id
    def _variableGroup(self, stop):
        self._idlist = []
        if self._lookahead == WrapTk.ID:
            self._idlist.append(self._lookahead.getLexeme())
            if not self._st.insert(self._lookahead.getLexeme(), kind=self._kindtemp, pos=self._scanner.getPos()):
                SemError(SemError.REDEFINED_ID, self._scanner.getPos(), self._lookahead)
        else:
            if not self._st.insert("NoName", kind=self._kindtemp):
                SemError(SemError.REDEFINED_ID, self._scanner.getPos(), self._lookahead)
        self._match(WrapTk.ID, stop.union((WrapTk.COMMA, WrapTk.ID, WrapTk.COLON)))
        while self._lookahead == WrapTk.COMMA:
            self._match(WrapTk.COMMA, stop.union((WrapTk.COMMA, WrapTk.ID, WrapTk.COLON)))
            if self._lookahead == WrapTk.ID:
                self._idlist.append(self._lookahead.getLexeme())
                if not self._st.insert(self._lookahead.getLexeme(), kind=self._kindtemp, pos=self._scanner.getPos()):
                    SemError(SemError.REDEFINED_ID, self._scanner.getPos(), self._lookahead)
            else:
                if not self._st.insert("NoName", kind=self._kindtemp):
                    SemError(SemError.REDEFINED_ID, self._scanner.getPos(), self._lookahead)
            self._match(WrapTk.ID, stop.union((WrapTk.COMMA, WrapTk.ID, WrapTk.COLON)))
        self._match(WrapTk.COLON, stop.union([WrapTk.ID]))
        if (self._lookahead == WrapTk.ID):
            if (self._lookahead.getLexeme() not in self._idlist):
                if not self._st.lookup(self._lookahead.getLexeme()):
                    SemError(SemError.UNDECLARED_ID, self._scanner.getPos(), self._lookahead)
            else:
                SemError(SemError.REDEFINED_ID, self._scanner.getPos(), self._lookahead)

        self._match(WrapTk.ID, stop)

    # <ProcedureDefinition> ::= procedure id <ProcedureBlock> ;
    def _procedureDefinition(self, stop):
        self._match(WrapTk.PROCEDURE, stop.union((WrapTk.ID, WrapTk.SEMICOLON), self._ff.first("procedureBlock")))
        if self._lookahead == WrapTk.ID:
            if not self._st.insert(self._lookahead.getLexeme(), kind=WrapCl.PROCEDURE, pos=self._scanner.getPos()):
                SemError(SemError.REDEFINED_ID, self._scanner.getPos(), self._lookahead)
        else:
            if not self._st.insert("NoName", kind=WrapCl.PROCEDURE):
                SemError(SemError.REDEFINED_ID, self._scanner.getPos(), self._lookahead)
        self._match(WrapTk.ID, stop.union(self._ff.first("procedureBlock"), [WrapTk.SEMICOLON]))
        self._procedureBlock(stop.union([WrapTk.SEMICOLON]))
        self._match(WrapTk.SEMICOLON, stop)

    # <ProcedureBlock> ::= [( <FormalParameterList> )] ; <BlockBody>
    def _procedureBlock(self, stop):
        self._st.set()
        if self._lookahead == WrapTk.LEFTPARENTHESIS:
            self._match(WrapTk.LEFTPARENTHESIS, stop.union((WrapTk.RIGHTPARENTHESIS, WrapTk.SEMICOLON), self._ff.first("formalParameterList"), self._ff.first("blockBody")))
            self._formalParameterList(stop.union((WrapTk.RIGHTPARENTHESIS, WrapTk.SEMICOLON), self._ff.first("blockBody")))
            self._match(WrapTk.RIGHTPARENTHESIS, stop.union([WrapTk.SEMICOLON], self._ff.first("blockBody")))
        self._match(WrapTk.SEMICOLON, stop.union(self._ff.first("blockBody")))
        self._blockBody(stop)
        self._st.buildTrace()
        self._st.reset()

    # <FormalParameterList> ::= <ParameterDefinition> {; <ParameterDefinition>}
    def _formalParameterList(self, stop):
        self._parameterDefinition(stop.union([WrapTk.SEMICOLON]))
        while self._lookahead == WrapTk.SEMICOLON:
            self._match(WrapTk.SEMICOLON, stop.union([WrapTk.SEMICOLON], self._ff.first("parameterDefinition")))
            self._parameterDefinition(stop.union([WrapTk.SEMICOLON]))

    # <ParameterDefinition> ::= [var] <VariableGroup>
    def _parameterDefinition(self, stop):
        if self._lookahead == WrapTk.VAR:
            self._kindtemp = WrapCl.VAR_PARAMETER
            self._match(WrapTk.VAR, stop.union(self._ff.first("variableGroup")))
        else:
            self._kindtemp = WrapCl.VALUE_PARAMETER
        self._variableGroup(stop)

    # <Statement> ::= id <StatementGroup> | <IfStatement> | <WhileStatement> | <CompoundStatement> | ~
    def _statement(self, stop):
        if self._lookahead == WrapTk.ID:
            if not self._st.lookup(self._lookahead.getLexeme()):
                SemError(SemError.UNDECLARED_ID, self._scanner.getPos(), self._lookahead)
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

    # <StatementGroup> ::= {<Selector>} := <Expression> | <ProcedureStatement>
    def _statementGroup(self, stop):
        if self._lookahead in [WrapTk.LEFTBRACKET, WrapTk.PERIOD, WrapTk.BECOMES]:
            while self._lookahead in [WrapTk.LEFTBRACKET, WrapTk.PERIOD]:
                self._selector(stop.union([WrapTk.BECOMES], self._ff.first("selector"), self._ff.first("expression")))
            self._match(WrapTk.BECOMES, stop.union(self._ff.first("expression")))
            self._expression(stop)
        elif self._lookahead == WrapTk.LEFTPARENTHESIS:
            self._procedureStatement(stop)
        else:
            self._syntaxCheck(stop)

    # <ProcedureStatement> ::= [( <ActualParameterList> )]
    def _procedureStatement(self, stop):
        if self._lookahead == WrapTk.LEFTPARENTHESIS:
            self._match(WrapTk.LEFTPARENTHESIS, stop.union([WrapTk.RIGHTPARENTHESIS], self._ff.first("actualParameterList")))
            self._actualParameterList(stop.union([WrapTk.RIGHTPARENTHESIS]))
            self._match(WrapTk.RIGHTPARENTHESIS, stop)

    # <ActualParameterList> ::= <Expression> {, <Expression>}
    def _actualParameterList(self, stop):
        self._expression(stop.union([WrapTk.COMMA]))
        while self._lookahead == WrapTk.COMMA:
            self._match(WrapTk.COMMA, stop.union([WrapTk.COMMA], self._ff.first("expression")))
            self._expression(stop.union([WrapTk.COMMA]))

    # <IfStatement> ::= if <Expression> then <Statement> [else <Statement>]
    def _ifStatement(self, stop):
        self._match(WrapTk.IF, stop.union((WrapTk.THEN, WrapTk.ELSE), self._ff.first("expression"), self._ff.first("statement")))
        self._expression(stop.union((WrapTk.THEN, WrapTk.ELSE), self._ff.first("statement")))
        self._match(WrapTk.THEN, stop.union([WrapTk.ELSE], self._ff.first("statement")))
        self._statement(stop.union([WrapTk.ELSE], self._ff.first("statement")))
        self._syntaxCheck(stop.union([WrapTk.ELSE]))
        if self._lookahead == WrapTk.ELSE:
            self._match(WrapTk.ELSE, stop.union(self._ff.first("statement")))
            self._statement(stop)

    # <WhileStatement> ::= while <Expression> do <Statement>
    def _whileStatement(self, stop):
        self._match(WrapTk.WHILE, stop.union([WrapTk.DO], self._ff.first("expression"), self._ff.first("statement")))
        self._expression(stop.union([WrapTk.DO], self._ff.first("statement")))
        self._match(WrapTk.DO, stop.union(self._ff.first("statement")))
        self._statement(stop)

    # <CompoundStatement> ::= begin <Statement> {; <Statement>} end
    def _compoundStatement(self, stop):
        self._match(WrapTk.BEGIN, stop.union((WrapTk.SEMICOLON, WrapTk.END), self._ff.first("statement")))
        self._statement(stop.union((WrapTk.SEMICOLON, WrapTk.END)))
        while self._lookahead == WrapTk.SEMICOLON:
            self._match(WrapTk.SEMICOLON, stop.union((WrapTk.SEMICOLON, WrapTk.END), self._ff.first("statement")))
            self._statement(stop.union((WrapTk.SEMICOLON, WrapTk.END)))
        self._match(WrapTk.END, stop.union([WrapTk.PERIOD]))

    # <Expression> ::= <SimpleExpression> [<RelationalOperator> <SimpleExpression>]
    def _expression(self, stop):
        self._simpleExpression(stop.union(self._ff.first("relationalOperator")))
        if self._lookahead in [WrapTk.LESS, WrapTk.EQUAL, WrapTk.GREATER, WrapTk.NOTGREATER, WrapTk.NOTEQUAL, WrapTk.NOTLESS]:
            self._relationalOperator(stop.union(self._ff.first("simpleExpression")))
            self._simpleExpression(stop)

    # <RelationalOperator> ::= < | = | > | <= | <> | >=
    def _relationalOperator(self, stop):
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
            self._syntaxError(stop, self._ff.first("relationalOperator"))

    # <SimpleExpression> ::= [<SignOperator>] <Term> {<AdditiveOperator> <Term>}
    def _simpleExpression(self, stop):
        if self._lookahead in [WrapTk.PLUS, WrapTk.MINUS]:
            self._signOperator(stop.union(self._ff.first("term"), self._ff.first("additiveOperator")))
        self._term(stop.union(self._ff.first("additiveOperator")))
        while self._lookahead in [WrapTk.PLUS, WrapTk.MINUS, WrapTk.OR]:
            self._additiveOperator(stop.union(self._ff.first("additiveOperator"), self._ff.first("term")))
            self._term(stop.union(self._ff.first("additiveOperator")))

    # <SignOperator> ::= + | -
    def _signOperator(self, stop):
        if self._lookahead == WrapTk.PLUS:
            self._match(WrapTk.PLUS, stop)
        elif self._lookahead == WrapTk.MINUS:
            self._match(WrapTk.MINUS, stop)
        else:
            self._syntaxError(stop, self._ff.first("signOperator"))

    # <AdditiveOperator> ::= + | - | or
    def _additiveOperator(self, stop):
        if self._lookahead == WrapTk.PLUS:
            self._match(WrapTk.PLUS, stop)
        elif self._lookahead == WrapTk.MINUS:
            self._match(WrapTk.MINUS, stop)
        elif self._lookahead == WrapTk.OR:
            self._match(WrapTk.OR, stop)
        else:
            self._syntaxError(stop, self._ff.first("additiveOperator"))

    # <Term> ::= <Factor> {<MultiplyingOperator> <Factor>}
    def _term(self, stop):
        self._factor(stop.union(self._ff.first("multiplyingOperator")))
        while self._lookahead in [WrapTk.ASTERISK, WrapTk.DIV, WrapTk.MOD, WrapTk.AND]:
           self._multiplyingOperator(stop.union(self._ff.first("multiplyingOperator"), self._ff.first("factor")))
           self._factor(stop.union(self._ff.first("multiplyingOperator")))

    # <MultiplyingOperator> ::= * | div | mod | and
    def _multiplyingOperator(self, stop):
        if self._lookahead == WrapTk.ASTERISK:
            self._match(WrapTk.ASTERISK, stop)
        elif self._lookahead == WrapTk.DIV:
            self._match(WrapTk.DIV, stop)
        elif self._lookahead == WrapTk.MOD:
            self._match(WrapTk.MOD, stop)
        elif self._lookahead == WrapTk.AND:
            self._match(WrapTk.AND, stop)
        else:
            self._syntaxError(stop, self._ff.first("multiplyingOperator"))

    # <Factor> ::= numeral | id {<Selector>} | ( <Expression> ) | not <Factor>
    def _factor(self, stop):
        if self._lookahead == WrapTk.NUMERAL:
            self._match(WrapTk.NUMERAL, stop)
        elif self._lookahead == WrapTk.ID:
            if not self._st.lookup(self._lookahead.getLexeme()):
                SemError(SemError.UNDECLARED_ID, self._scanner.getPos(), self._lookahead)
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
            self._syntaxError(stop, self._ff.first("factor"))

    # <Selector> ::= <IndexSelector> | <FieldSelector>
    def _selector(self, stop):
        if self._lookahead == WrapTk.LEFTBRACKET:
            self._indexSelector(stop)
        elif self._lookahead == WrapTk.PERIOD:
            self._fieldSelector(stop)
        else:
            self._syntaxError(stop, self._ff.first("selector"))

    # <IndexSelector> ::= [ <Expression> ]
    def _indexSelector(self, stop):
        self._match(WrapTk.LEFTBRACKET, stop.union([WrapTk.RIGHTBRACKET], self._ff.first("expression")))
        self._expression(stop.union([WrapTk.RIGHTBRACKET]))
        self._match(WrapTk.RIGHTBRACKET, stop)

    # <FieldSelector> ::= . id
    def _fieldSelector(self, stop):
        self._match(WrapTk.PERIOD, stop.union([WrapTk.ID]))
        if self._lookahead == WrapTk.ID:
            if not self._st.lookup(self._lookahead.getLexeme()):
                SemError(SemError.UNDECLARED_ID, self._scanner.getPos(), self._lookahead)
        self._match(WrapTk.ID, stop)

    # <Constant> ::= numeral | id
    def _constant(self, stop):
        if self._lookahead == WrapTk.NUMERAL:
            self._match(WrapTk.NUMERAL, stop)
        elif self._lookahead == WrapTk.ID:
            if (self._lookahead.getLexeme() not in self._idlist):
                if not self._st.lookup(self._lookahead.getLexeme()):
                    SemError(SemError.UNDECLARED_ID, self._scanner.getPos(), self._lookahead)
            else:
                SemError(SemError.REDEFINED_ID, self._scanner.getPos(), self._lookahead)
            self._match(WrapTk.ID, stop)
        else:
            self._syntaxError(stop, self._ff.first("constant"))
