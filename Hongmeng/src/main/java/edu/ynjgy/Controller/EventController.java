package edu.ynjgy.Controller;

import java.util.List;

import org.springframework.web.bind.annotation.DeleteMapping;
import org.springframework.web.bind.annotation.GetMapping;
import org.springframework.web.bind.annotation.PathVariable;
import org.springframework.web.bind.annotation.PostMapping;
import org.springframework.web.bind.annotation.PutMapping;
import org.springframework.web.bind.annotation.RequestBody;
import org.springframework.web.bind.annotation.RequestMapping;
import org.springframework.web.bind.annotation.RequestParam;
import org.springframework.web.bind.annotation.RestController;

import edu.ynjgy.Service.EventService;
import edu.ynjgy.entity.EventInfo;
import edu.ynjgy.mapper.EventInfoMapper;
import edu.ynjgy.utils.PageResult;
import edu.ynjgy.utils.Result;
import edu.ynjgy.vo.EventInfoVO;
import lombok.RequiredArgsConstructor;
import lombok.extern.slf4j.Slf4j;

@Slf4j
@RestController
@RequestMapping("/api/event")
@RequiredArgsConstructor
public class EventController {

    private final EventService eventService;
    private final EventInfoMapper eventInfoMapper;

    @GetMapping("/list")
    public Result<?> getEventList(
            @RequestParam(defaultValue = "1") Integer page,
            @RequestParam(defaultValue = "10") Integer pageSize,
            @RequestParam(required = false) String eventName,
            @RequestParam(required = false) String eventLevel,
            @RequestParam(required = false) Integer eventStatus) {

        int offset = (page - 1) * pageSize;
        List<EventInfo> pageData = eventInfoMapper.selectPage(eventName, eventLevel, eventStatus, offset, pageSize);
        Long total = eventInfoMapper.countFiltered(eventName, eventLevel, eventStatus);
        PageResult<EventInfo> pageResult = PageResult.of(pageData, total, page, pageSize);
        return Result.success(pageResult);
    }

    @GetMapping("/all")
    public Result<?> getAllEvents() {
        return eventService.getAllEvents();
    }

    @GetMapping("/{eventId:\\d+}")
    public Result<?> getEventById(@PathVariable Integer eventId) {
        return eventService.getEventDetail(eventId);
    }

    @PostMapping
    public Result<?> createEvent(@RequestBody EventInfoVO eventVO) {
        return eventService.createEvent(eventVO);
    }

    @PutMapping("/{eventId}")
    public Result<?> updateEvent(@PathVariable Integer eventId, @RequestBody EventInfoVO eventVO) {
        return eventService.updateEvent(eventId, eventVO);
    }

    @DeleteMapping("/{eventId}")
    public Result<?> deleteEvent(@PathVariable Integer eventId) {
        return eventService.deleteEvent(eventId);
    }

    @DeleteMapping
    public Result<?> batchDelete(@RequestParam String ids) {
        for (String id : ids.split(",")) {
            eventService.deleteEvent(Integer.parseInt(id.trim()));
        }
        return Result.success("删除成功");
    }

    @GetMapping("/status/{status}")
    public Result<?> getEventsByStatus(@PathVariable Integer status) {
        return eventService.getEventsByStatus(status);
    }
}
