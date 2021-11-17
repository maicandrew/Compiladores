PROGRAM EJER55;
       

        VAR sns:REAL; {salario neto semanal}
         htrabajadas, hextra:REAL;
         precioh, preciohextra:REAL;
         total:REAL;
         impuestos0,impuestos25,impuestos45:REAL;
        {Impuestos con cada % correspondiente}
BEGIN

     WRITELN ('INTRODUZCA LOS DATOS PARA CALCULAR EL SALARIO NETO SEMANAL');
     WRITELN ('');
     WRITE ('Las horas trabajadas semanales son 35, las demas debe ');
     WRITELN ('considerarlas como horas extra. Escriba en dolares.');
     WRITELN ('');
     WRITE ('Horas trabajadas: ');    
	 READLN (htrabajadas);
     WRITE ('Horas extra: ');         
	 READLN (hextra);
     WRITE ('Precio por cada hora: '); 
	 READLN (precioh);
     WRITELN ('');

     preciohextra:=precioh * 1.5;
     sns:=(htrabajadas * precioh) + (hextra * preciohextra);

     impuestos0:=0;
     impuestos25:=sns - ((sns - 50) * 0.25);
     impuestos45:=sns - ((sns - 90) * 0.45);

     IF sns <= 50 THEN
     WRITELN ('El salario neto semanal es: ')
     ELSE 
     WRITELN ('El salario neto semanal es: ')
END.
