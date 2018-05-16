# IP地址取自国内髙匿代理IP网站：http://www.xicidaili.com/nn/
# 仅仅爬取首页IP地址就足够一般使用

from bs4 import BeautifulSoup
import requests
import random
import re
import subprocess

class IP_PROXIES():
    def __init__(self):
        self.headers = {'Upgrade-Insecure-Requests': '1',
                        'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.36',
                        'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
                        'Referer': 'http://www.xicidaili.com/2016-05-13/beijing',
                        'Accept-Encoding': 'gzip, deflate, sdch',
                        'Accept-Language': 'zh-CN,zh;q=0.8',
                        }
        self.ip_proxies_url = 'http://www.xicidaili.com/2016-05-13/beijing'
        self.lose_time, self.waste_time = self.initpattern()
        self.proxy_list = self.get_ip_list()

    def get_ip_list(self):
        web_data = requests.get(self.ip_proxies_url, headers=self.headers)
        soup = BeautifulSoup(web_data.text, 'lxml')
        ips = soup.find_all('tr')
        ip_list = []
        for i in range(1, len(ips)):
            ip_info = ips[i]
            tds = ip_info.find_all('td')

            #test ip
            if self.check_ip(tds[1].text, self.lose_time, self.waste_time)==True:
                ip_list.append(tds[1].text + ':' + tds[2].text)
                print("add:",tds[1].text + ':' + tds[2].text)
                if len(ip_list)>10:
                    break

        proxy_list = []
        for ip in ip_list:
            proxy_list.append('http://' + ip)
        print(len(proxy_list))
        return proxy_list

    def get_random_ip(self):
        proxy_ip = random.choice(self.proxy_list)
        proxies = {'http': proxy_ip}
        return proxies

    """
    函数说明:初始化正则表达式
    Parameters:
        无
    Returns:
        lose_time - 匹配丢包数
        waste_time - 匹配平均时间
    Modify:
        2017-05-27
    """

    def initpattern(self):
        # 匹配丢包数
        lose_time = re.compile(u"丢失 = (\d+)", re.IGNORECASE)
        # 匹配平均时间
        waste_time = re.compile(u"平均 = (\d+)ms", re.IGNORECASE)
        return lose_time, waste_time

    """
    函数说明:检查代理IP的连通性
    Parameters:
        ip - 代理的ip地址
        lose_time - 匹配丢包数
        waste_time - 匹配平均时间
    Returns:
        average_time - 代理ip平均耗时
    Modify:
        2017-05-27
    """

    def check_ip(self,ip, lose_time, waste_time):
        # 命令 -n 要发送的回显请求数 -w 等待每次回复的超时时间(毫秒)
        cmd = "ping -n 3 -w 3 %s"
        # 执行命令
        p = subprocess.Popen(cmd % ip, stdin=subprocess.PIPE, stdout=subprocess.PIPE, stderr=subprocess.PIPE, shell=True)
        # 获得返回结果并解码
        out = p.stdout.read().decode("gbk")
        # 丢包数
        lose_time = lose_time.findall(out)
        # 当匹配到丢失包信息失败,默认为三次请求全部丢包,丢包数lose赋值为3
        if len(lose_time) == 0:
            lose = 3
        else:
            lose = int(lose_time[0])
        # 如果丢包数目大于2个,则认为连接超时,返回平均耗时1000ms
        if lose > 2:
            # 返回False
            average_time=1000
        # 如果丢包数目小于等于2个,获取平均耗时的时间
        else:
            # 平均时间
            average = waste_time.findall(out)
            # 当匹配耗时时间信息失败,默认三次请求严重超时,返回平均好使1000ms
            if len(average) == 0:
                average_time=1000
            else:
                average_time = int(average[0])
                # 返回平均耗时

        if average_time > 200:
            return False
        else:
            return True

if __name__ == '__main__':
    ip_proxies=IP_PROXIES()
    proxies=ip_proxies.get_random_ip()
    print(proxies)
