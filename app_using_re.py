#请求数据
import requests 
from bs4 import BeautifulSoup
import pandas as pd
import time
import os , pickle , re
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.common.exceptions import WebDriverException , TimeoutException
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.service import Service
from loguru import logger
logger.add("log/error.log", level="ERROR", rotation="10 MB", format="{time:YYYY-MM-DD HH:mm:ss.SSS} | {message}")

# 设置Chrome浏览器驱动路径
driver_path = '/home/geo/Downloads/development/download-bot/geckodriver-v0.33.0-linux64/'

class download_chinamoney:
    r'''download_chinamoney.

    含以下反爬虫技术:
        - 请求限制.
        - 动态生成页面.
        - 内容隐藏检测.
    '''
    # 定义类属性
    df = pd.read_excel('ref/index_firm.xlsx')
    key_words = pd.read_csv('ref/key_words_for_re.txt',header=None)
    fname_unique = []

    def __init__(self) -> None:
        ...

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

    def requests_get(self,link):
        return requests.get(link)

    def download_link(self,link,path,fname):
        link = self.replace_link(link)
        response = self.requests_get(link)
        # print(f'link 是否成功?')
        if response.status_code == 200 :
            url = self.get_sub_web_content(response)
            res = self.requests_get(url)
            if fname not in self.fname_unique :
                if res.status_code == 200 :
                    with open(f'{path}/{fname}.pdf','wb') as f :
                        f.write(res.content)
                    print(f'{url} : {fname} , please check > completed.')
                    self.fname_unique.append(fname)
                else :
                    logger.error(f'{url} not work please check it.')
            else : 
                print(f'{fname} repeat.')
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
        df = self.df
        provinces = []
        for province , city , firm in zip(df['省份'] , df['城市'] ,df['机构名称']) :
            path = f'data/{province}/{city}/{firm}'
            provinces.append(path)
            os.makedirs(path, exist_ok=True)
        return provinces , df['机构名称']
    
    def __soup_filter_links(self,item):
        soup = BeautifulSoup(item.prettify(),'html.parser')
        a = soup.select('a')
        for link in a :
            text = link.text 
            if text : 
                link = link.find_previous('a')
                if link :
                    return link
    
    def text_filter(self,soup):
        pattern = self.generate_pattern()
        links = []
        for item in soup :
            if re.search(pattern, str(item)):
                link = self.__soup_filter_links(item)    
                links.append(link)
        return links

    def generate_pattern(self):
        key_words = self.key_words
        pattern = "|".join(key_words[0])
        return re.compile(fr"{pattern}",re.IGNORECASE)
    
    def init_browser(self):
        service = Service(executable_path=driver_path)
        options = webdriver.FirefoxOptions()
        options.add_argument("--headless")  # 启用Headless模式 , 则不跳出模拟器运行.
        options.add_argument("--disable-gpu")  # 禁用GPU加速
        return service , options
    
    def get_and_download_pdf(self,url,page_id,path):
        service , options = self.init_browser()
        browser = webdriver.Firefox(service=service, options=options)
        browser.get(url)
        wait = WebDriverWait(browser, 3)
        element = wait.until(EC.presence_of_element_located((By.CLASS_NAME, 'records-total')))
        
        # 在页面上找到了目标元素
        print(f'共 {element.text} 条记录.')

        soup = BeautifulSoup(browser.page_source,'html.parser')
        
        ul = soup.find(id=page_id)
        ul = self.text_filter(ul)
        # print(f'ul 有过滤清楚吗? {ul}')
        for div in ul :                
            self.get_download_link_and_text(div,path)
            time.sleep(10)  
        browser.close()

    def get_and_download_pdf_only_financial_statements(self):
        paths , firm_name_list = self.generate_file_path_and_maka_dir()
        for path , firm_name in zip(paths,firm_name_list) :
            url = f'https://www.chinamoney.com.cn/chinese/zqcwbgcwgd/?tabid=0&inextp=3,5&org={firm_name}&year=&repoType='
            print(f'财务报告 : 爬虫截取文章 : {url}')
            self.get_and_download_pdf(url,'bond-finance-content-list',path)
            print(f'{firm_name} 财务报告 done.')
            time.sleep(20)

    def get_and_download_pdf_only_rating_reports(self):
        paths , firm_name_list = self.generate_file_path_and_maka_dir()
        for path , firm_name in zip(paths,firm_name_list) :
            url = f'https://www.chinamoney.com.cn/chinese/zxpjbgh/?bondSrno=&tabtabNum=1&tabid=0&bnc={firm_name}&ro=&sdt=&edt='
            print(f'评级报告 : 爬虫截取文章 : {url}')
            self.get_and_download_pdf(url,'page-disclosure-bond-rating-report-list',path)
            print(f'{firm_name} 评级报告 done.')
            time.sleep(20)

    def get_and_download_pdf_for_all(self):
        paths , firm_name_list = self.generate_file_path_and_maka_dir()
        for path , firm_name in zip(paths,firm_name_list) :
            # 针对财务报告.
            url = f'https://www.chinamoney.com.cn/chinese/zqcwbgcwgd/?tabid=0&inextp=3,5&org={firm_name}&year=&repoType='
            print(f'财务报告 > 爬虫截取文章 : {url}')
            self.get_and_download_pdf(url,'bond-finance-content-list',path)
            print(f'{firm_name} 财务报告 done.')
            time.sleep(20)
            # 针对评级报告.
            url = f'https://www.chinamoney.com.cn/chinese/zxpjbgh/?bondSrno=&tabtabNum=1&tabid=0&bnc={firm_name}&ro=&sdt=&edt='
            print(f'评级报告 > 爬虫截取文章 : {url}')
            self.get_and_download_pdf(url,'page-disclosure-bond-rating-report-list',path)
            print(f'{firm_name} 评级报告 done.')
            time.sleep(20)   

