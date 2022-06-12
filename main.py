import requests
import datetime
import schedule
import time
from bs4 import BeautifulSoup
def job(): 
    # 爬取主页并获得各组页面网址
    url = 'https://qldoc.sylu.edu.cn/'
    header = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/80.0.3987.149 Safari/537.36'
    }
    r = requests.get(url,headers=header,verify=False)
    r.encoding = 'utf-8'
    soup = BeautifulSoup(r.text,'html.parser')
    img_url = soup.find('div',class_='manual-list').find_all('a') 
    all_img_url = set()
    for a in img_url:
        all_img_url.add(a['href']) 
    r.close()    

    # 爬取各组分页面并获得下载网址
    all_download_url = []
    for i in all_img_url:
        url = i+'?output=markdown'
        all_download_url.append(url)

    # 在根目录下下载文档并按照时间进行命名
    for download_url in all_download_url:
        num = download_url.rfind('/')
        num1 = download_url.rfind('?')
        name1 = download_url[num+1:num1-1]
        download = requests.get(download_url,headers=header,verify=False)
        download.encoding = 'utf-8'
        location_time = str(datetime.date.today())
        name = location_time+'_'+name1+'.zip'
        with open(name,mode='wb') as f:
           f.write(r.content)
    download.close()
schedule.every().day.at("12:00").do(job)
while True:
    schedule.run_pending()
    time.sleep(1)
