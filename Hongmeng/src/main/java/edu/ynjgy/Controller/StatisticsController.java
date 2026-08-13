package edu.ynjgy.Controller;

import edu.ynjgy.Service.StatisticsService;
import edu.ynjgy.utils.Result;
import lombok.RequiredArgsConstructor;
import org.springframework.web.bind.annotation.*;

@RestController
@RequestMapping("/admin/statistics")
@RequiredArgsConstructor
public class StatisticsController {

    private final StatisticsService statisticsService;

    @GetMapping("/class/{classId}")
    public Result<?> classStatistics(@PathVariable Integer classId) {
        return statisticsService.getClassScoreStatistics(classId);
    }

    @GetMapping("/eventTrend")
    public Result<?> eventTrend() {
        return statisticsService.getEventTrendStatistics();
    }

    @GetMapping("/major/{majorId}")
    public Result<?> majorStatistics(@PathVariable Integer majorId) {
        return statisticsService.getMajorScoreStatistics(majorId);
    }
}