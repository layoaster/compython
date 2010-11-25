{------------------------------------------------------------------------------
- AUTOR : Daniel J. Diaz Gonzalez
- NUM EXPEDIENTE : alu2036. En caso de cualquier duda, un mail.
- ASIGNATURA : Introduccion a los compiladores I.
- CURSO : 2000/2001.
- FECHA DE ENTREGA : 19/10/2000.
- PROFESOR ENCARGADO : Francisco de Sande.
- OBJETIVO : Hacer una pequenya rutina en Pascal - que nos permita comprobar el
				 compilador de Pascal -, asi como familiarizarnos con el lenguaje.
- DESCRIPCION : El programa se encarga de informar de cuales son los numeros 
					 primos por los que es divisible un numero que se pide por te-
					 clado. Por ello, segun se ejecuta el programa con el interpre-
					 te este se queda esperando a que le metas el numero que quieres
					 comprobar. El procedimiento que siggue es determinar en primer l					 lugar totodos los numeros primos existentes entre 1 y el numero
					 que se ha introducido (el metodo lo explicare en la funcion) y 
					 despues comprobar por cuales de ellos es divisible.
					 Si metes un numero mayor que el maximo que puedes meter, te apa-
					 recen un monton de 0 y se acaba el programa. El maximo es el nu-
					 mero que aparece al principio.
- OBSERVACIONES : He implementado una pequenya rutina que te halla la parte su-
						perior de la raiz cuadrada de un numero; la he llamado 
						sqrtsup.
------------------------------------------------------------------------------}
program prac1;

const
	MAXIMO = 1000;							{Maximo valor permitido}
	VERMAX = 40;							{Numero de 0 que se ven si hay un error}

{*****************************************************************************}
type
	t_vecb = array [1..MAXIMO] of boolean; 
	t_veci = array [1..MAXIMO] of integer;

{*****************************************************************************}
var
	cantprimos : integer;					{Numero de primos hallados}
	vectorb : t_vecb;							{Vector de comprobacion para primos}
	vectori : t_veci;							{Vector donde se almacenan los primos}
	numero : integer;							{Numero a comprobar}
	i : integer;

{-----------------------------------------------------------------------------
	sqrtsup : Halla la raiz cuadrada de un numero, o en caso de que dicho nume-
				 ro no sea un cuadrado perfecto, la parte superior de la misma.
				 Para ello va probando uno a uno todos los numeros naturales mas el
				 0 hasta determinar cual es el numero cuyo cuadrado da el que esta-
				 mos buscando o, en su caso, cual es el primero cuyo cuadrado es ma-
				 yor que el que estamos buscando.
	parametros :
					num1 : numero al que le vamos a hallar la raiz cuadrada.
					result : raiz cuadrada del numero (o parte superior).
------------------------------------------------------------------------------}
procedure sqrtsup (num1 : integer;  var result : integer);
	begin
		result := 0;
		while ((result * result < num1) and (result <= num1 div 2)) do
			result := result + 1;
	end;
{------------------------------------------------------------------------------
	inivecb : Inicializa un vector booleano a TRUE o FALSE segun se le indique.
	parametros :
					vec : vector booleano a inicializar.
					n : Numero de elementos de los que esta formado el vector.
					valor : valor al que quiero inicializar el vector.
------------------------------------------------------------------------------}
procedure inivecb (var vec : t_vecb; n : integer; valor : boolean);
	var
		i : integer;
	
	begin
		i := 1;
		while (i <= n) do
			begin
			vec[i] := valor;
			i := i + 1;
			end;
	end;
{------------------------------------------------------------------------------
	divisores : comprueba por cuales de los numeros primos es divisible el nume-
					ro. El metodo de comprobacion es muy simple : recorro un array en
					el que previamente he introducido los numeros primos y voy ha-
					ciendo un mod.
	parametros : 
					num : numero a comprobar.
------------------------------------------------------------------------------}
procedure divisores (num : integer);
	var
		i : integer;

	begin
		i := 1;
		while (i <= num) do
			begin
			if ((vectorb[i] = TRUE) and (num mod i = 0)) then
				begin
				cantprimos := cantprimos + 1;
				vectori[cantprimos] := i;
				end;
			i := i +1;
			end;
	end;


{------------------------------------------------------------------------------
	 primos : Determina los numeros primos existentes hasta un determinado nu-
				mero. Para ello hace lo siguiente.
					1) Marca como primos a todos los numeros hasta el numero en
						cuestion
					2) Empezando en 2, va desmarcando todos los multiplos del nu-
						mero que se esta comprobando; cuando termina con uno, pa-
						sa al siguiente primo, que sera el siguiente que no se ha
						desmarcado.
					3) El algoritmo concluye cuando se llega a la raiz cuadrada
						(o parte superior de la misma) del numero solicitado, ya
						que se supone que todos los no primos ya han sido desmar-
						cados.
		parametros :
						num : Numero hasta el que queremos hallar los primos.
------------------------------------------------------------------------------}
procedure primos (num : integer);
	var
		i, j : integer;
		result : integer;				{raiz de num}

	begin
		cantprimos := 0;
		inivecb (vectorb, num, TRUE);
		sqrtsup (numero, result);
		i := 2;
		while (i <= result) do
			begin
			if (vectorb[i] = TRUE) then
				begin
				j := 2;
				while (j <= num div i) do				{Hago las mult necesarias}
					begin
					vectorb[i*j] := FALSE;
					j := j + 1;
					end;
				end;
			i := i + 1;
			end;
	end;
{------------------------------------------------------------------------------
	mostrar : muestra un vector de enteros.
	parametros :
					n : Numero de elementos a mostrar dentro del vector.
------------------------------------------------------------------------------}
procedure mostrar (vec : t_veci; n : integer);
	var
		i : integer;

	begin
		i := 1;
		while (i <= n) do
			begin
			write ((-1) * vec[i]);
			i := i + 1;
			end;
	end;
{**************************************************************************}	
begin
	write (MAXIMO);
	read (numero);
	if (numero > MAXIMO) then
		begin
		i := 1;
		while (i <= VERMAX) do
			begin
			write (0);
			i := i + 1;
			end;
		end
	else
		begin
		primos (numero);			{Calculo los primos posibles}
		divisores (numero);				
		mostrar (vectori, cantprimos);
		end;
end.
