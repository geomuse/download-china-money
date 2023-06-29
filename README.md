下周才爬虫针对评级

# 使用说明书:
0. 前提说明
  - 在terminal执行 `export OPENSSL_CONF=openssl.cnf` 更新ssl协议.因为ssl协议旧版不能用了.
  - 下载内容是基于`index_firm.xlsx` 和 `key_words.txt`进行调配.
    - `index_firm.xlsx` 要爬取的公司清单,包含公司名字 , 省份 , 城市
    - `key_words.txt` 如果要爬去`2023年年度报告`要提供相关文字 <b>有些公司年报会写2023年度报告所以如果你不加入2023年度报告就会没有办法截取这份报告</b>.

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

4. 执行后会在terminal显示以下结果

```
爬虫截取文章 : https://www.chinamoney.com.cn/chinese/zqcwbgcwgd/?tabid=0&inextp=3,5&org=江东控股集团有限责任公司&year=&repoType= # 为爬虫主要目标网站
共 49 条记录. # 为文章第一页有49条财报内容.
https://www.chinamoney.com.cn/dqs/cm-s-notice-query/fileDownLoad.do?mode=open&contentId=2617842&priority=0 please check when the download is complete. # 自动下载的连接
https://www.chinamoney.com.cn/dqs/cm-s-notice-query/fileDownLoad.do?mode=open&contentId=2616628&priority=0 please check when the download is complete. # 自动下载的连接
江东控股集团有限责任公司 done. # 下载成功
```

如果后续有特殊情况的下载内容目前不支持 , 可以到 `log/error.log` 查看错误内容手动下载并且告诉我 , 我会主动再次优化.

# 目前程式的缺陷: 

1. 只针对文字过滤的财报进行下载,并没有做到自动侦测真正想要的.
2. browser因为是firefox请下载相容版本已使得模拟器可以启动,并没有考虑个版本个型号问题.
3. 只针对大部分情况适用,如果存在少部分情况需要手动下载,大部分情况是基于文字过滤的.
4. server可能因为你过多进行数据请求而block掉你的请求,但是经过调整已经适用于目前的爬取请求.

# 后续可以进行的优化:

1. 建立一个flask frame work > 半自动审查 > 批量下载.
2. 检测资源占用，提供使用者提醒.
3. 请求过久就转换ip.
