package edu.ynjgy.Service.impl;

import edu.ynjgy.Service.StudentService;
import edu.ynjgy.entity.OrgInfo;
import edu.ynjgy.entity.StudentInfo;
import edu.ynjgy.mapper.OrgInfoMapper;
import edu.ynjgy.mapper.StuScoreRecordMapper;
import edu.ynjgy.mapper.StudentInfoMapper;
import edu.ynjgy.utils.PageResult;
import edu.ynjgy.utils.Result;
import edu.ynjgy.vo.StudentInfoVO;
import lombok.RequiredArgsConstructor;
import lombok.extern.slf4j.Slf4j;
import org.springframework.cache.annotation.CacheEvict;
import org.springframework.cache.annotation.Cacheable;
import org.springframework.stereotype.Service;
import org.springframework.transaction.annotation.Transactional;

import java.math.BigDecimal;
import java.util.ArrayList;
import java.util.HashMap;
import java.util.List;
import java.util.Map;
import java.util.stream.Collectors;

@Slf4j
@Service
@RequiredArgsConstructor
public class StudentServiceImpl implements StudentService {

    private final StudentInfoMapper studentInfoMapper;
    private final OrgInfoMapper orgInfoMapper;
    private final StuScoreRecordMapper scoreRecordMapper;

    @Override
    @Cacheable(value = "studentInfo", key = "#stuId")
    public Result<StudentInfoVO> getStudentInfo(Integer stuId) {
        StudentInfo student = studentInfoMapper.selectById(stuId);
        if (student == null) {
            return Result.error("学生不存在");
        }

        StudentInfoVO vo = convertToVO(student);
        if (student.getClassOrgId() != null) {
            OrgInfo org = orgInfoMapper.selectById(student.getClassOrgId());
            if (org != null) {
                vo.setClassName(org.getOrgName());
            }
        }

        return Result.success(vo);
    }

    @Override
    @Cacheable(value = "studentsByClass", key = "#classOrgId")
    public Result<List<StudentInfoVO>> getStudentsByClass(Integer classOrgId) {
        List<StudentInfo> students = studentInfoMapper.selectByClassId(classOrgId);
        List<StudentInfoVO> voList = students.stream()
                .map(this::convertToVO)
                .collect(Collectors.toList());

        OrgInfo org = orgInfoMapper.selectById(classOrgId);
        if (org != null) {
            voList.forEach(vo -> vo.setClassName(org.getOrgName()));
        }

        return Result.success(voList);
    }

    @Override
    public Result<PageResult<StudentInfoVO>> searchStudents(String keyword, String gender, Integer classOrgId,
                                                             String enrollYear, String trainLevel,
                                                             Integer pageNum, Integer pageSize) {
        int offset = (pageNum - 1) * pageSize;
        String kw = (keyword != null && !keyword.isEmpty()) ? keyword : null;
        String g = (gender != null && !gender.isEmpty()) ? gender : null;
        String ey = (enrollYear != null && !enrollYear.isEmpty()) ? enrollYear : null;
        String tl = (trainLevel != null && !trainLevel.isEmpty()) ? trainLevel : null;
        List<StudentInfo> pageData = studentInfoMapper.searchPage(kw, g, classOrgId, ey, tl, offset, pageSize);
        Long total = studentInfoMapper.countSearch(kw, g, classOrgId, ey, tl);
        List<StudentInfoVO> voList = pageData.stream()
                .map(this::convertToVO)
                .collect(Collectors.toList());
        PageResult<StudentInfoVO> pageResult = PageResult.of(voList, total, pageNum, pageSize);
        return Result.success(pageResult);
    }

