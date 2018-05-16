import re
import urllib
import urllib.request
import requests

from bs4 import BeautifulSoup

from selenium import webdriver
import os
import time


from multiprocessing import Process,Pool

import random
from PIL import Image


from get_ip_proxies import IP_PROXIES


"""
phantomjs:http://phantomjs.org/
chromedriver:http://chromedriver.storage.googleapis.com/index.html
"""


class chaoxing_spider():
    def __init__(self):
        self.browser = webdriver.Chrome()
        #self.browser = webdriver.PhantomJS(executable_path="./phantomjs.exe")

        #self.headers =  \
        #{'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/55.0.2882.87 Safari/537.36'}

        self.headers = {
            "X-Requested-With": 'XMLHttpRequest',
            "User-Agent": 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/53.0.2785.89 Safari/537.36',
            "Origin": 'http://book.chaoxing.com',
            "Cookie": 'user_trace_token=20170211115515-2db01e4efbb24178989f2b6139d3698e; LGUID=20170211115515-e593a6c4-f00d-11e6-8f71-5254005c3644; showExpriedIndex=1; showExpriedCompanyHome=1; showExpriedMyPublish=1; hasDeliver=0; index_location_city=%E5%85%A8%E5%9B%BD; login=false; unick=""; _putrc=""; Hm_lvt_4233e74dff0ae5bd0a3d81c6ccf756e6=1486785316; Hm_lpvt_4233e74dff0ae5bd0a3d81c6ccf756e6=1486789519; _ga=GA1.2.1374329991.1486785316; LGRID=20170211130519-af0ec03c-f017-11e6-a32c-525400f775ce; TG-TRACK-CODE=search_code; JSESSIONID=A5AC6E7C54130E13C1519ABA7F70BC3C; SEARCH_ID=053c985ab53e463eb5f747658872ef29',
            "Connection": 'keep-alive'
        }
        self.url_0="http://book.chaoxing.com"

        #self.ip_proxies=IP_PROXIES()




    def parse_url(self,url):
        """
        #代理设置
        proxies = self.ip_proxies.get_random_ip()
        proxy_support = urllib.request.ProxyHandler(proxies)#proxies = {'http':'49.79.196.45:61234'}
        opener = urllib.request.build_opener(proxy_support,urllib.request.HTTPHandler)
        opener.addheaders = [('User-Agent',
                              'Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/56.0.2924.87 Safari/537.36')]
        urllib.request.install_opener(opener)
        """


        page = urllib.request.Request(url, headers=self.headers)
        #print(page)
        page_info = urllib.request.urlopen(page).read().decode('utf-8')
        #print(page_info)
        time.sleep(5)
        soup = BeautifulSoup(page_info, 'html.parser')
        time.sleep(1)


        # 以格式化的形式打印html
        # print(soup.prettify())
        return soup

    def has_class_but_no_id(self,tag):
        return tag.has_attr('class')

    def schedule(self,a, b, c):
        # a:已下载的数据块 b:数据块的大小 c:远程文件的大小
        per = 100.0 * a * b / c
        if per > 100:
            per = 100
        print ('%.2f%%' % per)

    def downImg(self,imgUrl, dirpath, imgName):
        filename = os.path.join(dirpath, imgName)
        """
        #method-1
        try:
            urllib.urlretrieve(imgUrl, filename,self.schedule)
        except:
            print(" This is Exception：", imgUrl)
            return False

        """
        #method-2
        try:
            #proxies = self.ip_proxies.get_random_ip()
            res = requests.get(imgUrl, timeout=20,headers=self.headers)#,proxies=proxies)
            if str(res.status_code)[0] == "4":
                print(str(res.status_code), ":", imgUrl)
                return False
        except Exception as e:
            print(" This is Exception：", imgUrl)
            print(e)
            return False
        with open(filename, "wb") as f:
            f.write(res.content)

        return True


    def check_imgs(self,dirname):
        imgnames=os.listdir(dirname)
        if (len(imgnames)!=17):
            return False
        for imgname in imgnames:
            try:
                Image.open(dirname+imgname).verify()
            except:
                return False
        return True


    def processing(self):
        interrupt_flag=False

        soup_0 = self.parse_url(self.url_0)
        titles_0 = soup_0.find_all("a", title=re.compile(''),
                                   target="_blank")  # ,,href=re.compile(r'.html'),title=re.compile(r'*')


        for n_t,title_0 in enumerate(titles_0):
            if os.path.exists(title_0.string.replace(".","_")):
                pass
            else:
                os.mkdir(title_0.string.replace(".","_"))

            url_1 = self.url_0 + title_0.get('href')



            my_flag=True
            titles_1=[]
            while True:
                soup_1 = self.parse_url(url_1)
                titles_1_tmp = soup_1.find_all("a", href=re.compile("/ebook/detail_"), title=re.compile(''),
                                           target="_blank")
                if len(titles_1_tmp)>0:
                    if titles_1_tmp[0] not in titles_1 or titles_1_tmp[-1] not in titles_1:
                        titles_1.extend(titles_1_tmp)
                        print("add url:",url_1)
                    else:
                        print("already in url:",url_1)
                        break
                else:
                    print("the last url:",url_1)
                    break

                page_num=int(url_1.split("_")[-1].split(".")[0])
                url_1 = url_1.replace("page_%d.html"%(page_num),"page_%d.html"%(page_num+1))

                print(titles_1)

            for i in range(len(titles_1)):
                if titles_1[i].string != None:
                    url_2 = self.url_0 + titles_1[i].get('href')
                    # print(url_2)
                    # url_2="http://book.chaoxing.com/ebook/detail_81029588258cf78eaf26a1377d6c57b2dc82c52ee.html"
                    soup_2 = self.parse_url(url_2)
                    book_name_2 = soup_2.find_all(name="h1")
                    bookname = str(book_name_2[0])[4:-5]

                    titles_2 = soup_2.find_all(name="a", class_="shidu leftF")
                    if titles_2 == []:
                        continue
                    else:
                        if os.path.exists(title_0.string.replace(".","_") + "/" + bookname):
                            if self.check_imgs(title_0.string.replace(".","_") + "/" + bookname+"/")==True:
                                print("already downed:",title_0.string.replace(".","_") + "/" + bookname)
                                continue
                        else:
                            os.mkdir(title_0.string.replace(".","_") + "/" + bookname)

                    url_3 = self.url_0 + titles_2[0].get('href')
                    soup_3 = self.parse_url(url_3)
                    titles_3 = soup_3.find_all(id="ifr")
                    frame_url = titles_3[0].get("src")

                    try:
                        for f_num in range(17):
                            try:
                                Image.open("./" + title_0.string.replace(".","_") + "/" + bookname + "/"+"%05d.jpg" % f_num).verify()
                            except:
                                self.browser.get(frame_url)
                                time.sleep(10)
                                pic_des = self.browser.find_element_by_id('rimg_0').get_attribute('src')
                                self.downImg(pic_des, "./" + title_0.string.replace(".","_") + "/" + bookname + "/", "%05d.jpg" % f_num)
                                print("downing %s %d" % (bookname, f_num))
                            frame_url = frame_url[:-1] + '%d' % (int(frame_url[-1]) + 1)
                    except Exception as e:
                        #验证码异常
                        print("ERROR   %s %d" % (bookname, f_num))
                        #interrupt_flag=True
                        #break
            #if interrupt_flag == True:
            #    break



def Myprocess():
    cxs = chaoxing_spider()
    cxs.processing()




if __name__=="__main__":
    #进程池多进程处理
    num_process=1

    p = Pool(num_process)
    for i in range(num_process):
        if i!=num_process-1:
            p.apply_async(Myprocess, args=())
        else:
            p.apply_async(Myprocess, args=())


    p.close()  # 关闭进程池
    p.join()
    print('All subprocesses done')













