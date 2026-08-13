package edu.ynjgy.Controller;

import edu.ynjgy.utils.Result;
import lombok.extern.slf4j.Slf4j;
import org.springframework.beans.factory.annotation.Value;
import org.springframework.web.bind.annotation.*;
import org.springframework.web.multipart.MultipartFile;

import java.io.IOException;
import java.nio.file.Files;
import java.nio.file.Path;
import java.nio.file.Paths;
import java.util.UUID;

@Slf4j
@RestController
@RequestMapping("/api/upload")
public class FileUploadController {

    @Value("${app.upload-path:/data/uploads/certificates}")
    private String uploadPath;

    @PostMapping("/cert")
    public Result<?> uploadCert(@RequestParam("file") MultipartFile file) {
        if (file.isEmpty()) {
            return Result.error("上传文件不能为空");
        }

        String originalFilename = file.getOriginalFilename();
        String ext = originalFilename != null ? originalFilename.substring(originalFilename.lastIndexOf(".")) : ".jpg";
        String newFilename = UUID.randomUUID() + ext;

        try {
            Path dir = Paths.get(uploadPath);
            if (!Files.exists(dir)) {
                Files.createDirectories(dir);
            }
            Path targetPath = dir.resolve(newFilename);
            file.transferTo(targetPath.toFile());

            String fileUrl = "/uploads/certificates/" + newFilename;
            return Result.success(fileUrl);
        } catch (IOException e) {
            log.error("文件上传失败", e);
            return Result.error("文件上传失败: " + e.getMessage());
        }
    }
}
