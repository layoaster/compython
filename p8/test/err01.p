{ Pascal- Test3 : Syntax Errors }

program test3;
const
  a := 1;                         { 5: Error }
  b = 2;
  c = ;                           { 7: Error }
  d = 4;
type
 S = recrod f,g : integer end;    { 10: Error }
 t = array[1..2] of integer;
var
  x : integer;
begin
  if = 2 then                     { 15: Error }
    x := 1
end.
