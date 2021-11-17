PROGRAM EJER56;
        USES CRT;

        VAR num, x:INTEGER;
        VAR primo:INTEGER;
BEGIN
     ClrScr;

     WRITELN ('Introduzca un numero para comprobar si es primo.');
     WRITELN ('');

     x:=1;

     WRITE ('Introduzca el numero: ');
     READLN (num);
     WRITELN ('');

     REPEAT
     x:= x + 1;
     primo:= num mod x;

     WRITELN (primo);
     UNTIL x = 5;   WRITELN ('');

     WRITELN ('Si ninguno de los resultados es 0, el numero es primo.');
     WRITELN ('Si alguno es 0, el numero no es primo.');
END.
