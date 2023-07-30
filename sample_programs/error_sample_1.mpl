// This program is for demonstration of the error catching during semantical analysis phase. In the program, the value of the control variable of the loop is tried to change inside the for loop. Therefore, the program will not be executed.

var e : int; // We use variable e as a control variable.

// var p: int; // By uncommenting this variable declaration, it can be experimented that during parsing, the later declaration of p gives an error.
for e in 50..60 do 
  print "Outer loop: control variable e = ";
  print e;
  print "\n";
  var p : int := 100; // During runtime this is ok, because the declaration is before the for loop having p as control variable.
  for p in 1..5 do
    print "Inner loop: control variable p = ";
    print p;
    print "\n";
    e := e + 2; // This will cause an error. Comment this line away to get the program work.
  end for;
end for;

