{ Pascal- Test_2c : Syntax Errors }

program test_2c;
const
  a = 1;
  b = 2;
  c = 1;
  d = 4;
type
 S = recrod f,g : integer end;      { Error }
 t = array[1..2] of integer;
var
  x : integer;
begin
  if = 2 then                       { Error }
    x := 1
end.

