"""
URL取得エリア
"""
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.chrome.options import Options
import os
import time
from dotenv import load_dotenv
load_dotenv()
import ast

os.environ["PROJECT_ROOT"] = '/Users/nishitsujiyouhei/Documents/RPA/input_and_study/liny-manual-chatbot'
os.environ["CHROME_DRIVER_PATH"] = '/Users/nishitsujiyouhei/Documents/RPA/input_and_study/liny-manual-chatbot/chromedriver'
os.chdir(os.getenv('PROJECT_ROOT'))
import re
import csv

import os
import csv
def save(text,path):
    with open(path, "w") as file:
        file.write(text)
def read(path):
    with open(path, "r") as file:
        return file.read()
def is_extst(path):
    return os.path.isfile(path)
def add(text, path):
    with open(path, "a") as file:
        file.write(text+'\n')
def add_csv(data, path,encoding='utf-8'):
    with open(path, mode='a', newline='',encoding=encoding) as log_file:
            writer = csv.writer(log_file)
            writer.writerow(data)
def is_contain(text, path):
    if not is_extst(path):
        return False
    with open(path, "r") as file:
        return text in file.read()

def _get_headline_and_text(html):
    pattern = re.compile(r'<(h[1-4]|p|table)[^>]*>(.*?)<\/\1>|<(img)[^>](.*?)\/>', re.DOTALL)
    # 単一タグのものも消す
    matches = pattern.findall(html)
    post = "\n".join([item[0]+':'+item[1] for item in matches])
    post = re.sub(r'^.*?h1:', 'h1:', post, flags=re.DOTALL)
    post = re.sub(r'<.*?>', '', post)
    post = post.replace('p:', '')
    post = post.replace('h1:', '大見出し：')
    post = post.replace('h2:', '中見出し：')
    post = post.replace('h3:', '小見出し：')
    post = post.replace('h4:', '小見出し：')
    post = post.replace('img:', '画像：')
    post = post.replace('\t', '')
    post =  re.sub(r'\n{2,}', '\n', post)
    return post.strip()

class Driver():
    def __init__(self):
        options = Options()
        # options.add_argument('--headless')
        self.dv = webdriver.Chrome(options=options,executable_path=os.environ["CHROME_DRIVER_PATH"])
    def getDriver(self):
        return self.dv



"""
ページの概要取得エリア
"""
# selenium = Driver()
# dr = selenium.getDriver()
# manual_url = 'https://www.make.com/en/help'
# dr.get(manual_url)
# # 親ページのURLを取得する
# xml_parent_all_el = '/html/body/div[3]/div/div/aside/ul[2]/li'
# parents_el=dr.find_elements(By.XPATH, xml_parent_all_el)
#
# # xml_parent_all_el = '/html/body/div[3]/div/div/aside/ul[2]/li[*]/ul/li[*]/a'
# todo:3階層目も取得する
# urls = []
# for parent_el in parents_el:
#     print(parent_el.text)
#     if len(parent_el.find_elements(By.XPATH, "ul"))==0:
#         continue
#     children = parent_el.find_elements(By.XPATH, "ul/li[*]/a")
#     for child in children:
#         url = child.get_attribute("href")
#         title = child.get_attribute("text")
#         urls.append([url,parent_el.text+'/'+title])
# print(urls)
# with open('src/nocode/data.csv', mode='w', newline='') as file:
#     writer = csv.writer(file)
#     writer.writerows(urls)


import pandas as pd

dir_path = "storage/make/help"
df = pd.read_csv('src/nocode/data.csv',header=None)
urls = df.iloc[1:, :].values.tolist()
selenium = Driver()
dr = selenium.getDriver()
for url,title in urls:
    print(title)
    file_path = f'{dir_path}/{title}.txt'
    # if is_extst(file_path):
    #     continue
    dr.get(url)
    html = dr.page_source
    url = dr.current_url
    post = _get_headline_and_text(html)
    sub_title = title.split('/',maxsplit=1)[1]
    os.makedirs(f'{dir_path}/{title.split("/")[0]}', exist_ok=True)
    save(f'url:{url}\ntitle:{title}\n'+post, file_path)

# # 新しいタブで開く
# single_page_urls = [for el in single_pages]
#     # 繰り返しでURLを取得する
# # ネストページのURLを取得する
#     # 親ページを全部クリックして開く
#     xml_parent_el = '//*[@id="sidebarForShow"]/div/div[1]/div/ul/li[*]/a'
#     # 子ページのURLを取得する
    # xml_child_el = '//*[@id="sidebarForShow"]/div/div[*]/div/ul/li[*]/div/div/ul/li[*]'
dr.quit()
"""
記事情報保存エリア
"""



