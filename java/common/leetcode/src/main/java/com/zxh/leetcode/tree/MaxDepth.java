// 最大深度：自底向上
// 先递归得到左右子树深度，再在当前层 +1
int maxDepth(TreeNode root) {
    if (root == null) {
        return 0;
    }
    int leftDepth = maxDepth(root.left);
    int rightDepth = maxDepth(root.right);
    return Math.max(leftDepth, rightDepth) + 1;
}
