#
# Rylon production proccess
#
# This finds the optimal solution for maximizing Rylon's profit
#
/* sets */
set PROD;

/* parameters */
param Rev{i in PROD};
param Cost{i in PROD};
param Labh{i in PROD};

var x{i in PROD} >= 0; /*x1: No. of oz of Regular Brute
                         x2: No. of oz of Luxury Brute
                         x3: No. of oz of Regular Chanelle
                         x4: No. of oz of Luxury Chanelle
                         x5: No. of lbs of raw material */

maximize z: sum{i in PROD} (Rev[i]*x[i] - Cost[i]*x[i]);

/* Constraints */
s.t. raw:   x['raw'] <= 4000;
s.t. time:  sum{i in PROD} Labh[i]*x[i] <= 6000;
s.t. mass1: x['rb'] + x['lb'] - 3*x['raw'] <= 0;
s.t. mass2: x['rc'] + x['lc'] - 4*x['raw'] <= 0;

data;
set PROD:= rb lb rc lc raw;

param Rev:= 
rb      7
lb      18
rc      6
lc      14
raw     0;

param Labh:=
rb      0
lb      3
rc      0
lc      2
raw     1;

param Cost:=
rb      0
lb      4
rc      0
lc      4
raw     3;

end;

