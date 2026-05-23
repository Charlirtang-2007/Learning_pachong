# 爬虫与数据存储示例集

本目录包含多个使用 `requests` + `parsel` 进行网页数据抓取，并将结果保存为不同格式（CSV、Excel、JSON、TXT）的示例，以及使用 `requests` 直接下载图片、视频、音频文件的简单脚本。

## 环境依赖

安装所需第三方库：

```bash
pip install requests parsel pandas fake-useragent
```

> 注：`pandas` 仅在 `Excel_demo.py` 中使用，若无需保存 Excel 可略过。

## 文件说明

### 1. `csv_demo.py`
抓取指定 URL 中的列表数据（小说章节列表），使用 CSS 选择器解析，并将结果保存为 **CSV 文件**。

- 目标网站：`https://www.xzmncy.com/list/58017/`
- 解析规则：`div#list dl` → `dd a` 获取 `href` 和文本
- 输出文件：`xzmncy.csv`（UTF-8-sig 编码）
- 包含随机延迟（1~3 秒）和随机 User-Agent

```bash
python csv_demo.py
```

### 2. `Excel_demo.py`
类似 `csv_demo.py`，但将数据保存为 **Excel 文件**（`.xlsx`）。

- 额外使用 `pandas` 库
- 解析规则更宽松：同时尝试 `ul.chapter li a` 和 `div#list dl dd a`
- 对链接中的 `_m` 进行替换清洗
- 输出文件：`xzmncy.xlsx`，工作表名为“蚊天帝”

```bash
python Excel_demo.py
```

### 3. `json_demo.py`
抓取数据并保存为 **JSON 文件**。

- 目标 URL：`https://www.xzmncy.com/list/55501/`
- 根据页面结构自适应选择 `div#list dl` 或 `ul.chapter`
- 每条数据保存为 `{title: href}` 字典，再放入列表
- 输出文件：`xzmncy.json`（格式化缩进，`ensure_ascii=False`）

> 注意：代码末尾保存 JSON 的部分被注释掉了，如需保存请取消注释。

```bash
python json_demo.py
```

### 4. `text_demo.py`
抓取数据并保存为 **纯文本文件**（`.txt`）。

- 解析逻辑与 `json_demo.py` 相同，但最终将整个字典转换为字符串写入
- 输出文件：`xzmncy.txt`
- 提示：TXT 格式不便于后续解析，一般仅作简单记录

```bash
python text_demo.py
```

### 5. `图片.py`
下载单张图片并保存为本地文件。

- URL 为示例图片链接（壁纸站）
- 使用 `response.content` 以二进制写入模式保存
- 输出文件：`downloaded_image.png`（实际格式需根据 Content-Type 调整后缀）

```bash
python 图片.py
```

### 6. `视频.py`
下载单个 MP4 视频文件。

- URL 为示例视频链接（含过期时间戳和签名）
- 保存为 `downloaded_mp4.mp4`

```bash
python 视频.py
```

### 7. `音频.py`
下载单个 MP3 音频文件。

- URL 为示例音乐链接（酷我音乐）
- 保存为 `download.mp3`

```bash
python 音频.py
```

## 通用注意事项

1. **网站可用性**  
   示例中的 URL（`https://www.xzmncy.com/...`）可能随时间失效或变更反爬策略。如果运行失败，请检查网站是否可访问，并更新选择器规则。

2. **随机延迟与 User-Agent**  
   每个爬虫脚本都加入了 `time.sleep(random.uniform(1,3))` 和随机 UA，以降低被封风险。实际使用时可根据目标网站调整延迟时间。

3. **CSS 选择器兼容性**  
   不同页面的结构可能不同，例如：
   - `csv_demo.py` 只用了 `div#list dl`
   - `Excel_demo.py` 同时兼容 `ul.chapter` 和 `div#list`
   如果目标网站改版，需要相应修改选择器。

4. **链接拼接**  
   代码中提取的 `href` 是相对路径，已通过 `f"https://www.xzmncy.com{href}"` 补全。若目标网站域名变化，请同步修改。

5. **Excel 文件写入**  
   `Excel_demo.py` 依赖 `openpyxl`（pandas 的 Excel 引擎），若未安装请执行：
   ```bash
   pip install openpyxl
   ```

6. **图片/视频/音频下载**  
   这些脚本未做异常处理和重试机制，对于大文件建议加入流式下载（`stream=True`）以节省内存。示例：
   ```python
   with requests.get(url, stream=True) as r:
       with open('file.mp4', 'wb') as f:
           for chunk in r.iter_content(chunk_size=8192):
               f.write(chunk)
   ```

7. **法律与道德**  
   请尊重目标网站的 `robots.txt` 和服务条款，勿高频请求或用于商业用途。本示例仅供学习 Python 爬虫技术使用。

## 扩展建议

- **多页抓取**：可以在现有代码外层添加 for 循环，遍历分页 URL。
- **错误重试**：使用 `requests` 的 `adapters` 或 `tenacity` 库实现自动重试。
- **数据去重**：保存前检查 `data_list` 中是否已存在相同标题/链接。
- **代理池**：若目标网站反爬严格，可参考您之前提供的代理池脚本集成到这些爬虫中。

---

如果您在使用过程中遇到任何问题（如选择器失效、保存格式错误等），欢迎提供具体报错信息以便进一步排查。