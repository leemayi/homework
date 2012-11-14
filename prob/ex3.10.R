rt <- read.table('table3.6.txt', header=T)
rt <- rt[2:length(rt)]

AVG <- apply(rt, 1, mean)
sort(AVG, decreasing=T)

cor(rt)

stars(rt)

attach(rt)
rt$G1 <- (SC+LC+SMS+DRV+AMB+GSP+POT)/7
rt$G2 <- (FL+EXP+SUIT)/3
rt$G3 <- (LA+HON+KJ)/3
rt$G4 <- AA
rt$G5 <- APP

stars(rt[c("G1", "G2", "G3", "G4", "G5")])
