import org.scalacheck.Prop.forAll

object MonoidTest {

trait Monoid[A] {
  def op(a1: A, a2: A): A
  def zero: A
}

object Monoid {
  val stringMonoid = new Monoid[String] {
    def op(a1: String, a2: String) = a1 + a2
    val zero = ""
  }

  def listMonoid[A] = new Monoid[List[A]] {
    def op(a1: List[A], a2: List[A]) = a1 ++ a2
    val zero = Nil
  }

  val intAddition: Monoid[Int] = new Monoid[Int] {
    def op(a: Int, b: Int) = a + b
    val zero = 0
  }

  val intMultiplication: Monoid[Int] = new Monoid[Int] {
    def op(a: Int, b: Int) = a * b
    val zero = 1
  }

  val booleanOr: Monoid[Boolean] = new Monoid[Boolean] {
    def op(a: Boolean, b: Boolean) = a || b
    val zero = false
  }

  val booleanAnd: Monoid[Boolean] = new Monoid[Boolean] {
    def op(a: Boolean, b: Boolean) = a && b
    val zero = true
  }

  def optionMonoid[A]: Monoid[Option[A]] = new Monoid[Option[A]] {
    def op(a: Option[A], b: Option[A]) = a orElse b
    val zero = None
  }

  def EndoMonoid[A]: Monoid[A => A] = new Monoid[A => A] {
    def op(a: A => A, b: A => A) = a compose b
    val zero = (a: A) => a
  }

  val wordsMonoid: Monoid[String] = new Monoid[String] {
    def op(a: String, b: String) = a.trim() + " " + b.trim()
    val zero = ""
  }

  def concatenate[A](as: List[A], m: Monoid[A]): A =
    as.foldLeft(m.zero)(m.op)

  val monoidLaws[A](m: Monoid[A]): Prop = forAll {
    (a1: A, a2: A) => m.op(a1, a2) == m.op(a2, a1)
  } && forAll {
    (a: A) => m.op(m.zero, a) == m.op(a, m.zero)
  }

  def foldMap[A,B](as: List[A], m: Monoid[B])(f: A => B): B =
    as.foldLeft(m.zero)((z, a) => m.op(z, f(a)))

//  def foldLeft[A,B](z: B)(f: (B, A) => B): B => {
//    foldMap(Nil, listMonoid)(
    
    



}


def main(args: Array[String]): Unit = {
  import Monoid._
  val words = List("   Hic", "est ", "chorda ")
  println(concatenate(words, wordsMonoid))
}}
