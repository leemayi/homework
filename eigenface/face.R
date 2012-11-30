dump.file <- function(a, fname) { write.table(a, fname, row.names=F, col.names=F) }
toFF <- function(a) { a <- a-min(a); a*255/max(a) }
dist <- function(i, j) {sum((i-j)**2)}
predict <- function(x) { which.min(apply(training_weights, 2, function(i) {dist(i,x)})) }
shuffle <- function(a) { m <- dim(a)[1]; p <- sample.int(m,m); a[p,] }

faces <- read.table('datain.txt')
faces <- shuffle(faces)
data <- faces[,c(-1, -2)]
labels <- faces[,1]

total <- dim(data)[1]
N <- dim(data)[2]
M <- 100

training <- t(data[1:M,])
testing <- t(data[(M+1):total,])
testing_labels <- labels[(M+1):total]

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

k <- which.max(ca>.9)
R <- u[,1:k]

training_weights <- t(R) %*% A
testing_weights <- t(R) %*% apply(testing, 2, function(i) {i-mean.face})

pr <- labels[apply(testing_weights, 2, predict)]
pr == testing_labels
correct_ratio <- sum(pr == testing_labels) / length(pr)
