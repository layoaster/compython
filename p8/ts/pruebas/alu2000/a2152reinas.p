{-------------------------------------------------------
Program :   n_reinsa.p
Autor:	    Miriam Quitnero Padron
Fecha:	    10 de Octubre de 2000
Asignatura: Compiladores 1
Descripcion:Colocar n reinas en un tablero de tamanno n
            de manera que no se amenacen unas a otras
            con el metodo de Backtraking e imprime por
            pantalla todas las soluciones posibles
Nota:
	    Entrada:	    
	    El usuario debe introducir
	    el tamanno del tablero (4,6,9....)
 	    preferiblemente un numero < 8 debido a las limitaciones del
	    Pascal- para sacar las soluciones por pantalla
	    Salida:
	    nm -> donde n indica el numero de reina
	 	  y m lo posicion que ocupa
	    Ejemplo: 	Tamanno del tablero 4
	    Salida: 	12243143
	    indica: 	reina 1 pos 2
			reina 2 pos 4
			reina 3 pos 1
			reina 4 pos 3 
	    Cada solucion esta separada por un 0
----------------------------------------------------------}

Program n_reinas;

const MAX = 50;
type vector = array[1..MAX] of integer;
var
    reinas : vector;   	{ soluciones parciales de las pos. de las reinas }
    k,                 	{ reina }
    n,		       	{ tama¤o del tablero }
    conta : integer;	{ contador de soluciones }
    sol : boolean;      { nos dice si una reinas es solucion }

{******************************************************
procesar: imprime el vector solucion por pantalla
********************************************************}
Procedure procesar (reinas : vector; var conta: integer);
var
    i : integer;
begin
    i := 1;
    conta := 0;
    write (conta);
    while i <= n do
    begin
        write (i);
        write (reinas[i]);
        i := i + 1;
    end;
    conta := conta + 1;        { incrementamos el num. de soluciones }
end;

{****************************************************************
es solucion : nos indica si las reinas colocadas hasta el momento
no se amenazan, de ser asi la variable sol devuelve TRUE
****************************************************************}
Procedure es_solucion (var reinas : vector; j : integer; var sol : boolean);
var
    i : integer;
begin
    sol := True;
    i := 1;
    while ((i < j) and sol) do
	begin
        if ((reinas[i] = reinas[j]) or                    { misma fila }
			(reinas[i]-i = reinas[j]-j)       { misma columna }
			or (reinas[i] + i = reinas[j]+j)) then  { diagonal }
            	sol := False;
    	i := i + 1;
	end;
end;

{---------------- PRINCIPAL ---------------------------}
begin
    conta := 1;
    { write (' Tamanno del tablero: '); }
    read (n);
    k := 1;
    reinas[k] := 0;

    while ( k > 0 ) do                  { mientras existan posibilidades }
    	if ( reinas [k] < n )  then     { no hemos colocado todas las reinas }
        begin
            reinas[k] := reinas[k] + 1; { avanzamos una posicion }
            es_solucion( reinas, k, sol );  { miramos si es solusion parcial }
            if sol then
            	if k = n then           { una solucion obtenida }
               	    procesar(reinas, conta)
                else
                begin                   { colocamos la siguiente reina }
                    k := k + 1;
                    reinas [k] := 0;
                end;
        end
        else
            k := k - 1;                 { no es una solucion factible }
end.
