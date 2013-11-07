object StateTest {

trait RNG {
  def nextInt: (Int, RNG)
}

object RNG {
  def simple(seed: Long): RNG = new RNG {
    def nextInt = {
      val seed2 = (seed*0x5DEECE66DL + 0xBL) & ((1L << 48) - 1)
      ((seed2 >>> 16).asInstanceOf[Int], simple(seed2))
    }
  }

type Rand[+A] = RNG => (A, RNG)

val int: Rand[Int] = _.nextInt

def unit[A](a: A): Rand[A] =
  rng => (a, rng)

def map[A,B](s: Rand[A])(f: A => B): Rand[B] =
  rng => {
    val (a, rng2) = s(rng)
    (f(a), rng2)
    }
def _map[A,B](s: Rand[A])(f: A => B): Rand[B] =
  flatMap(s){ a => unit(f(a)) }

def map2[A,B,C](ra: Rand[A], rb: Rand[B])(f: (A, B) => C): Rand[C] =
  rng => {
    val (a, r1) = ra(rng)
    val (b, r2) = rb(r1)
    (f(a, b), r2)
    }
def _map2[A,B,C](ra: Rand[A], rb: Rand[B])(f: (A, B) => C): Rand[C] =
  flatMap(ra) { a =>
    map(rb)(b => f(a, b))
  }

def sequence[A](fs: List[Rand[A]]): Rand[List[A]] =
  rng =>
    fs.foldLeft((List[A](), rng))((b, rand) => {
      val (t, r) = b
      val (v, r2) = rand(r)
      (v :: t, r2)
      })
def flatMap[A,B](f: Rand[A])(g: A => Rand[B]): Rand[B] =
  rng => {
    val (a, r1) = f(rng)
    g(a)(r1)
  }

def positiveInt(rng: RNG): (Int, RNG) = {
  val (i, rng2) = rng.nextInt
  ((i + 1).abs, rng2)
  }
val positiveInt2: Rand[Int] =
  flatMap(int) { i =>
    if (i == Int.MinValue) int
    else if (i < 0) unit(-i)
    else unit(i)
  }
def double(rng: RNG): (Double, RNG) = {
  val (i, r) = positiveInt(rng)
  (i / (Int.MaxValue.toDouble + 1), r)
  }
val double2: Rand[Double] =
  map(positiveInt)(_ / (Int.MaxValue.toDouble + 1))

def intDouble(rng: RNG): ((Int,Double), RNG) = {
  val (i, r) = rng.nextInt
  val (d, r2) = double(r)
  ((i, d), r2)
  }
val intDouble2: Rand[(Int, Double)] =
  map2(int, double)((_, _))

def doubleInt(rng: RNG): ((Double,Int), RNG) = {
  val ((i, d), r) = intDouble(rng)
  ((d, i), r)
  }
val doubleInt2: Rand[(Double, Int)] =
  map2(double2, int)((_, _))

def double3(rng: RNG): ((Double,Double,Double), RNG) = {
  val (d1, r1) = double(rng)
  val (d2, r2) = double(r1)
  val (d3, r3) = double(r2)
  ((d1, d2, d3), r3)
  }
val double32: Rand[List[Double]] =
  sequence(List[Rand[Double]](double, double, double))

def ints(count: Int)(rng: RNG): (List[Int], RNG) =
  (1 to count).foldLeft((List[Int](), rng))((b, a) => {
    val (t, r) = b
    val (i, r2) = r.nextInt
    ((i :: t), r2)
    })
def positiveMax(n: Int): Rand[Int] =
  map(double)(x => (x * n).toInt)

}

case class State[S,+A](run: S => (A,S)) {

  def map[B](f: A => B): State[S,B] =
    flatMap(a => State.unit(f(a)))

  def map2[B,C](sb: State[S,B])(f: (A, B) => C): State[S,C] =
    flatMap(a => sb.map(b => f(a, b)))

  def flatMap[B](f: A => State[S,B]): State[S,B] =
    State(s => {
      val (a, s1) = run(s)
      f(a).run(s1)
      })
}

object State {
  type Rand[A] = State[RNG, A]

  def sequence[S,A](fs: List[State[S,A]]): State[S,List[A]] =
    State(startState =>
      fs.foldLeft((List[A](), startState))(
        (tmp, action) => {
          val (tail, state) = tmp
          val (value, nextState) = action.run(state)
          (value :: tail, nextState)
        }))

  def unit[S,A](a: A): State[S,A] =
    State(s => (a, s))
 
  val int: Rand[Int] = State(_.nextInt)

  val positiveInt: Rand[Int] =
    int.flatMap({ i =>
    if (i == Int.MinValue) int
    else if (i < 0) unit(-i)
    else unit(i)
    })

  val double: Rand[Double] =
    positiveInt.map(_ / (Int.MaxValue.toDouble + 1))
}


def unfold[A, S](z: S)(f: S => Option[(A, S)]): Stream[A] =
  f(z) match {
    case Some((h,s)) => Stream.cons(h, unfold(s)(f))
    case None => Stream[A]()
  }
def randomTest[A](rng: RNG)(f: RNG => (A, RNG)) =
  unfold(rng)(s => Some(f(s)))
def randomTest2[A](rng: RNG)(action: State.Rand[A]) =
  unfold(rng)(s => Some(action.run(s)))


def main(args: Array[String]): Unit = {
  import java.util.Date
  val rng = RNG.simple(new Date().getTime())
  //randomTest(rng)(intDouble) take 5 print
  //ints(10)(rng)._1 foreach println
  randomTest(rng)(RNG.int) take 20 print
  //randomTest2(rng)(State.int) take 20 print
}

}
