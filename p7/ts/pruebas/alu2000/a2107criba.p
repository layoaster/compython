{*****************************************************************************
  PROGRAMA : primos.p
  AUTOR : Jose Ramon Lopez Hernandez
  FECHA : 13-10-2000
  OBJETIVO : Dados dos numeros, un inicio y un final, el programa generara
           todos los numeros primos entre ambos, mostrandolos por pantalla.
           Para ello se tiene un array en el que se iran marcando los nume-
           ros que no sean primos que hallare por multiplicaciones de los
           mismos.
  OBSERVACIONES: El programa espera recibir antes que nada el numero en el
           que comienza el intervalo y luego en el que acaba.
  COMPILADOR : Pascal-, compilador elaborado en las asignaturas de compila-
           dores.
  HISTORIA :
*****************************************************************************}
program primos;

const
  MENORPRIMO = 2;
  MAYORPRIMO = 5000;
	
type
  t_primos = array [1..MAYORPRIMO] of boolean;

var
  primos : t_primos;
  inicio, fin,                 {Limites de los intervalos}
  i, j : integer;              {Contadores en los bucles}

{*****************************************************************************
  hallar_primos -- Dado un numero maximo, el procedimiento marca los numeros
                 que no son primos antes que este. Para marcar hallo los mul-
                 tiplos de los numeros que no han sido marcados comenzando
                 en orden ascendente desde el principio del array.
  parametros:
          fin : limite del intervalo.
*****************************************************************************}
procedure hallar_primos(fin : integer);
begin
  i := MENORPRIMO;
  while i <= fin do
  begin
    j := MENORPRIMO;
    while (i*j) <= fin do   {No hallamos primos mas alla del limite final}
    begin
      primos[i*j] := true;
      j := j + 1;
    end;
    i := i + 1;
  end;
end;

{*****************************************************************************
  mostrar_primos -- Muestra los numeros que corresponden a posiciones del vec-
                 tor que no han sido marcadas. Seran posiciones que correspon-
                 den a numeros primos.
  parametros:
           inicio, fin : Limites del intervalo.
*****************************************************************************}
procedure mostrar_primos(inicio, fin : integer);
begin
  i := inicio;
  while i <= fin do
  begin
    if not primos[i] then
      write(-1*i); {Para que muestre un separador lo multiplico por -1}
    i := i + 1;
  end;
end;

{*********************
  programa_principal
**********************}
begin
  read(inicio);
  read(fin);
  hallar_primos(fin);
  mostrar_primos(inicio, fin);
end.
