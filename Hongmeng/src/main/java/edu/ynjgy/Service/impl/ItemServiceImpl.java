package edu.ynjgy.Service.impl;

import edu.ynjgy.Service.ItemService;
import edu.ynjgy.entity.ItemInfo;
import edu.ynjgy.mapper.ItemInfoMapper;
import edu.ynjgy.utils.PageResult;
import edu.ynjgy.utils.Result;
import lombok.RequiredArgsConstructor;
import org.springframework.stereotype.Service;
import java.util.List;

@Service
@RequiredArgsConstructor
public class ItemServiceImpl implements ItemService {

    private final ItemInfoMapper mapper;

    @Override
    public Result<PageResult<ItemInfo>> getItemList(Integer page, Integer pageSize, Integer eventId, String itemName) {
        int offset = (page - 1) * pageSize;
        List<ItemInfo> pageData = mapper.selectPage(eventId, itemName, offset, pageSize);
        Long total = mapper.countFiltered(eventId, itemName);
        return Result.success(PageResult.of(pageData, total, page, pageSize));
    }

    @Override
    public Result<List<ItemInfo>> getItemsByEventId(Integer eventId) {
        return Result.success(mapper.selectByEventId(eventId));
    }

    @Override
    public Result<?> getItemById(Integer itemId) {
        ItemInfo item = mapper.selectById(itemId);
        if (item == null) return Result.error("项目不存在");
        return Result.success(item);
    }

    @Override
    public Result<?> createItem(ItemInfo item) {
        int rows = mapper.insert(item);
        if (rows > 0) return Result.success("创建成功");
        return Result.error("创建失败");
    }

    @Override
    public Result<?> updateItem(Integer itemId, ItemInfo item) {
        item.setItemId(itemId);
        int rows = mapper.update(item);
        if (rows > 0) return Result.success("更新成功");
        return Result.error("更新失败");
    }

    @Override
    public Result<?> deleteItem(Integer itemId) {
        int rows = mapper.deleteById(itemId);
        if (rows > 0) return Result.success("删除成功");
        return Result.error("删除失败");
    }
}
