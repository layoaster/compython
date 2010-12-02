PROGRAM Goldbath;

{ Practica 1 de Introduccion a los Compiladores
		Introduccion al lenguaje Pascal -

  AUTOR: Frederic Gilberto varela Garcia
  FECHA: 18 de Octubre de 2000
	DESCRIPCION: A este programa se le pasan dos numeros pares a y b, mayores
	que 0, escribiendo luego en pantalla todos los numeros pares entre estos
	dos (ellos incluidos) descompuestos en la suma de dos numeros primos,
	tal y como sugiere la Conjetura de Goldbath.

}

CONST MAX = 100;

TYPE
  registro =

	Record
  	par, primo1, primo2 : integer

  END;

	vect = array[1..MAX] of integer;		{ Estructura utilizada para almacenar
  																			cada par con su descomposici¢n en
                                        dos primos }
VAR
	a,b : integer;  { variables con los pares iniciales del problema }

PROCEDURE Gold(VAR a,b : integer);

VAR
	i,j,x,y : integer;
	v : vect;                  { vector con cada par y su descomposicion}
                             { x,y  variables con los dos primos }

PROCEDURE Primo(VAR l : integer;k : integer);

{ Devuelve el primer primo entre l+1 y k, almacenandolo en l }

VAR

	i,pri : integer;  {pri en un flag para detener la comprobacion de que el
										 numero analizado es un primo}
BEGIN

	If l = 0 Then l := 1 { se devuelve el 1 directamente como siguiente primo
  											 al 0 }
	Else	
  BEGIN
		pri := 0;

		While ((l < k) AND (pri = 0)) DO
    BEGIN

			l := l + 1;
			i := 2;
			pri := 1;

			{ Se va probando si el numero almacenado en l es divisible por alg£n
        numero entre 2 y l-1. Si es as¡, no es primo, pri = 0 y se busca
				una nueva posibilidad en l+1, mientras no se sobrepase el limite k }

      While ((i<l) AND (pri = 1)) DO
      BEGIN

				If (l MOD i = 0) Then pri := 0;
				i := i + 1;
			END;
		END;
	END;
END;


PROCEDURE Escribir(tam : integer);

{ Escribe por pantalla cada par con su descomposicion en dos primos }

VAR
	i : integer;

BEGIN
  i := 1;

  While (i < tam) DO
  BEGIN
	 	write(v[i]);
    i := i + 1;

  END;
END;

BEGIN
  j := 1;

	While a <= b DO  { a va recorriendo todos los pares entre a y b }
  BEGIN
		x := 0;
    y := 0;

		While x+y <> a DO { Se buscan los dos primos que sumen a }
    BEGIN
			Primo(x, a);
			y := 0;

			While ((y<a) AND (x+y <> a)) DO
			BEGIN
				Primo(y, a);

      END;

		END;

    v[j] := a;    { Se almacena cada par y su descomposici¢n en una  }
    v[j+1] := x;	{ casilla del vector, definida como una estructura }
    v[j+2] := y;
    j := j + 3;
    a := a + 2;

	END;

  Escribir(j);

END;


BEGIN { cuerpo del programa principal }
	read(a);
	read(b);
	Gold(a,b)

END.
