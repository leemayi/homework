import java.util.Iterator;
import java.util.NoSuchElementException;


public class RandomizedQueue<Item> implements Iterable<Item> {
    private Item[] a;
    private int N;

    public RandomizedQueue() {           // construct an empty randomized queue
        a = (Item[]) new Object[2];
    }

    public boolean isEmpty() {           // is the queue empty?
        return N == 0;
    }

    public int size() {                  // return the number of items on the queue
        return N;
    }

    public void enqueue(Item item) {     // add the item
        if (N == a.length)
            resize(2*a.length);
        a[N++] = item;
    }

    public Item dequeue() {              // delete and return a random item
        if (isEmpty())
            throw new RuntimeException("random queue is empty");

        int idx = pick(N);
        Item item = a[idx];
        a[idx] = a[N-1];
        a[N-1] = null;
        N--;

        if (N > 0 && N == a.length/4)
            resize(a.length/2);

        return item;
    }

    public Item sample() {               // return (but do not delete) a random item
        if (isEmpty())
            throw new RuntimeException("random queue is empty");
        return a[pick(N)];
    }

    public Iterator<Item> iterator() {   // return an independent iterator over items in random order
        return new RandomIterator();
    }

    private class RandomIterator implements Iterator<Item> {
        private int n = N;
        private Item[] clone;

        private RandomIterator() {
            clone = (Item[]) new Object[N];
            for (int i = 0; i < N; ++i)
                clone[i] = a[i];
        }

        public boolean hasNext() {
            return n > 0;
        }

        public void remove() {
            throw new UnsupportedOperationException();
        }
        
        public Item next() {
            if (!hasNext()) throw new NoSuchElementException();
            int idx = pick(n);
            Item item = clone[idx];
            clone[idx] = clone[n-1];
            clone[n-1] = null;
            n--;
            return item;
        }
    }

    private void resize(int capacity) {
        Item[] temp = (Item[]) new Object[capacity];
        for (int i = 0; i < N; i++)
            temp[i] = a[i];
        a = temp;
    }

    private int pick(int n) {
        return StdRandom.uniform(n);
    }

    public static void main(String[] args) {
        RandomizedQueue<String> q = new RandomizedQueue<String>();
        while (!StdIn.isEmpty()) {
            String item = StdIn.readString();

            if (item.startsWith("exit"))
                break;

            if (item.startsWith("-")) {
                String out = q.dequeue();
                StdOut.printf("pop: %s\n", out);
            }
            else if (item.startsWith("+"))
                q.enqueue(item.substring(1));

            StdOut.printf("%d [ ", q.size());
            for (String s : q)
                StdOut.printf("%s ", s);
            StdOut.println("]");
        }

        for (String i : q)
            for (String j : q)
                StdOut.printf("(%s, %s) ", i, j);
        StdOut.println();
    }
}
