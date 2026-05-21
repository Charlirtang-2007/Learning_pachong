import time
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
#创建浏览器设置对象
o1=Options()
#保持打开
o1.add_experimental_option("detach", True)
#禁用沙盒
o1.add_argument('--no-sandbox')

#创建并启动浏览器
a1=webdriver.Chrome(service=Service(r"D:\浏览器自动化\chromedriver-win64\chromedriver-win64\chromedriver.exe"),options=o1)
a1.get('https://www.bequke.com/login')
time.sleep(2)
#定位账号登录节点
zah=a1.find_element(By.XPATH,'//*[@id="username"]')
a1.execute_script("arguments[0].click()",zah)
zah.send_keys('')
time.sleep(3)
#定位账号登录节点
mma=a1.find_element(By.XPATH,'//*[@id="userpass"]')
a1.execute_script("arguments[0].click()",mma)
mma.send_keys('')
time.sleep(3)
node=a1.find_element(By.XPATH,'//*[@id="wrapper"]/div[1]/div/div[1]/form/div[3]/button').click()
time.sleep(3)
node1=a1.find_element(By.XPATH,'//*[@id="wrapper"]/div[1]/div/div/h4/a').click()
time.sleep(3)
alert=a1.switch_to.alert
alert.accept()