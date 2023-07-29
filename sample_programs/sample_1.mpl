// Try also to remove an end of statement symbol (;). It will give an error while parsing, and starts recovering process. The parsing will start after the next semicolon.
var X : int := 4 + (6 * 2);
assert (X=16);
print X;
print "\n";
