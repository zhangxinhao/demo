class DoublyListNode {
    int val;
    DoublyListNode next, prev;
    DoublyListNode(int val) { this.val = val; }
}

DoublyListNode createDoublyListNode(int[] nums) {
    DoublyListNode dummy = new DoublyListNode(0);
    DoublyListNode current = dummy;
    for (int num : nums) {
        current.next = new DoublyListNode(num);
        current.next.prev = current;
        current = current.next;
    }
    return dummy.next;
}

// 遍历输出双向链表
void printDoublyListNode(DoublyListNode head) {
    DoublyListNode current = head;
    while (current != null) {
        System.out.print(current.val + " ");
        current = current.next;
    }
    System.out.println();
}

// 删除节点
void deleteDoublyListNode(DoublyListNode head, int val) {
    DoublyListNode current = head;
    while (current != null) {
        if (current.val == val) {
            current.prev.next = current.next;
            current.next.prev = current.prev;
            break;
        }
        current = current.next;
    }
}