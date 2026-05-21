import asyncio
import aiohttp
import aiomysql
import logging
import random
from parsel import Selector
from fake_useragent import UserAgent
import uuid
import time
# ------------------- 日志配置 -------------------
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    handlers=[logging.StreamHandler()]
)
logger = logging.getLogger(__name__)

# ------------------- 带重试的异步请求函数 -------------------
async def fetch_with_retry(session, url, base_headers, retries=3, delay=1):
    """
    使用指数退避重试机制发送GET请求，每次请求前随机延时，并随机生成User-Agent
    """
    ua = UserAgent()
    for attempt in range(1, retries + 1):
        # 随机延时
        wait_time = random.uniform(0.3, 0.5)
        logger.debug(f"等待 {wait_time:.2f} 秒后请求 {url}")
        await asyncio.sleep(wait_time)

        # 动态生成请求头，随机User-Agent
        headers = base_headers.copy() if base_headers else {}
        headers['User-Agent'] = ua.random

        try:
            async with session.get(url, headers=headers) as resp:
                if resp.status == 200:
                    return await resp.text()
                else:
                    logger.warning(f"请求失败 {resp.status}：{url}，第{attempt}次重试")
        except Exception as e:
            logger.error(f"请求异常 {url}: {e}，第{attempt}次重试")
        if attempt < retries:
            await asyncio.sleep(delay * (2 ** (attempt - 1)))  # 指数退避
    logger.error(f"重试{retries}次后仍失败：{url}")
    return None


# ------------------- 异步获取商品列表页中的所有单品URL -------------------
async def aioget_html_urls(index_urls, headers, session, sem):
    """
    异步获取列表页中每个商品的详情页URL（使用信号量控制并发）
    """
    html1_url_list = []
    for index_url in index_urls:
        async with sem:
            logger.info(f"正在爬取列表页：{index_url}")
            html = await fetch_with_retry(session, index_url, headers)
            if html:
                selector = Selector(html)
                pic_mode_box = selector.css('div.content div.pic-mode-box ul#J_PicMode')
                li_list = pic_mode_box.css('li > a:first-child::attr(href)').getall()
                for li in li_list:
                    html1_url_list.append("https://detail.zol.com.cn" + li)
            else:
                logger.warning(f"列表页请求最终失败：{index_url}")
    return html1_url_list

# ------------------- 从单品页中提取参数页URL -------------------
async def aioget_html3_url_list(html1_url_list, headers, session, sem):
    """
    从商品详情页中提取参数页的URL（处理单品页和系列页两种结构）
    """
    urls_try = []       # 存储需要二次尝试的单品页URL
    html3_url_list = []
    for url in html1_url_list:
        async with sem:
            logger.info(f"正在解析单品页：{url}")
            html = await fetch_with_retry(session, url, headers)
            if not html:
                logger.warning(f"单品页请求最终失败：{url}")
                continue
            selector = Selector(html)
            # 尝试系列页结构（产品型号表格）
            param_links = selector.css('#_j_series_model .model__item td.cell-8 a::attr(href)').getall()
            if param_links:
                for pl in param_links:
                    html3_url_list.append("https://detail.zol.com.cn" + pl)
            else:
                urls_try.append(url)

    # 处理第一次未提取到参数链接的单品页（可能是单品页结构）
    for url in urls_try:
        async with sem:
            logger.info(f"二次尝试解析单品页：{url}")
            html = await fetch_with_retry(session, url, headers)
            if not html:
                logger.warning(f"二次尝试单品页请求最终失败：{url}")
                continue
            selector = Selector(html)
            param_link2 = selector.css('#_j_tag_nav ul.nav__list li a:contains("参数")::attr(href)').get()
            if param_link2:
                html3_url_list.append("https://detail.zol.com.cn" + param_link2)
            else:
                logger.error(f"未能从单品页提取参数链接：{url}")
    return html3_url_list

# ------------------- 提取参数页面中的详细参数 -------------------
def extract_params(data):
    """
    从参数页面 HTML 中提取所有参数（同步解析，无需异步）
    """
    sel = Selector(text=data)
    param_names = [
        "产品型号", "电商报价", "上市时间", "产品类型", "产品定位", "操作系统",
        "CPU系列", "CPU型号", "CPU主频", "最高睿频", "核心/线程数", "三级缓存", "制程工艺",
        "内存容量", "内存类型", "硬盘容量", "硬盘描述",
        "触控屏", "屏幕类型", "屏幕尺寸", "显示比例", "屏幕分辨率", "亮度", "屏占比",
        "NTSC色域", "对比度", "屏幕技术", "像素密度",
        "显卡类型", "显卡芯片", "显存容量",
        "摄像头", "音频系统", "扬声器", "麦克风",
        "无线网卡", "蓝牙",
        "数据接口", "视频接口", "音频接口",
        "指取设备", "键盘描述", "指纹识别", "人脸识别",
        "电池类型", "续航时间", "电源适配器",
        "笔记本重量", "长度", "宽度", "厚度", "外壳描述",
        "其它特点", "附带软件", "特色功能", "包装清单"
    ]
    params = {}
    for name in param_names:
        try:
            row = sel.css(f'tr:contains("{name}")')
            if not row:
                params[name] = None
                continue
            td = row.css('td')
            if not td:
                params[name] = None
                continue
            value = None
            a_texts = td.css('a::text').getall()
            if a_texts:
                value = ' '.join([t.strip() for t in a_texts if t.strip()])
            if not value:
                span_texts = td.css('span::text').getall()
                if span_texts:
                    value = ' '.join([t.strip() for t in span_texts if t.strip()])
            if not value:
                raw = td.xpath('normalize-space()').get()
                if raw:
                    value = raw.strip()
            params[name] = value if value else None
        except Exception:
            params[name] = None
    return params

