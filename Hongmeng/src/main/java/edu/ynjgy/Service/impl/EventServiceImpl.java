package edu.ynjgy.Service.impl;

import edu.ynjgy.Service.EventService;
import edu.ynjgy.entity.EventInfo;
import edu.ynjgy.mapper.EventInfoMapper;
import edu.ynjgy.mapper.StuScoreRecordMapper;
import edu.ynjgy.utils.Result;
import edu.ynjgy.vo.EventInfoVO;
import lombok.RequiredArgsConstructor;
import lombok.extern.slf4j.Slf4j;
import org.springframework.cache.annotation.CacheEvict;
import org.springframework.cache.annotation.Cacheable;
import org.springframework.stereotype.Service;
import org.springframework.transaction.annotation.Transactional;

import java.util.List;
import java.util.Map;
import java.util.stream.Collectors;

@Slf4j
@Service
@RequiredArgsConstructor
public class EventServiceImpl implements EventService {

    private final EventInfoMapper eventInfoMapper;
    private final StuScoreRecordMapper scoreRecordMapper;

    @Override
    @Cacheable(value = "allEvents")
    public Result<List<EventInfoVO>> getAllEvents() {
        List<EventInfo> events = eventInfoMapper.selectAll();
        List<EventInfoVO> voList = events.stream()
                .map(this::convertToVO)
                .collect(Collectors.toList());
        return Result.success(voList);
    }

    @Override
    @Cacheable(value = "eventDetail", key = "#eventId")
    public Result<EventInfoVO> getEventDetail(Integer eventId) {
        EventInfo event = eventInfoMapper.selectById(eventId);
        if (event == null) {
            return Result.error("赛事不存在");
        }
        EventInfoVO vo = convertToVO(event);
        return Result.success(vo);
    }

    @Override
    @Transactional
    @CacheEvict(value = {"allEvents", "eventsByStatus"}, allEntries = true)
    public Result<?> createEvent(EventInfoVO eventVO) {
        EventInfo event = new EventInfo();
        event.setEventNo(eventVO.getEventNo());
        event.setEventName(eventVO.getEventName());
        event.setHostUnit(eventVO.getHostUnit());
        event.setEventLevel(eventVO.getEventLevel());
        event.setEventDesc(eventVO.getEventDesc());
        event.setCharterPath(eventVO.getCharterPath());
        event.setEventStatus(eventVO.getEventStatus());
        event.setBaseScore(eventVO.getBaseScore());

        int rows = eventInfoMapper.insert(event);
        if (rows > 0) {
            return Result.success("赛事创建成功");
        }
        return Result.error("创建失败");
    }

    @Override
    @Transactional
    @CacheEvict(value = {"allEvents", "eventDetail", "eventsByStatus"}, allEntries = true)
    public Result<?> updateEvent(Integer eventId, EventInfoVO eventVO) {
        EventInfo event = eventInfoMapper.selectById(eventId);
        if (event == null) {
            return Result.error("赛事不存在");
        }

        event.setEventName(eventVO.getEventName());
        event.setHostUnit(eventVO.getHostUnit());
        event.setEventLevel(eventVO.getEventLevel());
        event.setEventDesc(eventVO.getEventDesc());
        event.setEventStatus(eventVO.getEventStatus());
        event.setBaseScore(eventVO.getBaseScore());

        int rows = eventInfoMapper.update(event);
        if (rows > 0) {
            return Result.success("赛事更新成功");
        }
        return Result.error("更新失败");
    }

    @Override
    @Transactional
    @CacheEvict(value = {"allEvents", "eventDetail", "eventsByStatus"}, allEntries = true)
    public Result<?> deleteEvent(Integer eventId) {
        EventInfo event = eventInfoMapper.selectById(eventId);
        if (event == null) {
            return Result.error("赛事不存在");
        }

        int rows = eventInfoMapper.deleteById(eventId);
        if (rows > 0) {
            return Result.success("赛事删除成功");
        }
        return Result.error("删除失败");
    }

    @Override
    @Cacheable(value = "eventsByStatus", key = "#status")
    public Result<List<EventInfoVO>> getEventsByStatus(Integer status) {
        List<EventInfo> events = eventInfoMapper.selectByStatus(status);
        List<EventInfoVO> voList = events.stream()
                .map(this::convertToVO)
                .collect(Collectors.toList());
        return Result.success(voList);
    }

    private EventInfoVO convertToVO(EventInfo event) {
        EventInfoVO vo = new EventInfoVO();
        vo.setEventId(event.getEventId());
        vo.setEventNo(event.getEventNo());
        vo.setEventName(event.getEventName());
        vo.setHostUnit(event.getHostUnit());
        vo.setEventLevel(event.getEventLevel());
        vo.setEventDesc(event.getEventDesc());
        vo.setCharterPath(event.getCharterPath());
        vo.setEventStatus(event.getEventStatus());
        vo.setStatusDesc(getStatusDesc(event.getEventStatus()));
        vo.setBaseScore(event.getBaseScore());
        vo.setBackStr1(event.getBackStr1());
        return vo;
    }

    private String getStatusDesc(Integer status) {
        switch (status) {
            case 0: return "未开始";
            case 1: return "进行中";
            case 2: return "已结束";
            default: return "未知";
        }
    }
}