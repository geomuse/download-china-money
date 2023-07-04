'''
需求:按照机构名称从中国货币网批量下载评级和财务报告，并按照省份、城市、机构名称分别建立文件夹，将该机构的评级和财务报告放入文件夹。
债券信息披露-评级报告下载最新评级报告
网址:https://www.chinamoney.com.cn/chinese/pjgg/
债券信息披露-财务报告下载2022年年度报告/审计报告、2023年一季度财务报表
网址:https://www.chinamoney.com.cn/chinese/cqcwbglm/
'''

'''
def get_and_download_pdf_flie(i):
   url='https://www.chinamoney.com.cn/ags/ms/cm-u-notice-issue/financeRepo?year=&type=&orgName=&pageSize=30&pageNo=1&inextp=3%2C5&limit=1&'
   r=requests.get(url)
   r.encoding=r.apparent_encoding#防止网页乱码
   json=r.json()
    #存储数据
   records = json['records']
   items=[]
   for d in records:
       title = d['title']
       releaseDate =d['releaseDate']
       draftPath = d['draftPath']
       child_url = 'https://www.chinamoney.com.cn/'+draftPath
       item=[title, releaseDate,child_url]
       items.append(item)
       filename =f'{title}.PDF'
       saving_path=r'C:\\系统默认\\公告'#设置存储年报的文件夹
       filepath = saving_path+'\\'+filename
       child_r = requests.get(child_url)
    #下载PDF
       with open(filepath,'wb') as f:
           f.write(child_r.content)
    #制作索引
    return items

import pandas as pd
df=pd.DataFrame()
for pageNum in range(1,3):
    items=get_and_download_pdf_flie(pageNum)
    df_=pd.DataFrame(items,columns=['标题','发文日期','网址'])
    df=pd.concat([df,df_],ignore_index=True)
df.to_excel(r'C:\系统默认\金融学\公告索引.xlsx')
'''

'''
def read_firm():
    df = pd.read_excel('index_firm.xlsx')
    print(df.head())

def get_and_download_pdf(firm_name):
    
    firm_name = quote(firm_name)
    # url = f'https://example.com/{firm_name}'
    url = f'https://www.chinamoney.com.cn/chinese/zqcwbgcwgd/?tabid=0&inextp=3,5&org={firm_name}&year=&repoType='
    print(url)
    respone = requests.get(url)
    print(respone.status_code)
'''

'''
from urllib.parse import quote
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.service import Service

# 设置Chrome浏览器驱动路径
driver_path = '/home/geo/Downloads/Trade/download-bot/geckodriver-v0.33.0-linux64/'

def read_firm():
    df = pd.read_excel('index_firm.xlsx')
    print(df.head())

def get_and_download_pdf(firm_name):
    url = f'https://www.chinamoney.com.cn/chinese/zqcwbgcwgd/?tabid=0&inextp=3,5&org={firm_name}&year=&repoType='
    service = Service(executable_path=driver_path)
    options = webdriver.FirefoxOptions()
    wait_time = 5
    with webdriver.Firefox(service=service, options=options) as browser :
        browser.get(url)
        wait = WebDriverWait(browser, wait_time)
        browser.close()
'''

'''
def read_firm():
    df = pd.read_excel('index_firm.xlsx')
    print(df.head())

def get_and_download_pdf(firm_name):
    # url = f'https://example.com/{firm_name}'
    url = f'https://www.chinamoney.com.cn/chinese/zqcwbgcwgd/?tabid=0&inextp=3,5&org={firm_name}&year=&repoType='
    print(url)
    df = requests.get(url)
    if df.status_code :
        soup = BeautifulSoup(df.text, 'html.parser')
        txt = soup.find_all('a')
        print(txt)
'''

'''
def get_and_download_pdf(firm_name):
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
    
    
    links = browser.find_elements(By.ID, 'bond-finance-content-list')
    links = links[0]
    # print(links.text)
    soup = BeautifulSoup(links,'html.parser')
    print(soup)
        
        # div = link.find_elements(By.TAG_NAME, 'p')
        # div = link.find_elements(By.CLASS_NAME, 'san-grid-m')
        # print(div.text)

    browser.close()    
'''

'''
import pandas as pd
def read_firm():
    df = pd.read_excel('index_firm.xlsx')
    return df

p = read_firm()
print(p)
'''

'''
path = '安徽省/马鞍山市/江东控股集团有限责任公司'
with open(f'{path}.log','w') as f :
    f.write("respone.content.")
'''

'''
import pandas as pd
target_text = pd.read_csv('key_words.txt',header=None)
# print(target_text)

for target in target_text[0] :
    print(target)
    print(type(target))
'''

'''
import requests

def adjust_url(url):
    url = url.replace("'",'https://www.chinamoney.com.cn/dqs/cm-s-notice-query/')
    return url

url = "'fileDownLoad.do?mode=open&contentId=2616628&priority=0"
url = adjust_url(url)
url = 'https://www.chinamoney.com.cn/dqs/cm-s-notice-query/fileDownLoad.do?mode=open&contentId=2617842&priority=0'
response = requests.get(url)

with open('text.pdf','wb') as f :
    f.write(response.content)
'''

'''
import requests

url = 'https://www.chinamoney.com.cn/chinese/cwbg/20230428/2617842.html#cp=cwbg'

headers = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/80.0.3987.149 Safari/537.36",
    # "Referer": "https://www.example.com"
}

print(requests.get(url , headers=headers).status_code)

session = requests.Session()
response = session.get(url)
'''
ips = [0.1,1,13,124,115,'failed',16,77,87]
ips = [[1,1],[1,'failed'],[1,2],[1,8]]
for n , ip in enumerate(ips):
    # print(n,ip)
    try : 
        ip[1] += 1
    except :
        ip = ips[n+1]
        ip[1] += 1
        ips.pop(n+1)
    finally :
        print(ip)
    # except Exception as e :
    #     ip[1] = ips[n+1]
    #     ip[1] = ip[1]+1
    #     ips.pop(n+1)
    # finally :
    #     print(ip[1])
