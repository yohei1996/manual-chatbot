################################
# create_vedcors_from_posts.py #
################################
"""
URL取得エリア
"""
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.chrome.options import Options
import os
import time
import ast

os.environ["CHROME_DRIVER_PATH"] = '/Users/nishitsujiyouhei/Documents/RPA/input_and_study/liny-manual-chatbot/chromedriver'
import re
import csv

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

def fetch_post_data(dr:webdriver.Chrome,el_xml:str,posts_path:str):
    el = dr.find_element(By.XPATH,el_xml)
    while True:
        try:
            el.click()
            break
        except Exception as e:
            time.sleep(0.5)
            print(e)
            el = dr.find_element(By.XPATH,el_xml)
    html = dr.page_source
    url = dr.current_url
    page_title = dr.title.replace("/", r"\/")
    post = _get_headline_and_text(html)
    file_path = f'{posts_path}/{page_title}.txt'
    if is_extst(file_path):
        return
    save(url+'\n'+post,file_path)
    add_row([url,page_title],f'./url一覧.csv')

class Driver():
    def __init__(self):
        options = Options()
        # options.add_argument('--headless')
        self.dv = webdriver.Chrome(options=options,executable_path=os.environ["CHROME_DRIVER_PATH"])
    def getDriver(self):
        return self.dv


selenium = Driver()
dr = selenium.getDriver()
manual_url = 'https://manual.liny.jp/new'
dr.get(manual_url)

"""
ページの概要取得エリア
"""
# 親ページのURLを取得する
# xml_parent_all_el = '//*[@id="sidebarForShow"]/div/div[1]/div/ul/li[*]/a'
# parent_el_list=dr.find_elements(By.XPATH,xml_parent_all_el)

# # ボタンがあるかどうか
# single_pages_index = []
# nest_page_index = []
# for i,el in enumerate(parent_el_list):
#     toggle_button = el.find_elements(By.XPATH,'span')

#     # 
#     if toggle_button:
#         el.click()
#         els_childs = el.find_elements(By.XPATH,'../div/div/ul/li[*]/a')
#         for j,el_child in enumerate(els_childs):
#             print(el_child.text)
#             if el_child.text == '':
#                 time.sleep(0.5)
#             nest_page_index.append((i,j,el.text,el_child.text))
#     else:
#         single_pages_index.append((i,el.text))

# save(str(nest_page_index),'./nest_page_index.txt')
# save(str(single_pages_index),'./single_pages_index.txt')

nest_page_index = ast.literal_eval(read('./nest_page_index.txt'))
single_pages_index = ast.literal_eval(read('./single_pages_index.txt'))

posts_path = './posts'
os.makedirs(posts_path, exist_ok=True)



"""
# シングルページのURLを取得する
for i,title in single_pages_index:
    el_xml = f'//*[@id="sidebarForShow"]/div/div[1]/div/ul/li[{i+1}]/a'
    dr.get(manual_url)
    fetch_post_data(dr,el_xml,posts_path)
"""

for i,j,_,__ in nest_page_index:
    dr.get(manual_url)
    el_xml = f'//*[@id="sidebarForShow"]/div/div[1]/div/ul/li[{i+1}]'
    # ネストページのURLを取得する
    while True:
        try:
            el = dr.find_element(By.XPATH,el_xml)
            break
        except Exception as e:
            time.sleep(0.5)
            print(e)
            el = dr.find_element(By.XPATH,el_xml)
    el.find_element(By.XPATH,'./a').click()
    parent_name = el.text
    el_xml = f'//*[@id="sidebarForShow"]/div/div[1]/div/ul/li[{i+1}]/div/div/ul/li[{j+1}]'
    fetch_post_data(dr,el_xml,posts_path)
    # add_row([parent_name,''],f'./url一覧.csv')

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