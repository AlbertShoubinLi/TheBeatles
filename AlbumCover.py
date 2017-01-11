from selenium import webdriver
from bs4 import BeautifulSoup
import requests
import os
import time

class AlbumCover():

    def __init__(self):
        self.init_url = "http://music.163.com/#/artist/album?id=101988&limit=120&offset=0"
        self.folder_path = "E:\TheBeatles"

    def save_img(self, url, file_name): ##保存图片
        print('开始请求图片地址，过程会有点长...')
        img = self.request(url)
        print('开始保存图片')
        f = open(file_name, 'ab')
        f.write(img.content)
        print(file_name,'图片保存成功！')
        f.close()

    def request(self, url):  #封装的requests 请求
        r = requests.get(url)  # 像目标url地址发送get请求，返回一个response对象。有没有headers参数都可以。
        return r

    def mkdir(self, path):  ##这个函数创建文件夹
        path = path.strip()
        isExists = os.path.exists(path)
        if not isExists:
            print('创建名字叫做', path, '的文件夹')
            os.makedirs(path)
            print('创建成功！')
            return True
        else:
            print(path, '文件夹已经存在了，不再创建')
            return False

    def get_files(self, path): #获取文件夹中的文件名称列表
        pic_names = os.listdir(path)
        return pic_names

    def spider(self):
        print("Start!")
        driver = webdriver.PhantomJS()
        driver.get(self.init_url)
        driver.switch_to.frame("g_iframe")  #加载 iframe 框架中的内容
        html = driver.page_source  #获取加载的网页内容

        is_new_folder = self.mkdir(self.folder_path)  # 创建文件夹，并判断是否是新创建
        print('开始切换文件夹')
        os.chdir(self.folder_path)  # 切换路径至上面创建的文件夹

        file_names = self.get_files(self.folder_path)  # 获取文件夹中的所有文件名，类型是list

        all_li = BeautifulSoup(html, 'lxml').find(id='m-song-module').find_all('li')
        # print(type(all_li))

        for li in all_li:
            album_img = li.find('img')['src']  #获取专辑封面的url
            album_name = li.find('p', class_='dec')['title']  #获取专辑的名称
            album_date = li.find('span', class_='s-fc3').get_text()  #获取专辑的发行日期
            end_pos = album_img.index('?')  #找到图片url中宽高的参数位置，即问号的位置
            album_img_url = album_img[:end_pos]  #截取图片url的宽高参数，得到原始图片的 url

            photo_name = album_date + ' - ' + album_name.replace('/','').replace(':',',') + '.jpg'  #图片命名
            print(album_img_url, photo_name)

            #去重判定
            if photo_name in file_names:
                print('图片已经存在，不再重新下载')
            else:
                self.save_img(album_img_url, photo_name)  #下载图片

album = AlbumCover()
album.spider()

