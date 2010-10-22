(* ************************************************
 *  MODULO DE ANALISIS SINTACTICO CON MODO PANICO
 * ************************************************
 * AUTOR : Alejandro Samarin Perez
 * ALU   : 3862
 * FECHA : 28/10/2009
 *
 * DESCRIPCION: Este analizador sintactico corres-
 * ponde a la practica num. 3 de la asignatura de
 * Compiladores de la ULL. Examina la secuencia de 
 * tokens obtenida por el analizador lexico a par-
 * tir del fichero fuente, y determina si la estruc-
 * tura resultante es valida sintacticamente, segun
 * especifica la gramatica de Pascal-. Ademas, im-
 * plementa el modo panico de recuperacion de erro-
 * res, con el que el programa es capaz de continuar
 * el proceso de compilacion para encontrar el mayor
 * numero posible de errores en un solo paso
 * ************************************************)

unit synan;

interface

uses lexan;

type  
   token_set = set of token;

var
   lookahead : token;
   argvalue  : argtype;
   line_error : integer = 0; (* Almacena la ultima linea en la que se produjo error *)
   err_found : boolean = false;

procedure match (tok : token; stop : token_set);
procedure syntax_error (stop : token_set);

procedure programm_ (stop : token_set);
procedure block_body (stop : token_set);
procedure constant_definition_part (stop : token_set);
procedure constant_definition (stop : token_set);
procedure type_definition_part (stop : token_set);
procedure type_definition (stop : token_set);
procedure new_type (stop : token_set);
procedure new_array_type (stop : token_set);
procedure index_range (stop : token_set);
procedure new_record_type (stop : token_set);
procedure field_list (stop : token_set);
procedure record_section (stop : token_set);
procedure variable_definition_part (stop : token_set);
procedure variable_definition (stop : token_set);
procedure variable_group (stop : token_set);
procedure procedure_definition (stop : token_set);
procedure procedure_block (stop : token_set);
procedure formal_parameter_list (stop : token_set);
procedure parameter_definition (stop : token_set);
procedure statement (stop : token_set);
procedure statement2 (stop : token_set);
procedure assignment_statement (stop : token_set);
procedure procedure_statement (stop : token_set);
procedure actual_parameter_list (stop : token_set);
procedure if_statement (stop : token_set);
procedure while_statement (stop : token_set);
procedure compound_statement (stop : token_set);
procedure expression (stop : token_set);
procedure relational_operator (stop : token_set);
procedure simple_expression (stop : token_set);
procedure sign_operator (stop : token_set);
procedure additive_operator (stop : token_set);
procedure term (stop : token_set);
procedure multiplying_operator (stop : token_set);
procedure factor (stop : token_set);
procedure factor2 (stop : token_set);
procedure variable_access (stop : token_set);
procedure selector (stop : token_set); 
procedure index_selector (stop : token_set);
procedure field_selector (stop : token_set); 
procedure constant (stop : token_set);

implementation

const
   block_body_1st             = [CONST_, TYPE_, VAR_, PROCEDURE_, BEGIN_];
   statement_1st              = [ID_, IF_, WHILE_, BEGIN_];
   statement2_1st             = [LEFTPARENTHESIS_, LEFTBRACKET_, PERIOD_, BECOMES_];
   actual_parameter_list_1st  = [PLUS_, MINUS_, NUMERAL_, ID_, LEFTPARENTHESIS_, NOT_];
   expression_1st             = [PLUS_, MINUS_, NUMERAL_, ID_, LEFTPARENTHESIS_, NOT_];
   rel_operator_1st           = [LESS_, EQUAL_, GREATER_, NOTGREATER_, NOTEQUAL_, NOTLESS_];
   simple_expression_1st      = [PLUS_, MINUS_, NUMERAL_, ID_, LEFTPARENTHESIS_, NOT_];
   term_1st                   = [NUMERAL_, ID_, LEFTPARENTHESIS_, NOT_];
   multiplying_op_1st         = [ASTERISK_, DIV_, MOD_, AND_];
   factor_1st                 = [NUMERAL_, ID_, LEFTPARENTHESIS_, NOT_];


