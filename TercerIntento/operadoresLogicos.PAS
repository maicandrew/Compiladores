program logicos;
   
    VAR
    x : boolean;
    y : boolean;
    z : boolean;
begin
    x := TRUE;
    y := false;
    z := x AND y;
    writeln(z);
    z := x OR y;
    writeln(z);
    z := NOT x;
    writeln(z)

end.
