{Programa : Devolucion de Cambio
 Entrada : Cambio a devolver
 Salida : Monedas devueltas
 Autor : Jesús Díaz Díaz
 Fecha : 19/10/2000
}
program cambio;
const MAX_MONEDA = 6; 
      MAX_CANTIDAD = 150;
      INFINITO = 30000; 

type T_Cantidad = array[0..MAX_CANTIDAD] of integer; 
     T_Moneda = array[1..MAX_MONEDA] of integer; 
     T_Tabla = array[0..MAX_MONEDA] of T_cantidad; 

var 
  din_tabla: T_Tabla; 
  moneda: T_Moneda;  
  k,i,j: integer; 
  cambio: integer; 
   
 
begin 
  { inicializamos el vector de monedas } 
  moneda[1] := 1; 
  moneda[2] := 5; 
  moneda[3] := 10; 
  moneda[4] := 25; 
  moneda[5] := 50; 
  moneda[6] := 100; 
  { pedimos por teclado la cantidad a devolver } 
  read(cambio); 
   
  { Rellenamos la Tabla } 
  { Rellenamos la fila de 0 monedas }  
  j := 0; 
  while (j <= cambio) do 
  begin 
    din_tabla[0][j] := 0; 
    j := j + 1; 
  end; 
   
  { Rellenamos la fila de la moneda mas baja } 
  i := 1; 
  while (i <= MAX_MONEDA) do 
  begin 
    din_tabla[i][0] := 0;  
    i := i + 1; 
  end; 
  i := 1; 
  while (i <= MAX_MONEDA) do 
  begin 
    j := 1; 
    while (j <= cambio) do 
    begin 
      if (i = 1) and (j < moneda[i]) then 
        din_tabla[i][j] := infinito 
      else if (i = 1) then 
        din_tabla[i][j] := 1 + din_tabla[i][j - moneda[i]] 
      else if (j < moneda[i]) then 
        din_tabla[i][j] := din_tabla[i - 1][j] 
      else 
      begin 
        if ((din_tabla[i - 1][j]) < (1 + din_tabla[i][j - moneda[i]])) then  
          din_tabla[i][j] := din_tabla[i - 1][j] 
	else 
	  din_tabla[i][j] := 1 + din_tabla[i][j - moneda[i]]; 
      end;  
      j := j + 1; 
    end; 
    i := i + 1; 
  end; 
   
  { Buscamos la solucion en la tabla } 
  i := MAX_MONEDA; 
  j := cambio; 
  while (i <> 0) and (j <> 0) do 
  begin 
    if (din_tabla[i][j] = din_tabla[i - 1][j]) then 
    begin 
      i := i - 1; 
    end 
    else 
    begin 
      j := j - moneda[i]; 
      write(moneda[i]); 
    end; 
  end 
end. 
