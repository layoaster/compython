{****************************************************************************
    El programa implementado para probar el compilador de PASCAL- es el 
    algoritmo utilizado para obtener los numeros primos menores de un 
    cierto valor que se le solicita al usuario (Criba de Erat¢stenes).
    NOTA: Pasos a seguir en la ejecuci¢n de CRIBA.P
          1._) Introduce el valor m ximo (Aparecer n en pantalla todos
               los n£meros menores que el introducido).
          2._) Se debe pulsar el 0 para continuar (Aparecer n en
               pantalla todos los n£meros primos menores que dicho valor).
          3._) Se debe pulsar el 0 para terminar.
*****************************************************************************}
program CRIBA;

const MAXN  100;                            {error}

type numeros = array [2..MAXN] of integer;

var vector_num : numeros                    {error}
    N          : integer;

{****************************************************************************
  FINALIDAD: Procedimiento encargado de inicializar un vector de numeros de
             1 a N
*****************************************************************************}
procedure inicializar_numeros (vr vector_num : numeros; N : integer); {error}

var num : integer;

begin                                           
  num := 2;
  while num <= N) do                       {error}
  begin
    vector_num [num]. := num;              {error}
    num := num + 1;
                                           {error}
end;

{****************************************************************************
  FINALIDAD: Procedimiento que deja en el vector solo los primos menores
             que N.
*****************************************************************************}
procedure eliminar_no_primos (var vector_num  numeros; N : integer); {error}

var primo_actual : integer;
var num          : integer;                {error}

begin
  primo_actual := ;                        {error}
  while (primo_actual*primo_actual) <= N do
  begin
    num := 2;
    while (primo_actual*num <= N) do       
    begin
      vector_num [primo_actual*num] := 0;
      num := num + 1;
    end;
    primo_actual := primo_actual + 1;
    while (primo_actual <= N) an (vector_num [primo_actual] = 0) do {error}
      primo_actual := primo_actual + 1;
  end;
end;

{****************************************************************************
  FINALIDAD: Procedimiento encargado de mostrar en pantalla los elementos
             del vector distintos de 0.
*****************************************************************************}
procedure mostrar_numeros (vector_num : numeros; N : integer);

var num : integer;

begin
  num := 2;
  while num <= N do
  begin
    if vector_num [num] <> 0 then
      write (vector_num [num]);
    num := num + 1;
  end;
end;

{****************************************************************************
  FINALIDAD: Procedimiento encargado de parar la ejecuci¢n del programa hasta
             que se pulse el cero.
*****************************************************************************}
procedure pause;

var stop : integer;

begin
  stop := 1;
  while stop <> 0 do
    read (stop);
end;

{****************************************************************************}
begin
  read (N);
  inicializar_numeros (vector_num, N;         {error}
  mostrar_numeros (vector_num, N);
  pause ();                                   {error}
  eliminar_no_primos (vector_num, N);
  mostrar_numeros (vector_num N);             {error}
  pause;
end.
