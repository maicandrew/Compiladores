(* *************************************** *

        mandelbrot.pas

        El conjunto de Mandelbrot es el más 
        conocido de los conjuntos fractales y el 
        más estudiado. Se conoce así en honor al 
        matemático Benoît Mandelbrot, que 
        investigó sobre él en los años setenta. 

 * *************************************** *)

program mandelbrot;

function in_mandelbrot(x0 real, y0 real, n integer) bool;

var x real := 0.0;
var y real := 0.0;
var xtemp real;

begin
        while n > 0 do;
        begin
                xtemp := x*x - y*y + x0;
                y := 2.0*x*y + y0;
                x := xtemp;
                n := n - 1;
                if x*x + y*y > 4.0 then
                        return false
        end;
        return true
end

function mandel() int;

var dx float := (xmax - xmin)/width;
var dy float := (ymax - ymin)/height;

var y float := ymax;
var x float;

begin
        while y >= ymin do
        begin
                x := xmin;
                while x < xmax do;
                begin
                        if in_mandelbrot(x,y,threshhold) then
                                write('*');
                        else
                                write('.');
                        x := x + dx;
                end;
                write('\n');
                y := y - dy
        end;
        return 0
end

const xmin = -2.0;
const xmax = 1.0;
const ymin = -1.5;
const ymax = 1.5;
const width = 80.0;
const height = 40.0;
const threshhold = 1000;

begin
        return mandel()
end