assert(1=1);
var X : int := 4 + (8 + (6 * 2) + 5);
print X;
if !(1=1) do
print "1 is not equal to 1\n";
else
print "1 is equal to 1\n";

end if;
print X;
assert (X = X);
print 1;
var hk : int;
hk := 1 + 2 + 3;
var harri : string;
harri := "Harri" + " K" + ".";
print harri;
assert (!(!(1=1)));
var tottako : bool;
tottako := !(1=1);
var ntimes : int := 80;
var aa : int := 0;
var XD : int;
for XD in 20+50..ntimes-1 do
//  XD := XD + 2;
  print XD;
  print "\n";
  for aa in 1..10 do
    hk := aa;
    print hk;
    print "\n";
    //XD := XD + 10;
  end for;
end for;

var a_number : int := 1;
var a_string : string := "";
var a_bool : bool;
a_bool := !(1=1) & (2=1) & ("H" = "H");
print a_bool;

var ep : int := 100;
print (4 + (8 + (6 * 2) + 5)) * 100;
print !(2=2);
print !(2=3);
print "\nGive a number\n";
read a_number;
if (a_number / 2) * 2 = a_number do
  print a_number;
  print " is even.\n";
else
  print a_number;
  print " is odd.\n";
end if;

print "First line of the string.\nSecond line of the string.\n";
print "\a\b\f\n\r\t\v\"";
print "start\\end";
