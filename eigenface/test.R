dump.file <- function(a, fname) { write.table(a, fname, row.names=F, col.names=F) }
toFF <- function(a) { a=a-min(a); a*255/max(a) }
dist <- function(i, j) {sum((i-j)**2)}
predict <- function(x) { which.min(apply(training_weights, 2, function(i) {dist(i,x)})) }
shuffle <- function(a) { a[sample.int(length(a), length(a))] }

faces <- read.table('yalefaces/all2.txt')
data <- faces[,-1]
total <- dim(data)[1]
N <- dim(data)[2]

M <- as.integer(total*.9)
training <- t(data[1:sz,])
testing <- t(data[(sz+1):total,])
labels <- faces[,1]
testing_labels <- labels[(sz+1):total]

mean.face <- apply(training, 1, sum) / M
dump.file(t(mean.face), 'meanface.txt')

A <- apply(training, 2, function(i) {i-mean.face})
L <- t(A) %*% A
e <- eigen(L)
u <- A %*% e$ve

cca <- e$va/sum(e$va)
ca <- cumsum(cca)
dump.file(t(cbind(e$va, cca, ca)), 'eigenvalues.txt')
dump.file(t(apply(u, 2, toFF)), 'eigenfaces.txt')

R <- u[,1:40]
training_weights <- t(R) %*% A
testing_weights <- t(R) %*% apply(testing, 2, function(i) {i-mean.face})

apply(testing_weights, 2, predict)

