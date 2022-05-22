from lib2to3.pgen2 import driver
from time import sleep, time
from tkinter import PAGES
import requests

# from bs4 import BeautifulSoup
from webdriver_manager.chrome import ChromeDriverManager
from selenium import webdriver
from threading import Thread
from multiprocessing.dummy import Pool as ThreadPool
import random
import math


domain = 'https://zxzjtv.com'
target = 'https://zxzjtv.com/video/480-1-1.html'
HAVE_DOWN = ['第01集', '第02集']


driver = webdriver.Chrome(ChromeDriverManager().install())


PAGE_URLS = []
VIEDO_URLS = []

ua_list = [
        'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/535.1 (KHTML, like Gecko) Chrome/14.0.835.163 Safari/535.1',
        'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/73.0.3683.103 Safari/537.36Chrome 17.0',
        'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_7_0) AppleWebKit/535.11 (KHTML, like Gecko) Chrome/17.0.963.56 Safari/535.11',
        'Mozilla/5.0 (Windows NT 6.1; WOW64; rv:6.0) Gecko/20100101 Firefox/6.0Firefox 4.0.1',
        'Mozilla/5.0 (Macintosh; Intel Mac OS X 10.6; rv:2.0.1) Gecko/20100101 Firefox/4.0.1',
        'Mozilla/5.0 (Macintosh; U; Intel Mac OS X 10_6_8; en-us) AppleWebKit/534.50 (KHTML, like Gecko) Version/5.1 Safari/534.50',
        'Mozilla/5.0 (Windows; U; Windows NT 6.1; en-us) AppleWebKit/534.50 (KHTML, like Gecko) Version/5.1 Safari/534.50',
        'Opera/9.80 (Windows NT 6.1; U; en) Presto/2.8.131 Version/11.11',
    ]

# print(video.get_attribute('class'))

def getVideoIndex():
    """
    r = req.get(url = target)
    r.encoding = 'utf-8'
    print(r.text)
    bs = BeautifulSoup(r.text, 'lxml')
    """

    driver.get(target)
    aa = driver.find_elements_by_xpath('//*[@id="play-box"]/div[1]/div[2]/div[1]/ul/li/a')
    for a in aa:
        print(a.text, a.get_dom_attribute('href'))
        PAGE_URLS.append({'title': a.text, 'href': a.get_dom_attribute('href')})

    print('获取视频页面地址：', PAGE_URLS)

    # driver.close()


def getVideoURLS():
    for item in PAGE_URLS:
        if item['title'] in HAVE_DOWN:
            continue
        print(domain + item['href'])
        driver.get(domain + item['href'])
        iframe = driver.find_elements_by_tag_name("iframe")[2]
        driver.switch_to.frame(iframe)
        video = driver.find_element_by_tag_name('video')
        videoURL = video.get_attribute('src')
        print('视频地址：', item['title'], videoURL)
        # driver.close()
        VIEDO_URLS.append({'title': item['title'], 'url': videoURL});
    
    print('-----------------------------')
    print('全部视频地址获取成功:', VIEDO_URLS)
    driver.close()

def downVideo(videoData):
    print('开始下载：', videoData['title'])
    video_res = requests.get(videoData['url'], headers={
            'User-Agent': random.choice(ua_list)
        })
    with open('/Users/kele/Pictures/new_m/{name}.mp4'.format(name=videoData['title']), "wb") as video_file:
        video_file.write(video_res.content)
        video_file.close()
        print("{name} 下载完毕".format(name=videoData['title']));


def downloadSteam(videoData):
    
    video_res = requests.get(videoData['url'], headers={
            'User-Agent': random.choice(ua_list)
        }, stream=True)

    size = 0
    chunk_size = 1024
    content_size = int(video_res.headers['content-length'])

    print('开始下载：', videoData['title'], '总大小{size:.2f}M'.format(size = content_size / 1024 / 1024))

    f = open('/Users/kele/Pictures/疑犯追踪/{name}.mp4'.format(name=videoData['title']), 'wb')
    for chunk in video_res.iter_content(chunk_size=1024):
        if chunk:
            size += len(chunk)
            print('下载进度{name}：{t}{p:.2f} %'.format(t=('>'*int(size*50 / content_size)),name=videoData['title'], p=float(size/content_size * 100)))

            f.write(chunk)

def main():
    getVideoIndex()
    getVideoURLS()


main()

pool = ThreadPool(processes=4)
results2 = pool.map(downloadSteam, VIEDO_URLS)
pool.close()
pool.join()


print('======全部下载完毕======')
