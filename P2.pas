PROGRAM EJER7B;
        VAR radio , volumen:REAL;
BEGIN
        {Este programa calcula el volumen de una esfera}

        WRITE ('PARA CALCULAR EL VOLUMEN DE LA ESFERA ESCRIBA EL RADIO: ');
        READ (radio);
        volumen := 3.1416*radio*radio/3*radio*4;

        WRITE ('VOLUMEN DE LA ESFERA: ');         WRITE(volumen)
END.
