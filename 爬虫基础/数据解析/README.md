# 数据提取与基础格式处理教学示例

本目录包含四个独立的 Python 脚本，分别演示了：
- **CSS 选择器** 与 **XPath 选择器** 在网页解析中的应用（基于 `parsel` 库）
- **正则表达式** 在文本中提取目标内容
- **JSON 格式** 的序列化（`dumps`）与反序列化（`loads`）

这些示例适合作为学习 Python 爬虫中“解析数据”和“处理常见数据格式”的入门材料。

## 环境依赖

所有脚本均使用 Python 标准库及少量第三方库，请提前安装：

```bash
pip install requests parsel fake-useragent
```

> 注：`json.py` 和 `正则表达式.py` 仅使用标准库，无需额外安装。

## 文件说明

### 1. `css选择器.py`
**功能**：从单个小说章节页面中提取标题和正文内容，使用 **CSS 选择器** 定位元素。

- 目标 URL：`https://www.xzmncy.com/list/56209/26983835.html`（小说章节页）
- 主要步骤：
  1. 发送请求，获取 HTML
  2. 创建 `Selector` 对象
  3. 使用 `css()` 方法定位章节容器 `div.readbar`
  4. 从容器中提取标题（`div.bookname h1::text`）和正文段落（`div#htmlContent p::text`）
- 输出：打印标题和每一段正文

**运行命令**：
```bash
python css选择器.py
```

**关键知识点**：
- `selector.css(...)` 返回选择器对象列表（非字符串），可继续调用 `.css()` 进行链式选择
- `.get()` 获取第一个匹配的文本，`.getall()` 获取所有匹配的文本列表
- 不要混淆 `extract()`/`extract_first()`（旧版 API）与 `get()`/`getall()`（推荐）

---

### 2. `Xpath选择器.py`
**功能**：与 `css选择器.py` 相同，但使用 **XPath 语法** 定位元素。

- 同样提取标题和正文
- XPath 表达式示例：
  - 容器：`//div[@class="readbar"]`
  - 标题：`.//div[@class="bookname"]/h1/text()`
  - 正文：`.//div[@id="htmlContent"]//p/text()`
- 输出：打印标题和正文

**运行命令**：
```bash
python Xpath选择器.py
```

**关键知识点**：
- XPath 中的 `.//` 表示从当前节点开始递归查找
- `text()` 获取文本节点
- `.get()` / `.getall()` 用法与 CSS 选择器一致

---

### 3. `正则表达式.py`
**功能**：演示使用正则表达式（`re` 模块）从一段文本中提取特定模式的字符串。

- 文本内容：一篇名为《小云朵的晚安旅行》的童话
- 任务：提取“小云朵轻轻打了个**小小的哈欠**”中的目标短语
- 使用非贪婪匹配：`re.findall('小云朵轻轻打了个(.*?)，慢慢、慢慢地，飘进了甜甜的梦里', text)`
- 输出：`小小的哈欠`

**运行命令**：
```bash
python 正则表达式.py
```

**关键知识点**：
- `re.findall(pattern, text)` 返回所有匹配的字符串列表
- `.*?` 表示匹配任意字符（非贪婪），尽可能短地匹配
- 适合处理结构较为固定、但无法用 HTML/XML 解析器直接提取的文本

---

### 4. `json.py`
**功能**：演示 Python 数据类型与 JSON 字符串之间的相互转换（序列化与反序列化）。

- 定义了一个包含书籍信息的列表（`books`），每个元素为字典
- `json.dumps(books, indent=2, ensure_ascii=False)` → 将 Python 对象转为格式化的 JSON 字符串（带缩进，保留中文）
- `json.loads(json_str)` → 将 JSON 字符串重新解析为 Python 对象
- 演示如何访问转换后的数据（如取第一本书的标题）

**运行命令**：
```bash
python json.py
```

**关键知识点**：
- `json.dumps()` 用于序列化（Python → JSON 字符串）
- `json.loads()` 用于反序列化（JSON 字符串 → Python）
- 参数 `indent` 美化输出，`ensure_ascii=False` 避免中文转义
- 实际爬虫中常将抓取的数据保存为 JSON 文件，反之也常从 API 响应中解析 JSON

---

## 教学建议顺序

1. **JSON 基础**（`json.py`）  
   先了解 Python 字典/列表与 JSON 的对应关系，为后续存储数据打基础。

2. **正则表达式入门**（`正则表达式.py`）  
   学习简单的文本模式匹配，适用于清洗或提取非结构化文本。

3. **CSS 选择器**（`css选择器.py`）  
   掌握网页解析最常用的方法，直观易懂。

4. **XPath 选择器**（`Xpath选择器.py`）  
   作为 CSS 选择器的补充，理解 XPath 的节点查找逻辑。

## 常见问题

- **`parsel` 未安装**  
  运行 CSS/XPath 脚本前请执行 `pip install parsel`。

- **网站请求失败**  
  示例中的 URL 可能随时间失效。可以替换为您自己可访问的任意 HTML 页面，并相应调整选择器表达式。

- **正则表达式匹配不到内容**  
  请检查原始文本是否与正则模式完全匹配（包括标点符号、换行等）。推荐使用在线正则测试工具辅助调试。

- **JSON 中文字符显示为 `\u...`**  
  因为未设置 `ensure_ascii=False`。示例中已正确设置，一般不会出现该问题。

## 扩展练习

- 修改 `css选择器.py`，提取页面中的所有超链接。
- 将 `json.py` 中的 `books` 数据保存为真实的 `books.json` 文件（使用 `json.dump()`）。
- 结合 `正则表达式.py` 与 `css选择器.py`，从网页中抓取数据后用正则进一步清洗。

---

如果您在学习和使用过程中遇到任何问题，欢迎随时提问。