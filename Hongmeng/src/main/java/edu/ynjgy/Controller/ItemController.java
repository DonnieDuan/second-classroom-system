package edu.ynjgy.Controller;

import org.springframework.web.bind.annotation.DeleteMapping;
import org.springframework.web.bind.annotation.GetMapping;
import org.springframework.web.bind.annotation.PathVariable;
import org.springframework.web.bind.annotation.PostMapping;
import org.springframework.web.bind.annotation.PutMapping;
import org.springframework.web.bind.annotation.RequestBody;
import org.springframework.web.bind.annotation.RequestMapping;
import org.springframework.web.bind.annotation.RequestParam;
import org.springframework.web.bind.annotation.RestController;

import edu.ynjgy.Service.ItemService;
import edu.ynjgy.entity.ItemInfo;
import edu.ynjgy.utils.Result;
import lombok.RequiredArgsConstructor;
import lombok.extern.slf4j.Slf4j;

@Slf4j
@RestController
@RequestMapping("/api/item")
@RequiredArgsConstructor
public class ItemController {

    private final ItemService itemService;

    @GetMapping("/list")
    public Result<?> getItemList(
            @RequestParam(defaultValue = "1") Integer page,
            @RequestParam(defaultValue = "10") Integer pageSize,
            @RequestParam(required = false) Integer eventId,
            @RequestParam(required = false) String itemName) {
        return itemService.getItemList(page, pageSize, eventId, itemName);
    }

    @GetMapping("/event/{eventId}")
    public Result<?> getItemsByEventId(@PathVariable Integer eventId) {
        return itemService.getItemsByEventId(eventId);
    }

    @GetMapping("/{itemId:\\d+}")
    public Result<?> getItemById(@PathVariable Integer itemId) {
        return itemService.getItemById(itemId);
    }

    @PostMapping
    public Result<?> createItem(@RequestBody ItemInfo itemInfo) {
        return itemService.createItem(itemInfo);
    }

    @PutMapping("/{itemId}")
    public Result<?> updateItem(@PathVariable Integer itemId, @RequestBody ItemInfo itemInfo) {
        return itemService.updateItem(itemId, itemInfo);
    }

    @DeleteMapping("/{itemId}")
    public Result<?> deleteItem(@PathVariable Integer itemId) {
        return itemService.deleteItem(itemId);
    }

    @DeleteMapping
    public Result<?> batchDelete(@RequestParam String ids) {
        for (String id : ids.split(",")) {
            itemService.deleteItem(Integer.parseInt(id.trim()));
        }
        return Result.success("删除成功");
    }
}
