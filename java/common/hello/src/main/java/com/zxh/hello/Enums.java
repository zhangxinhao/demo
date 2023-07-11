package com.zxh.hello;

import java.util.TreeMap;

public class Enums {
    TreeMap<Integer, String> data = new TreeMap<>();

    public Enums parseStr(String str) {
        String[] enumEle = str.split(",");
        for (int i = 0; i < enumEle.length; i++) {
            int splitIdx = enumEle[i].lastIndexOf('-');
            String enumName = enumEle[i].substring(0, splitIdx).replaceAll("'", "").trim();
            String enumValue = enumEle[i].substring(splitIdx + 1).trim();
            data.put(Integer.parseInt(enumValue), enumName);
        }
        return this;
    }
}
