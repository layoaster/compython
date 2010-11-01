program qsort;  { Programa que realiza ordenacion por metodo quicksort }
CONST
   Nmax = 8;                    { Numero maximo de elementos a ordenar }

TYPE
   cadena = ARRAY [1..8] OF integer;          { Tipo cadena de enteros }

VAR
   vector : cadena;                      { Vector de enteros a ordenar }
   cont   : integer;                               { Contador auxiliar }

   procedure quicksort(iz, de : integer);      { Proced. de Ordenacion }
   VAR i, j  : integer;                           { Indices del vector }
       media : integer;                    { Posicion media del vector }
       reg   : integer;                            { registro auxiliar }
   
   begin
      i := iz;                     { indice izquierda = limite inferior }
      j := de;                       { indice derecha = limite superior }
      media := vector[((iz + de) div 2)];        { halla posici¢n media } 

      while (vector[i] < media) do     { Inc. i mientras menor que media }
         i := i + 1;
         
      while (media < vector[j]) do     { Dec. j mientras mayor que media }
         j := j - 1;
            
      if (i <= j) then                             { Si j sobrepasa a i }
      begin
         reg := vector[i];                { Guardamos pos. i del vector }
         vector[i] := vector[j]; { Intercambia valores index. por i y j }
         vector[j] := reg;                           { Actualiza pos. j }             
         i := i + 1;                                    { Inc. indice i }
         j := j - 1;                                    { Inc. indice j }
      end;
      
      while (i <= j) do      { => indice i este por debajo del indice j }
      begin
         while (vector[i] < media) do { Inc. i mientras menor que media }
            i := i + 1;
         
         while (media < vector[j]) do { Dec. j mientras mayor que media }
            j := j - 1;
            
         if (i <= j) then                         { Si j sobrepasa a i }
         begin
            reg := vector[i];            { Guardamos pos. i del vector }
            vector[i] := vector[j];  { Inter. valores index. por i y j }
            vector[j] := reg;                       { Actualiza pos. j }             
            i := i + 1;                                { Inc. indice i }
            j := j - 1;                                { Inc. indice j }
         end;
      end;

      if (iz < j) then quicksort(iz, j);    { llama funcion quick sort con nuevos limites de vector }
      if (i < de) then quicksort(i, de);    { llama funcion quick sort con nuevos limites de vector }
   end;

BEGIN
   cont := Nmax;                                  { inicializa contador }
   while (cont >= 1) do                          { inicializamos vector }
   begin
      vector[(Nmax - cont + 1)] := cont;
      write(cont);
      cont := cont - 1;
   end;
   quicksort(1, Nmax);                                  { ordena vector }
   cont := 1;
   while (cont <= Nmax) do                       { muestra vector ordenado }
   begin
      write(vector[cont]);
      cont := cont + 1;
   end;
END.
