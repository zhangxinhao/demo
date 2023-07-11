package com.zxh.hello;

import java.util.Map;

public class Hello {
    public static void main(String[] args) {
        // <Param>:<DataType>:<Type>:<range/enums>:<Resolution>
        String str = "unit_mode_SSM : enum : function_call : 'None'-0, 'Self-Test'-1 : N/A";
        // 解析Parameter字符串
        Parameter parameter = new Parameter().parseStr(str);

        // 打印<Param>
        System.out.println("===Param===");
        System.out.println(parameter.param);

        // 打印解析出来的<range/enums>
        System.out.println("===range/enums===");
        Enums enums = null;
        if (parameter.dataType == DataType.ENUM) {
            enums = parameter.enums;
        }
        assert enums != null;
        for (Map.Entry<Integer, String> entry : enums.data.entrySet()) {
            System.out.println(entry.toString());
        }
        // 获取enums中int对应的string
        int one = 1;
        String oneValue = enums.data.get(one);
        System.out.println("1:" + oneValue);
        int three = 3;
        String threeValue = enums.data.get(three);
        System.out.println("3:" + threeValue);

        // 打印<Resolution>
        System.out.println("===Resolution===");
        System.out.println(parameter.resolution);
    }
}