(* Despues de un error sintactico, el analizador ignora la
   entrada hasta que alcanza uno de los simbolos de parada *)
procedure syntax_error (stop : token_set);
begin
   if line_error <> line_num then begin    (* Si no se ha producido un error anterior en la misma linea *)
      err_found := true;
      if (lookahead = TOKEN_ERROR_) then     
         writeln (err_reason)
      else
         (* writeln (line_num, ': SYN_ERROR [Encontrado ', printable_tok[ord (lookahead)], ']'); *)
         writeln(line_num);
      line_error := line_num;
      while not (lookahead in stop) do begin
         lookahead := yylex (argvalue);
         (* writeln('saltando -> ', printable_tok[ord(lookahead)]); *)
      end;
   end;
end;

(* Despues de examinar el token actual, el analizador siempre se asegura 
   que el siguiente simbolo sea uno de los simbolos de parada esperados *)
procedure syntax_check (stop : token_set);
begin
   if not (lookahead in stop) then
      syntax_error (stop);
end;

procedure match (tok : token; stop : token_set);
begin
   if (lookahead = tok) then begin
      lookahead := yylex (argvalue);
      syntax_check (stop);
   end
   else
      syntax_error (stop);
end;

(* <program> ::= PROGRAM ID SEMICOLON <block_body> PERIOD *)
procedure programm_ (stop : token_set);
begin
   match (PROGRAM_, stop + [ID_, SEMICOLON_, PERIOD_] + block_body_1st);
   match (ID_, stop + [SEMICOLON_, PERIOD_] + block_body_1st);
   match (SEMICOLON_, stop + [PERIOD_] + block_body_1st);
   block_body (stop + [PERIOD_]);
   match (PERIOD_, stop);
   (* match (ENDTEXT_); *)
end;

(* <block_body> ::= [<constant_definition_part>]
                    [<type_definition_part>]
                    <variable_definition_part>]
                    /<procedure_definition>/
                    <compound_statement>*)
procedure block_body (stop : token_set);
begin
   if (lookahead = CONST_) then
      constant_definition_part (stop + [TYPE_, VAR_, PROCEDURE_, BEGIN_]);
   if (lookahead = TYPE_) then
      type_definition_part (stop + [VAR_, PROCEDURE_, BEGIN_]);
   if (lookahead = VAR_) then
      variable_definition_part (stop + [PROCEDURE_, BEGIN_]);
   syntax_check(stop + [PROCEDURE_]);
   while (lookahead = PROCEDURE_) do
      procedure_definition (stop + [PROCEDURE_, BEGIN_]);
   compound_statement (stop);
end;

(* <constant_definition_part> ::= CONST
                                 <constant_definition>
                                 /<constant_definition>/
*)
procedure constant_definition_part (stop : token_set);
begin
   match (CONST_, stop + [ID_]);
   constant_definition (stop + [ID_]);
   while (lookahead = ID_) do
      constant_definition (stop + [ID_]);
end;

(* <constant_deﬁnition> ::= ID = <constant> ; *)
procedure constant_definition (stop : token_set);
begin
   match (ID_, stop + [EQUAL_, NUMERAL_, ID_, SEMICOLON_]);
   match (EQUAL_, stop + [NUMERAL_, ID_, SEMICOLON_]);
   constant (stop + [SEMICOLON_]);
   match (SEMICOLON_, stop);
end;

(* <type_deﬁnition_part> ::= TYPE <type_deﬁnition> 
                            /<type_deﬁnition>/
*)
procedure type_definition_part (stop : token_set);
begin
   match (TYPE_, stop + [ID_]);
   type_definition (stop + [ID_]);
   while (lookahead = ID_) do
      type_definition (stop + [ID_]);
