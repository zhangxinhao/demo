// 并查集（Union-Find / Disjoint Set Union）：用于处理不相交集合的合并与查询问题
// 常用于：判断图的连通性、检测环、Kruskal最小生成树、岛屿数量等问题
public class UnionFind {

    // parent[i] 表示节点 i 的父节点。
    // 初始时每个节点的父节点都是自己，即每个节点都是一个独立的集合（自成一个"根"）。
    private final int[] parent;

    // rank[i] 用于记录以 i 为根的树的"秩"（可以理解为树高度的一个上界估计值）。
    // 在按秩合并时，总是把"矮树"挂到"高树"下面，从而避免树退化成链表，保证操作效率。
    private final int[] rank;

    // size[i] 用于记录以 i 为根的集合中一共包含多少个节点。
    // 有些题目需要知道某个连通分量的大小，因此额外维护这个数组（可选，非并查集必需）。
    private final int[] size;

    // 记录当前总共有多少个不相交的集合（连通分量个数）。
    // 每成功合并一次（两个不同集合被合并成一个），该值就减 1。
    private int count;

    /**
     * 初始化并查集，一共有 n 个节点，编号从 0 到 n-1。
     * 初始状态下，每个节点各自独立成一个集合，共有 n 个集合。
     */
    public UnionFind(int n) {
        parent = new int[n];
        rank = new int[n];
        size = new int[n];
        count = n;
        for (int i = 0; i < n; i++) {
            // 初始时，每个节点的父节点指向自己，代表它是自己所在集合的根节点
            parent[i] = i;
            // 初始时每棵树只有一个节点，秩为 0
            rank[i] = 0;
            // 初始时每个集合只包含自身这一个节点
            size[i] = 1;
        }
    }

    /**
     * 查找节点 x 所在集合的根节点（代表元素），并在查找过程中进行"路径压缩"。
     *
     * 路径压缩的核心思想：
     * 在向上查找根节点的过程中，把沿途经过的所有节点直接挂到根节点下面，
     * 这样下次再查询这些节点时，只需要一步就能找到根节点，
     * 从而把并查集树"压扁"，大幅降低后续查询的时间复杂度。
     *
     * 这里使用递归方式实现路径压缩：
     * 1. 如果 x 就是根节点（parent[x] == x），直接返回 x；
     * 2. 否则先递归找到真正的根节点 root，
     *    再把 parent[x] 直接指向 root（路径压缩的关键一步），
     *    最后返回 root。
     */
    public int find(int x) {
        if (parent[x] != x) {
            // 递归查找根节点，并把递归路径上的所有节点都直接指向根节点
            parent[x] = find(parent[x]);
        }
        return parent[x];
    }

    /**
     * 判断两个节点 x 和 y 是否属于同一个集合（是否连通）。
     * 只需要比较它们各自的根节点是否相同即可。
     */
    public boolean isConnected(int x, int y) {
        return find(x) == find(y);
    }

    /**
     * 合并节点 x 和节点 y 所在的两个集合（按秩合并 Union by Rank）。
     *
     * 按秩合并的核心思想：
     * 在合并两棵树时，总是把"秩"（树高度的估计值）较小的树的根节点，
     * 挂到"秩"较大的树的根节点下面。
     * 这样可以避免树越合并越高，从而保证树的高度始终维持在 O(log n) 级别，
     * 配合路径压缩后，并查集的操作接近 O(1) 的均摊时间复杂度（严格来说是反阿克曼函数级别）。
     *
     * 返回值：如果 x 和 y 原本就在同一个集合中（合并前已连通），返回 false；
     *        否则完成合并操作，返回 true。
     */
    public boolean union(int x, int y) {
        // 先分别找到 x 和 y 所在集合的根节点
        int rootX = find(x);
        int rootY = find(y);

        // 如果根节点相同，说明 x 和 y 本来就在同一个集合里，无需合并
        if (rootX == rootY) {
            return false;
        }

        // 按秩合并：把秩较小的树挂到秩较大的树下面，保持树的整体平衡
        if (rank[rootX] < rank[rootY]) {
            parent[rootX] = rootY;
            size[rootY] += size[rootX];
        } else if (rank[rootX] > rank[rootY]) {
            parent[rootY] = rootX;
            size[rootX] += size[rootY];
        } else {
            // 两棵树秩相同时，任选一个作为新的根节点（这里选择 rootX），
            // 并将新根节点的秩加 1，因为合并后树的高度可能增加了一层
            parent[rootY] = rootX;
            size[rootX] += size[rootY];
            rank[rootX]++;
        }

        // 两个集合合并成了一个，集合总数减 1
        count--;
        return true;
    }

    /**
     * 返回节点 x 所在集合的元素个数（连通分量大小）。
     */
    public int getSize(int x) {
        return size[find(x)];
    }

    /**
     * 返回当前不相交集合（连通分量）的总数。
     */
    public int getCount() {
        return count;
    }

    // 简单测试与用法示例
    public static void main(String[] args) {
        // 构造一个包含 10 个节点（编号 0~9）的并查集
        UnionFind uf = new UnionFind(10);

        // 初始时，10 个节点互不连通，共有 10 个集合
        System.out.println("初始集合数量: " + uf.getCount()); // 10

        // 依次合并若干节点，模拟构建连通关系
        uf.union(0, 1);
        uf.union(1, 2);
        uf.union(3, 4);
        uf.union(5, 6);
        uf.union(6, 7);
        uf.union(7, 8);

        // 此时应该形成 4 个集合：{0,1,2} {3,4} {5,6,7,8} {9}
        System.out.println("合并后集合数量: " + uf.getCount()); // 4

        // 验证连通性
        System.out.println("0 和 2 是否连通: " + uf.isConnected(0, 2)); // true
        System.out.println("0 和 3 是否连通: " + uf.isConnected(0, 3)); // false
        System.out.println("5 和 8 所在集合大小: " + uf.getSize(5));   // 4
    }
}
