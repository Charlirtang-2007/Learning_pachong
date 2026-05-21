import asyncio
import aiohttp
import aiofiles
import json
import os
import random
import logging
from tenacity import retry, stop_after_attempt, wait_exponential, retry_if_exception_type
from fake_useragent import UserAgent

# ---------------------- 日志配置 ----------------------
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[
        logging.StreamHandler(),                     # 控制台输出
        logging.FileHandler('crawler.log', encoding='utf-8')  # 文件输出
    ]
)
logger = logging.getLogger(__name__)

# ---------------------- 重试装饰器 ----------------------
def retry_async(max_attempts=3):
    """异步重试装饰器，针对网络异常"""
    return retry(
        stop=stop_after_attempt(max_attempts),
        wait=wait_exponential(multiplier=1, min=2, max=10),
        retry=retry_if_exception_type((aiohttp.ClientError, asyncio.TimeoutError))
    )

# ---------------------- 异步函数 ----------------------
@retry_async()
async def get_titles(session, book_url, headers):
    """
    获取章节目录，返回列表，每个元素为 (title, chapter_url)
    """
    await asyncio.sleep(random.uniform(1, 3))
    logger.info(f"正在获取章节目录: {book_url}")

    async with session.get(book_url, headers=headers, timeout=10) as resp:
        resp.raise_for_status()
        txt_obj = await resp.text()
        json_obj = json.loads(txt_obj)

    # 根据实际 API 响应调整字段路径（示例）
    novel_list = json_obj.get("data", {}).get("novel", {}).get("items", [])
    if not novel_list:
        logger.warning("未获取到章节列表，API 返回可能异常")
        return []

    chapter_urls = []
    for item in novel_list:
        title = item.get("title")
        cid = item.get("cid")
        if not title or not cid:
            logger.warning(f"章节数据不完整: {item}")
            continue
        # 构建 JSON 字符串并 URL 编码
        import urllib.parse
        chapter_data = json.dumps({
            "book_id": "4306063500",
            "cid": f"4306063500|{cid}",
            "need_bookinfo": 1
        })
        encoded_data = urllib.parse.quote(chapter_data)
        chapter_url = f"https://dushu.baidu.com/api/pc/getChapterContent?data={encoded_data}"
        chapter_urls.append((title, chapter_url))

    logger.info(f"共获取到 {len(chapter_urls)} 个章节")
    return chapter_urls


@retry_async()
async def aiodownload(session, chapter_url, headers, title, name, sem):
    """下载并保存单个章节"""
    async with sem:
        logger.debug(f"开始下载章节: {title} -> {chapter_url[:80]}...")
        try:
            async with session.get(chapter_url, headers=headers, timeout=15) as resp:
                if resp.status != 200:
                    logger.warning(f"请求失败 {chapter_url}，状态码 {resp.status}")
                    return
                txt_obj = await resp.text()
                json_obj = json.loads(txt_obj)
                # 根据实际 API 响应调整内容字段
                content = json_obj.get("data", {}).get("novel", {}).get("content", "")
                if not content:
                    logger.warning(f"章节 {title} 内容为空")
                    return

                # 保存文件
                folder = rf"D:\小说\{name}"
                os.makedirs(folder, exist_ok=True)
                safe_title = "".join(c for c in title if c not in r'\/:*?"<>|')
                file_path = os.path.join(folder, f"{safe_title}.txt")
                async with aiofiles.open(file_path, 'w', encoding='utf-8') as f:
                    await f.write(content)
                logger.info(f"保存成功: {title}")

        except json.JSONDecodeError as e:
            logger.error(f"JSON 解析失败 {chapter_url}: {e}")
        except asyncio.TimeoutError:
            logger.error(f"请求超时: {chapter_url}")
        except aiohttp.ClientError as e:
            logger.error(f"网络错误: {chapter_url} - {e}")
        except Exception as e:
            logger.exception(f"未知错误: {chapter_url} - {e}")


async def main(headers, book_url, name):
    """主函数"""
    async with aiohttp.ClientSession() as session:
        chapter_list = await get_titles(session, book_url, headers)
        if not chapter_list:
            logger.error("没有获取到章节列表，程序退出")
            return

        sem = asyncio.Semaphore(10)  # 控制并发数
        tasks = []
        for title, chapter_url in chapter_list:
            tasks.append(aiodownload(session, chapter_url, headers, title, name, sem))

        await asyncio.gather(*tasks)
        logger.info("全部章节下载完成")


if __name__ == "__main__":
    ua = UserAgent()
    headers = {'User-Agent': ua.random}
    # 注意：这里的 data 参数需要 URL 编码，但用 params 方式更简单
    import urllib.parse
    params = {"data": json.dumps({"book_id": "4306063500"})}
    book_url = "https://dushu.baidu.com/api/pc/getCatalog?" + urllib.parse.urlencode(params)
    name = "西游记"
    asyncio.run(main(headers, book_url, name))