package edu.ynjgy.Controller;

import edu.ynjgy.Service.EventLevelService;
import edu.ynjgy.entity.EventLevelInfo;
import edu.ynjgy.utils.Result;
import lombok.RequiredArgsConstructor;
import org.springframework.web.bind.annotation.*;

@RestController
@RequestMapping("/api/event-level")
@RequiredArgsConstructor
public class EventLevelController {

    private final EventLevelService eventLevelService;

    @GetMapping("/list")
    public Result<?> getEventLevelList() {
        return eventLevelService.getAllLevels();
    }

    @GetMapping("/{levelId}")
    public Result<?> getEventLevelById(@PathVariable Integer levelId) {
        return eventLevelService.getLevelById(levelId);
    }

    @PostMapping
    public Result<?> createEventLevel(@RequestBody EventLevelInfo levelInfo) {
        return eventLevelService.createLevel(levelInfo);
    }

    @PutMapping("/{levelId}")
    public Result<?> updateEventLevel(@PathVariable Integer levelId, @RequestBody EventLevelInfo levelInfo) {
        return eventLevelService.updateLevel(levelId, levelInfo);
    }

    @DeleteMapping("/{levelId}")
    public Result<?> deleteEventLevel(@PathVariable Integer levelId) {
        return eventLevelService.deleteLevel(levelId);
    }

    @DeleteMapping
    public Result<?> batchDelete(@RequestParam String ids) {
        for (String id : ids.split(",")) {
            eventLevelService.deleteLevel(Integer.parseInt(id.trim()));
        }
        return Result.success("删除成功");
    }
}
