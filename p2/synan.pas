unit synan;

interface

uses lexan;

var
   lookahead : token;
   argvalue  : argtype;

procedure match (tok : token);
procedure syntax_error ();

procedure programm_;
procedure block_body;
procedure constant_definition_part;
procedure constant_definition;
procedure type_definition_part;
procedure type_definition;
procedure new_type;
procedure new_array_type;
procedure index_range;
procedure new_record_type;
procedure field_list;
procedure record_section;
procedure variable_definition_part;
procedure variable_definition;
procedure variable_group;
procedure procedure_definition;
procedure procedure_block;
procedure formal_parameter_list;
procedure parameter_definition;
procedure statement;
procedure statement2;
procedure assignment_statement;
procedure procedure_statement;
procedure actual_parameter_list;
procedure if_statement;
procedure while_statement;
procedure compound_statement;
procedure expression;
procedure relational_operator;
procedure simple_expression;
procedure sign_operator;
procedure additive_operator;
procedure term;
procedure multiplying_operator;
procedure factor;
procedure factor2;
procedure variable_access;
procedure selector;
procedure index_selector;
procedure field_selector;
procedure constant;

implementation

procedure syntax_error ();
begin
   if (lookahead = TOKEN_ERROR_) then
      writeln (err_reason)
   else
      writeln (line_num, ': SYN_ERROR [Encontrado ', printable_tok[ord (lookahead)], ']');
   halt (1);
end;

procedure match (tok : token);
begin
   if (lookahead = tok) then
      lookahead := yylex (argvalue)
   else
      syntax_error ();
end;

 (* <program> ::= PROGRAM ID SEMICOLON <block_body> *)
procedure programm_;
begin
   match (PROGRAM_);
   match (ID_);
   match (SEMICOLON_);
   block_body ();
   match (PERIOD_);
   match (ENDTEXT_);
end;

 (* <block_body> ::= [<constant_definition_part>]
                   [<type_definition_part>]
                   <variable_definition_part>]
                   /<procedure_definition>/
                   <compound_statement>*)
procedure block_body;
begin
   if (lookahead = CONST_) then
      constant_definition_part ();
   if (lookahead = TYPE_) then
      type_definition_part ();
   if (lookahead = VAR_) then
      variable_definition_part ();
   while (lookahead = PROCEDURE_) do
      procedure_definition ();
   compound_statement ();
end;

 (* <constant_definition_part> ::= CONST
                                 <constant_definition>
                                 /<constant_definition>/
*)
procedure constant_definition_part;
begin
   match (CONST_);
   constant_definition ();
   while (lookahead = ID_) do
      constant_definition ();
end;

 (* <constant_deﬁnition> ::= ID = <constant> ; *)
procedure constant_definition;
begin
   match (ID_);
   match (EQUAL_);
   constant ();
   match (SEMICOLON_);
end;

 (* <type_deﬁnition_part> ::= TYPE <type_deﬁnition> 
                            /<type_deﬁnition>/
*)
procedure type_definition_part;
begin
   match (TYPE_);
   type_definition ();
   while (lookahead = ID_) do
      type_definition ();
end;

 (* <type_deﬁnition> ::= ID = <new_type> ; *)
procedure type_definition;
begin
   match (ID_);
   match (EQUAL_);
   new_type ();
   match (SEMICOLON_);
end;

 (* <new_type> ::= <new_array type> | <new_record_type> *)
procedure new_type;
begin
   if  (lookahead = ARRAY_) then
      new_array_type ()
   else if  (lookahead = RECORD_) then
      new_record_type ()
   else
      syntax_error ();
end;

 (* <new_array_type> ::= ARRAY "[" <index_range> "]" OF ID *)
procedure new_array_type;
begin
   match (ARRAY_);
   match (LEFTBRACKET_);
   index_range ();
   match (RIGHTBRACKET_);
   match (OF_);
   match (ID_);
end;

 (* <index_range> ::= <constant> .. <constant> *)
procedure index_range;
begin
   constant ();
   match (DOUBLEDOT_);
   constant ();
end;

 (* <new_record_type> ::= RECORD <field_list> END *)
procedure new_record_type;
begin
   match (RECORD_);
   field_list ();
   match (END_);
end;

 (* <field_list> ::= <record_section> /; <record_section>/ *)
procedure field_list;
begin
   record_section ();
   while (lookahead = SEMICOLON_) do
   begin
      match (SEMICOLON_);
      record_section ();
   end;
end;

 (* <record_section> ::= ID /, ID/ : ID *)
procedure record_section;
begin
   match (ID_);
   while (lookahead = COMMA_) do
   begin
      match (COMMA_);
      match (ID_);
   end;
   match (COLON_);
   match (ID_);
