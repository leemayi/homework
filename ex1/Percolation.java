public class Percolation {
    private int n;
    private int top = 0;
    private int bottom = 1;
    private WeightedQuickUnionUF uf;
    private boolean[] openState;

    public Percolation(int N) {
        n = N;
        openState = new boolean[n*n];
        uf = new WeightedQuickUnionUF(n*n+2);

        for (int j = 1; j <= n; j++) {
            union(top, 1, j);
            union(bottom, n, j);
        }
    }

    public void open(int i, int j) {
        validate(i, j);

        if (isOpen(i, j))
            return;

        openState[xyTo1D(i, j)] = true;

        if (i > 1 && isOpen(i-1, j)) // top
            union(i, j, i-1, j);
        else if (i < n && isOpen(i+1, j)) // bottom
            union(i, j, i+1, j);
        else if (j > 1 && isOpen(i, j-1)) // left
            union(i, j, i, j-1);
        else if (j < n && isOpen(i, j+1)) // right
            union(i, j, i, j+1);
    }

    public boolean isOpen(int i, int j) {
        validate(i, j);
        return openState[xyTo1D(i, j)];
    }

    public boolean isFull(int i, int j) {
        return isOpen(i, j) && uf.connected(top, xyTo1D(i, j)+2);
    }

    public boolean percolates() {
        return uf.connected(top, bottom);
    }

    private int xyTo1D(int i, int j) {
        validate(i, j);
        return (i-1) * n + (j-1);
    }

    private void validate(int i, int j) {
        if (i < 1 || i > n || j < 1 || j > n)
            throw new IndexOutOfBoundsException("row index i out of bounds");
    }

    private void union(int i1, int j1, int i2, int j2) {
        uf.union(xyTo1D(i1, j1)+2, xyTo1D(i2, j2)+2);
    }
    private void union(int p, int i, int j) {
        uf.union(p, xyTo1D(i, j)+2);
    }
}
