var x1 >= 0;
var x2 >= 0;
var x3 >= 0;
var x4 >= 0;

minimize z: 0.5*x1 + 0.2*x2 + 0.3*x3 + 0.8*x4;

s.t. Calories : 400*x1 + 200*x2 + 150*x3 + 500*x4 >= 500;
s.t. Chocolate : 3*x1 + 2*x2 >= 6;
s.t. Sugar : 2*x1 + 2*x2 + 4*x3 + 4*x4 >= 10;
s.t. Fat : 2*x1 + 4*x2 + x3 + 5*x4 >= 8;

end;

