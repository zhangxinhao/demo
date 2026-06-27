class ListNode {
    int val;
    ListNode next;
    ListNode(int val) { this.val = val; }
}

ListNode createListNode(int[] nums) {
    ListNode dummy = new ListNode(0);
    ListNode current = dummy;
    for (int num : nums) {
        current.next = new ListNode(num);
        current = current.next;
    }
    return dummy.next;
}