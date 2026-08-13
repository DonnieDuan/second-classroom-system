package edu.ynjgy.vo;
import lombok.Data;
import java.util.List;

@Data
public class ClassScoreVO {
    private String className;
    private List<StudentScoreVO> students;
    private List<StudentScoreVO> warningList;
}
