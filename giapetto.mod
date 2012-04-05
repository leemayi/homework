#
# Giapetto's problem
#
# This finds the optimal solution for maximizing Giapetto's profit
#

/* Decision variables */
var x1 >=0;  /* soldier */
var x2 >=0;  /* train */

/* Objective function */
maximize z: 3*x1 + 2*x2;

/* Constraints */
s.t. Finishing : 2*x1 + x2 <= 100;
s.t. Carpentry : x1 + x2 <= 80;
s.t. Demand    : x1 <= 40;

end;
