{ Pascal- Test_2a : Syntax Errors }

program test_2a;
const
  a := 1;                         { Error }
  b = 2;
  c = ;                           { Error }
  d = 4;
type
 S = recrod f,g : integer end;    { Error }
 t = array[1..2] of integer;
var
  x : integer;
begin
  if = 2 then                     { Error }
    x := 1
end.
