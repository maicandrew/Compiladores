PROGRAM EJER36;
 VAR num:INTEGER;
(* Escribe el nombre del dia
segun el numero *)
BEGIN
 WRITE ('Escriba un numero para ver con que dia corresponde: ');
 READ (num);
 IF num=1 THEN
 WRITE ('Lunes');
 IF num=2 THEN
 WRITE ('Martes');
 IF num=3 THEN
 WRITE ('Miercoles');
 IF num=4 THEN
 WRITE ('Jueves');
 IF num=5 THEN
 WRITE ('Viernes');
 IF num=6 THEN
 WRITE ('Sabado');
 IF num=7 THEN
 WRITE ('Domingo')
END.
