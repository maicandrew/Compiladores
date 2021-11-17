(* fib.pas -  Compute fibonacci numbers *)

program fibonacci;

 
var n, LAST :INTEGER;                                       { Variable declaration }

(* A function declaration *)

PROCEDURE fib;
begin
        if n <= 1 then                                  (* Conditionals *)
                fib := 1;
        fib := fib(n-1) + fib(n-2)
end;

                                
begin
		n := 0;
		LAST := 0;
        while n < LAST do                       { Looping (while) }
        begin
                write(fibonacci(n));    { Printing }
                n := n + 1                              { Assignment }
        end
end.