    @Override
    @Transactional
    @CacheEvict(value = {"studentInfo", "studentsByClass"}, allEntries = true)
    public Result<?> addStudent(StudentInfoVO studentVO) {
        if (studentVO.getStuNo() == null || studentVO.getStuNo().isEmpty()) {
            return Result.error("学号不能为空");
        }
        if (studentVO.getClassOrgId() == null) {
            return Result.error("班级不能为空");
        }
        StudentInfo exist = studentInfoMapper.selectByStuNo(studentVO.getStuNo());
        if (exist != null) {
            return Result.error("学号已存在");
        }

        StudentInfo student = new StudentInfo();
        student.setStuNo(studentVO.getStuNo());
        student.setStuName(studentVO.getStuName());
        student.setGender(studentVO.getGender());
        student.setPhone(studentVO.getPhone());
        student.setClassOrgId(studentVO.getClassOrgId());
        student.setEnrollYear(studentVO.getEnrollYear());
        student.setIdCard(studentVO.getIdCard());
        student.setBirthDate(studentVO.getBirthDate());
        student.setTrainLevel(studentVO.getTrainLevel());

        int rows = studentInfoMapper.insert(student);
        if (rows > 0) {
            return Result.success("学生添加成功");
        }
        return Result.error("添加失败");
    }

    @Override
    @Transactional
    @CacheEvict(value = {"studentInfo", "studentsByClass"}, allEntries = true)
    public Result<?> updateStudentInfo(Integer stuId, StudentInfoVO studentVO) {
        StudentInfo student = studentInfoMapper.selectById(stuId);
        if (student == null) {
            return Result.error("学生不存在");
        }

        student.setStuName(studentVO.getStuName());
        student.setGender(studentVO.getGender());
        student.setPhone(studentVO.getPhone());
        student.setClassOrgId(studentVO.getClassOrgId());
        student.setEnrollYear(studentVO.getEnrollYear());
        student.setIdCard(studentVO.getIdCard());
        student.setBirthDate(studentVO.getBirthDate());
        student.setTrainLevel(studentVO.getTrainLevel());

        int rows = studentInfoMapper.update(student);
        if (rows > 0) {
            return Result.success("学生信息更新成功");
        }
        return Result.error("更新失败");
    }

    @Override
    @Transactional
    @CacheEvict(value = {"studentInfo", "studentsByClass"}, allEntries = true)
    public Result<?> deleteStudent(Integer stuId) {
        StudentInfo student = studentInfoMapper.selectById(stuId);
        if (student == null) {
            return Result.error("学生不存在");
        }

        int rows = studentInfoMapper.deleteById(stuId);
        if (rows > 0) {
            return Result.success("学生删除成功");
        }
        return Result.error("删除失败");
    }

    @Override
    public Result<Map<String, Object>> getStudentStatistics(Integer classOrgId) {
        List<StudentInfo> students = studentInfoMapper.selectByClassId(classOrgId);

        Map<String, Object> stats = new HashMap<>();
        stats.put("totalStudents", students.size());

        long maleCount = students.stream().filter(s -> "男".equals(s.getGender())).count();
        long femaleCount = students.stream().filter(s -> "女".equals(s.getGender())).count();
        stats.put("maleCount", maleCount);
        stats.put("femaleCount", femaleCount);

        BigDecimal classAvgScore = scoreRecordMapper.getClassAvgScore(classOrgId);
        stats.put("averageScore", classAvgScore != null ? classAvgScore : BigDecimal.ZERO);

        return Result.success(stats);
    }

    private StudentInfoVO convertToVO(StudentInfo student) {
        StudentInfoVO vo = new StudentInfoVO();
        vo.setStuId(student.getStuId());
        vo.setStuNo(student.getStuNo());
        vo.setStuName(student.getStuName());
        vo.setGender(student.getGender());
        vo.setPhone(student.getPhone());
        vo.setClassOrgId(student.getClassOrgId());
        vo.setEnrollYear(student.getEnrollYear());
        vo.setIdCard(student.getIdCard());
        vo.setBirthDate(student.getBirthDate());
        vo.setTrainLevel(student.getTrainLevel());
        return vo;
    }
}