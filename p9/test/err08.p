program test_EBNF2;
	
	procedure ;					{ Falta ID de proc }
	begin
	end;

	procedure p2;
    							{ Falta el begin del procedimiento }
	end;

	procedure p3				{ Falta el ; del procedimiento }
	begin
	end;
	
begin
end.

{
FINALIDAD:
Probar el comportamiento del recuperador de errores con sentencias de la
forma:

block_body -> [constant_definition_part] [type_definition_part]
			 [VariabledefinitionPart] {procedure_definition }
			 compount_statement

dependiendo que en el conjunto de parada al analizar procedure_definition
se coloque como conjunto de parada
Stop + {PROCEDURE}
o bien
Stop + {PROCEDURE, ID, SEMICOLON, LEFTPAR, RIGHTPAR, ...}
}
