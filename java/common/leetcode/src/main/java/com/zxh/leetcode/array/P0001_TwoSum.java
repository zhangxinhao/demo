package com.zxh.leetcode.array;

import java.util.HashMap;
import java.util.Map;

/**
 * LeetCode 1. Two Sum
 * Difficulty: Easy | Tags: array, hash-table
 * https://leetcode.cn/problems/two-sum/
 */
public class P0001_TwoSum {

    public int[] twoSum(int[] nums, int target) {
        Map<Integer, Integer> indexByValue = new HashMap<>();
        for (int i = 0; i < nums.length; i++) {
            int complement = target - nums[i];
            Integer j = indexByValue.get(complement);
            if (j != null) {
                return new int[]{j, i};
            }
            indexByValue.put(nums[i], i);
        }
        throw new IllegalArgumentException("No two sum solution");
    }

    public static void main(String[] args) {
        P0001_TwoSum solution = new P0001_TwoSum();
        int[] result = solution.twoSum(new int[]{2, 7, 11, 15}, 9);
        System.out.println("[" + result[0] + ", " + result[1] + "]");
    }
}
