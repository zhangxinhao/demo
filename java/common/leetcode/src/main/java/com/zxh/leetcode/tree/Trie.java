// 字典树（前缀树）：高效存储与检索字符串前缀
public class Trie {
    static class TrieNode {
        TrieNode[] children = new TrieNode[26];
        boolean isEnd;

        boolean has(char c) {
            return children[c - 'a'] != null;
        }

        TrieNode get(char c) {
            return children[c - 'a'];
        }

        void put(char c, TrieNode node) {
            children[c - 'a'] = node;
        }
    }

    private final TrieNode root = new TrieNode();

    // 插入单词
    public void insert(String word) {
        TrieNode node = root;
        for (int i = 0; i < word.length(); i++) {
            char c = word.charAt(i);
            if (!node.has(c)) {
                node.put(c, new TrieNode());
            }
            node = node.get(c);
        }
        node.isEnd = true;
    }

    // 精确查找单词
    public boolean search(String word) {
        TrieNode node = find(word);
        return node != null && node.isEnd;
    }

    // 通配查找，'.' 匹配任意单个字符
    public boolean searchWildcard(String word) {
        return searchWildcard(root, word, 0);
    }

    private boolean searchWildcard(TrieNode node, String word, int i) {
        if (i == word.length()) {
            return node.isEnd;
        }
        char c = word.charAt(i);
        if (c == '.') {
            for (TrieNode child : node.children) {
                if (child != null && searchWildcard(child, word, i + 1)) {
                    return true;
                }
            }
            return false;
        }
        if (!node.has(c)) {
            return false;
        }
        return searchWildcard(node.get(c), word, i + 1);
    }

    // 是否存在以 prefix 为前缀的单词
    public boolean startsWith(String prefix) {
        return find(prefix) != null;
    }

    private TrieNode find(String s) {
        TrieNode node = root;
        for (int i = 0; i < s.length(); i++) {
            char c = s.charAt(i);
            if (!node.has(c)) {
                return null;
            }
            node = node.get(c);
        }
        return node;
    }
}
