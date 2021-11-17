PROGRAM EJER6B;
        VAR espacio,tiempo,espacio2,tiempo2:REAL;
        VAR velocidad,velocidad2:REAL;
BEGIN
        {Este programa calcula la velocidad de un cuerpo}

        ClrScr;

        WRITE ('Para calcular la velocidad debe escribirlo en
	unidades ');
        WRITE ('del sistema internacional');
        WRITELN (' ');
        WRITE ('Escriba el espacio recorrido: ');       READLN (espacio);
        WRITE ('Escriba el tiempo transcurrido: ');     READLN (tiempo);
        WRITELN (' ');

        velocidad:=(espacio)/(tiempo);

        WRITE ('VELOCIDAD DEL PROYECTIL: ');
        WRITE (velocidad:5:2); WRITELN (' m/s');

        WRITELN (' ');
        WRITELN ('Si lo desea en Km/h introduzca los datos: ');
        WRITELN (' ');
        WRITE ('Escriba el espacio recorrido: ');     READLN (espacio2);
        WRITE ('Escriba el tiempo transcurrido: ');   READLN (tiempo2);
        WRITELN (' ');

        velocidad2:=(espacio2)/(tiempo2);

        WRITE (velocidad2:5:2); WRITE (' Km/h ');
END.