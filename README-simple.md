# 使用说明书:

0. 前提说明
  - 在terminal执行 `export OPENSSL_CONF=openssl.cnf` 更新ssl协议.因为ssl协议旧版不能用了.
  - 下载内容是基于`index_firm.xlsx` 和 `key_words.txt`进行调配.
    - `index_firm.xlsx` 要爬取的公司清单,包含公司名字 , 省份 , 城市
    - `key_words.txt` 如果要爬去`2023年年度报告`要提供相关文字 <b>有些公司年报会写2023年度报告所以如果你不加入2023年度报告就会没有办法截取这份报告</b>.
    - 爬虫相关中国新闻 https://www.163.com/dy/article/H7JID2CR05199NPP.html

1. 环境配置(建议使用虚拟环境,因执行环境兼任问题)
    - 本人python版本为`3.10.6`
    - 进入虚拟环境后在terminal执行 `pip intall -r requirement.txt`
    - 如果要使用虚拟环境 参考 : https://www.freecodecamp.org/chinese/news/how-to-setup-virtual-environments-in-python/

2. 如何执行程式码
    - 进到目录里会看到app.py
    - 在cmd/terminal使用 `python3 app.py` , 因为python是解释型语言所以可以直接在terminal执行.
    - 通常不会执行成功因为要参考步骤3

3. 进去app.py修正文件,driver_path输入绝对路径
    driver_path = '/home/geo/Downloads/Trade/download-bot/geckodriver-v0.33.0-linux64/' 为你模拟器的存放路径
    本人的firefox版本为 114.0.2 (64-bit)
    请自己检查相对应的版本
    firefox如何检查版本? `bars > help > about firefox`

4. 新版的网络爬虫分别有三个版本普通版,典型版,豪华版.

    - 普通版就旧版格式,不支持代理ip和headers.
    - 典型版,不支持代理ip.
    - 豪华版,支持所有反爬虫技术.

    **但是因为使用代理ip功能而代理ip是免费且公开的没有证书,所以会有资安疑虑,主要常见的情况是`中间人攻击`.**

5. 执行后会在terminal显示以下结果

新版输出内容: 

```
评级报告 : 爬虫截取文章 : https://www.chinamoney.com.cn/chinese/zxpjbgh/?bondSrno=&tabtabNum=1&tabid=0&bnc=芜湖宜居投资(集团)有限公司&ro=&sdt=&edt= # 为爬虫主要目标网站
im start to web scraping the website with 192.111.135.18 # 使用这个代理ip
共 2 条记录. # 为文章第一页有2条财报内容.
https://www.chinamoney.com.cn/dqs/cm-s-notice-query/fileDownLoad.do?mode=open&contentId=2653918&priority=0 : 芜湖宜居投资(集团)有限公司2023年度跟踪评级报告 , please check > completed. # 自动下载的连接
https://www.chinamoney.com.cn/dqs/cm-s-notice-query/fileDownLoad.do?mode=open&contentId=2654083&priority=0 : 芜湖宜居投资(集团)有限公司2023年度跟踪评级报告 , please check > completed. # 自动下载的连接
芜湖宜居投资(集团)有限公司 评级报告 done. # 下载成功
```

旧版输出内容:

```
爬虫截取文章 : https://www.chinamoney.com.cn/chinese/zqcwbgcwgd/?tabid=0&inextp=3,5&org=江东控股集团有限责任公司&year=&repoType= # 为爬虫主要目标网站
共 49 条记录. # 为文章第一页有49条财报内容.
https://www.chinamoney.com.cn/dqs/cm-s-notice-query/fileDownLoad.do?mode=open&contentId=2617842&priority=0 : 江东控股集团有限责任公司2023年一季度财务报表 , please check > completed. # 自动下载的连接
https://www.chinamoney.com.cn/dqs/cm-s-notice-query/fileDownLoad.do?mode=open&contentId=2616628&priority=0 : 江东控股集团有限责任公司2022年年度报告 , please check > completed. # 自动下载的连接
江东控股集团有限责任公司 done. # 下载成功
```



