# BeQuKe 自动验证码搜索工具

一句话简介：通过百度 OCR 自动识别验证码，在 bequke.com 上实现带 Cookie 持久化的关键词搜索。

## 功能特性

- **Cookie 持久化**：首次验证成功后保存 Cookie，后续运行自动加载，无需重复打码
- **自动获取验证码**：从 `/searchVerify/captcha` 接口获取 Base64 验证码图片
- **百度 OCR 识别**：调用百度高精度文字识别接口，自动返回验证码数字
- **智能重试**：Cookie 失效时自动识别并提交，验证成功后更新本地 Cookie
- **友好延时**：搜索前等待 30 秒，降低请求频率，礼貌爬取

## 环境要求

- Python 3.6 或更高版本
- 已注册百度智能云账号，并开通 **文字识别** 服务（获取 `APP_ID`、`API_KEY`、`SECRET_KEY`）

## 安装步骤

```bash
# 1. 克隆或下载本项目
git clone <你的仓库地址>
cd <项目目录>

# 2. 安装依赖
pip install requests fake-useragent baidu-aip

# 3. 配置百度 OCR 密钥
# 在项目根目录下创建文件夹 api_key，然后新建 api_peizhi.py 文件，内容如下：