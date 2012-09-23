import java.util.Arrays;

public class Fast {
    private Point[] points;

    public Fast(Point[] points) {
        this.points = points;
    }

    public void solve(boolean draw) {
        int N = points.length;

        Point[] other = new Point[N];

        for (int i = 0; i < N; ++i) {
            Point p = points[i];

            for (int j = 0; j < N; ++j)
                other[j] = points[j];
            other[i] = points[N-1];
            Arrays.sort(other, 0, N-1, p.SLOPE_ORDER);

            int start = -1;
            int end = -1;
            double prev = 0;

            for (int j = 0; j < N-1; ++j) {
                Point q = other[j];
                double slope = p.slopeTo(q);

                if (start == -1)
                    start = j;
                else if (slope == prev)
                    end = j;
                else {
                    if (end - start >= 2 && p.compareTo(other[start]) <= 0) {
                        if (draw)
                            p.drawTo(other[end]);
                        else {
                            StdOut.printf("%s", p);
                            for (int k = start; k <= end; ++k)
                                StdOut.printf(" -> %s", other[k]);
                            StdOut.printf("\n");
                        }
                    }
                    start = j;
                }

                prev = slope;
            }

            if (end == N-1 && end-start >= 2 && p.compareTo(other[start]) <= 0) {
                if (draw)
                    p.drawTo(other[end]);
                else {
                    StdOut.printf("%s", p);
                    for (int k = start; k <= end; ++k)
                        StdOut.printf(" -> %s", other[k]);
                    StdOut.printf("\n");
                }
            }
        }
    }

    public static void main(String[] args) {
        String filename = args[0];
        In in = new In(filename);
        int N = in.readInt();

        Point[] points = new Point[N];
        for (int i = 0; i < N; i++) {
            int x = in.readInt();
            int y = in.readInt();
            points[i] = new Point(x, y);
        }

        Fast fast = new Fast(points);
        fast.solve(false);
    }
}
