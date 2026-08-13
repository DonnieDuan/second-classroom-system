package edu.ynjgy.Service;

import edu.ynjgy.utils.Result;
import edu.ynjgy.vo.EventInfoVO;

import java.util.List;

public interface EventService {
    Result<List<EventInfoVO>> getAllEvents();
    Result<EventInfoVO> getEventDetail(Integer eventId);
    Result<?> createEvent(EventInfoVO eventVO);
    Result<?> updateEvent(Integer eventId, EventInfoVO eventVO);
    Result<?> deleteEvent(Integer eventId);
    Result<List<EventInfoVO>> getEventsByStatus(Integer status);
}