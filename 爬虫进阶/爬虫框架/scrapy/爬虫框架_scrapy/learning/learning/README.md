# Scrapy 爬虫教学项目：笔趣阁小说下载器

本目录包含一个完整的 Scrapy 爬虫项目，用于抓取 `https://www.xzmncy.com`（笔趣阁类网站）上的小说章节，并将每章正文保存为独立的文本文件。代码结构清晰、注释充分，适合作为 **Scrapy 框架入门** 的教学范例。

## 📁 项目结构

```
learning/                     # Scrapy 项目根目录
├── scrapy.cfg                # Scrapy 部署配置文件
├── learning/                 # 项目主模块
│   ├── __init__.py
│   ├── items.py              # 定义数据容器（Item）
│   ├── middlewares.py        # 自定义中间件（请求/响应处理）
│   ├── pipelines.py          # 数据管道（存储处理）
│   ├── settings.py           # 项目配置（并发、延时、管道启用等）
│   └── spiders/              # 爬虫脚本目录
│       ├── __init__.py
│       └── xzmncy.py         # 核心爬虫：解析小说目录及正文
```

## 🚀 环境依赖

- Python 3.7+
- Scrapy 2.11+（推荐最新版）

安装 Scrapy：
```bash
pip install scrapy
```

## 📖 文件功能详解

### 1. `xzmncy.py` —— 核心爬虫（Spider）

**功能**：从小说目录页提取所有章节链接，然后依次请求每个章节页，提取标题和正文。

**代码解析**：
```python
class XzmncySpider(scrapy.Spider):
    name = "xzmncy"                          # 爬虫唯一标识
    allowed_domains = ["www.xzmncy.com"]     # 限制爬取域名
    start_urls = ["https://www.xzmncy.com/list/58089/"]  # 起始URL（小说目录页）

    def parse(self, response):
        # 提取所有章节的链接（相对路径）
        book_links = response.css("div#list dl dd a::attr(href)").getall()
        for book_link in book_links:
            # 生成新的请求，回调 parse_book 处理章节页
            yield response.follow(book_link, self.parse_book)

    def parse_book(self, response):
        # 提取标题和正文内容，并生成 Item（此处直接 yield 字典）
        yield {
            "title": response.css("div#read div.readbar div.bookname h1::text").get(),
            "content": '\n'.join(response.css("div#read div.readbar div#htmlContent p::text").getall()),
        }
```

**教学要点**：
- `response.follow()` 自动处理相对/绝对 URL，比手动拼接更安全。
- CSS 选择器链式调用，逐级缩小范围。
- `yield` 返回字典 → Scrapy 会自动交给 Item Pipeline 处理。

---

### 2. `pipelines.py` —— 数据存储管道

**功能**：接收 Spider 产生的 Item（字典），将正文保存为 `.txt` 文件。

**代码解析**：
```python
class LearningPipeline:
    def process_item(self, item):
        folder = "D:/小说/xzmncy"
        os.makedirs(folder, exist_ok=True)
        safe_title = item['title'].replace("/", "_").replace("\\", "_").replace(":", "_")
        filename = os.path.join(folder, f"{safe_title}.txt")
        with open(filename, "w", encoding="utf-8") as f:
            f.write(item['content'])
        return item   # 必须返回 item，以便后续管道继续处理（如果有）
```

**教学要点**：
- 管道是处理数据的“流水线”，可以串联多个管道（如清洗、去重、存储）。
- `process_item` 必须返回 Item 或抛出异常。
- 文件名清洗：去除 Windows 不允许的字符（`/ \ :` 等）。

---

### 3. `settings.py` —— 项目配置

**关键配置项**：
```python
BOT_NAME = "learning"                      # 项目名称
SPIDER_MODULES = ["learning.spiders"]      # 爬虫模块路径

# 日志级别（WARNING 只显示警告和错误，减少输出）
LOG_LEVEL = "WARNING"

# 遵守 robots.txt（设置为 True 则自动遵循目标网站的爬虫协议）
ROBOTSTXT_OBEY = True

# 对同一域名的并发请求数（设为 1 表示串行请求）
CONCURRENT_REQUESTS_PER_DOMAIN = 1

# 下载延迟（秒），避免对服务器造成压力
DOWNLOAD_DELAY = 1

# 启用 Item Pipeline（键为管道类路径，值为执行优先级，数字越小越先执行）
ITEM_PIPELINES = {
   "learning.pipelines.LearningPipeline": 300,
}

# 输出编码（默认 UTF-8）
FEED_EXPORT_ENCODING = "utf-8"
```