class classic_download_chinamoney(download_chinamoney):
    r'''classic_download_chinamoney.
    
    https://www.chinamoney.com.cn/robots.txt > not work.

    所以我不用没有办法判断爬取它的标准和协议的规范在哪里.

    除了父类的反爬虫以外含以下反爬虫技术:
        - User-Agent检测.
    '''
    def __init__(self) -> None:
        super(download_chinamoney,self).__init__()
        print('loading classic.')
        # print(self.df.head() , self.key_words[0:3])

    def init_browser(self):
        service , options = super().init_browser()
        options.add_argument("user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/90.0.4430.212 Safari/537.36")
        return service , options

    def requests_get(self, link):
        headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
        }
        return requests.get(link, headers=headers)

class luxury_download_chinamoney(classic_download_chinamoney):
    r'''anti_web_scrap_download_chinamoney.

    除了父类的反爬虫以外含以下反爬虫技术:
        - IP封禁.
    '''
    proxy_list = pd.read_csv('ref/socks5_proxies.txt',header=None)

    def __init__(self) -> None:
        super(classic_download_chinamoney,self).__init__()
        print('loading luxury.')

    def load_support_proxy(self):
        with open('anti-component/support_proxy.pkl', 'rb') as file:
            loaded_list = pickle.load(file)        
        print(loaded_list[0:3])
        return loaded_list
    
    def read_support_proxy(self):
        proxy_list = self.proxy_list
        proxy_list[0] = proxy_list[0].apply(lambda text : str(text).split(":"))
        proxy = []
        for _ in range(len(proxy_list)):
            # print(proxy_list[0][_])
            ip , port = proxy_list[0][_]
            port = int(port)
            proxy.append([ip,port])
        return proxy

    def get_and_download_pdf(self,url,page_id,path,proxys):
        service , options = self.init_browser() 
        
        for item , proxy in enumerate(proxys) : 
            print(f'im start to web scraping the website with {proxy[0]}.')
            try :
                options.add_argument(f'--proxy-server=socks5://{proxy[0]}:{proxy[1]}')
                browser = webdriver.Firefox(service=service, options=options)
                browser.get(url)
                wait = WebDriverWait(browser, 7)
                element = wait.until(EC.presence_of_element_located((By.CLASS_NAME, 'records-total')))
                
                # 在页面上找到了目标元素.
                print(f'共 {element.text} 条记录.')

                soup = BeautifulSoup(browser.page_source,'html.parser')
                
                ul = soup.find(id=page_id)
                ul = self.text_filter(ul)
                # print(f'ul 有过滤清楚吗? {ul}')
                for div in ul :                
                    self.get_download_link_and_text(div,path)
                    time.sleep(10)  

                # 如果成功执行爬取操作,跳出循环.
                break

            except TimeoutException as e:
                print('Proxy IP {} failed. TimeoutException.'.format(proxy))
                print('failed url {url}.')
                # 切换到下一个代理IP.
                service , options = self.init_browser()
                proxy = proxys[item+1]
                proxys.pop(item+1)
                options.add_argument(f'--proxy-server=socks5://{proxy[0]}:{proxy[1]}')
                print(f'previous ip failed bcs timeout , im start to web scraping the website with {proxy[0]}.')

            except WebDriverException as e:
                # 处理代理IP失败的情况.
                print('Proxy IP {} failed. Trying another IP.'.format(proxy))
                print('failed url {url}.')
                # 切换到下一个代理IP.
                service , options = self.init_browser()
                proxy = proxys[item+1]
                proxys.pop(item+1)
                options.add_argument(f'--proxy-server=socks5://{proxy[0]}:{proxy[1]}')
                print(f'previous ip failed bcs timeout , im start to web scraping the website with {proxy[0]}.')
            finally :
                # print('browser close.') 
                browser.close()

    def get_and_download_pdf_only_financial_statements(self):
        proxys = self.read_support_proxy()
        paths , firm_name_list = self.generate_file_path_and_maka_dir()
        for path , firm_name in zip(paths,firm_name_list) :
            url = f'https://www.chinamoney.com.cn/chinese/zqcwbgcwgd/?tabid=0&inextp=3,5&org={firm_name}&year=&repoType='
            print(f'财务报告 : 爬虫截取文章 : {url}')
            self.get_and_download_pdf(url,'bond-finance-content-list',path,proxys)
            print(f'{firm_name} 财务报告 done.')
            time.sleep(20)

    def get_and_download_pdf_only_rating_reports(self):
        proxys = self.read_support_proxy()
        paths , firm_name_list = self.generate_file_path_and_maka_dir()
        for path , firm_name in zip(paths,firm_name_list) :
            url = f'https://www.chinamoney.com.cn/chinese/zxpjbgh/?bondSrno=&tabtabNum=1&tabid=0&bnc={firm_name}&ro=&sdt=&edt='
            print(f'评级报告 : 爬虫截取文章 : {url}')
            self.get_and_download_pdf(url,'page-disclosure-bond-rating-report-list',path,proxys)
            print(f'{firm_name} 评级报告 done.')
            time.sleep(20)

    def get_and_download_pdf_for_all(self):
        proxys = self.read_support_proxy()
        paths , firm_name_list = self.generate_file_path_and_maka_dir()
        for path , firm_name in zip(paths,firm_name_list) :
            # 针对财务报告.
            url = f'https://www.chinamoney.com.cn/chinese/zqcwbgcwgd/?tabid=0&inextp=3,5&org={firm_name}&year=&repoType='
            print(f'财务报告 > 爬虫截取文章 : {url}')
            self.get_and_download_pdf(url,'bond-finance-content-list',path,proxys)
            print(f'{firm_name} 财务报告 done.')
            time.sleep(20)
            # 针对评级报告.
            url = f'https://www.chinamoney.com.cn/chinese/zxpjbgh/?bondSrno=&tabtabNum=1&tabid=0&bnc={firm_name}&ro=&sdt=&edt='
            print(f'评级报告 > 爬虫截取文章 : {url}')
            self.get_and_download_pdf(url,'page-disclosure-bond-rating-report-list',path,proxys)
            print(f'{firm_name} 评级报告 done.')
            time.sleep(20)    
    
if __name__ == '__main__':
    # eng = download_chinamoney()
    # 只针对财务报表.
    # print(eng.read_firm())
    # eng.get_and_download_pdf_only_financial_statements()
    # 只针对评价报告.
    # eng.get_and_download_pdf_only_rating_reports()
    # 针对财务报表和评价报告.
    # eng.get_and_download_pdf_for_all()
    
    # 典型的反爬虫技术.
    # classic_eng = anti_web_scrap_download_chinamoney()
    # classic_eng.get_and_download_pdf_only_rating_reports()
    
    # 标准的反爬虫技术.
    luxury_eng = luxury_download_chinamoney()
    # 只针对财务报表.
    # luxury_eng.get_and_download_pdf_only_financial_statements()
    # 只针对评价报告.
    # luxury_eng.read_support_proxy()
    luxury_eng.get_and_download_pdf_only_rating_reports()
    # 针对财务报表和评价报告.
    # luxury_eng.get_and_download_pdf_for_all()