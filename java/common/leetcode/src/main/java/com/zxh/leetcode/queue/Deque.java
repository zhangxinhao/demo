// 实现双端队列 + 常用操作
public class Deque {
    int[] nums;
    int size;
    int head;
    int tail;
    public Deque(int size) {
        this.size = size;
        this.nums = new int[size];
        this.head = 0;
        this.tail = 0;
    }
    public void addFirst(int val) {
        nums[head] = val;
        head = (head - 1) % size;
    }
    public void addLast(int val) {
        nums[tail] = val;
        tail = (tail + 1) % size;
    }
    public int removeFirst() {
        int val = nums[head];
        head = (head + 1) % size;
        return val;
    }
    public int removeLast() {
        int val = nums[tail];
        tail = (tail - 1) % size;
        return val;
    }
    public int getFirst() {
        return nums[head];
    }
    public int get(int index) {
        return nums[(head + index) % size];
    }
    public boolean isEmpty() {
        return head == tail;
    }
    public boolean isFull() {
        return (tail + 1) % size == head;
    }
    public void clear() {
        head = 0;
        tail = 0;
    }
}