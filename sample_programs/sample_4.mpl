var hk : int;
hk := 2 + 3 * 4 + 5;
var hk_string : string := "2 + 3 * 4 + 5";
print hk_string;
print " = ";
print hk;
print "\n";
assert (hk = 19);

var ep : int := 2 + (3 * 4) + 5;
var ep_string : string := "2 + (3 * 4) + 5";
print ep_string;
print " = ";
print ep ;
print "\n";
assert (ep = 19);

assert (hk = ep);
if hk = ep do
  print "Both expressions give the same result!\n";
else
  print "This does not work :(\n";
end if;

var is_same : bool;

is_same := 5 + (7 * 5) = 40;
print "5 + (7 * 5) = 40 is ";
print is_same;
print "\n";

print "5 + (7 * 5) = (30 + 10) is ";
print 5 + (7 * 5) = (30 + 10);
print "\n";
print "Note that in Mini-PL, 5 + (7 * 5) = 30 + 10 is not a correct expression. In Mini-PL, the expression is executed such that first the left hand side expression 5 + (7 * 5) gives 40, which is then compared to the right hand side integer 30, giving a bool type value. Then the bool value should be added to integer value 10. But, according to the definition of the language, addition of two different types is forbidden.\n";
// print 5 + (7 * 5) = 30 + 10; // If you uncomment this and run the code, this results to a runtime error.
print "\n";