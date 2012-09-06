import java.util.Iterator;
import java.util.NoSuchElementException;

public class Deque<Item> implements Iterable<Item> {
    private int N;
    private Node head;
    private Node tail;

    private class Node {
        private Item item;
        private Node prev;
        private Node next;

        public Node(Item item, Node prev, Node next) {
            this.item = item;
            this.prev = prev;
            this.next = next;
        }
    }

    public Deque() {
        N = 0;
        head = new Node(null, null, null);
        tail = new Node(null, null, null);
        head.next = tail;
        tail.prev = head;
    }

    public boolean isEmpty() {
        return N == 0;
    }

    public int size() {
        return N;
    }

    public void addFirst(Item item) {
        if (item == null)
            throw new NullPointerException("Adding null item to Deque");
        Node that = new Node(item, head, head.next);
        head.next.prev = that;
        head.next = that;
        N++;
    }

    public void addLast(Item item) {
        if (item == null)
            throw new NullPointerException("Adding null item to Deque");
        Node that = new Node(item, tail.prev, tail);
        tail.prev.next = that;
        tail.prev = that;
        N++;
    }

    public Item removeFirst() {
        if (isEmpty())
            throw new NoSuchElementException("Deque empty");
        Node that = head.next;
        that.next.prev = head;
        head.next = that.next;
        that.prev = null;
        that.next = null;
        N--;
        return that.item;
    }

    public Item removeLast() {
        if (isEmpty())
            throw new NoSuchElementException("Deque empty");
        Node that = tail.prev;
        that.prev.next = tail;
        tail.prev = that.prev;
        that.prev = null;
        that.next = null;
        N--;
        return that.item;
    }

    public Iterator<Item> iterator() {
        return new ListIterator();
    }

    private class ListIterator implements Iterator<Item> {
        private Node current = head.next;

        public boolean hasNext() {
            return current != tail;
        }

        public void remove() {
            throw new UnsupportedOperationException();
        }

        public Item next() {
            if (!hasNext()) throw new NoSuchElementException();
            Item item = current.item;
            current = current.next;
            return item;
        }
    }

    public static void main(String[] args) {
        Deque<String> d = new Deque<String>();

        while (!StdIn.isEmpty()) {
            String item = StdIn.readString();

            if (item.equals("exit") || item.equals("quit"))
                break;

            if (item.startsWith("<"))
                d.removeFirst();
            else if (item.startsWith(">"))
                d.removeLast();
            else if (item.startsWith("+"))
                d.addLast(item.substring(1));
            else
                d.addFirst(item);

            StdOut.printf("%d [ ", d.size());
            for (String s : d)
                StdOut.printf("%s ", s);
            StdOut.println("]");
        }
    }
}
