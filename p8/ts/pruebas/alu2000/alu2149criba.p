program BuscaPrimos;
{*******************************************************************************
Practica 1, Introduccion a los compiladores
Alumno: Jorge Pestano Medina (alu2149)
Fecha: 19/10/2000
Objetivo: El objetivo primordial de la practica es familiarizarse con el lenguaje Pasal-. En
	concreto este programa calcula los N primeros numeros primos.
Comentarios: Primero se pide por teclado el numero de numeros primos a calcular
	N. El algoritmo para calcularlos es el siguiente:
		1. Se asume que todos los numeros son PRIMOS.
		2. i = 2.
		3. Si i esta marcado como PRIMO ir seguir con el paso 3.1.,
			 sino ir al paso 4.
		3.1. Marcar todos los múltiplos de i, menores o iguales a N, como NO PRIMOS
		4. i = i + 1.
		5. Si i < N ir al paso 3, sino acabar.
		La salida del programa son los numeros primos uno tras de otro y al final,
	el recuento de numeros primos.
*******************************************************************************}
const
	MAXN = 100; {Numero maximo de numeros}

type
	TArrayBol = array[1..MaxN] of boolean;

var
	N				: integer;	{Numero maximo a probar.}
	Primo 	: TArrayBol; {Si Primo[i] es True entonces i es un numero primo}
	NPrimos	: integer;	{Numero de num. primos encontrado}

	procedure CalcuPrimos(N : integer; var Primo : TArrayBol; var NPrimos : integer);
	{Objetivo: Calcular los numeros primos entre 1 y N, marcando como True los elementos del array
		Primo que son numeros primos.
	 Parametros: N - numero de 'numeros' a comprobar.
							 Primo - array booleano para marcar los numeros primos.
							 NPrimos - contador de numeros primos.
	}
	var
		i, j 	: integer;
	begin
		NPrimos := 1;
        i := 1;
		while i <= N do
		begin
        	Primo[i] := True;
        	i := i + 1
        end;
		Primo[1] := True;
		i := 2;
		while i <= N do
		begin
			if Primo[i] then
			begin
				j := i + i;
				while j <= N do
				begin
					Primo[j] := False;
					j := j + i
				end;
				NPrimos := NPrimos + 1
			end;
			i := i + 1
		end
	end;

	procedure MuestraPrimos(N : integer; Primo : TArrayBol);
	{Objetivo: Muestra los numeros primos.}
	var
		i : integer;
	begin
		i := 1;
		while i <= N do
		begin
			if Primo[i] then
				write(-1*i); {Se multiplica por -1 para usar el signo como separador.}
			i := i + 1
		end
	end;

begin
	{Primero leemos el tope para la busqueda y lo limitamos a MaxN}
	read(N);
	if N > MAXN then
		N := MAXN;

	{Calculamos los numeros primos y los metemos en el array}
	CalcuPrimos(N, Primo, NPrimos);

	{Ahora mostramos la tabla y el numero total de primos:}
	MuestraPrimos(N, Primo);
	write(-1*NPrimos) {Se multiplica por -1 para usar el signo como separador.}
end.

