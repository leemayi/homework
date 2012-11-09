#
# Diet problem
#
# This finds the optimal solution for minimizing the cost of my diet
#

/* sets */
set FOOD;
set NEED;

/* parameters */
param NutrTable {i in FOOD, j in NEED};
param Cost {i in FOOD};
param Need {j in NEED};

/* decision variables: x1: Brownie, x2: Ice cream, x3: soda, x4: cake*/
var x {i in FOOD} >= 0;

/* objective function */
minimize z: sum{i in FOOD} Cost[i]*x[i];

/* Constraints */
s.t. const{j in NEED} : sum{i in FOOD} NutrTable[i,j]*x[i] >= Need[j];

/* data section */
data;

set FOOD := Brownie "Ice cream" soda cake;
set NEED := Calorie Chocolate Sugar Fat;

param NutrTable: Calorie        Chocolate       Sugar   Fat:=
Brownie          400            3               2       2
"Ice cream"      200            2               2       4
soda             150            0               4       1
cake             500            0               4       5;

param Cost:=
Brownie         0.5
"Ice cream"     0.2
soda            0.3
cake            0.8;

param Need:=
Calorie         500
Chocolate       6
Sugar           10
Fat             8;

end;
