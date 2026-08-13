package edu.ynjgy.Controller;
import edu.ynjgy.Service.StudentService;
import edu.ynjgy.utils.Result;
import edu.ynjgy.vo.StudentInfoVO;
import lombok.RequiredArgsConstructor;
import org.springframework.validation.annotation.Validated;
import org.springframework.web.bind.annotation.*;

@RestController
@RequestMapping("/api/student")
@RequiredArgsConstructor
@Validated
public class StudentController {

    private final StudentService studentService;
    @GetMapping("/list")
    public Result<?> getStudentList(
            @RequestParam(defaultValue = "") String keyword,
            @RequestParam(defaultValue = "") String stuName,
            @RequestParam(required = false) String gender,
            @RequestParam(required = false) Integer classOrgId,
            @RequestParam(required = false) String enrollYear,
            @RequestParam(required = false) String trainLevel,
            @RequestParam(defaultValue = "1") Integer page,
            @RequestParam(defaultValue = "10") Integer pageSize) {
        String kw = keyword.isEmpty() ? stuName : keyword;
        return studentService.searchStudents(kw, gender, classOrgId, enrollYear, trainLevel, page, pageSize);
    }
    @GetMapping("/{stuId}")
    public Result<?> getStudentInfo(@PathVariable Integer stuId) {
        return studentService.getStudentInfo(stuId);
    }

    @GetMapping("/class/{classOrgId}")
    public Result<?> getStudentsByClass(@PathVariable Integer classOrgId) {
        return studentService.getStudentsByClass(classOrgId);
    }

    @PostMapping
    public Result<?> addStudent(@RequestBody StudentInfoVO studentVO) {
        return studentService.addStudent(studentVO);
    }

    @PutMapping("/{stuId}")
    public Result<?> updateStudentInfo(
            @PathVariable Integer stuId,
            @RequestBody StudentInfoVO studentVO) {
        return studentService.updateStudentInfo(stuId, studentVO);
    }

    @DeleteMapping("/{stuId}")
    public Result<?> deleteStudent(@PathVariable Integer stuId) {
        return studentService.deleteStudent(stuId);
    }

    @DeleteMapping
    public Result<?> batchDelete(@RequestParam String ids) {
        for (String id : ids.split(",")) {
            studentService.deleteStudent(Integer.parseInt(id.trim()));
        }
        return Result.success("删除成功");
    }

    @GetMapping("/statistics/class/{classOrgId}")
    public Result<?> getClassStatistics(@PathVariable Integer classOrgId) {
        return studentService.getStudentStatistics(classOrgId);
    }
}
