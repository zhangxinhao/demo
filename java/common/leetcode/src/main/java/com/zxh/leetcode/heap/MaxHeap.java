package com.zxh.leetcode.heap;

public class MaxHeap {
    int[] nums;
    int size;
    int capacity;

    public MaxHeap(int capacity) {
        this.capacity = capacity;
        this.nums = new int[capacity];
        this.size = 0;
    }

    public MaxHeap() {
        this(16);
    }

    // 插入元素
    public void offer(int val) {
        if (size == capacity) {
            resize();
        }
        nums[size] = val;
        siftUp(size);
        size++;

    }

    // 弹出堆顶（最大值）
    public int poll() {
        int max = nums[0];
        size--;
        nums[0] = nums[size];
        siftDown(0);
        return max;
    }

    public int peek() {
        return nums[0];
    }

    public int size() {
        return size;
    }

    public boolean isEmpty() {
        return size == 0;
    }

    // 上浮：当前节点比父节点大则交换，直到根或满足堆性质
    private void siftUp(int i) {
        while (i > 0) {
            int parent = (i - 1) / 2;
            if (nums[i] <= nums[parent]) {
                break;
            }
            swap(i, parent);
            i = parent;
        }
    }

    // 下沉：与较大的子节点交换，直到叶子或满足堆性质
    private void siftDown(int i) {
        while (true) {
            int left = 2 * i + 1;
            int right = 2 * i + 2;
            int largest = i;

            if (left < size && nums[left] > nums[largest]) {
                largest = left;
            }
            if (right < size && nums[right] > nums[largest]) {
                largest = right;
            }
            if (largest == i) {
                break;
            }
            swap(i, largest);
            i = largest;
        }
    }

    private void swap(int i, int j) {
        int temp = nums[i];
        nums[i] = nums[j];
        nums[j] = temp;
    }

    private void resize() {
        capacity *= 2;
        int[] newNums = new int[capacity];
        System.arraycopy(nums, 0, newNums, 0, size);
        nums = newNums;
    }
}
