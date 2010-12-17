
 Program golbath;
 type  tr  = array [1..10] of integer;
 Var
  npmin : integer;           {* El valor inicial del c¢mputo o la cota menor/}
  npmax : integer;           {/* El valo final del c¢mputo o la cota mayor */ }

 {**********************************************************************/}
  Procedure buscarprimo(prim : integer);
  {*Busca el mayor primo del valor pasado,una vez encontrado se le resta
  al valor par y ese n£mero que ser  tambi‚n primo ser  el otro miembro
  de la adici¢n del n£mero par,que lo escribiremos en el fichero*}
  var
    prim1,prim2,i : integer;
    encontrado,p : boolean;
  begin
	i := prim - 1;      {* comienzo ha buscar el mayor primo desde el anterior*/}
	encontrado := FALSE; {/*puesto que un n£mero par no es primo*/}
	while  ((i > 1 )AND (encontrado = FALSE)) do
    begin
      primo(i,p);
      if p then
      begin
		  prim2 := prim -i;
		  prim1 := i;
		  encontrado := TRUE;
		  write(prim);
		  write(prim1);
          write(prim2);
      end;
	 i := i -1 ;
    end;
  end;
{**********************************************************************}
  Procedure leerdato;   {*Pedir y comprobar valores de entrada *}
  var
    i : integer;
    p : boolean;
  begin
    read(npmin);
    par(npmin,p);
    if p then
    begin
      read(npmax);
      par(npmax,p);
      if p then
      begin
         i := npmin;
        While (i <= npmax) do   {  Mando a buscar los primos de los }
        begin
          if(((i mod 2 ) = 0) AND (i > 2)) then  { N£meros pares comprendidos en el */}
		      buscarprimo(i);         { rango y mayores que dos */}
          i := i +1 ;
        end;
      end;
    end;
  end;
 {************************************************************************}
 Begin
  leerdato;
 End.
