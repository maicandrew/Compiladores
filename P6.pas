program fact;
var f, n: integer;
begin
	read(n);
	if n <> 0 then
	begin
		f := n;
		n := n-1;
		while n <> 0 do begin
			f := n*f;
			n := n-1
		end
	end
	else begin
		f := 0
	end;
	write(f)
end.
