package com.zxh.leetcode;

public class Demo {
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

    private TrieNode root;

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

    private TrieNode find(String word) {
        TrieNode node = root;
        for (int i = 0; i < word.length(); i++) {
            char c = word.charAt(i);
            if (!node.has(c)) {
                return null;
            }
            node = node.get(c);
        }
        return node;
    }

    public boolean search(String word) {
        TrieNode node = find(word);
        return node != null && node.isEnd;
    }

    public boolean startsWith(String prefix) {
        TrieNode node = find(prefix);
        return node != null;
    }
}
