// 栈 + 常用操作
public class Stack {
    int[] nums;
    int size;
    int top;
    public Stack(int size) {
        this.size = size;
        this.nums = new int[size];
        this.top = -1;
    }
    public void push(int val) {
        nums[++top] = val;
    }
    public void pop() {
        top--;
    }
    public int top() {
        return nums[top];
    }
    public boolean isEmpty() {
        return top == -1;
    }
    public boolean isFull() {
        return top == size - 1;
    }
    public void clear() {
        top = -1;
    }
    public void print() {
        for (int i = 0; i <= top; i++) {
            System.out.print(nums[i] + " ");
        }
    }
}