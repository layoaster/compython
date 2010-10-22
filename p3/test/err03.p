{ Pascal- Test_2a : Syntax Errors }

program test_rec_err;

const
	a := 1;                                 { Error }
	b = 2;
	c = ;                                   { Error }
	d = 4;
	e = 3                                   { Error }

type
	s1 = recrod f,g: integer end;           { Error }
	s2 = record
		f,g: integer;
		h,i,j;r: boolean;               { Error }

	t1 = array[1..2] of integer;
	t2 = array[1..] of integer;             { Error }
	t3 = array[1..] integer;                { Error }

var
	x, x1: integer;
	x2: t3                                  { Error }
	x3, y1, y2: s1;
	b1, b2: boolean;
	z:= integer;                            { Error }

	procedure HolaMundo (x,y: integer);
	begin
		t1[3] := 3456;                  
		b1 = FALSE;                     { Error, becomes }
	end                                     { Error, el semicolon }

	procedure;                              { Error, falta id }
	var                                     { Error falta las variables }
	begin
		v := 5 * 3 +;                   { Error falta id }
	end;

	procedure MasErrores (suma);            { Error, falta el tipo }
						{ Error, falta el begin }
		v := 5 * 3 +/ and or 345 + (8) * 0 - 3; { Error, mala expresion }
		if b = true                     { Error falta el then }
			y := 45;                { Error falta el begin }
			x := 6456 or 3343       { Error fata el end }
		else
			nada;
	end;

begin
	if = 2 then                             { Error }
		x := 1;                         { Error }
	else
		x := 0;
	while 2 == x do                         { Error }
		begin
		b1 := TRUE;
		b2 = b1;                        { Error }
		x3 := y1                        { Error }
		end;
	write(x);
	read(x);
	HolaMundo(1,2,);                        { Error }

end                                             { Error falta el punto }
