import os
import requests

def download_urls(number):
    urls_name = str(number)+".txt"
    if os.path.exists(urls_name):
        # 创建一个以学号命名 的目录，如果它不存在的话
        download_dir = str(number)
        os.makedirs(download_dir, exist_ok=True)

        # 读取文本文件中的链接
        with open(urls_name, 'r') as file:
            urls = file.readlines()

        # 遍历链接并下载图片
        for url in urls:
            url = url.strip()  # 移除换行符

            response = requests.get(url)

            if response.status_code == 200:
                # 从 URL 中提取文件名
                file_name = os.path.join(download_dir, url.split('/')[-1])

                # 写入图片文件
                with open(file_name, 'wb') as img_file:
                    img_file.write(response.content)
                print(f'Downloaded: {file_name}')
            else:
                print(f'Failed to download: {url}')
        print("下载完成")
    else:
        print("urls.txt不存在")