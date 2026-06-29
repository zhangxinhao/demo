import java.util.Stack;

// 循环队列 + 常用操作
public class CircularQueue {
    int[] nums;
    int size;
    int head;
    int tail;
    public CircularQueue(int size) {
        this.size = size;
        this.nums = new int[size];
        this.head = 0;
        this.tail = 0;
    }
    public void enqueue(int val) {
        nums[tail] = val;
        tail = (tail + 1) % size;
    }
    public int dequeue() {
        int val = nums[head];
        head = (head + 1) % size;
        return val;
    }
    public int peek() {
        return nums[head];
    }
}

// 使用两个栈实现队列 + 常用操作
public class Queue {
    Stack stack1;
    Stack stack2;
    public Queue(int size) {
        this.stack1 = new Stack(size);
        this.stack2 = new Stack(size);
    }
    public void enqueue(int val) {
        stack1.push(val);
    }
    public int dequeue() {
        if (stack2.isEmpty()) {
            while (!stack1.isEmpty()) {
                stack2.push(stack1.pop());
            }
        }
        return stack2.pop();
    }
    public int peek() {
        if (stack2.isEmpty()) {
            while (!stack1.isEmpty()) {
}