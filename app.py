#请求数据
import requests 
from bs4 import BeautifulSoup
import pandas as pd
import time
import os 
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.service import Service
from loguru import logger
logger.add("log/error.log", level="ERROR", rotation="10 MB", format="{time:YYYY-MM-DD HH:mm:ss.SSS} | {message}")

# 设置Chrome浏览器驱动路径
driver_path = '/home/geo/Downloads/Trade/download-bot/geckodriver-v0.33.0-linux64/'

class download_chinamoney:
    def __init__(self) -> None:
        pass

    def read_firm(self):
        df = pd.read_excel('index_firm.xlsx')
        return df

    def get_download_link_and_text(self,soup,path):
        # soup = BeautifulSoup(txt,'html.parser')
        title , link = soup.text , soup['href']
        self.download_link(link,path,title)

    def get_download_link_and_text_for_a_tags_1(self,txt,path):
        soup = BeautifulSoup(txt,'html.parser')
        txt = soup.select('[class~=san-grid-m]')
        for t in txt :
            sub_soup = BeautifulSoup(t.prettify(),'html.parser')
            a_tags = sub_soup.select('a')
            try :
                link = a_tags[1]['href']
                print(f'{a_tags[0].text}')
                fname = a_tags[0].text
                self.download_link(link,path,fname)
            except Exception as e:
                print('link not work maybe didnt have any download link.')
                logger.error(f'{a_tags} : link not work maybe didnt have any download link. \ncode status > {str(e)}')
    
    def replace_link(self,link):
        # https://www.chinamoney.com.cn/chinese/cwbg/20230428/2617842.html#cp=cwbg
        # /chinese/cwbg/20230428/2617842.html#cp=cwbg
        link = link.replace('/chinese','https://www.chinamoney.com.cn/chinese')
        return link

    def replace_link_for_a_tags_1(self,link):
        link = link.replace('/dqs','https://www.chinamoney.com.cn/dqs').replace('amp;priority=0&amp','priority=0&mode=save')
        return link
    
    def adjust_url(self,url):
        url = url.replace("'",'https://www.chinamoney.com.cn/dqs/cm-s-notice-query/')
        return url

    def download_link(self,link,path,fname):
        link = self.replace_link(link)
        response = requests.get(link)
        if response.status_code == 200 :
            url = self.get_sub_web_content(response)
            res = requests.get(url)
            if res.status_code == 200 :
                with open(f'{path}/{fname}.pdf','wb') as f :
                    f.write(res.content)
                print(f'{url} : {fname} , please check > completed.')
            else :
                logger.error(f'{link} not work please check it.')
        else : 
            logger.error(f'{link} not work please check it.')

    def get_sub_web_content(self,response):
        soup = BeautifulSoup(response.text,'html.parser')
        df = soup.select('img')
        for link in df :
            link = link.find_previous('a')
            link = link['onclick']
            start = link.find("'fileDownLoad")
            end = link.rfind("'")
            link = link[start:end]
            url = self.adjust_url(link)
            
        return url
    
    def generate_file_path_and_maka_dir(self):
        df = self.read_firm()
        provinces = []
        for province , city , firm in zip(df['省份'] , df['城市'] ,df['机构名称']) :
            path = f'data/{province}/{city}/{firm}'
            provinces.append(path)
            os.makedirs(path, exist_ok=True)

        return provinces , df['机构名称']
    
    def text_filter(self,soup):
        # target_text = ['2023年一季度财务报表','2022年年度报告','2022年度报告','2022年年度报告(更正)','2022年度报告(更正)','2023年一季度财务报表的更正公告及更正后文件']
        target_text = pd.read_csv('key_words.txt',header=None)
        target_links = []
        for target in target_text[0] : 
            df = soup.find_all(string=lambda text: target in text)
            for element in df:
                link = element.find_previous('a')
                if link:
                    target_links.append(link)
        return target_links
    
    def get_and_download_pdf(self):
        paths , firm_name_list = self.generate_file_path_and_maka_dir()
        for path , firm_name in zip(paths,firm_name_list) :
            url = f'https://www.chinamoney.com.cn/chinese/zqcwbgcwgd/?tabid=0&inextp=3,5&org={firm_name}&year=&repoType='
            print(f'爬虫截取文章 : {url}')
            service = Service(executable_path=driver_path)
            options = webdriver.FirefoxOptions()
            options.add_argument("--headless")  # 启用Headless模式
            options.add_argument("--disable-gpu")  # 禁用GPU加速
            browser = webdriver.Firefox(service=service, options=options)
            browser.get(url)
            wait = WebDriverWait(browser, 3)
            element = wait.until(EC.presence_of_element_located((By.CLASS_NAME, 'records-total')))
            
            # 在页面上找到了目标元素
            print(f'共 {element.text} 条记录.')

            soup = BeautifulSoup(browser.page_source,'html.parser')
            
            ul = soup.find(id='bond-finance-content-list')
            ul = self.text_filter(ul)
            for div in ul :                
                self.get_download_link_and_text(div,path)
            print(f'{firm_name} done.')
            time.sleep(20)
            browser.close()    

if __name__ == '__main__':
    eng = download_chinamoney()
    eng.get_and_download_pdf()
    