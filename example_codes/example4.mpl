if 2 + 3 < 6 do
print "Totta!";
end if;

fortesting := "There must be slash slash: //. And there a printed comment /*comment*/";
multiline_string = "First row of the string 
second row of the string."
var y : , int; // Here is an error.
var hk : int := 2000    ;
var tosi : bool;
print "Give a number";
hk := hk + 20;
assert (hk = 2020);
var n : int; // This is a comment.
read n;
/* Here is a multiline
comment. /*Here is also a nested
multiline comment.
/*Another nested comment.*/
*/
These all should be removed.
*/
var v : int := 1;
var i : int;
for i in 1..n-2 do
v := (v * i);
end for;
print "The result is: ";
print v;