# ------------------- 异步请求所有参数页并提取数据 -------------------
async def aiorequests(html3_url_list, headers, session, sem):
    """
    并发请求所有参数页，限制并发数为20，并提取参数
    """
    params_datas = []

    async def fetch_one(url):
        async with sem:
            logger.info(f"正在请求参数页：{url}")
            html = await fetch_with_retry(session, url, headers)
            if html:
                return extract_params(html)
            else:
                logger.warning(f"参数页请求最终失败：{url}")
                return None

    tasks = [fetch_one(url) for url in html3_url_list]
    results = await asyncio.gather(*tasks)
    for res in results:
        if res is not None:
            params_datas.append(res)
    return params_datas

# ------------------- 异步写入数据库（使用 aiomysql） -------------------
async def aiowriter(params_datas, db_config):
    """
    将提取的参数列表追加写入 MySQL 数据库（异步）
    表名：new_product_params，字段名与 param_names 一致（中文）
    为每条数据生成一个随机唯一编码（UUID），并以此作为去重依据。
    如果产品型号为 None 或空字符串，则跳过该条记录（保留业务逻辑）。
    """
    if not params_datas:
        logger.info("无数据写入")
        return
    pool = await aiomysql.create_pool(
        host=db_config['host'],
        user=db_config['user'],
        password=db_config['password'],
        db=db_config['db'],
        charset='utf8',
        autocommit=True
    )
    inserted_count = 0
    skipped_count = 0
    async with pool.acquire() as conn:
        async with conn.cursor() as cursor:
            # 获取所有字段名（加上 unique_code 列）
            sample = params_datas[0]
            columns = list(sample.keys())
            # 添加 unique_code 列（用于去重）
            columns_with_code = columns + ['unique_code']
            # 创建表（如果不存在），unique_code 设为唯一键
            create_sql = f"""
            CREATE TABLE IF NOT EXISTS new_product_params (
                id INT AUTO_INCREMENT PRIMARY KEY,
                {', '.join([f'`{col}` TEXT' for col in columns])},
                `unique_code` VARCHAR(64) NOT NULL,
                UNIQUE KEY `unique_code_idx` (`unique_code`)
            )
            """
            await cursor.execute(create_sql)

            # 查询已存在的 unique_code 集合（可选，用于批量检查，但随机码几乎不会重复，为性能可不查）
            # 但为了严谨，仍查询已存在的编码，避免极小概率的冲突
            select_sql = "SELECT `unique_code` FROM new_product_params"
            await cursor.execute(select_sql)
            existing_codes = {row[0] for row in await cursor.fetchall()}

            # 准备插入的数据
            insert_data = []
            for data in params_datas:
                model = data.get("产品型号")
                if not model:
                    logger.warning(f"跳过无产品型号的数据：{data}")
                    skipped_count += 1
                    continue
                # 生成唯一编码
                unique_code = uuid.uuid4().hex
                if unique_code in existing_codes:
                    # 理论上极小概率，但若冲突则重新生成一次
                    unique_code = uuid.uuid4().hex
                existing_codes.add(unique_code)
                # 构造插入行：原始参数值 + unique_code
                row_values = [data.get(col, None) for col in columns] + [unique_code]
                insert_data.append(row_values)

            if insert_data:
                placeholders = ', '.join(['%s'] * len(columns_with_code))
                insert_sql = f"INSERT INTO new_product_params ({', '.join([f'`{col}`' for col in columns_with_code])}) VALUES ({placeholders})"
                for row_vals in insert_data:
                    await cursor.execute(insert_sql, row_vals)
                    inserted_count += 1
                logger.info(f"成功插入 {inserted_count} 条新数据")
            else:
                logger.info("没有需要插入的新数据")

    pool.close()
    await pool.wait_closed()
    logger.info(f"共处理 {len(params_datas)} 条，插入 {inserted_count} 条，跳过 {skipped_count} 条（无产品型号）")

# ------------------- 主流程 -------------------
async def main(index_urls, base_headers, db_config):
    sem = asyncio.Semaphore(100)
    async with aiohttp.ClientSession() as session:
        html1_url_list = await aioget_html_urls(index_urls, base_headers, session, sem)
        logger.info(f"共获取到 {len(html1_url_list)} 个单品页URL")
        html3_url_list = await aioget_html3_url_list(html1_url_list, base_headers, session, sem)
        logger.info(f"共获取到 {len(html3_url_list)} 个参数页URL")
        params_datas = await aiorequests(html3_url_list, base_headers, session, sem)
        logger.info(f"成功提取 {len(params_datas)} 份参数数据")
        await aiowriter(params_datas, db_config)

if __name__ == '__main__':
    index_urls = []
    base_headers = {
        'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
        'Accept-Language': 'zh-CN,zh;q=0.8,en-US;q=0.5,en;q=0.3',
        'Connection': 'keep-alive',
        'Upgrade-Insecure-Requests': '1',
        # 注意：User-Agent 将在 fetch_with_retry 中动态生成，这里可以不写
    }
    for page_num in range(1, 2): #参数代表爬取，页面数
        url = f"https://detail.zol.com.cn/notebook_index/subcate16_0_list_1_0_99_2_0_{page_num}.html?from=360Sub1&baiduTop="
        index_urls.append(url)

    db_config = {
        'host': 'localhost',
        'user': 'root',
        'password': '',
        'db': 'data'
    }
    t1=time.time()
    asyncio.run(main(index_urls, base_headers, db_config))
    t2=time.time()
    print("总用时：")
    print(t2-t1)