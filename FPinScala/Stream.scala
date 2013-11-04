object test {

import Stream._

trait Stream[+A] {
  def uncons: Option[(A, Stream[A])]
  def isEmpty: Boolean = uncons.isEmpty
  def toList: List[A] = uncons match {
    case Some((h, t)) => h :: t.toList
    case _ => Nil
  }
  def toListFast: List[A] = {
    val buf = new collection.mutable.ListBuffer[A]
    def go(s: Stream[A]): List[A] = s.uncons match {
      case Some((h, t)) =>
        buf += h
        go(t)
      case _ => buf.toList
    }
    go(this)
  }
  def take(n: Int): Stream[A] =
    if (n > 0) uncons match {
      case Some((h, t)) if n == 1 => cons(h, Stream())
      case Some((h, t)) => cons(h, t.take(n-1))
      case _ => empty
    }
    else Stream()
  def takeWhile(p: A => Boolean): Stream[A] = uncons match {
    case Some((h, t)) if p(h) => cons(h, t takeWhile p)
    case _ => Stream()
  }
  def foldRight[B](z: => B)(f: (A, => B) => B): B =
    uncons match {
      case Some((h, t)) => f(h, t.foldRight(z)(f))
      case None => z
    }
  def exists(p: A => Boolean): Boolean =
    foldRight(false)((a, b) => p(a) || b)
  def forAll(p: A => Boolean): Boolean =
    foldRight(true)((a, b) => p(a) && b)
  def takeWhile2(p: A => Boolean): Stream[A] =
    foldRight(empty[A])((a, b) =>
      if (p(a)) cons(a, b)
      else b)
  def map[B](p: A => B): Stream[B] =
    foldRight(empty[B])((h, t) => cons(p(h), t))
  def filter(p: A => Boolean): Stream[A] =
    foldRight(empty[A])((h, t) =>
      if (p(h)) cons(h, t.filter(p))
      else t)
  def append[B>:A](s: Stream[B]): Stream[B] =
    foldRight(s)((h, t) => cons(h, t))
  def flatMap[B](p: A => Stream[B]): Stream[B] =
    foldRight(empty[B])((h, t) => p(h) append t)

  def mapViaUnfold[B](p: A => B): Stream[B] =
    unfold(this)(_.uncons match {
      case None => None
      case Some((h, t)) => Some(p(h), t)
    })
  def takeViaUnfold[B](n: Int): Stream[A] =
    unfold((this, n))((p) => (p._1.uncons, p._2) match {
      case (None, _) => None
      case (_, 0) => None
      case (Some((h, t)), n) => Some(h, (t, n-1))
    })
  def takeWhileViaUnfold(p: A => Boolean): Stream[A] =
    unfold(this)(_.uncons match {
      case Some((h, t)) if p(h) => Some(h, t)
      case _ => None
    })
  def zip[B](s2: Stream[B]): Stream[(A, B)] = 
    unfold((this, s2)) { case (s1, s2) =>
      (s1.uncons, s2.uncons) match {
        case (Some((h1, t1)), Some((h2, t2))) => Some((h1, h2), (t1, t2))
        case _ => None
        }
    }
  def zipAll[B](s2: Stream[B]): Stream[(Option[A], Option[B])] =
    unfold((this, s2)) { case (s1, s2) =>
      (s1.uncons, s2.uncons) match {
        case (Some((h1, t1)), Some((h2, t2))) => Some((Some(h1), Some(h2)), (t1, t2))
        case (Some((h1, t1)), None)           => Some((Some(h1), None),     (t1, empty[B]))
        case (None, Some((h2, t2)))           => Some((None, Some(h2)),     (empty[A], t2))
        case (None, None)                     => None
        }
      }

def zipAll2[B](s2: Stream[B]): Stream[(Option[A],Option[B])] = 
    zipWithAll(s2)((_,_))
def zipWithAll[B,C](s2: Stream[B])(f: (Option[A],Option[B]) => C): Stream[C] = {
    val a = this map (Some(_)) append (constant(None)) 
    val b = s2 map (Some(_)) append (constant(None)) 
    unfold((a, b)) {
      case (s1,s2) => for {
        c1 <- s1.uncons
        c2 <- s2.uncons
      } yield (f(c1._1, c2._1), (c1._2, c2._2))
    }
  }

def tails: Stream[Stream[A]] =
  unfold(this)(s => s.uncons match {
    case None => None
    case Some((h, t)) => Some((s, t))
    }) append (Stream(empty))

def scanRight[B](z: => B)(f: (A, => B) => B): Stream[B] =
  foldRight((z, Stream(z)))((a, s) => {
    val b = f(a, s._1)
    (b, cons(b, s._2))
    })._2

}

object Stream {

def empty[A]: Stream[A] =
  new Stream[A] { def uncons = None }

def cons[A](hd: => A, tl: => Stream[A]): Stream[A] =
  new Stream[A] {
    lazy val uncons = Some((hd, tl))
  }

def apply[A](as: A*): Stream[A] =
  if (as.isEmpty) empty
  else cons(as.head, apply(as.tail: _*))

def constant[A](a: A): Stream[A] = cons(a, constant(a))

def from(n: Int): Stream[Int] = cons(n, from(n+1))

val fibs: Stream[Int] = {
  def start(n1: Int, n2: Int): Stream[Int] =
    cons(n1, start(n2, n1+n2))
  start(0, 1)
  }

def unfold[A, S](z: S)(f: S => Option[(A, S)]): Stream[A] =
  f(z) match {
    case None => empty[A]
    case Some((h, t)) => cons(h, unfold(t)(f))
    }

val odd: Stream[Int] = unfold(1)((n) => Some(n, n+2))
val fibs2: Stream[Int] = unfold((0, 1))((s) => Some(s._1, (s._2, s._1 + s._2)))
def constant2[A](a: A): Stream[A] = unfold(a)(_ => Some(a, a))

def startsWith[A](s: Stream[A], s2: Stream[A]): Boolean =
  s.zipAll(s2).forAll {
    case (h1, h2) =>
      h1 == h2 || h2 == None
    }

}

def main(args: Array[String]): Unit = {
  val s = Stream(1 to 5: _*)
  println(s toList)
  println(s.scanRight(0)(_ + _) toList)
}
}
