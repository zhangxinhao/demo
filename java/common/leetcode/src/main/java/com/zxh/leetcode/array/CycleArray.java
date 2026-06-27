package com.zxh.leetcode.array;

/**
 * 环形数组（循环队列）
 */
public class CycleArray {

    private final int[] nums;
    private final int capacity;
    private int head;
    private int tail;

    public CycleArray(int capacity) {
        if (capacity <= 0) {
            throw new IllegalArgumentException("capacity must be positive");
        }
        this.capacity = capacity;
        this.nums = new int[capacity];
        this.head = 0;
        this.tail = 0;
    }

    /** 在队尾添加元素 */
    public void add(int val) {
        if (isFull()) {
            throw new IllegalStateException("CycleArray is full");
        }
        nums[tail] = val;
        tail = (tail + 1) % capacity;
    }

    /** 删除第一个匹配的元素 */
    public boolean delete(int val) {
        int count = size();
        for (int i = 0; i < count; i++) {
            int physicalIndex = (head + i) % capacity;
            if (nums[physicalIndex] == val) {
                for (int j = i; j < count - 1; j++) {
                    nums[(head + j) % capacity] = nums[(head + j + 1) % capacity];
                }
                tail = (tail - 1 + capacity) % capacity;
                return true;
            }
        }
        return false;
    }

    /** 按逻辑下标获取元素（0 为队首） */
    public int get(int index) {
        if (index < 0 || index >= size()) {
            throw new IndexOutOfBoundsException("index: " + index + ", size: " + size());
        }
        return nums[(head + index) % capacity];
    }

    /** 当前元素个数 */
    public int size() {
        return (tail - head + capacity) % capacity;
    }

    public boolean isEmpty() {
        return head == tail;
    }

    public boolean isFull() {
        return (tail + 1) % capacity == head;
    }

    public void clear() {
        head = 0;
        tail = 0;
    }

    /** 从队首到队尾打印元素 */
    public void print() {
        int current = head;
        while (current != tail) {
            System.out.print(nums[current] + " ");
            current = (current + 1) % capacity;
        }
        System.out.println();
    }

    public static void main(String[] args) {
        CycleArray array = new CycleArray(5);
        array.add(1);
        array.add(2);
        array.add(3);
        array.print(); // 1 2 3

        array.delete(2);
        array.print(); // 1 3

        System.out.println("size=" + array.size());
        System.out.println("get(1)=" + array.get(1));
    }
}
