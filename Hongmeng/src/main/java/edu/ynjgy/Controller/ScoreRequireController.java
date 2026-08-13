package edu.ynjgy.Controller;

import edu.ynjgy.entity.ScoreRequire;
import edu.ynjgy.mapper.ScoreRequireMapper;
import edu.ynjgy.utils.Result;
import lombok.RequiredArgsConstructor;
import org.springframework.web.bind.annotation.*;

import java.util.List;

@RestController
@RequestMapping("/api/score-require")
@RequiredArgsConstructor
public class ScoreRequireController {

    private final ScoreRequireMapper scoreRequireMapper;

    @GetMapping("/list")
    public Result<?> getScoreRequireList() {
        List<ScoreRequire> list = scoreRequireMapper.selectAll();
        return Result.success(list);
    }

    @GetMapping("/{reqId}")
    public Result<?> getScoreRequireById(@PathVariable Integer reqId) {
        ScoreRequire require = scoreRequireMapper.selectById(reqId);
        return Result.success(require);
    }

    @PostMapping
    public Result<?> createScoreRequire(@RequestBody ScoreRequire scoreRequire) {
        int rows = scoreRequireMapper.insert(scoreRequire);
        if (rows > 0) {
            return Result.success("创建成功");
        }
        return Result.error("创建失败");
    }

    @PutMapping("/{reqId}")
    public Result<?> updateScoreRequire(@PathVariable Integer reqId, @RequestBody ScoreRequire scoreRequire) {
        scoreRequire.setReqId(reqId);
        int rows = scoreRequireMapper.update(scoreRequire);
        if (rows > 0) {
            return Result.success("更新成功");
        }
        return Result.error("更新失败");
    }

    @DeleteMapping("/{reqId}")
    public Result<?> deleteScoreRequire(@PathVariable Integer reqId) {
        int rows = scoreRequireMapper.deleteById(reqId);
        if (rows > 0) {
            return Result.success("删除成功");
        }
        return Result.error("删除失败");
    }

    @DeleteMapping
    public Result<?> batchDelete(@RequestParam String ids) {
        for (String id : ids.split(",")) {
            scoreRequireMapper.deleteById(Integer.parseInt(id.trim()));
        }
        return Result.success("删除成功");
    }
}
