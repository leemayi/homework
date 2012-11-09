/*************************************************************************
 * Name:
 * Email:
 *
 * Compilation:  javac Point.java
 * Execution:
 * Dependencies: StdDraw.java
 *
 * Description: An immutable data type for points in the plane.
 *
 *************************************************************************/

import java.util.Comparator;
import java.util.Arrays;

public class Point implements Comparable<Point> {

    // compare points by slope
    public final Comparator<Point> SLOPE_ORDER;       // YOUR DEFINITION HERE

    private final int x;                              // x coordinate
    private final int y;                              // y coordinate

    // create the point (x, y)
    public Point(int x, int y) {
        /* DO NOT MODIFY */
        this.x = x;
        this.y = y;
        SLOPE_ORDER = new SlopeOrder(this);
    }

    // plot this point to standard drawing
    public void draw() {
        /* DO NOT MODIFY */
        StdDraw.point(x, y);
    }

    // draw line between this point and that point to standard drawing
    public void drawTo(Point that) {
        /* DO NOT MODIFY */
        StdDraw.line(this.x, this.y, that.x, that.y);
    }

    // slope between this point and that point
    public double slopeTo(Point that) {
        int dy = that.y - y;
        if (dy == 0) return 0;

        int dx = that.x - x;
        if (dx == 0) {
            if (dy > 0)
                return Double.POSITIVE_INFINITY;
            return Double.NEGATIVE_INFINITY;
        }
        return (double) dy / dx;
    }

    // is this point lexicographically smaller than that one?
    // comparing y-coordinates and breaking ties by x-coordinates
    public int compareTo(Point that) {
        if (y == that.y && x == that.x)
            return 0;
        if (y < that.y || y == that.y && x < that.x)
            return -1;
        return 1;
    }

    // return string representation of this point
    public String toString() {
        /* DO NOT MODIFY */
        return "(" + x + ", " + y + ")";
    }

    private class SlopeOrder implements Comparator<Point> {
        private Point base;

        private SlopeOrder(Point base) {
            this.base = base;
        }

        public int compare(Point v, Point w) {
            double s1 = base.slopeTo(v);
            double s2 = base.slopeTo(w);
            if (s1 < s2)
                return -1;
            if (s1 > s2)
                return 1;
            return v.compareTo(w);
        }
    }

    // unit test
    public static void main(String[] args) {
        int N = 9;
        Point p = new Point(10000, 0);

        Point[] other = new Point[N-1];
        other[0] = new Point(0, 10000);
        other[1] = new Point(3000, 7000);
        other[2] = new Point(7000, 3000);
        other[3] = new Point(20000, 21000);
        other[4] = new Point(3000, 4000);
        other[5] = new Point(14000, 15000);
        other[6] = new Point(6000, 7000);
        other[7] = new Point(5000, 5000);
        Arrays.sort(other, 0, N-1, p.SLOPE_ORDER);
    }
}
