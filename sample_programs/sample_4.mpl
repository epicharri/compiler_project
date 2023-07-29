var hk : int := 0;
hk := 2 + 3*4 + 5;
print "2 + 3*4 + 5 = ";
print hk;
print ", because in Mini-PL language, \"Nested expressions are always fully parenthesized to specify the execution order of operations.\", and thus 2 + 3*4 + 5 is the same as (2 + 3)*4 + 5 = 25.\n";
assert (hk = (((2 + 3) * 4) + 5));
print "Consider the expression 2 + (3*4) + 5, which equals to ";
hk := 2 + (3*4) + 5;
print hk;
print ", because since 3*4 is surrounded with parenthesises, the result is 2 plus 3*4 plus 5, equaling 19.\n";
assert (hk = 19);

var is_same : bool;

is_same := 5 + (7 * 5) = 40;
print "5 + (7 * 5) = 40 is ";
print is_same;
print "\n";

print "5 + (7 * 5) = (30 + 10) is ";
print 5 + (7 * 5) = (30 + 10);
print "\n";
print "Note that in Mini-PL, 5 + (7 * 5) = 30 + 10 is not correct expression. In Mini-PL, the expression is executed such that first the left hand side expression 5 + (7 * 5) gives 40, which is then compared to the right hand side integer 30, giving a bool type value. Then the bool value should be added to integer value 10. But, according to the definition of the language, addition of two different types is forbidden.\n";
// print 5 + (7 * 5) = 30 + 10;
print "\n";
