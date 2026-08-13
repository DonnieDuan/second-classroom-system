package edu.ynjgy.Controller;

import edu.ynjgy.dto.ScoreSubmitDTO;
import edu.ynjgy.Service.ScoreRecordService;
import edu.ynjgy.utils.Result;
import lombok.RequiredArgsConstructor;
import org.springframework.validation.annotation.Validated;
import org.springframework.web.bind.annotation.*;

import jakarta.validation.Valid;

@RestController
@RequestMapping("/api/app/score")
@RequiredArgsConstructor
@Validated
public class StudentScoreController {

    private final ScoreRecordService scoreRecordService;

    @PostMapping("/submit")
    public Result<?> submitScore(@Valid @RequestBody ScoreSubmitDTO dto) {
        return scoreRecordService.submitScore(dto);
    }

    @GetMapping("/myScores")
    public Result<?> getMyScores(@RequestParam Integer stuId) {
        return scoreRecordService.getMyScores(stuId);
    }

    @GetMapping("/myTotal")
    public Result<?> getMyTotal(@RequestParam Integer stuId) {
        return scoreRecordService.getMyTotalScore(stuId);
    }

    // 前端鸿蒙应用使用的路径（路径参数风格）
    @GetMapping("/my/{stuId}")
    public Result<?> getMyScoresByPath(@PathVariable Integer stuId) {
        return scoreRecordService.getMyScores(stuId);
    }

    @GetMapping("/total/{stuId}")
    public Result<?> getMyTotalByPath(@PathVariable Integer stuId) {
        return scoreRecordService.getMyTotalScore(stuId);
    }
}
