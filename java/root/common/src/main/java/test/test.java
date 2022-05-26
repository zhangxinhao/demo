package test;

import java.util.HashMap;
import java.util.Map;

public class test {
    public static void main(String[] args) {
        Map<String, String> myMap = new HashMap<>();
        String aa = myMap.get("aa");
        System.out.println("hello: " + aa);
    }
}