program prueba;
const a = 4;
      b = a;
      c = true;
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
    otro = array[1..4] of cosa;

var
   x, y, z : pepa;
   v : integer;
   w : paco;
   h : boolean;

procedure prueba2(var prueba2, pepe, boolean : pepa; u : integer);
var 
   a : integer;
   pepi : pepa;
   v : cosa;
   z : otro;
begin
    {a := 3 + 3;}
    z[2].unrecord.paco := true;
    v.unarray[11] := 6;
    v.unrecord.pepe := false;
end;

begin  
    prueba2(x, y, z, v);
    w.a := 6;
    if  a < 6 then
        write(2);
  h := c;
end.
