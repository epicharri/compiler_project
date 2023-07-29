print "Give a number in range [3, 20]: ";
var count : int;
read count;

if (!(count < 3)) & (count < 21) do
  var e : int;
  var p : int;
  for e in 1..count do
    for p in 1..e do
      print "*";
    end for;
    print "\n";
  end for;
  else print "You gave too low or high number. Goodbye!\n";
end if;

assert (e = (count + 1));
assert (p = (count + 1));