end;

 (* <variable_deﬁnition_part> ::= VAR <variable_deﬁnition> 
                                /<variable_deﬁnition>/
*)
procedure variable_definition_part;
begin
   match (VAR_);
   variable_definition ();
   while (lookahead = ID_) do
      variable_definition ();
end;

 (* <variable_deﬁnition> ::= <variable_group> ; *)
procedure variable_definition;
begin
   variable_group ();
   match (SEMICOLON_);
end;

 (* <variable_group> ::= ID /, ID/ : ID *)
procedure variable_group;
begin
   match (ID_);
   while (lookahead = COMMA_) do
   begin
      match (COMMA_);
      match (ID_);
   end;
   match (COLON_);
   match (ID_);
end;

 (* <procedure_deﬁnition> ::= PROCEDURE ID 
                            <procedure_block> ;
*)
procedure procedure_definition;
begin
   match (PROCEDURE_);
   match (ID_);
   procedure_block ();
   match (SEMICOLON_);
end;

 (* <procedure_block> ::= [( <formal_parameter_list> )] ;
                        <block_body>
*)
procedure procedure_block;
begin
   if (lookahead = LEFTPARENTHESIS_) then
   begin
      match (LEFTPARENTHESIS_);
      formal_parameter_list ();
      match (RIGHTPARENTHESIS_);
   end;
   match (SEMICOLON_);
   block_body ();
end;

 (* <formal_parameter_list> ::= <parameter_deﬁnition> 
                              /; <parameter_deﬁnition>/
*)
procedure formal_parameter_list;
begin
   parameter_definition ();
   while (lookahead = SEMICOLON_) do
   begin
      match (SEMICOLON_);
      parameter_definition ();
   end;
end;

 (* <parameter_deﬁnition> ::= [VAR] <variable_group> *)
procedure parameter_definition;
begin
   if (lookahead = VAR_) then
      match (VAR_);
   variable_group ();
end;

 (* <statement> ::= ID <statement2> | 
                  <if_statement> | 
                  <while_statement> | 
                  <compound_statement> |
                  e
*)
procedure Statement;
begin
   if (lookahead = ID_) then
   begin
      match (ID_);
      statement2 ();
   end
   else if (lookahead = IF_) then
      if_statement ()
   else if (lookahead = WHILE_) then
      while_statement ()
   else if (lookahead = BEGIN_) then
      compound_statement ();
end;

 (* <statement2> ::= <procedure_statement> | /<selector>/
                                           BECOMES
                                           <expression>
                                         | e
*) 
procedure statement2;
begin
   if (lookahead = LEFTPARENTHESIS_) then
      procedure_statement ()
   else if (lookahead in [LEFTBRACKET_, PERIOD_, BECOMES_]) then
   begin
      while (lookahead in [LEFTBRACKET_, PERIOD_]) do
         selector ();
      match (BECOMES_);
      expression ();
   end
end;

 (* <assignment_statement> ::= <variable_access> 
                              BECOMES 
                              <expression> *) 
procedure assignment_statement;
begin
   variable_access ();
   match (BECOMES_);
   expression ();
end;

 (* <procedure_statement> ::= [LEFTPARENTHESIS
                             <actual_parameter_list>
                             RIGHTPARENTHESIS] *)
procedure procedure_statement;
begin
   if (lookahead = LEFTPARENTHESIS_) then begin
      match (LEFTPARENTHESIS_);
      actual_parameter_list ();
      match (RIGHTPARENTHESIS_);
   end;      
end;

 (* <actual_parameter_list> ::= <actual_parameter> 
                               /COMMA <actual_parameter/ *)
procedure actual_parameter_list;
begin
   expression ();
   while (lookahead = COMMA_) do begin
      match (COMMA_);
      expression ();
   end;        
end;

 (* <if_statement> ::= IF <expression> THEN <statement>
                      [ELSE <statement>] *)
procedure if_statement;
begin
   match (IF_);
   expression ();
   match (THEN_);
   statement ();
   if (lookahead = ELSE_) then begin
      match (ELSE_);
      statement ();
   end;
end;

 (* <while_statement> ::= WHILE <expression> DO <statement> *)
procedure while_statement;
begin
   match (WHILE_);
   expression ();
   match (DO_);
   statement ();
end;

 (* <compound_statement> ::= BEGIN <statement> /; <statement>/ END *)
procedure compound_statement;
begin
   match (BEGIN_);
   statement ();
   while (lookahead = SEMICOLON_) do begin
      match (SEMICOLON_);
      statement ();
   end;
   match (END_);
