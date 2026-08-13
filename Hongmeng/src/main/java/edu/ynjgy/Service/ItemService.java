package edu.ynjgy.Service;

import edu.ynjgy.entity.ItemInfo;
import edu.ynjgy.utils.PageResult;
import edu.ynjgy.utils.Result;
import java.util.List;

public interface ItemService {
    Result<PageResult<ItemInfo>> getItemList(Integer page, Integer pageSize, Integer eventId, String itemName);
    Result<List<ItemInfo>> getItemsByEventId(Integer eventId);
    Result<?> getItemById(Integer itemId);
    Result<?> createItem(ItemInfo item);
    Result<?> updateItem(Integer itemId, ItemInfo item);
    Result<?> deleteItem(Integer itemId);
}