end;

(* <type_deﬁnition> ::= ID = <new_type> ; *)
procedure type_definition (stop : token_set);
begin
   match (ID_, stop + [EQUAL_, ARRAY_, RECORD_, SEMICOLON_]);
   match (EQUAL_, stop + [ARRAY_, RECORD_, SEMICOLON_]);
   new_type (stop + [SEMICOLON_]);
   match (SEMICOLON_, stop);
end;

(* <new_type> ::= <new_array type> | <new_record_type> *)
procedure new_type (stop : token_set);
begin
   if (lookahead = ARRAY_) then
      new_array_type (stop)
   else if (lookahead = RECORD_) then
      new_record_type (stop)
   else
      syntax_error (stop);
end;

(* <new_array_type> ::= ARRAY "[" <index_range> "]" OF ID *)
procedure new_array_type (stop : token_set);
begin
   match (ARRAY_, stop + [LEFTBRACKET_, NUMERAL_, ID_, RIGHTBRACKET_, OF_]);
   match (LEFTBRACKET_, stop + [NUMERAL_, ID_, RIGHTBRACKET_, OF_]);
   index_range (stop + [RIGHTBRACKET_, OF_, ID_]);
   match (RIGHTBRACKET_, stop + [OF_, ID_]);
   match (OF_, stop + [ID_]);
   match (ID_, stop);
end;

(* <index_range> ::= <constant> .. <constant> *)
procedure index_range (stop : token_set);
begin
   constant (stop + [DOUBLEDOT_, ID_, NUMERAL_]);
   match (DOUBLEDOT_, stop + [ID_, NUMERAL_]);
   constant (stop);
end;

(* <new_record_type> ::= RECORD <field_list> END *)
procedure new_record_type (stop : token_set);
begin
   match (RECORD_, stop + [ID_, END_]);
   field_list (stop + [END_]);
   match (END_, stop);
end;

(* <field_list> ::= <record_section> /; <record_section>/ *)
procedure field_list (stop : token_set);
begin
   record_section (stop + [SEMICOLON_]);
   while (lookahead = SEMICOLON_) do begin
      match (SEMICOLON_, stop + [ID_, SEMICOLON_]);
      record_section (stop + [SEMICOLON_]);
   end;
end;

(* <record_section> ::= ID /, ID/ : ID *)
procedure record_section (stop : token_set);
begin
   match (ID_, stop + [COMMA_, ID_, COLON_]);
   while (lookahead = COMMA_) do begin
      match (COMMA_, stop + [ID_, COMMA_, COLON_]);
      match (ID_, stop + [ID_, COMMA_, COLON_]);
   end;
   match (COLON_, stop + [ID_]);
   match (ID_, stop);
end;

(* <variable_deﬁnition_part> ::= VAR <variable_deﬁnition> 
                                /<variable_deﬁnition>/
*)
procedure variable_definition_part (stop : token_set);
begin
   match (VAR_, stop + [ID_]);
   variable_definition (stop + [ID_]);
   while (lookahead = ID_) do
      variable_definition (stop + [ID_]);
end;

(* <variable_deﬁnition> ::= <variable_group> ; *)
procedure variable_definition (stop : token_set);
begin
   variable_group (stop + [SEMICOLON_]);
   match (SEMICOLON_, stop);
end;

(* <variable_group> ::= ID /, ID/ : ID *)
procedure variable_group (stop : token_set);
begin
   match (ID_, stop + [COMMA_, ID_, COLON_]);
   while (lookahead = COMMA_) do begin
      match (COMMA_, stop + [COMMA_, COLON_, ID_]);
      match (ID_, stop + [COMMA_, COLON_, ID_]);
   end;
   match (COLON_, stop + [ID_]);
   match (ID_, stop);
end;

