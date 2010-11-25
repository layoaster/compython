{ *********************************************************
  PROGRAMA: BRESENHAM
  FUNCION: Genera una linea entre dos extremos de la pantalla
	de texto por medio del metodo de Bresenham.
  AUTOR: José Julio Ramos Pérez
  UTILIZACION: Introduce la primera x, la primera y
         y luego la segunda x y la segunda y
			y saldra en pantalla las coordenadas de la linea. 
			Los limites de la pantalla son 80 y 80.
  ********************************************************* }

program lineabresenham;
type
	{ Vector de la pantalla }
	TColumna = array [1..80] of boolean;
	TPunto = array [1..80] of TColumna;
var
	pantalla: TPunto;
	x, x2, y, y2: integer; {Coordenadas de la linea}
	DELIMITADOR : integer;

{Procedimiento que 'pinta en pantalla' en la coordenada dada }

procedure putpixel(x, y: integer);
begin
	pantalla[x][y] := true;
end;

{Procedimiento de la linea de Bresenham}
procedure bresenham(x, y, x2, y2: integer);
var
	d, dx, dy, ai, bi, xi, yi: integer;
begin
	if x < x2 then
	begin
		xi := 1;
		dx := x2 - x;
	end
	else
	begin
		xi := -1;
		dx := x - x2;
	end;
	if (y < y2) then
	begin
		yi := 1;
		dy := y2 - y;
	end
	else
	begin
		yi := -1;
		dy := y - y2;
	end;
	putpixel(x, y);
	if dx > dy then
	begin
		ai := (dy - dx) * 2;
		bi := dy * 2;
		d := bi - dx;
		while x <> x2 do
		begin
			if d >= 0 then
			begin
				y := y + yi;
				d := d + ai;
			end
			else
				d := d + bi;
			x := x + xi;
			putpixel(x,y);
		end
	end
	else
	begin
		ai := (dx - dy) * 2;
		bi := dx * 2;
		d := bi - dy;
		while y <> y2 do
		begin
			if d >= 0 then
			begin
				x := x + xi;
				d := d + ai;
			end
			else
				d := d + bi;
			y := y + yi;
			putpixel(x, y);
		end
	end;
end;

begin
	DELIMITADOR := -1;
	{ Pedimos las coordenadas en pantalla}
	read(x);
	read(y);
	read(x2);
	read(y2);
	bresenham(x, y, x2, y2);
	{ Ahora mostramos en pantalla las coordenadas de la linea }
	y := 1;
	while y <= 80 do
	begin
		x := 1;
		while x <= 80 do
		begin
			if pantalla[x][y] = true then
			begin
			   write(DELIMITADOR*x);	
				write(DELIMITADOR*y);
			end;
			x := x + 1;
		end;
		y := y + 1;
	end
end.
