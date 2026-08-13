package edu.ynjgy.entity;

import lombok.Data;

@Data
public class ItemInfo {
    private Integer itemId;
    private Integer eventId;
    private String itemNo;
    private String itemName;
    private String trackName;
    private String majorDesc;
    private String teamType;
    private String openCond;
    private String deptName;
    private String backStr1;
    private String backStr2;
    private String backStr3;
    private Integer backInt1;
    private Integer backInt2;
}