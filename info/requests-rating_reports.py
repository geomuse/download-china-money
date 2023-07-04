import requests

firm_name = '上海临港经济发展(集团)有限公司'
url = f'https://www.chinamoney.com.cn/chinese/zxpjbgh/?bondSrno=&tabtabNum=1&tabid=0&bnc={firm_name}&ro=&sdt=&edt='

def generate_url(firm_name):
    url = f'https://www.chinamoney.com.cn/chinese/zxpjbgh/?bondSrno=&tabtabNum=1&tabid=0&bnc={firm_name}&ro=&sdt=&edt='
    return url

p = requests.get(url)
print(p)
print(url)