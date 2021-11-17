program fact;
VAR n, f : integer;
BEGIN
  read(n);
  if n <> 0 THEN BEGIN
      f := n;
      n := n-1 + a;
      while n > 0 do BEGIN
        f := f*n;
        n := n - 1
      END
    END
  else
    BEGIN
      f := 0
    END;
  write(f)
end.
