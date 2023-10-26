from selenium import webdriver
import time
from captcha2text import captcha2text
from selenium.webdriver.common.keys import Keys

def csu_classroom_login(number):
    number_str = str(number)
    password = "Csu@{}".format(number_str[-6:])

    # 创建一个浏览器对象，指定使用 Chrome 驱动程序
    driver = webdriver.Chrome()

    # 打开网页
    driver.get('http://classroom.csu.edu.cn/#/')
    # 隐式等待10秒
    driver.implicitly_wait(10)

    # 找到用户名、密码元素，填写用户名、密码
    username_input = driver.find_element_by_xpath("//input[@placeholder='请输入账号']")
    password_input = driver.find_element_by_xpath("//input[@placeholder='请输入密码']")
    username_input.send_keys(number)
    password_input.send_keys(password)

    # 找到验证码图片的元素，截屏，识别并填充
    driver.find_element_by_xpath("//img[@class='el-icon-codestr']").screenshot("captcha.png")
    captcha_text = captcha2text('captcha.png')
    captcha_input = driver.find_element_by_xpath("//input[@placeholder='请输入验证码']")
    captcha_input.send_keys(captcha_text)

    # 提交表单
    captcha_input.send_keys(Keys.RETURN)
    # 登陆成功等一等
    time.sleep(2)

    # 获取当前网址，判断是否登录成功
    current_url = driver.current_url
    if current_url == "http://classroom.csu.edu.cn/#/StudentHome":
        print('登陆成功')
    else:
        driver.quit()  # 关闭浏览器
        return 42
    # 打开原始数据界面
    driver.get('http://classroom.csu.edu.cn/#/StudentOriginalData')

    # 找到更改日期元素
    click_time_element = driver.find_element_by_xpath("//input[@placeholder='开始日期']")
    click_time_element.click()

    # 找到所有 <button> 元素
    buttons = driver.find_elements_by_tag_name("button")

    # 筛选出“最近三个月”按钮并点击
    three_months_buttons = [button for button in buttons if button.text == "最近三个月"]
    three_months_buttons[0].click()

    # 筛选出“查询”按钮并点击
    search_buttons = [button for button in buttons if button.text == "查询"]
    search_buttons[0].click()

    # 找到页码输入框
    input_element = driver.find_element_by_xpath("//input[@min='1']")
    # 获取分页数量
    max_value = int(input_element.get_attribute("max"))

    # 创建一个空列表来存储 src 属性
    urls = []
    # 循环输入值
    for value in range(1, max_value+1):
        # 找到输入框元素，再次寻找元素的原因是：打开新的分页后，元素ID发生变化，不能用原来的ID操作新页面的元素
        input_element = driver.find_element_by_xpath("//input[@min='1']")
        input_element.clear() # 清除页码
        input_element.send_keys(str(value))
        input_element.send_keys(Keys.RETURN)
        time.sleep(3) #等待分页加载完全
        
        # 找到所有具有 class="table-img-div" 的元素（元素内含图片链接）
        elements = driver.find_elements_by_css_selector(".table-img-div")

        # 遍历元素并提取 src 属性
        for element in elements:
            src = element.find_element_by_tag_name("img").get_attribute("src")
            # 避免存错，避免重复
            if (src.startswith("http://") or src.startswith("https://")) and src not in urls:
                urls.append(src)

    # 将提取的URL写入文件
    urls_name = str(number)+".txt"
    with open(urls_name, 'w') as file:
        for url in urls:
            file.write(url + '\n')

    # 关闭浏览器
    driver.quit()