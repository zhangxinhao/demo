// 链地址法的哈希表实现，仅存int
public class HashMap {
    static class Node {
        int key, val;
        Node next;

        Node(int key, int val) {
            this.key = key;
            this.val = val;
        }
    }

    Node[] buckets;
    int size;
    static final double LOAD_FACTOR = 0.75;

    public HashMap() {
        this(16);
    }

    public HashMap(int capacity) {
        buckets = new Node[capacity];
        size = 0;
    }

    int index(int key) {
        return Math.floorMod(key, buckets.length);
    }

    public void put(int key, int val) {
        int i = index(key);
        Node node = buckets[i];
        while (node != null) {
            if (node.key == key) {
                node.val = val;
                return;
            }
            node = node.next;
        }
        Node newNode = new Node(key, val);
        newNode.next = buckets[i];
        buckets[i] = newNode;
        size++;
        if ((double) size / buckets.length > LOAD_FACTOR) {
            resize();
        }
    }

    void resize() {
        Node[] old = buckets;
        buckets = new Node[old.length * 2];
        size = 0;
        for (Node head : old) {
            Node node = head;
            while (node != null) {
                Node next = node.next;
                int i = index(node.key);
                node.next = buckets[i];
                buckets[i] = node;
                size++;
                node = next;
            }
        }
    }

    public int get(int key) {
        Node node = buckets[index(key)];
        while (node != null) {
            if (node.key == key) {
                return node.val;
            }
            node = node.next;
        }
        throw new IllegalArgumentException("key not found: " + key);
    }

    public int getOrDefault(int key, int defaultVal) {
        Node node = buckets[index(key)];
        while (node != null) {
            if (node.key == key) {
                return node.val;
            }
            node = node.next;
        }
        return defaultVal;
    }

    public boolean remove(int key) {
        int i = index(key);
        Node node = buckets[i];
        Node prev = null;
        while (node != null) {
            if (node.key == key) {
                if (prev == null) {
                    buckets[i] = node.next;
                } else {
                    prev.next = node.next;
                }
                size--;
                return true;
            }
            prev = node;
            node = node.next;
        }
        return false;
    }

    public boolean containsKey(int key) {
        Node node = buckets[index(key)];
        while (node != null) {
            if (node.key == key) {
                return true;
            }
            node = node.next;
        }
        return false;
    }

    public int size() {
        return size;
    }

    public boolean isEmpty() {
        return size == 0;
    }

    public void clear() {
        for (int i = 0; i < buckets.length; i++) {
            buckets[i] = null;
        }
        size = 0;
    }

    public void print() {
        for (Node head : buckets) {
            Node node = head;
            while (node != null) {
                System.out.print("(" + node.key + "=" + node.val + ") ");
                node = node.next;
            }
        }
        System.out.println();
    }
}