(* <procedure_deﬁnition> ::= PROCEDURE ID 
                            <procedure_block> ;
*)
procedure procedure_definition (stop : token_set); 
begin
   match (PROCEDURE_, stop + [ID_, LEFTPARENTHESIS_, SEMICOLON_]);
   match (ID_, stop + [LEFTPARENTHESIS_, SEMICOLON_]);
   procedure_block (stop + [SEMICOLON_]);
   match (SEMICOLON_, stop);
end;

(* <procedure_block> ::= [( <formal_parameter_list> )] ;
                        <block_body>
*)
procedure procedure_block (stop : token_set);
begin
   if (lookahead = LEFTPARENTHESIS_) then begin
      match (LEFTPARENTHESIS_, stop + [VAR_, ID_, RIGHTPARENTHESIS_, SEMICOLON_] + block_body_1st);
      formal_parameter_list (stop + [RIGHTPARENTHESIS_, SEMICOLON_] + block_body_1st);
      match (RIGHTPARENTHESIS_, stop + [SEMICOLON_] + block_body_1st);
   end;
   match (SEMICOLON_, stop + block_body_1st);
   block_body (stop);
end;

(* <formal_parameter_list> ::= <parameter_deﬁnition> 
                              /; <parameter_deﬁnition>/
*)
procedure formal_parameter_list (stop : token_set);
begin
   parameter_definition (stop + [SEMICOLON_]);
   while (lookahead = SEMICOLON_) do begin
      match (SEMICOLON_, stop + [VAR_, ID_, SEMICOLON_]);
      parameter_definition (stop + [SEMICOLON_]);
   end;
end;

(* <parameter_deﬁnition> ::= [VAR] <variable_group> *)
procedure parameter_definition (stop : token_set);
begin
   if (lookahead = VAR_) then
      match (VAR_, stop + [ID_]);
   variable_group (stop);
end;

(* <statement> ::= ID <statement2> | 
                  <if_statement> | 
                  <while_statement> | 
                  <compound_statement> |
                  e
*)
procedure statement (stop : token_set);
begin
   if (lookahead = ID_) then begin
      match (ID_, stop + statement2_1st);
      statement2 (stop);
   end
   else if (lookahead = IF_) then
      if_statement (stop)
   else if (lookahead = WHILE_) then
      while_statement (stop)
   else if (lookahead = BEGIN_) then
      compound_statement (stop)
   else
      syntax_check (stop);
end;

(* <statement2> ::= <procedure_statement> | /<selector>/
                                           BECOMES
                                           <expression>
                                         | e
*) 
procedure statement2 (stop : token_set);
begin
   if (lookahead = LEFTPARENTHESIS_) then
      procedure_statement (stop)
   else if (lookahead in [LEFTBRACKET_, PERIOD_, BECOMES_]) then begin
      while (lookahead in [LEFTBRACKET_, PERIOD_]) do
         selector (stop + [LEFTBRACKET_, PERIOD_, BECOMES_] + expression_1st);
      match (BECOMES_, stop + expression_1st);
      expression (stop);
   end
   else
      syntax_check (stop);
end;

(* <assignment_statement> ::= <variable_access> 
                              BECOMES 
                              <expression> *) 
procedure assignment_statement (stop : token_set);
begin
   variable_access (stop + [BECOMES_] + expression_1st);
   match (BECOMES_, stop + expression_1st);
   expression (stop);
end;

(* <procedure_statement> ::= [LEFTPARENTHESIS
                             <actual_parameter_list>
                             RIGHTPARENTHESIS] *)
procedure procedure_statement (stop : token_set);
begin
   if (lookahead = LEFTPARENTHESIS_) then begin
      match (LEFTPARENTHESIS_, stop + actual_parameter_list_1st + [RIGHTPARENTHESIS_]);
      actual_parameter_list (stop + [RIGHTPARENTHESIS_]);
      match (RIGHTPARENTHESIS_, stop);
   end;
end;

