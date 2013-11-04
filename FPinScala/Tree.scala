object test {

sealed trait Tree[+A]
case class Leaf[A](value: A) extends Tree[A]
case class Branch[A](left: Tree[A], right: Tree[A]) extends Tree[A]

object Tree {
  def size[A](t: Tree[A]): Int = t match {
    case Leaf(_) => 1
    case Branch(left, right) => 1 + size(left) + size(right)
  }
  def maxinum(t: Tree[Int]): Int = t match {
    case Leaf(value) => value
    case Branch(left, right) => maxinum(left) max maxinum(right)
  }
  def depth[A](t: Tree[A]): Int = t match {
    case Leaf(_) => 0
    case Branch(left, right) => 1 + (depth(left) max depth(right))
  }
  def map[A,B](t: Tree[A])(f: A => B): Tree[B] = t match {
    case Leaf(value) => Leaf(f(value))
    case Branch(left, right) => Branch(map(left)(f), map(right)(f))
  }
  def fold[A,B](t: Tree[A])(f: A => B)(g: (B, B) => B): B =
    t match {
      case Leaf(v) => f(v)
      case Branch(l, r) => g(fold(l)(f)(g), fold(r)(f)(g))
    }
  def size2[A](t: Tree[A]): Int = fold(t)(_ => 1)(1 + _ + _)
  def maxinum2(t: Tree[Int]): Int = fold(t)((x: Int) => x)(_ max _)
  def depth2[A](t: Tree[A]): Int = fold(t)(a => 0)((a, b) => 1 + (a max b))
  def map2[A,B](t: Tree[A])(f: A=>B): Tree[B] =
    fold(t)(a => Leaf(f(a)): Tree[B])(Branch(_, _))

  val example = Branch(Branch(Leaf(1), Leaf(2)), Leaf(3))
}

  def main(args: Array[String]): Unit = {
    println(Tree.size(Tree.example))
    println(Tree.size2(Tree.example))
    println(Tree.maxinum(Tree.example))
    println(Tree.maxinum2(Tree.example))
    println(Tree.depth(Tree.example))
    println(Tree.depth2(Tree.example))
    println(Tree.map(Tree.example)(_*2))
    println(Tree.map2(Tree.example)(_*2))
  }

}


