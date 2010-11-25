program _prueba                   { Error }

const
  a = 1;
  b = ;                           { Error }
  c = 1;
  d = 4;
type
 S = record f,g : integer end;    { Error }
 t = array[1..2] of integer;
var
  x : integer;
begin
if = 2 then                       { Error }
 x := 1;
while a = do                      { Error }
 a := 1*3;
3;                                { Error }
end.
