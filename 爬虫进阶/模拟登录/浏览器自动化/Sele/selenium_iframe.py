from selenium import webdriver
from selenium.common import TimeoutException
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.wait import WebDriverWait

# 创建设置对象
options = Options()
options.add_experimental_option("detach", True)
service = Service(r"D:\浏览器自动化\chromedriver-win64\chromedriver-win64\chromedriver.exe")
driver = webdriver.Chrome(service=service, options=options)
driver.get("https://pinco.seewo.com/teacher/login?redirectUrl=%2Fteacher%2Fmain%2Fcourse%2Fmanage%2Flearning")

# 定位iframe节点
driver.switch_to.frame(0)  # 通过索引切换

# 定位账号登录节点
node = driver.find_element(By.XPATH, '//*[@id="scanLoginTab"]/h2')
node.click()
# 显式等待：用户名输入框可见
wait = WebDriverWait(driver, 10)
wait.until(EC.visibility_of_element_located((By.ID, 'username')))

# 定位用户名输入框节点
user = driver.find_element(By.XPATH, '//*[@id="username"]')
user.click()
user.send_keys("123456")
# 显式等待：密码输入框可见
wait.until(EC.visibility_of_element_located((By.ID, 'password')))

# 定位密码输入框节点
pawd = driver.find_element(By.XPATH, '//*[@id="password"]')
pawd.click()
pawd.send_keys("123456")
# 显式等待：协议复选框存在
wait.until(EC.presence_of_element_located((By.XPATH, '//label[@class="agreement-checkbox-label"]/input')))

# 定位政策节点
checkbox_input = wait.until(
    EC.presence_of_element_located(
        (By.XPATH, '//label[@class="agreement-checkbox-label"]/input[@name="agreement-checkbox-login"]')
    )
)
if checkbox_input.is_displayed()==False:
    print('元素隐藏')
# 因为input隐藏，用JS勾选
driver.execute_script("arguments[0].checked = true;", checkbox_input)
driver.execute_script("arguments[0].dispatchEvent(new Event('change'));", checkbox_input)

# 显式等待：登录按钮可点击
wait.until(EC.element_to_be_clickable((By.ID, 'login-btn')))

# 定位登录按钮并点击
node3 = driver.find_element(By.XPATH, '//*[@id="login-btn"]')
driver.execute_script("arguments[0].checked = true;", node3)
driver.execute_script("arguments[0].dispatchEvent(new Event('change'));", node3)
driver.execute_script("arguments[0].click()", node3)

# 循环检测登录结果
while True:
    #  先回到主页面（防止之前切到iframe里）
    driver.switch_to.default_content()

    try:
        #  尝试在3秒内找到“课程空间”元素
        wait = WebDriverWait(driver, 3)
        element = wait.until(EC.presence_of_element_located(
            (By.XPATH, '//*[@id="root"]//*[contains(text(), "课程空间")]')
        ))
        # 如果找到了，并且文本正确，就成功退出
        if element and element.text == '课程空间':
            print('登录成功')
            break

    except TimeoutException:
        # 如果在3秒内没找到“课程空间”（即登录还没成功），
        #    就进入重试逻辑：去点击重试验证码的按钮
        print("还没成功，尝试点重置按钮...")

        try:
            #先切回登录框所在的iframe
            driver.switch_to.default_content()   # 确保在外面再切进去，避免嵌套错误
            driver.switch_to.frame(0)

            # 等待并点击那个“重试/验证”按钮
            retry_btn = WebDriverWait(driver, 3).until(
                EC.element_to_be_clickable(
                    (By.XPATH, '//*[@id="j-loginNoCaptcha"]/div[2]/div[2]/div[1]/div[3]/span[1]')
                )
            )
            retry_btn.click()

            #  再次点击登录按钮（node3 需要提前定义好，并且要确保在当前iframe内有效）
            #  注意：node3 是在之前定义的，要确保它没有被stale（过时）。保险的做法是重新定位。
            login_btn = driver.find_element(By.XPATH, '//*[@id="login-btn"]')
            login_btn.click()
            try:
                wait = WebDriverWait(driver, 3)
                yanz_btn=wait.until(EC.presence_of_element_located((By.XPATH,'//*[@id="j-loginNoCaptcha"]/div[2]/div[2]/div[2]/div/div[2]/span[1]')))
                if yanz_btn:
                    print("验证成功，再次点击登录按钮")
                    login_btn.click()
                    break
            except TimeoutException:
                a=input("是否继续重试(y/n)\n")
                if a == 'n':
                    break
        except Exception as e:
            #  如果点击重试的过程中出错（比如按钮找不到），打印并退出循环避免无限报错
            print(f"重试环节出错: {e}")
            break