如果后续有特殊情况的下载内容目前不支持 , 可以到 `log/error.log` 查看错误内容手动下载并且告诉我 , 我会主动再次优化.

# 目前程式的缺陷: 

1. 只针对文字过滤的财报进行下载,并没有做到自动侦测真正想要的.
2. browser因为是firefox请下载相容版本已使得模拟器可以启动,并没有考虑个版本个型号问题.
3. 只针对大部分情况适用,如果存在少部分情况需要手动下载,大部分情况是基于文字过滤的.
4. server可能因为你过多进行数据请求而block掉你的请求,但是经过调整已经适用于目前的爬取请求.
5. 可能会造成目标服务器瘫痪.

# 后续可以进行的优化:

1. 建立一个flask frame work > 半自动审查 > 批量下载.
2. 检测资源占用，提供使用者提醒.
3. 请求过久就转换ip.

# 后续进行中的反爬虫技术:

```
    [no need]验证码（CAPTCHA）：网站可能要求用户在访问前完成人机验证任务，例如输入验证码、选择特定图像等。这种技术可以有效地阻止自动化程序的访问。

    [done]IP封禁：网站可以根据用户的IP地址来限制访问。如果某个IP地址频繁发送请求或被认为是恶意爬虫，网站可以将该IP地址列入黑名单，禁止其访问网站。

    [done]请求频率限制：网站可以限制特定IP地址或用户的请求频率。例如，限制每秒或每分钟的请求次数，防止过度频繁的访问。

    [done]User-Agent检测：网站可以检查请求中的User-Agent标头，以确定请求是否来自常见的爬虫程序。如果User-Agent标头表明是爬虫程序，网站可以采取进一步的措施，如拒绝访问或返回错误信息。

    [done]动态生成页面：网站可以通过使用JavaScript等技术动态生成页面内容，而不是在初始请求中提供完整的数据。这使得爬虫难以直接从初始请求中获取所需的数据。

    [done]Cookie和Session：网站可以使用Cookie和Session来跟踪用户状态和活动。对于爬虫程序来说，管理Cookie和Session会更加困难，因为它们需要模拟和处理与网站交互的用户行为。

    [done]内容隐藏：网站可以在HTML结构中隐藏或混淆关键数据，使其难以被爬虫程序直接提取。这可能包括使用JavaScript解密、使用CSS样式隐藏数据等。

    反爬虫策略更新：网站维护人员可以持续改变网站的结构、URL格式、请求参数等，以使已有的爬虫程序失效。这迫使爬虫开发人员不断调整和更新他们的程序，以适应新的反爬虫措施。
```

网络爬虫主要框架.

``` py
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.common.exceptions import WebDriverException

# 代理IP列表.
proxy_list = ['ip1:port1', 'ip2:port2', 'ip3:port3', ...]

# 配置Chrome选项.
Firefox_options = Options()
Firefox_options.add_argument('--proxy-server={}'.format(proxy_list[0]))

# 循环尝试不同的代理IP.
for proxy in proxy_list:
    try:
        # 创建WebDriver实例.
        browser = webdriver.Firefox(options=Firefox_options)
        
        # 进行爬取操作
        # ...
        
        # 如果成功执行爬取操作，跳出循环.
        break # 这很重要,不然会一直重复换ip执行同一个爬虫.
    
    except # 建议添加时间超出机制. 
        
    except WebDriverException as e:
        # 处理代理IP失败的情况.
        print('Proxy IP {} failed. Trying another IP.'.format(proxy))
        
        # 切换到下一个代理IP.
        Firefox_options = Options()
        Firefox_options.add_argument('--proxy-server={}'.format(proxy))

# 关闭browser.
browser.close()
```