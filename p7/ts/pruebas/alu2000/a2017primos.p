{============================================================================
 ============================================================================
 AUTOR: Jose Eduardo Calderon Benito.
 ASIGNATURA: Introduccion a los compiladores I.
 FECHA: 19-10-2000.
 PRACTICA 1: In troduccion al lenguaje Pascal-.
 ============================================================================
 OBJETIVO: Familiarizarse con el lenguaje Pascal-, para el cual hay que dise-
   ¤ar un compilador a lo largo del curso.

 DESCRIPCION: La practica haya los numeros primos que generan un numero in-
   troducido por teclado. Previamente se han calculado los numeros primos
   desde el dos hasta la constante MAX. EL numero introducido sera dividido
   por los numeros primos desde el dos en adelante hasta que sea uno. Un
   primo sera generador siempre que su modulo sea cero.

 MODO DE USO: Una vez ejecutado habra que introducir un numero. Luego saldra
   una linea con el numero introducido al principio y los primos generadores
   separado cada numero por ceros. Despues de ver esta linea habra que pul-
   sar una tecla y enter para finalizar el programa (para q no salga la solu-
	cion al lado del prom).
 ============================================================================
 HISTORIA:
 ============================================================================}
program practica1;
const
   MAX = 200;                        { Calcula los primos desde 2 hasta MAX }
   MAX_GEN = 10;

type
   vector = array [1..MAX] of boolean;       { Primos a TRUE }
   vect_gen = array [1..MAX_GEN] of integer; { Vector con los prim generad}

var
   v_primos: vector;
{============================================================================
  Primo -> Calcula los primos desde 1 hasta MAX.

  Para ello se hace uso de un vector booleano cuyos elementos estaran ini-
  cialmente a TRUE, y se ira recorriendo desde la posicion 2 hasta la "raiz
  cuadrada" de MAX marcando a FALSE todas las posiciones multipo de la que
  estamos estudiando (2->4, 6, 8, ...).
============================================================================}
procedure primo;
var
   i, j, num, x: integer;
begin
   i := 1;
   j := 2;
   { Inicializar vector a TRUE }
   while i < MAX do
   begin
      v_primos[i] := TRUE;
	   i := i + 1;
	end;
   { Recorre vector y pone a FALSE los que no son primos }
   num := MAX div 2;
	while j < num do
	begin
      if v_primos[j] = TRUE then     { Es numero primo }
      begin
         x := j + j;
         while x <= MAX do
         begin
            v_primos[x]:= FALSE;     { Pone a FALSE el numero pq no es primo}
            x:= x + j;
         end;
      end;
  	   j := j + 1;
	end;
end;
{============================================================================
  Mostrar -> Muestra el numero introducido y sus primos generadores separados
  por cero ya que no permite escribir espacio. Para fininalizar habra que
  pulsar una tecla y enter para que la solucion no salga al lado del prom.

  prim_gen -> Contiene los primos que generan num.
  num -> numero introducido por teclado.
  num_gen -> Numero de primos que generan num.
============================================================================}
procedure mostrar (prim_gen : vect_gen; num, num_gen : integer);
var
   i, aux: integer;

begin
	i := 1;
   write (num);
 	while i <= num_gen do
	begin
		write (0);
      write (prim_gen[i]);
		i := i + 1;
	end;
	read (aux);		{ Para que el prom no salga al lado del resultado }
end;

{============================================================================
 Primos_generad  ->La practica haya los numeros primos que generan un numero
 introducido por teclado. EL numero introducido sera dividido por los numeros
 primos desde el dos en adelante hasta que sea uno. Un primo sera generador
 siempre que su modulo sea cero.
============================================================================}
procedure primos_generad;
var
   num,                 { Numero introducido por teclado }
   i, j, aux1, aux2,
   num_gen: integer;    { Numero de primos generadores que tiene num}
   prim_gen: vect_gen;

begin
   read (num);
   aux1 := num;
   num_gen := 0;
   j := 1;
   i := 2;
   while (i < num) and (aux1 <> 1) do
   begin
       if (v_primos[i]) then           { Si es primo }
	    begin
   	    aux2 := aux1;                { Se guarda el valor si no es generad}
          aux1 := aux2 div i;
          if (aux1 * i = aux2) then    { Es generador}
          begin
             prim_gen[j] := i;
             j := j + 1;
             num_gen := num_gen + 1;
	       end
   	    else
      	 begin
             i := i + 1;
             aux1 := aux2;  { Si no es generador se coloca el valor anterio }
	  		 end;
   	 end
	 	 else
   	    i := i + 1;
   end;
   mostrar (prim_gen, num, num_gen);
end;



begin
   primo;
   primos_generad;
end.


