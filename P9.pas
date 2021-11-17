(* fib.pas -  Compute fibonacci numbers *)

program fibonacci;

var LAST, n : INTEGER;
 {w : array [0..3] of INTEGER;   }                                 (* A constant declaration *)

(* A function declaration *)

function fib(n : INTEGER; y : INTEGER) : INTEGER ;
begin
        if n <= 1 then                                  (* Conditionals *)
                fib := 1 ;
        fib := fib(n-1) + fib(n-2)
end;

procedure hola;
begin
	write('hola')
end;

                                 { Variable declaration }
begin
		n := 0;
		LAST := 30;
        while n < LAST do                       { Looping (while) }
        begin
                w[0] := 5;
                write(fibonacci(n));    { Printing }
                n := n + 1                              { Assignment }
        end
end.
