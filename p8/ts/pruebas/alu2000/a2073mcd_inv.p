{****************************************************************************
* AUTOR: Juan Ram¢n Gonz lez Gonz lez
* PRACTICA 1: Introducci¢n al lenguaje Pascal-
* DESCRIPCIàN: Programa en Pascal- que permite calcular el m ximo com£n divi-
*              sor de 2 n£meros y el inverso del menor (m¢dulo el mayor).
* ASIGNATURA: Introducci¢n a los Compiladores I
* ULTIMA MODIFICACIàN: 18-10-2000
* MODO DE USO:
*    -Introducir el n£mero menor y el mayor en ese orden.
*    -Se obtiene el mcd y el inverso del menor (mod el mayor) en ese orden.
****************************************************************************}
program mcd_inv;

type
	ArrayInt3 = array[0..2] of integer;             { Array de 3 enteros }

var
	numMenor, numMayor, mcd, inverso : integer;

{****************************************************************************
* MCDInverso -- Calcula el m ximo com£n divisor de numMenor y numMayor, que
* devuelve en mcd; y el inverso de num_menor (mod num_mayor) que devuelve en
* inverso.
* -C lculo del mcd: Para calcular el mcd se utiliza el algoritmo de Euclides,
*  que consiste en dividir inicialmente los 2 n£meros de los que se quiere
*  calcular el mcd. A continuaci¢n, hasta que el resto sea cero, se va divi-
*  diendo el £ltimo divisor por el £ltimo resto, obteni‚ndose como mcd el di-
*  visor de la divisi¢n que di¢ como resto 0.
* -C lculo del inverso: El inverso de numMenor (mod numMayor), se calcula
*  aprovechando el mismo algoritmo de Euclides, con el c lculo adicional de
*  x[i] = x[i - 2] - (el cociente de la iteraci¢n actual) * x[i - 1].
*  Como valores iniciales se tiene que x[i - 1] = 1 y que x[i - 2] = 0, ob-
*  teni‚ndose como inverso el x[i] de la £ltima divisi¢n cuyo resto fue dis-
*  tinto de 0.
* IMPORTANTE: El inverso s¢lo existe si mcd = 1, con lo que sino es as¡, se
* devuelve un 0 indicando este hecho.
****************************************************************************}
procedure MCDInverso(numMenor, numMayor : integer;
                      var mcd, inverso : integer);
var
	divisor, resto, aux : integer;
	x : ArrayInt3;         { Para realizar el c lculo del inverso se utiliza
									 un array que almacena los valores de x[i],
									 x[i - 1] e x[i - 2]. Para ahorrar intercambios
									 de valores, la situaci¢n del x[i] actual y los
									 anteriores va variando por aritm‚tica modular }
	i : integer;           { Öndice actual del array x, que corresponde con
									 la posici¢n del x[i] actual. Va variando me-
									 diante aritm‚tica modular en el siguiente orden:
									 2, 0, 1, 2, 0, 1, 2, ... }

begin
	divisor := numMayor;
	resto := numMenor;
	i := 1;                { Para que el i empiece en 2 en el bucle }
		{ Se inicializa x adecuadamente para un i inicial de 2 }
	x[0] := 0;
	x[1] := 1;
	while (resto <> 0) do
	begin
		i := (i + 1) mod 3;
		 {-------------------------------------------------------------------
		 | x[i - 1] corresponde con x[((i - 1) + 3) mod 3] = x[(i + 2) mod 3].
		 | x[i - 2] corresponde con x[((i - 2) + 3) mod 3] = x[(i + 1) mod 3].
		  -------------------------------------------------------------------}
		x[i] := x[(i + 1) mod 3] - (divisor div resto) * x[(i + 2) mod 3];
		aux := resto;
		resto := divisor mod resto;
		divisor := aux;
	end;
	mcd := divisor;
		 {-------------------------------------------------------------------
		 | El inverso no es el £ltimo x[i], sino el anterior. Para mayor fa-
		 | cilidad, si el inverso da negativo, se pasa a un n£mero positivo
		 | equivalente.
		  -------------------------------------------------------------------}
	if (mcd = 1) then    { Existe el inverso }
	begin
		inverso := x[(i + 2) mod 3];
		inverso := inverso mod numMayor;
		inverso := (inverso + numMayor) mod numMayor;
	end
	else
		inverso := 0;
end;

begin
	read(numMenor);
	read(numMayor);
	MCDInverso(numMenor, numMayor, mcd, inverso);
	write(mcd);
	write(inverso);
end.

