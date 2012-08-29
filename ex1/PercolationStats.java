public class PercolationStats {
    private double[] fractions;
    private int N;

    public PercolationStats(int N, int T) {
        this.N = N;

        fractions = new double[T];

        for (int i = 0; i < T; i++) {
            double frac = oneTime() / (N * N);
            fractions[i] = frac;
        }
    }

    public double mean() {
        return StdStats.mean(fractions);
    }

    public double stddev() {
        return StdStats.stddev(fractions);
    }

    private double oneTime() {
        Percolation perc = new Percolation(N);
        double sitesOpened = 0;

        while (!perc.percolates()) {
            int i = rand();
            int j = rand();

            if (!perc.isOpen(i, j)) {
                perc.open(i, j);
                sitesOpened++; 
            }
        }
        return sitesOpened;
    }

    private int rand() {
        return StdRandom.uniform(N) + 1;
    }

    public static void main(String[] args) {
        int N = Integer.parseInt(args[0]);
        int T = Integer.parseInt(args[1]);

        PercolationStats stat = new PercolationStats(N, T);
        double mean = stat.mean();
        double std = stat.stddev();
        double left = mean - 1.96 * std / Math.sqrt(T);
        double right = mean + 1.96 * std / Math.sqrt(T);

        StdOut.printf("%23s = %f\n", "mean", mean);
        StdOut.printf("%23s = %f\n", "stddev", std);
        StdOut.printf("%23s = %f, %f\n", "95% confidence interval", left, right);
    }
}
