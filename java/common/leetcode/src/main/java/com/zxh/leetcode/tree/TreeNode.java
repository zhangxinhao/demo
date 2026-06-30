// 二叉树节点定义
class TreeNode {
    int val;
    TreeNode left, right;

    TreeNode(int val) {
        this.val = val;
    }
}

// 层序构建二叉树，null 表示空节点
TreeNode createTreeNode(Integer[] nums) {
    if (nums == null || nums.length == 0 || nums[0] == null) {
        return null;
    }
    TreeNode root = new TreeNode(nums[0]);
    TreeNode[] queue = new TreeNode[nums.length];
    int head = 0, tail = 0;
    queue[tail++] = root;
    int i = 1;
    while (head < tail && i < nums.length) {
        TreeNode node = queue[head++];
        if (i < nums.length && nums[i] != null) {
            node.left = new TreeNode(nums[i]);
            queue[tail++] = node.left;
        }
        i++;
        if (i < nums.length && nums[i] != null) {
            node.right = new TreeNode(nums[i]);
            queue[tail++] = node.right;
        }
        i++;
    }
    return root;
}

// 前序遍历输出
void printTreeNode(TreeNode root) {
    if (root == null) {
        return;
    }
    System.out.print(root.val + " ");
    printTreeNode(root.left);
    printTreeNode(root.right);
}