end;

 (* <expression> ::= <simple_expression> 
                    [<relational_operator> <simple_expression>] *)
procedure expression;
begin
   simple_expression ();
   if (lookahead in [LESS_, EQUAL_, GREATER_, NOTGREATER_, NOTEQUAL_, NOTLESS_]) then begin
      relational_operator ();
      simple_expression ();
   end;
end;

 (* <relational_operator> ::= LESS | EQUAL | GREATER | NOTGREATER | NOTEQUAL | NOTLESS *)
procedure relational_operator;
begin
   if (lookahead = LESS_) then
      match (LESS_)
   else if (lookahead = EQUAL_) then
      match (EQUAL_)
   else if (lookahead = GREATER_) then
      match (GREATER_)
   else if (lookahead = NOTGREATER_) then
      match (NOTGREATER_)
   else if (lookahead = NOTEQUAL_) then
      match (NOTEQUAL_)
   else if (lookahead = NOTLESS_) then
      match (NOTLESS_)
   else
      syntax_error ();
end;

 (* <simple_expression> ::= [<sign_operator>] <term> /<additive_operator> <term>/ *)
procedure simple_expression;
begin
   if (lookahead in [PLUS_, MINUS_]) then
      sign_operator ();
   term ();
   while (lookahead in [PLUS_, MINUS_, OR_]) do begin
      additive_operator ();
      term ();
   end;
end;

 (* <sign_operator> ::= PLUS | MINUS *)
procedure sign_operator;
begin
   if (lookahead = PLUS_) then
      match (PLUS_)
   else if (lookahead = MINUS_) then
      match (MINUS_)
   else
      syntax_error ();
end;

 (* <additive_operator> ::= PLUS | MINUS | OR *)
procedure additive_operator;
begin
   if (lookahead = PLUS_) then
      match (PLUS_)
   else if (lookahead = MINUS_) then
      match (MINUS_)
   else if (lookahead = OR_) then
      match (OR_)
   else
      syntax_error ();
end;

 (* <term> ::= <factor> /<multiplying_operator> <factor>/ *)
procedure term;
begin
   factor ();
   while (lookahead in [ASTERISK_, DIV_, MOD_, AND_]) do begin
      multiplying_operator ();
      factor ();
   end;
end;

 (* <multiplying_operator> ::= ASTERISK | DIV | MOD | AND *)
procedure multiplying_operator;
begin
   if (lookahead = ASTERISK_) then
      match (ASTERISK_)
   else if (lookahead = DIV_) then
      match (DIV_)
   else if (lookahead = MOD_) then
      match (MOD_)
   else if (lookahead = AND_) then
      match (AND_)
   else
      syntax_error ();
end;

 (* <factor> ::= NUMERAL | 
                ID <factor2> | 
                LEFTPARENTHESIS <expression> RIGHTPARENTHESIS | 
                NOT <factor> *)
procedure factor;
begin
   if (lookahead = NUMERAL_) then
      match (NUMERAL_)
   else if (lookahead = ID_) then begin
      match (ID_);
      factor2 ();
   end
   else if (lookahead = LEFTPARENTHESIS_) then begin
      match (LEFTPARENTHESIS_);
      expression ();
      match (RIGHTPARENTHESIS_);
   end
   else if (lookahead = NOT_) then begin
      match (NOT_);
      factor ();
   end
   else
      syntax_error ();
end;

 (* <factor2> ::= /<selector>/ | e *)
procedure factor2;
begin
   while (lookahead in [LEFTBRACKET_, PERIOD_]) do
      selector ();
end;

 (* <variable_access> ::= ID /<selector>/ *)
procedure variable_access;
begin
   match (ID_);
   while  (lookahead in [LEFTBRACKET_, PERIOD_]) do
      selector ();
end;

 (* <selector> ::= <index_selector> | <field_selector> *)
procedure selector;
begin
   if  (lookahead = LEFTBRACKET_) then
      index_selector ()
   else if  (lookahead = PERIOD_) then
      field_selector ()
   else
      syntax_error ();
end;

 (* <index_selector> ::= LEFTBRACKET <expression> RIGHTBRACKET *)
procedure index_selector;
begin
   match (LEFTBRACKET_);
   expression ();
   match (RIGHTBRACKET_);
end;

 (* <field_selector> ::= PERIOD ID *)
procedure field_selector;
begin
   match (PERIOD_);
   match (ID_);
end;

 (* <constant> ::= NUMERAL | ID *)
procedure constant;
begin
   if  (lookahead = NUMERAL_) then
      match (NUMERAL_)
   else if  (lookahead = ID_) then
      match (ID_)
   else
      syntax_error ();
end;

begin

end.
