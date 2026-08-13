package edu.ynjgy.Service;

import java.util.List;
import java.util.Map;

import edu.ynjgy.utils.PageResult;
import edu.ynjgy.utils.Result;
import edu.ynjgy.vo.StudentInfoVO;

public interface StudentService {
    Result<StudentInfoVO> getStudentInfo(Integer stuId);
    Result<List<StudentInfoVO>> getStudentsByClass(Integer classOrgId);
    Result<PageResult<StudentInfoVO>> searchStudents(String keyword, String gender, Integer classOrgId,
                                                     String enrollYear, String trainLevel,
                                                     Integer pageNum, Integer pageSize);
    Result<?> addStudent(StudentInfoVO studentVO);
    Result<?> updateStudentInfo(Integer stuId, StudentInfoVO studentVO);
    Result<?> deleteStudent(Integer stuId);
    Result<Map<String, Object>> getStudentStatistics(Integer classOrgId);
}