(* <actual_parameter_list> ::= <actual_parameter> 
                               /COMMA <actual_parameter/ *)
procedure actual_parameter_list (stop : token_set);
begin
   expression (stop + [COMMA_]);
   while (lookahead = COMMA_) do begin
      match (COMMA_, stop + expression_1st + [COMMA_]);
      expression (stop + [COMMA_]);
   end;        
end;

(* <if_statement> ::= IF <expression> THEN <statement>
                      [ELSE <statement>] *)
procedure if_statement (stop : token_set);
begin
   match (IF_, stop + expression_1st + [THEN_, ELSE_] + statement_1st);
   expression (stop + [THEN_, ELSE_] + statement_1st);
   match (THEN_, stop + [ELSE_] + statement_1st);
   statement (stop + [ELSE_] + statement_1st);
   if (lookahead = ELSE_) then begin
      match (ELSE_, stop + statement_1st);
      statement (stop);
   end;
end;

(* <while_statement> ::= WHILE <expression> DO <statement> *)
procedure while_statement (stop : token_set);
begin
   match (WHILE_, stop + expression_1st + [DO_] + statement_1st);
   expression (stop + [DO_] + statement_1st);
   match (DO_, stop + statement_1st);
   statement (stop);
end;

(* <compound_statement> ::= BEGIN <statement> /; <statement>/ END *)
procedure compound_statement (stop : token_set);
begin
   match (BEGIN_, stop + statement_1st + [SEMICOLON_, END_]);
   statement (stop + [SEMICOLON_, END_]);
   while (lookahead = SEMICOLON_) do begin
      match (SEMICOLON_, stop + [SEMICOLON_, END_] + statement_1st);
      statement (stop + [SEMICOLON_, END_]);
   end;
   match (END_, stop);
end;

(* <expression> ::= <simple_expression> 
                    [<relational_operator> <simple_expression>] *)
procedure expression (stop : token_set);
begin
   simple_expression (stop + rel_operator_1st);
   if (lookahead in [LESS_, EQUAL_, GREATER_, NOTGREATER_, NOTEQUAL_, NOTLESS_]) then begin
      relational_operator (stop + simple_expression_1st);
      simple_expression (stop);
   end;
end;

(* <relational_operator> ::= LESS | EQUAL | GREATER | NOTGREATER | NOTEQUAL | NOTLESS *)
procedure relational_operator (stop : token_set);
begin
   if (lookahead = LESS_) then
      match (LESS_, stop)
   else if (lookahead = EQUAL_) then
      match (EQUAL_, stop)
   else if (lookahead = GREATER_) then
      match (GREATER_, stop)
   else if (lookahead = NOTGREATER_) then
      match (NOTGREATER_, stop)
   else if (lookahead = NOTEQUAL_) then
      match (NOTEQUAL_, stop)
   else if (lookahead = NOTLESS_) then
      match (NOTLESS_, stop)
   else
      syntax_error (stop);
end;

(* <simple_expression> ::= [<sign_operator>] <term> /<additive_operator> <term>/ *)
procedure simple_expression (stop : token_set);
begin
   if (lookahead in [PLUS_, MINUS_]) then
      sign_operator (stop + term_1st + [PLUS_, MINUS_, OR_]);
   term (stop + [PLUS_, MINUS_, OR_] + term_1st);
   while (lookahead in [PLUS_, MINUS_, OR_]) do begin
      additive_operator (stop + [PLUS_, MINUS_, OR_] + term_1st);
      term (stop + [PLUS_, MINUS_, OR_]);
   end;
end;

(* <sign_operator> ::= PLUS | MINUS *)
procedure sign_operator (stop : token_set);
begin
   if (lookahead = PLUS_) then
      match (PLUS_, stop)
   else if (lookahead = MINUS_) then
      match (MINUS_, stop)
   else
      syntax_error (stop);
end;

