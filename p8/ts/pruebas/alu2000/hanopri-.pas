{*****************************************************************************
ASIGNATURA: Introduccion a los compiladores I.
PROGRAMA: Practica 1. Introduccion al lenguaje Pascal-.
FINALIDAD: La finalidad del programa es familiarizarse con el lenguaje
             pascal-, para lo cual se han implementado algunos peque¤os
             programas independientes entre si, juntandolos en una solo.
             Los diferentes modulos implementados son los siguientes:
                 - Simulador del problema de las Torres de Hanoi.
                 - Calculo de un numero primo.
                 - Implementacion de un vector en memoria estatica.
             La descripcion de cada uno de ellos se encuentra en la cabecera
             de los mismos.
             La razon por la que se han implementado tres modulos tan diferen
             tes ha sido tratar de comprobar el comportamiento del compilador
             de pascal- ante diferentes casos como la recursividad, el trata
             miento de arrays y punteros, operadores aritmeticos, etc... para
             en definitiva obtener una idea lo mas real posible de las carac
             teristicas propias del lenguaje pascal-.
DESCRIPCION: El programa calcula sucesivamente el numero de movimientos de
             discos que realiza Hanoi tantas veces como se defina en la cons
             tante 'NUM_ELEM' inicialmente 10, que el usuario del programa
             modificar si lo desea. El numero minimo de discos con el que
             trabaja el programa es 3 y viene definido en la constante
             DISCINIC.  
             Se comprueba si el numero
             de iteracion es primo, y si lo es se introduce en la lista estati
             ca. Finalmente se imprime por pantalla el contenido de la lista
             estatica.
SALIDA:      El programa saca como salida el numero de iteraciones para 3 dis
	     cos (7) , para 4 discos (15), etc... con lo cual una salida tipica
	     del programa podria ser:
			71531127511...
	     Ya que no se pueden introducir saltos de linea ni espacios se mez
	     unas soluciones con otras.
AUTOR: Rodrigo Cano Mart¡n.
FECHA: 18 - 10 - 00.
*****************************************************************************}
program hanoi_primo;
const
     NUM_ELEM = 8;  { nem de ejecuciones de hanoi }
     DISCINIC = 3;   { numero inicial de discos para hanoi }

type
	vector = array[1..NUM_ELEM] of integer;

var
   valor:integer;
   numdiscos: integer; { num de discos de hanoi }
   i:integer;
   nmov: integer; { numero de movimientos de disco para hanoi }
   P : boolean;
   vec : vector; 
{*****************************************************************************
PROCEDURE: MoverTorre
DECRIPCION: El procedimiento simula de manera recursiva el conocido problema
            de las Torres de Hanoi. El problema consiste en lo siguiente:
                   Se parte de tres postes separados.
                   En el poste 1 se colocan un numero determinado de discos de
                   diferentes tama¤os de manera que el mayor se coloca abajo,
                   y el resto sobre el ordenados de mayor a menor.
                   Se trata de mover la pila de discos del poste 1 al poste 3,
                   con las siguientes normas:
                       - Solo se mueve un disco cada vez.
                       - No se puede colocar un disco mayor sobre otro menor.
            La idea es calcular el numero de movimientos de discos necesarios
            para cada numero de discos iniciales.
            Al procedimiento se le pasan:
               - N: Numero de discos.
               - Uno, dos, tres: los postes.

*****************************************************************************}
procedure MoverTorre (N : integer; Uno, Dos, Tres : integer);
    procedure MoverDisco (Desde, Hasta : integer);
        begin
             {Write(desde);
             Write(hasta);}
             nmov := nmov+1;
        end;
    begin
         if N = 1 then
            MoverDisco (Uno, Tres)
         else
             begin
                  MoverTorre (N - 1, Uno, Tres, Dos);
                  MoverDisco (Uno, Tres);
                  MoverTorre (N - 1, Dos, Uno, Tres)
             end
    end;
{*****************************************************************************
PROCEDURE: primo
DESCRIPCION: Calcula si un numero es primo. Va comprobando si el numero es
             divisible por algun otro hasta 'q/2', si no lo es por ninguno
             resuelve que es primo. Devuelve true si q es primo, false
             en caso contrario.
*****************************************************************************}
   procedure Primo(Q: integer; var P:boolean);
   { precondicion q>0 }
   var
      D: integer; { contador }
      C: integer; { cociente }
      R: integer; { resto }

   begin { primo }
         if Q < 4
         then
             P := true
         else
         begin
              P := true;
              D := 2;
              while P and (D <= Q div 2) do
              begin
                   R := Q mod D; 
		   P := R <> 0;
                   D := D + 1;
              end;
         end
   end; { primo }
{*****************************************************************************
PROGRAMA PRINCIPAL
*****************************************************************************}
begin
     numdiscos := DISCINIC; { numero inicial de discos para hanoi }
     i:=1;
     while i < NUM_ELEM do
     begin
         nmov := 0;
         MoverTorre (numdiscos, 1, 2, 3);
         numdiscos := numdiscos+1;
         Primo(i, P);
         if P then
	 begin 
       		vec[i] := nmov; 
		write(vec[i]);
	 end;	
         i := i+1;
     end;
end.
