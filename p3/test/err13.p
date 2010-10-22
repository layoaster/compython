{ alu1246  Daniel Martin Lambea. 26.11.98

  Este programa casca los compiladores que no usan una heuristica correcta.
  El token PERIOD ('.') _NO_DEBERIA_ estar en ningun conjunto de parada,
  o provocara la anulacion de TODA la compilacion restante.
  Para verlo, pondremos un punto ANTES de un error. Dicho error no sera
  detectado por los compiladores defectuosos.
}

program  Test_01;

{ Aqui abajo, el primer error, y luego en el bucle WHILE faltara el '>'    }
{ (pone ">>"). Fijate en el rango 0..255  Es comun que falte un '.' 			}

type  TTable = array[0.255] of integer;

var   SinTable: TTable;
      CosTable: TTable;
      A, B, G: integer;       { Angulos }
      X, Y, Z: integer;       { Vector 3D }

begin
while A >> B do
	begin
   B:= A + G;
   G:= G + 1;
   end;
write(A);
write(B);
end.
