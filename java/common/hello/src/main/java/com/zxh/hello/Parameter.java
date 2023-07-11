package com.zxh.hello;

// <Param>:<DataType>:<Type>:<range/enums>:<Resolution>
public class Parameter {
    // <Param>
    String param;
    // <DataType>
    DataType dataType;
    // <Type>
    String type;
    // <range>
    Range range;
    // <enums>
    Enums enums;
    // <Resolution>
    String resolution;

    public Parameter parseStr(String str) {
        String[] strList = str.split(":");

        // 解析<Param>
        this.param = strList[0].trim();

        // 解析<Type>
        this.type = strList[2].trim();

        // 解析<DataType>和<range/enums>
        String dataTypeStr = strList[1].trim();
        if (dataTypeStr.equals("enum")) {
            String enumsStr = strList[3].trim();
            this.dataType = DataType.ENUM;
            this.enums = new Enums().parseStr(enumsStr);
        } else if (dataTypeStr.equals("int")) {
            String intStr = strList[3];
            this.dataType = DataType.INT;
            this.range = new Range().parseStr(intStr);
        }

        // 解析<Resolution>
        this.resolution = strList[4].trim();
        return this;
    }
}
