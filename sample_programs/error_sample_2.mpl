var e : int;
var p : int;

for e in 1..3 do
  for p in 10..13 do
    print e*p;
    if ((e*p) / 2) * 2 = (e*p) do
      print " is even number.\n";
    else
      print " is odd number.\n";
    end if;
  // end for; // Because this end for is not executed, there will be an error.
end for;