(* <additive_operator> ::= PLUS | MINUS | OR *)
procedure additive_operator (stop : token_set);
begin
   if (lookahead = PLUS_) then
      match (PLUS_, stop)
   else if (lookahead = MINUS_) then
      match (MINUS_, stop)
   else if (lookahead = OR_) then
      match (OR_, stop)
   else
      syntax_error (stop);
end;

(* <term> ::= <factor> /<multiplying_operator> <factor>/ *)
procedure term (stop : token_set);
begin
   factor (stop + multiplying_op_1st);
   while (lookahead in [ASTERISK_, DIV_, MOD_, AND_]) do begin
      multiplying_operator (stop + factor_1st + multiplying_op_1st);
      factor (stop + multiplying_op_1st);
   end;
end;

(* <multiplying_operator> ::= ASTERISK | DIV | MOD | AND *)
procedure multiplying_operator (stop : token_set);
begin
   if (lookahead = ASTERISK_) then
      match (ASTERISK_, stop)
   else if (lookahead = DIV_) then
      match (DIV_, stop)
   else if (lookahead = MOD_) then
      match (MOD_, stop)
   else if (lookahead = AND_) then
      match (AND_, stop)
   else
      syntax_error (stop);
end;

(* <factor> ::= NUMERAL | 
                ID <factor2> | 
                LEFTPARENTHESIS <expression> RIGHTPARENTHESIS | 
                NOT <factor> *)
procedure factor (stop : token_set);
begin
   if (lookahead = NUMERAL_) then
      match (NUMERAL_, stop)
   else if (lookahead = ID_) then begin
      match (ID_, stop + [LEFTBRACKET_, PERIOD_]);
      factor2 (stop);
   end
   else if (lookahead = LEFTPARENTHESIS_) then begin
      match (LEFTPARENTHESIS_, stop + expression_1st + [RIGHTPARENTHESIS_]);
      expression (stop + [RIGHTPARENTHESIS_]);
      match (RIGHTPARENTHESIS_, stop);
   end
   else if (lookahead = NOT_) then begin
      match (NOT_, stop + factor_1st);
      factor (stop);
   end
   else
      syntax_error (stop);
end;

(* <factor2> ::= /<selector>/ | e *)
procedure factor2 (stop : token_set);
begin
   while (lookahead in [LEFTBRACKET_, PERIOD_]) do
      selector (stop + [LEFTBRACKET_, PERIOD_]);
end;

(* <variable_access> ::= ID /<selector>/ *)
procedure variable_access (stop : token_set);
begin
   match (ID_, stop + [LEFTBRACKET_, PERIOD_]);
   while  (lookahead in [LEFTBRACKET_, PERIOD_]) do
      selector (stop + [LEFTBRACKET_, PERIOD_]);
end;

(* <selector> ::= <index_selector> | <field_selector> *)
procedure selector (stop : token_set);
begin
   if  (lookahead = LEFTBRACKET_) then
      index_selector (stop)
   else if  (lookahead = PERIOD_) then
      field_selector (stop)
   else
      syntax_error (stop);
end;

(* <index_selector> ::= LEFTBRACKET <expression> RIGHTBRACKET *)
procedure index_selector (stop : token_set);
begin
   match (LEFTBRACKET_, stop + expression_1st + [RIGHTPARENTHESIS_]);
   expression (stop + [RIGHTBRACKET_]);
   match (RIGHTBRACKET_, stop);
end;

(* <field_selector> ::= PERIOD ID *)
procedure field_selector (stop : token_set);
begin
   match (PERIOD_, stop + [ID_]);
   match (ID_, stop);
end;

(* <constant> ::= NUMERAL | ID *)
procedure constant (stop : token_set);
begin
   if  (lookahead = NUMERAL_) then
      match (NUMERAL_, stop)
   else if  (lookahead = ID_) then
      match (ID_, stop)
   else
      syntax_error (stop);
end;

begin

end.
