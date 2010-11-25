{
		autor : Rayco Hdez de Le¢n

		fecha : 19 de octubre del 2000

		practica : 1

		finalidad :
					El objetivo de esta pr ctica es la familiarizacion
					con el lenguaje pascal - que es el que vamos a
					implementar a lo largo del curso.

		programa :

																		   
	   Escribir un programa en Tp - que genere todos los valores i,j,k.l         
 positivos menores de 20, tales que verifiquen la relaci¢n:                
																		   
	  i^3+j^3+k^3 = l^3                                                   

		modo de empleo :
									hay que introducir hasta que numero hay que realizar la prueba
									el programa se ejecuta y solo tenemos que pulsar un numero
									para que sigua la ejecucion					

Por ejemplo, si la entrada es 10, el programa produce la siguiente salida:
3456
3546
4356
4536
5346
5436

(despues de cada numero, hay que introducir cualquier numero para que escriba el siguiente.)
}
																		   

program calculo;

{	variables :
					i, j, k, l : contadores de bucle
					valor1 : resultado de la izquierda del igual
					valor2 : resultado de la derecha del igual
					n : hasta que numero vamos a buscar soluciones
					num : variable para pulsar una tecla
}
 
var
		n, valor1, valor2, i, j, k, l, num : integer;

begin
	read(n);	
	i := 1;    
	while i < n - 1 do
	begin
		j := 1;
		while j < n - 1 do
		begin
			 k := 1;
			 while k < n - 1 do
			 begin
				  l := 1;
				  while l < n - 1 do
				  begin
					   valor1 := i * i * i + j * j * j + k * k * k;
					   valor2 := l * l * l;
						if valor1 = valor2 then
						begin
							 write(i);
							 write(j);
							 write(k);
							 write(l);
							 read(num);
						end;
						l := l + 1;
				  end;
				  k := k + 1;
			 end;
			 j := j + 1;
		end;
		i := i + 1;
	end;
end.
