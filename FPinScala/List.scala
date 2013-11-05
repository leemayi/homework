import scala.annotation.tailrec

object ListTest {

sealed trait List[+A]

case object Nil extends List[Nothing]
case class Cons[+A](head: A, tail: List[A]) extends List[A]

object List {
  def foldRight[A,B](l: List[A], z: B)(f: (A, B) => B): B =
    l match {
      case Nil => z
      case Cons(x, xs) => f(x, foldRight(xs, z)(f))
    }

  def sum2(l: List[Int]): Int =
    foldRight(l, 0)(_ + _)

  def product2(l: List[Int]): Int =
    foldRight(l, 1)(_ + _)

  def sum(ints: List[Int]): Int = ints match {
    case Nil => 0
    case Cons(x, xs) => x + sum(xs)
  }

  def product(ds: List[Double]): Double = ds match {
    case Nil => 1.0
    case Cons(0.0, _) => 0.0
    case Cons(x, xs) => x * product(xs)
  }

  def apply[A](as: A*): List[A] =
    if (as.isEmpty) Nil
    else Cons(as.head, apply(as.tail: _*))

  val example = Cons(1, Cons(2, Cons(3, Cons(4, Nil))))
  val example2 = List(1.0, 0.2, 3.3)
  val total = sum(example)

  def tail[A](as: List[A]): List[A] = as match {
    case Nil => Nil
    case Cons(x, xs) => xs
  }
  def drop[A](as: List[A], n: Int): List[A] = n match {
    case 0 => as
    case i => drop(tail(as), n-1)
  }
  def dropWhile[A](l: List[A], f: A => Boolean): List[A] = 
    l match {
      case Cons(h, t) if f(h) => dropWhile(t, f)
      case _ => l
    }
  def setHead[A](l: List[A], x: A): List[A] =
    Cons(x, tail(l))
  def init[A](l: List[A]): List[A] = l match {
    case Nil => Nil
    case Cons(x, Nil) => Nil
    case Cons(h, t) => Cons(h, init(t))
  }
  def length[A](l: List[A]): Int =
    foldRight(l, 0)((_, z) => z + 1)
  @tailrec
  def foldLeft[A,B](l: List[A], z: B)(f: (B, A) => B): B = l match {
    case Nil => z
    case Cons(h, t) => foldLeft(t, f(z, h))(f)
  }
  def sum3(l: List[Int]): Int =
    foldLeft(l, 0)(_ + _)
  def reverse[A](l: List[A]): List[A] =
    foldLeft(l, List[A]())((z, x) => Cons(x, z))
  def append[A](l: List[A], r: List[A]): List[A] =
    foldRight(l, r)(Cons(_, _))
  def concat[A](l: List[List[A]]): List[A] =
    foldRight(l, Nil: List[A])(append)
  def add1(l: List[Int]): List[Int] =
    foldRight(l, Nil:List[Int])((x, z) => Cons(x+1, z))
  def doubleToString(l: List[Double]): List[String] =
    foldRight(l, List[String]())((x, z) => Cons(x.toString, z))
  def map[A,B](l: List[A])(f: A => B): List[B] =
    foldRight(l, Nil: List[B])((x, z) => Cons(f(x), z))
  def filter[A](l: List[A])(f: A => Boolean): List[A] =
    foldRight(l, Nil: List[A])((x, z) => if (f(x)) Cons(x, z) else z)
  def flatMap[A,B](l: List[A])(f: A => List[B]): List[B] =
    //foldRight(l, Nil: List[B])((h, t) => append(f(h), t))
    concat(map(l)(f))
  def zipWith[A,B,C](l: List[A], r: List[B])(f: (A, B) => C): List[C] =
    (l, r) match {
      case (_, Nil) => Nil
      case (Nil, _) => Nil
      case (Cons(h1, t1), Cons(h2, t2)) => Cons(f(h1, h2), zipWith(t1, t2)(f))
    }
  def foldRightViaFoldLeft[A,B](l: List[A], z: B)(f: (A,B) => B): B = 
    foldLeft(reverse(l), z)((b,a) => f(a,b))
  def foldRightViaFoldLeft_1[A,B](l: List[A], z: B)(f: (A,B) => B): B = 
    foldLeft(l, (b:B) => b)((g,a) => b => g(f(a,b)))(z)
  def foldLeftViaFoldRight[A,B](l: List[A], z: B)(f: (B,A) => B): B = 
    foldRight(l, (b:B) => b)((a,g) => b => g(f(b,a)))(z)
  def hasSubsequence[A](l: List[A], sub: List[A]): Boolean = {
    @tailrec
    def startsWith(l: List[A], sub: List[A]): Boolean = (l, sub) match {
      case (_, Nil) => true
      case (Nil, _) => false
      case (Cons(lh, lt), Cons(subh, subt)) if subh == lh => startsWith(lt, subt)
      case _ => false
    }
    l match {
      case Nil => startsWith(l, sub)
      case Cons(h, t) => if (startsWith(l, sub)) true else startsWith(t, sub)
    }
  }
}

}
