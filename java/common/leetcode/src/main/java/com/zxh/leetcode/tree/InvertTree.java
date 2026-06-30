// 翻转二叉树：交换每个节点的左右孩子
TreeNode invertTree(TreeNode root) {
    if (root == null) {
        return null;
    }
    TreeNode tmp = root.left;
    root.left = root.right;
    root.right = tmp;
    invertTree(root.left);
    invertTree(root.right);
    return root;
}