**教学要点**：
- `CONCURRENT_REQUESTS_PER_DOMAIN` 和 `DOWNLOAD_DELAY` 共同控制爬取速度，是礼貌爬虫的关键。
- `ROBOTSTXT_OBEY` 建议开启，除非明确需要绕过。
- `ITEM_PIPELINES` 的优先级数字：数字越小，管道越先执行。

---

### 4. `items.py` —— 定义数据模型（可选）

当前文件为空，但通常建议定义 Item 类，以明确数据结构：
```python
import scrapy

class LearningItem(scrapy.Item):
    title = scrapy.Field()
    content = scrapy.Field()
```
然后在 Spider 中 `yield LearningItem(title=..., content=...)`。本示例直接使用字典，简化了教学。

---

### 5. `middlewares.py` —— 中间件（本示例未使用）

保留 Scrapy 生成的模板，可用于：
- 修改 User-Agent
- 添加代理
- 处理异常响应
本项目中未启用任何自定义中间件。

---

### 6. `scrapy.cfg` —— 部署配置

指定项目默认设置模块，若需要部署到 Scrapyd 可修改 `[deploy]` 部分。

## 🏃 运行方法

### 1. 进入项目根目录
```bash
cd learning   # 即 scrapy.cfg 所在目录
```

### 2. 运行爬虫
```bash
scrapy crawl xzmncy
```

### 3. 查看结果
所有章节将保存到 `D:/小说/xzmncy/` 目录下，每个章节一个 `.txt` 文件，文件名＝章节标题（特殊字符已替换）。

### 4. 其他常用命令
- 列出所有可用爬虫：`scrapy list`
- 以交互式 shell 调试选择器：`scrapy shell "https://www.xzmncy.com/list/58089/"`
- 输出到 JSON 文件（不经过 Pipeline）：`scrapy crawl xzmncy -o output.json`

## 🧪 自学练习建议

1. **修改起始 URL**  
   在 `xzmncy.py` 中更改 `start_urls`，尝试爬取其他小说 ID（如 56283、57955）。

2. **调整下载速度**  
   修改 `settings.py` 中的 `DOWNLOAD_DELAY` 和 `CONCURRENT_REQUESTS_PER_DOMAIN`，观察爬取速率变化。

3. **完善 Item 定义**  
   在 `items.py` 中定义 `LearningItem` 类，并修改 Spider 和 Pipeline 使用该类。

4. **添加异常处理**  
   在 Pipeline 中捕获文件写入异常，增加重试逻辑。

5. **增加 User‑Agent 轮换**  
   编写一个 Downloader Middleware，随机更换 `User-Agent`。

6. **将数据存入数据库**  
   编写另一个 Pipeline，将章节信息存入 SQLite 或 MySQL（参考前面数据库示例）。

## ⚠️ 注意事项

- **目标网站变化**：`xzmncy.com` 的 HTML 结构可能随时变动，若 CSS 选择器失效，需重新分析网页并更新。
- **遵守 robots.txt**：当前已开启 `ROBOTSTXT_OBEY = True`，若网站禁止爬虫，Scrapy 会自动停止。
- **存储路径**：Pipeline 中使用了硬编码路径 `D:/小说/xzmncy`，请确保该目录存在或有写入权限，或修改为相对路径（如 `./novels`）。
- **请求频率**：已设置 `DOWNLOAD_DELAY = 1`，即每秒最多一个请求，请勿改为过小值，以免对网站造成压力。

## 🔍 调试技巧

- 启用 DEBUG 日志：在 `settings.py` 中设置 `LOG_LEVEL = "DEBUG"`，观察每个请求和响应详情。
- 使用 `scrapy shell` 实时测试选择器：  
  ```python
  fetch("https://www.xzmncy.com/list/58089/")
  response.css("div#list dl dd a::attr(href)").getall()
  ```
- 在 Spider 中添加 `scrapy.Request` 的 `errback` 参数处理失败请求。

## 📜 开源许可

本项目代码遵循 **MIT 许可证**，可自由使用、修改、分发。欢迎用于教学和个人学习。

---

**Happy Scraping!** 如有疑问，请查阅 [Scrapy 官方文档](https://docs.scrapy.org/) 或提交 Issue。