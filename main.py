from login import csu_classroom_login
from download_urls import download_urls
import sys


number = 1234567890 # 此处填写学号


result = csu_classroom_login(number)
if result == 42:
    print("登录失败（密码错误或账户不存在）")
    sys.exit(0)
else:
    download_urls(number)
