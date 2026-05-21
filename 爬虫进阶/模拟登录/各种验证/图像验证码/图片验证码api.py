import requests
import base64
import json
import os
from io import BytesIO
from baidu_ocr import BaiDuOcr
from fake_useragent import UserAgent
import time
#实例化类
ua = UserAgent()
ocr = BaiDuOcr()
#定义cookie文件名
COOKIE_FILE = "bequke_cookies.json"


def save_cookies(session):
    """把当前Session的Cookie保存到本地文件，自动过滤掉search_delay"""
    try:
        del session.cookies['search_delay']
    except KeyError:
        pass

    cookies_dict = session.cookies.get_dict()
    with open(COOKIE_FILE, 'w') as f:
        json.dump(cookies_dict, f)
    print(f"Cookie已保存到 {COOKIE_FILE}")


def load_cookies(session):
    """从本地文件加载Cookie到Session，返回是否加载成功"""
    if not os.path.exists(COOKIE_FILE):
        return False
    try:
        with open(COOKIE_FILE, 'r') as f:
            cookies_dict = json.load(f)
        # 将 Cookie 真正设置到 Session 中
        from requests.utils import cookiejar_from_dict
        session.cookies = cookiejar_from_dict(cookies_dict)
        print(f"已加载本地Cookie（{len(cookies_dict)}项）")
        return True
    except Exception as e:
        print(f"Cookie加载失败: {e}")
        return False


def get_captcha_code(session):
    """获取验证码图片并保存到本地，返回图片字节流"""
    try:
        resp = session.get('https://www.bequke.com/searchVerify/captcha', timeout=10)
        if resp.status_code != 200:
            print(f"获取验证码失败，状态码: {resp.status_code}")
            return None
        data_uri = resp.text
        base64_data = data_uri.split(",", 1)[1] if data_uri.startswith("data:image/png;base64,") else data_uri
        image_bytes = base64.b64decode(base64_data)
        with open('captcha.jpg', 'wb') as f:
            f.write(image_bytes)
        return image_bytes
    except Exception as e:
        print(f"获取验证码异常: {e}")
        return None


def recognize_captcha(session):
    """获取并识别验证码，返回识别出的数字串"""
    img_bytes = get_captcha_code(session)
    if not img_bytes:
        return None
    result = ocr.ocr_image(img_bytes)
    if result:
        code = result[0]
        print(f"OCR识别结果: {code}")
        return code
    else:
        print("OCR识别结果为空")
        return None


def search_with_autocode(session, keyword):
    # 第一次尝试搜索
    resp = session.post('https://www.bequke.com/search', data={'searchkey': keyword})

    if "验证码" not in resp.text and "搜索间隔" not in resp.text:
        print("✅ 直接搜索成功")
        save_cookies(session)  # 持久化可能更新的 Cookie
        return resp.text

    print("🔐 需要更换新身份...")
    new_session = requests.Session()
    new_session.headers.update({"User-Agent": ua.random})

    try:
        new_session.get('https://www.bequke.com', timeout=15)
    except:
        pass

    print("⏳ 冷却30秒...")
    time.sleep(30)

    code = recognize_captcha(new_session)
    if not code:
        return None

    print("📤 提交验证码并搜索...")
    resp = new_session.post(
        'https://www.bequke.com/search',
        data={'searchkey': keyword, 'code': code},
    )

    if "验证码" in resp.text:
        print("❌ 验证码识别错误")
        return resp.text
    else:
        from requests.utils import cookiejar_from_dict
        session.cookies = cookiejar_from_dict(new_session.cookies.get_dict())
        save_cookies(session)  # 内部已清除 search_delay
        if "搜索间隔" in resp.text:
            print("⚠️ 搜索仍受频率限制，但Cookie已更新，稍后重试即可")
        else:
            print("✅ 搜索成功")
        return resp.text


# ========== 主程序 ==========
SESSION = requests.Session()
SESSION.headers.update({
    "User-Agent": ua.chrome,
})

# ★ 启动时先加载本地Cookie
load_cookies(SESSION)

searchkey = input("请输入名字:\n")
print("等待30秒后开始搜索，做个友善的爬虫...")
result_html = search_with_autocode(SESSION, searchkey)
if result_html:
    print("搜索结果：")
    print(result_html)
time.sleep(50)  # 防刷