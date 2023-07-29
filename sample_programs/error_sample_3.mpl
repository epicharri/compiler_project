var i : int := 5;
var s : string := ":)";
var b : bool := (1=1);

// print i + s + b; // Incompatible data types are found in parsing phase.
// print !1=7; // Unexpected token '=' found during parsing phase.
print 2*8=8*2+5;

// print "H" * "K"; // Multiplication of strings is not allowed. This is found during interpretation.

print !(1=7); // This works correctly.
print "\n";