# AQI 历史数据爬虫 (Scrapy + Selenium)

本项目基于 Scrapy 框架，结合 Selenium 和 `selenium-stealth` 插件，抓取 [aqistudy.cn](https://www.aqistudy.cn) 网站的历史空气质量数据。主要用于绕过网站的反爬虫机制（如 JavaScript 加密渲染），获取真实的 HTML 页面源码。

## 功能特点

- 通过 Scrapy 调度请求，控制并发和延迟。
- 自动更换随机 User-Agent（使用 `fake-useragent`）。
- 对于需要 JavaScript 渲染的页面（如 `daydata.php`），自动调用 Selenium 无头浏览器进行加载。
- 使用 `selenium-stealth` 隐藏浏览器自动化特征，降低被检测概率。
- 支持用户交互输入城市名称，自动抓取该城市所有月份的历史数据页面。

## 环境要求

- Python 3.8+
- Google Chrome 浏览器（版本与 ChromeDriver 匹配）
- ChromeDriver（与本地 Chrome 版本对应）

## 安装步骤

1. **克隆/下载项目代码**

   将本项目所有文件放置在同一个目录下，目录结构应类似：
   ```
   AQI/
   ├── spiders/
   │   ├── __init__.py
   │   └── aqi.py
   ├── middlewares.py
   ├── pipelines.py
   ├── settings.py
   └── scrapy.cfg 
   ```

2. **创建虚拟环境（推荐）**
   ```bash
   python -m venv venv
   # Windows
   venv\Scripts\activate
   # Linux/macOS
   source venv/bin/activate
   ```

3. **安装依赖包**
   ```bash
   pip install scrapy selenium selenium-stealth fake-useragent
   ```

4. **配置 ChromeDriver**

   - 下载与本地 Chrome 版本一致的 [ChromeDriver](https://chromedriver.chromium.org/)。
   - 将 `chromedriver.exe` 放在任意目录，然后**修改 `middlewares.py` 中的 `driver_path` 变量**，指向你的 `chromedriver.exe` 实际路径。

   ```python
   # 在 AqiSeleniumMiddleware 类的 __init__ 方法中
   driver_path = r"D:\你的路径\chromedriver.exe"
   ```

## 使用方法

1. **运行爬虫**

   在项目根目录（包含 `scrapy.cfg` 或 `settings.py` 的目录）打开终端，执行：
   ```bash
   scrapy crawl aqi
   ```

2. **输入城市名称**

   程序会提示 `请输入城市`，输入中文城市名（例如 `武汉`、`北京`），然后按回车。

3. **抓取过程**

   - 爬虫会先访问 `https://www.aqistudy.cn/historydata/monthdata.php?city={城市}`，提取所有月份链接。
   - 对每个月份链接，使用 Selenium 渲染并获取最终 HTML。
   - 抓取到的 HTML 源码会通过 `print(response.text)` 输出到控制台（在 `aqi_parse` 方法中可自定义处理逻辑，如保存到文件或提取数据）。

## 配置说明

### 设置文件 (`settings.py`)

- **DOWNLOADER_MIDDLEWARES**：启用了 `FakeUserAgentMiddleware`（随机 UA）和 `AqiSeleniumMiddleware`（Selenium 渲染）。
- **CONCURRENT_REQUESTS_PER_DOMAIN = 1**：限制同一域名并发请求数为 1。
- **DOWNLOAD_DELAY = 1**：请求间隔 1 秒，降低被封风险。
- **ROBOTSTXT_OBEY = True**：遵守网站的 `robots.txt` 规则（可根据需要关闭）。

### Selenium 中间件 (`AqiSeleniumMiddleware`)

- 使用无头模式 (`--headless`)，窗口大小 1920x1080。
- 禁用图片加载以加快速度。
- 应用 `selenium-stealth` 隐藏指纹。
- 仅对 `meta` 中包含 `'selenium': True` 的 Request 启用（如 `aqi.py` 中的 `yield` 语句）。

### 随机 User-Agent 中间件 (`FakeUserAgentMiddleware`)

- 自动为每个请求设置一个 Chrome 的 User-Agent，减少特征。

## 注意事项

1. **网站反爬虫策略**：`aqistudy.cn` 具有较强的反爬虫机制（如参数加密、数据加密、浏览器指纹检测等）。本项目仅使用 Selenium 获取渲染后的 HTML，不保证 100% 稳定。如果遇到大量失败，可尝试：
   - 增加 `time.sleep(2)` 等待时间（在 `middlewares.py` 的 `process_request` 中）。
   - 改用 Playwright + `playwright-stealth`。
   - 直接逆向 JS 加密算法，调用数据接口 `historyapi.php`。
   - 推荐使用逆向，playwright与selenium效果差不多

2. **ChromeDriver 版本**：确保 ChromeDriver 与本地 Chrome 浏览器主版本一致，否则会报错。

3. **性能**：Selenium 启动浏览器较慢，抓取大量月份时耗时较长。建议先测试少量月份，再扩展。

4. **输出处理**：当前 `aqi_parse` 仅打印响应文本。如需保存数据，可在此处添加解析逻辑（例如使用 `parsel` 提取表格并保存为 CSV）。

## 扩展建议

- **解析数据**：参考之前提供的 `extract_aqi_data` 函数，在 `aqi_parse` 中解析 HTML 表格，提取结构化数据。
- **存储**：通过 Scrapy 的 Item Pipeline 将数据保存至 CSV、JSON 或数据库。
- **错误处理**：为 Selenium 中间件添加超时重试机制（使用 `try...except`）。
- **代理 IP**：如果 IP 被封，可配置代理中间件（如 `scrapy-rotating-proxies`）。

## 许可证

本项目仅供学习交流使用，请勿用于商业或侵犯他人权益的行为。使用前请遵守目标网站的 `robots.txt` 及法律法规。


