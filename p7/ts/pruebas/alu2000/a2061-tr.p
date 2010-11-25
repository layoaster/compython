{ ************************************************************

	ASIGNATURA : INTRODUCCION A LOS COMPILADORES I

    PROFESOR : FRANCISCO DE SANDE.

    PRACTICA : N§1

    OBJETIVO : FALIMIARIZARSE CON EL USO Y SENTENCIAS
    			DEL COMPILADOR PASCAL MENOS.

************************************************************ }

program traspuesta_matrices;

const                	{ declaracion de constantes }
	MAX_FILA = 50;

type                    { declaracion de tipos }
	t_matriz1 = array [1..MAX_FILA] of integer;
   t_matriz = array [1..MAX_FILA] of t_matriz1;

{ ************************************************************

	PROCEDIMIENTO : inic_matriz

   UTILIZA : MATRIZ - 	matriz a la que se le inicializaran
                          los campos

   FINALIDAD : inicializa todos los campos de una matriz a 0

************************************************************ }

    procedure inic_matriz (var matriz : t_matriz);
    var
    	i, j : integer;  { contadores }

    begin
    	i := 1;
    	while (i <= MAX_FILA) do
      begin
        	j := 1;
         while (j <= MAX_FILA) do
         begin
           	matriz [i][j] := 0;
           	j := j + 1;
         end;
         i := i + 1;
      end;
   end;


{ ************************************************************

	PROCEDURE :  introducir_datos

   UTILIZA : MATRIZ - matriz en la que se introducen los datos

   FINALIDAD : se introducen todos los campos de una matriz.

************************************************************ }

	procedure introducir_datos (var matriz : t_matriz ; filas : integer);
   var
    	i, j : integer;

   begin
   	i := 1;
    	while (i <= filas) do
      begin
        	j := 1;
         while (j <= filas) do
         begin
           	read (matriz [i][j]);
           	j := j + 1;
         end;
         i := i + 1;
      end;
   end;


{ ************************************************************

	PROCEDURE : traspuesta

  UTILIZA : A - matriz a la que se le hallara la tras.
    		  B - matriz en la que se guardara la tras.

   FINALIDAD : Halla la traspuesta de una matriz.

************************************************************ }

	procedure traspuesta (a : t_matriz; var b : t_matriz; filas : integer);
   var
    	i, j : integer; {contadores }

   begin
    	i := 1;
    	while (i <= filas) do
      begin
        	j := 1;
         while (j <= filas) do
         begin
           	b [i][j] := a [j][i];
           	j := j + 1;
         end;
         i := i + 1;
      end;
   end;

{ ************************************************************

	PROCEDURE :ver matriz

    UTILIZA : MATRIZ - matriz que se visualizara por pantalla

    FINALIDAD : Visualiza una matriz por pantalla.

************************************************************ }


	procedure ver_matriz (matriz : t_matriz; filas : integer);
   var
    	i, j : integer;  { contadores  }

   begin
    	i := 1;
    	while (i <= filas) do
      begin
       	j := 1;
         while (j <= filas) do
         begin
          	write (matriz [i][j]);
           	j := j + 1;
         end;
         i := i + 1;
      end;
   end;



{ ************************************************************

	PROCEDURE : main

    FINALIDAD : procedimiento principal en que se hacen
                todas las llamadas necesarias para hallar
                la traspuesta de una matriz.

************************************************************ }

	procedure main;

    var
    	a, b : t_matriz;
      filas : integer;

    begin
    	read (filas);
    	inic_matriz (a);
    	inic_matriz (b);
      introducir_datos (a, filas);
      traspuesta (a, b, filas);
      ver_matriz (b, filas);
    end;

{ ************************************************************

************************************************************ }

begin
	main
end.
