object RandomTest{

import java.util.Random

trait Generator[+T] {
  self =>

  def generate: T

  def map[S](f: T => S): Generator[S] = new Generator[S] {
    def generate = f(self.generate)
  }

  def flatMap[S](f: T => Generator[S]): Generator[S] = new Generator[S] {
    def generate = f(self.generate).generate
  }
}

val integers = new Generator[Int] {
  val rand = new java.util.Random
  def generate = rand.nextInt()
}
val booleans = for (i <- integers) yield i > 0
def pairs[T, U](t: Generator[T], u: Generator[U]) = for (
  x <- t;
  y <- u
) yield (x, y)
def single[T](x: T): Generator[T] = new Generator[T] {
  def generate = x
}
def choose(lo: Int, hi: Int): Generator[Int] =
  for (x <- integers) yield lo + x % (hi - lo)
def oneOf[T](xs: T*): Generator[T] =
  for (idx <- choose(0, xs.length)) yield xs(idx)

def lists: Generator[List[Int]] = for {
  isEmpty <- booleans
  list <- if (isEmpty) emptyLists else nonEmptyLists
} yield list
def emptyLists = single(Nil)
def nonEmptyLists = for {
  head <- integers
  tail <- lists
} yield head :: tail

trait Tree
case class Inner(left: Tree, right: Tree) extends Tree
case class Leaf(x: Int) extends Tree
def trees: Generator[Tree] = for {
  isLeaf <- booleans
  tree <- if (isLeaf) leafs else inners
} yield tree
def leafs: Generator[Leaf] = for {
  x <- integers
} yield Leaf(x)
def inners: Generator[Tree] = for {
  l <- trees
  r <- trees
} yield Inner(l, r)

def test[T](r: Generator[T], noTimes: Int = 100)(test: T => Boolean) {
  for (_ <- 0 until noTimes) {
    val value = r.generate
    assert(test(value), "Test failed for: " + value)
  }
  println("Test passed "+noTimes+" times")
}



def main(args: Array[String]): Unit = {
  def makeStream[T](g: Generator[T]): Stream[T] = {
    def s: Stream[T] = g.generate #:: s
    s
  }

  //makeStream(lists) take 5 print
  val t = trees.generate
  println(t)

  test(pairs(integers, integers)) {
    case (x, y) => x + y > x - y
  }

}
}
