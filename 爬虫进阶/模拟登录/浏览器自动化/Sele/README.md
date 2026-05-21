```markdown
此代码介绍了，Selenium 模拟浏览器登录操作，包含普通表单登录和 iframe 内嵌表单登录两种场景

## 文件一：selenium_基础用法.py

目标网址：
````
https://www.bequke.com/login
````

核心代码解析：
```python
# 创建浏览器配置对象，保持浏览器打开
options = Options()
options.add_experimental_option("detach", True)

# 启动 Chrome 浏览器
driver = webdriver.Chrome(service=Service("chromedriver路径"), options=options)
driver.get('https://www.bequke.com/login')

# 定位用户名、密码输入框并填入信息
username = driver.find_element(By.XPATH, '//*[@id="username"]')
driver.execute_script("arguments[0].click()", username)
username.send_keys('你的账号')

# 点击登录按钮，处理后续跳转和弹窗
driver.find_element(By.XPATH, '//*[@id="wrapper"]/div[1]/div/div[1]/form/div[3]/button').click()
#退出登录的弹窗处理
alert = driver.switch_to.alert
alert.accept()
```

## 文件二：selenium_iframe.py

目标网址：
````
https://pinco.seewo.com/teacher/login?redirectUrl=%2Fteacher%2Fmain%2Fcourse%2Fmanage%2Flearning
````

核心代码解析：
```python
# 先切换进 iframe（通过索引 0）
driver.switch_to.frame(0)

# 点击“账号登录”标签，等待用户名输入框可见并输入
wait = WebDriverWait(driver, 10)
wait.until(EC.visibility_of_element_located((By.ID, 'username')))
user.send_keys("123456")

# 使用 JavaScript 勾选隐藏的协议复选框
driver.execute_script("arguments[0].checked = true;", checkbox_input)
#手动触发事件，防止监听
driver.execute_script("arguments[0].dispatchEvent(new Event('change'));", checkbox_input)
# 循环检测登录结果，若未成功则点击重试按钮并重新登录
while True:
    driver.switch_to.default_content()
    try:
        element = wait.until(EC.presence_of_element_located((By.XPATH, '//*[contains(text(), "课程空间")]')))
        if element.text == '课程空间':
            print('登录成功')
            break
    except TimeoutException:
        # 切回 iframe，点击重试验证按钮
        driver.switch_to.frame(0)
        retry_btn.click()
        login_btn.click()
```

> 注意：`selenium_iframe.py` 中涉及 iframe 切换、显式等待、JavaScript 操作隐藏元素以及登录结果轮询，适合处理需要二次验证或重试机制的登录页面。
```