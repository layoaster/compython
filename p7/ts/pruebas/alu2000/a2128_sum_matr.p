program pas;
const MAX = 2;
type vector = array [1..MAX] of integer;
     Tmatriz = array [1..MAX] of vector;
var Matriz:Tmatriz;
    Resultado:Tmatriz;
    i:integer; 
	 j:integer;
begin
    i:=1;
	
    while i <= MAX do
    begin
		j := 1;
		while j <= MAX do
		begin   
	    	read(Matriz[i][j]);
	    	j := j + 1;
		end;
		i := i + 1;
    end;
    i := 1;
    while i <= MAX do
    begin
      j := 1;
      while j <= MAX do
      begin
	 		Resultado[j][i] := Matriz[i][j];
	 		j := j + 1;
      end;
      i := i + 1;
    end; 
    i := 1;
    while i <= MAX do
    begin
      j := 1;
      while j <= MAX do
      begin
	 		write(Resultado[i][j]); 
	 		j := j + 1;
      end;
      i := i + 1;
    end;

end.
