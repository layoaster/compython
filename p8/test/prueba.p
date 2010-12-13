program prueba;
const a = 4;
      b = a;
      c = 4;
type
   pepe = record
            pepe, paco : boolean
          end;
   paco = record
            hola : pepe
          end;
   pepa = array[12..15] of integer;
   cosa = record
            unarray : pepa;
            unrecord : pepe
          end;

var
   x, y, z : pepa;
   v : integer;

procedure prueba2(var prueba2, pepe, boolean : pepa; u : integer);
var 
   a : integer;
   pepi : pepa;
   v : cosa;
begin
    a := 3 + 3;
    v.unarray[11] := 6;
    v.unrecord.pepe := false;
end;

begin  
    prueba2(x, y, z, v);
    if  a < 6 then
        write(2);
end.
