{ ************************************************************************

	ASIGNATURA : INTRODUCCION A LOS COMPILADORES I.

    PRACTICA : PRACTICA N§1

    PROFESOR : FRANCISCO DE SANDE

    OBJETIVO : USO Y FAMIRIALIZACION DE LAS SENTENCIAS
    			DEL LENGUAJE DE PROGRAMACION PASCAL -

    COMENTARIOS : ESTA PRACTICA HALLA EL MAXIMO COMUN
    				DIVISOR A PARTIR DE DOS NUMEROS.
    MODO DE USO : Primero se escribe el primer numero, luego se teclea
						enter, posteriormente se escribe el segundo numero y 
						nuevamente se teclea enter. Seguidamente saldra la so
						lucio en pantalla.
*************************************************************************}

program m_c_d;               { nombre del programa       }

const MAX_ARRAY = 50;        { declaracion de constantes }

type                         { declaracion de tipos      }

	t_vector = array [1..MAX_ARRAY] of integer;



{ *************************************************************************

	PROCEDIMIENTO : Inicializar vector
	UTILIZA :  VECTOR - vector donde colocaremos los datos referentes
							  a los divisores.

							  
	FINALIDAD : inicializa todos los campos de un vector a -1.

************************************************************************* }

	procedure inic_vector (var vector : t_vector);
	var
    	i : integer;   { contador }

    begin
    	i := 1;
        while (i <= MAX_ARRAY) do
        begin
        	vector [i] := -1;
            i := i + 1;
        end;
    end;

{ ******************************************************************************

	PROCEDIMIENTO : dividir

	UTILIZA : NUMERO - Num el cual vamos descomponer 
				 DIV1 - Array donde guardamos los factores en los que dividimos
						  el numero.
             REP1 - Array donde guardamos el grado de cada factor
																												FINALIDAD :Este programa descompone en factores u nnumero 

***************************************************************************** }

	procedure dividir (numero : integer; var div1 : t_vector;
						var rep1 : t_vector);
    var
    	cont : integer;
        i : integer;
        num : integer;

	begin
 		num := numero;
    	cont := 2;
      i := 1;
      while (num <> 1) do
      begin
        	if ((num mod cont) = 0) then   { Si es divisible exacto } 
			begin
           	if (div1 [i] <> -1) then   { si no es la primera vez que lo }
            begin                      { descomponemos.                 }
              	if (div1[i] = cont) then
                 	rep1 [i] := rep1 [i] + 1
               else    { factor diferente al anterior }
               begin
                 	i := i + 1;
                  div1 [i] := cont;
                  rep1 [i] := 1;
               end;
               num := num div cont;
            end
            else { si es la primera vez que lo descomponemos }
            begin
					div1 [i] := cont;
					rep1 [i] := 1;
					num := num div cont;
            end;
 			end
         else
           	cont := cont + 1; {en el caso de que no sea divisible }
		end;                    {aumentamos el divisor.             }

	end;

{ ****************************************************************************

	PROCEDIMIENTO : mcd

	UTILIZA : DIV1 - factores en los que se ha div el 1er numero.
				 REP1 - Grado de cada factor.
				 DIV2 - factores en los que se ha div el 2do numero.
				 REP2 - Grado de cada factor del 2do numero.
				 SOL_DIV - Array de soluciones donde meteremos los factores
							  comunes a ambos numeros 
				 SOL_REP - Array de soluciones donde meteremos los grados de los fac                       tores correspondientes.


	FINALIDAD : Este procedimiento selecciona aquellos facores comunes a ambos
					numeros, cogiendo el de menor grado


****************************************************************************** }

	procedure mcd (div1, rep1, div2, rep2 : t_vector;
	               var sol_div, sol_rep : t_vector);

	var
    	i, j : integer;
		found : boolean;
		cont : integer;


	begin
		cont := 1;
    	i := 1;
      while (div1 [i] <> -1) do { hasta que no haya mas factores 1er }
      begin
        	j := 1;
         found := false;
         while ((div2 [j] <> -1) and (found = false)) do {hasta que no haya }
           	if (div1 [i] = div2 [j]) then                {mas factores 2do  }
            begin        {si es comun }
              	if (rep1 [i] > rep2 [j]) then { cogemos el de menor grado }
               begin
                 	sol_div [cont] := div2 [j];
                  sol_rep [cont] := rep2 [j];
               end
               else
               begin
                 	sol_div [cont] := div1 [i];
                  sol_rep [cont] := rep1 [i];
               end;
               cont := cont + 1;
               found := true;
           end
           else
           	  j := j + 1;

        	  i := i + 1;
        end;
    end;


{****************************************************************************

	PROCEDIMIENTO : MAIN

	FINALIDAD : procedimiento principal en el que se hacen las llamadas oportunas               al los diferentes procedimientos vistos anteriormente para asi ha               hallar el maximo comun divisor.


*************************************************************************** }




	procedure main;
	var
    	num1, num2 : integer;
      div1, div2 : t_vector;
      rep1, rep2 : t_vector;
      sol_div : t_vector;
      sol_rep : t_vector;
      cont : integer;
      solucion : integer;
      i, j, valor : integer;


	begin
    	cont := 1;
    	read (num1);  { leemos el 1er numero }
      read (num2);  { leemos el 2do numero }
      inic_vector (div1); { inic el vector de factores del 1er numero }
      inic_vector (div2); { inic el vector de grados de los fac del 1er numero }
      inic_vector (rep1); { inic el vector de factores del 2do numero }
      inic_vector (rep2); { inic el vector de grados de los fac del 2do numero }
      inic_vector (sol_div);  {inic vectores de soluciones }
      inic_vector (sol_rep);
      dividir (num1, div1, rep1); { descomponemos el 1er numero en factores }
      dividir (num2, div2, rep2); { descomponemos el 2do numero en factores }
      mcd (div1, rep1, div2, rep2, sol_div, sol_rep); 
                                           {calculamos los factores comunes }
      solucion := 1;                       { y sus grados para multiplicarlos }  
      i := 1;
      while (sol_div [i] <> -1) do  { multiplicamos los factores y obtenemos } 
      begin                         { el mcd                                 }
       	j := 1;
         valor := 1;
         while (j <= sol_rep [i]) do
         begin
           	valor := valor * sol_div [i];
				j := j + 1;
         end;
         i := i + 1;
         solucion := solucion * valor;
      end;
      write (solucion);

	end;

{ ***************************************************************************}

begin
	main
end.
