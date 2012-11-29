faces <- read.table('yalefaces/all.txt')
dim(faces)
data <- faces[,-1]
dim(data)
training <- data[1:160,]
testing <- data[161:166,]
dim(training)
dim(testing)
training <- t(training)
testing <- t(testing)
dim(training)
dim(testing)
apply(training, 2, max)
max(apply(training, 2, max))
?scale
dim(trainig)
dim(training)
mf <- (apply(training, 1, sum) / 160)
dim(mf)
length(mf)
dump.file <- function(a, fname) {write.table(a, fname, row.names=F, col.names=F)}
dump.file(t(mf), 'meanface.txt')
dir()
dim(training)
A <- apply(training, 2, function(i) {i-mf})
dim(A)
L <- t(A) %*% A
dim(L)
e <- eigen(L)
e$va
u <- A %*% e$vec
dim(u)
dim(e$va)
dump.file(t(e$va), 'eigenvalues.txt')
sum((e$va/sum(e$va))[1])
sum((e$va/sum(e$va))[1:3])
sum((e$va/sum(e$va))[1:9])
sum((e$va/sum(e$va))[1:14])
sum((e$va/sum(e$va))[1:15])
sum((e$va/sum(e$va))[1:16])
sum((e$va/sum(e$va))[1:20])
sum((e$va/sum(e$va))[1:25])
sum((e$va/sum(e$va))[1:30])
sum((e$va/sum(e$va))[1:29])
sum((e$va/sum(e$va))[1:27])
sum((e$va/sum(e$va))[1:26])
sum((e$va/sum(e$va))[1:25])
sum((e$va/sum(e$va))[1:26])
dim(u)
dim(t(u[,1:26]))
dump.file(t(u[,1:26]), 'eigenfaces.txt')
R <- u[,1:26]
dim(R)
dim(u)
dim(U)
U <-u[,1:26]
dim(U)
models <- t(U) %*% apply(testing, 2, function(i) {i-mf})
dim(models)
models <- t(U) %*% apply(training, 2, function(i) {i-mf})
news <- t(U) %*% apply(testing, 2, function(i) {i-mf})
dim(models)
dim(news)
names <- data[,1]
dim(names)
length(names)
?min
dir()
ls()
dim(news)
dim(models)
2**2
3**2
dist <- function(i, j) {sum((i-j)**2)}
?which.max
dim(models)
predict <- function(x) { which.min(apply(models, 2, function(i) {dist(i,x)})) }
ls()
predict(new[1])
predict(news[1])
which.max(1:5)
which.max(5:1)
dist(news[1], models[1])
dim(models)
dim(apply(models, 2, function(i) {dist(i, news[1])}))
length(apply(models, 2, function(i) {dist(i, news[1])}))
predict <- function(x) { which.min(apply(models, 2, function(i) {dist(i, x)})) }
predict(news[1])
predict(news[2])
names[55]
ls()
labels <- data[,1]
dim(labels)
length(labels)
labels[55]
ls()
labels <- faces[,1]
predict(news[,1])
predict(news[,2])
predict(news[,3])
predict(news[,4])
predict(news[,5])
predict(news[,6])
labels[c(89,126,141,103,120,137)]
labels[161:166]
