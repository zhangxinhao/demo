// 数组实现的小顶堆 + 常用操作
// 堆是一棵完全二叉树：父节点 <= 子节点，最小值在堆顶 nums[0]
public class MinHeap {
    int[] nums;
    int size;
    int capacity;

    public MinHeap() {
        this(16);
    }

    public MinHeap(int capacity) {
        this.capacity = capacity;
        this.nums = new int[capacity];
        this.size = 0;
    }

    // 插入元素，末尾追加后上浮
    public void offer(int val) {
        if (size == capacity) {
            resize();
        }
        nums[size] = val;
        siftUp(size);
        size++;
    }

    // 弹出堆顶（最小值），末尾补到堆顶后下沉
    public int poll() {
        int min = nums[0];
        size--;
        nums[0] = nums[size];
        siftDown(0);
        return min;
    }

    // 查看堆顶，不删除
    public int peek() {
        return nums[0];
    }

    public int size() {
        return size;
    }

    public boolean isEmpty() {
        return size == 0;
    }

    // 上浮：当前节点比父节点小则交换，直到根或满足堆性质
    void siftUp(int i) {
        while (i > 0) {
            int parent = (i - 1) / 2;
            if (nums[i] >= nums[parent]) {
                break;
            }
            swap(i, parent);
            i = parent;
        }
    }

    // 下沉：与较小的子节点交换，直到叶子或满足堆性质
    void siftDown(int i) {
        while (true) {
            int left = 2 * i + 1;
            int right = 2 * i + 2;
            int smallest = i;

            if (left < size && nums[left] < nums[smallest]) {
                smallest = left;
            }
            if (right < size && nums[right] < nums[smallest]) {
                smallest = right;
            }
            if (smallest == i) {
                break;
            }
            swap(i, smallest);
            i = smallest;
        }
    }

    void swap(int i, int j) {
        int tmp = nums[i];
        nums[i] = nums[j];
        nums[j] = tmp;
    }

    void resize() {
        capacity *= 2;
        int[] newNums = new int[capacity];
        System.arraycopy(nums, 0, newNums, 0, size);
        nums = newNums;
    }

    public void print() {
        for (int i = 0; i < size; i++) {
            System.out.print(nums[i] + " ");
        }
    }
}
