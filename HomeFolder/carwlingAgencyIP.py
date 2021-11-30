#https://www.89ip.cn/

import requests
import os
import re
from bs4 import BeautifulSoup as bs
from PyQt5.QtCore import QDateTime
from PyQt5.QtCore import *
from PyQt5.QtGui import *
from PyQt5.QtWidgets import *
from PyQt5.QtWidgets import QMainWindow,QApplication,QHeaderView,QTableWidgetItem

class startCollect(QObject):
    filecontent = pyqtSignal(str,str,int)
    filetrail = pyqtSignal()
    def __init__(self):
        super(startCollect,self).__init__()
    def __del__(self):
        print(">>>__del-CollectIP__")
        #self.wait()

    def run(self):
        #要收集的页数
        for m in range(1,6):
            url = 'http://www.kxdaili.com/dailiip/1/%s.html'%m#
            headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:81.0) Gecko/20100101 Firefox/81.0'}

            r = requests.get(url=url, headers=headers)
            soup = bs(r.content, 'lxml')
            #print(soup)
            datas = soup.find_all(name='tr', attrs={})
            #print(datas)
            ips = []
            ports = []
            AgentLocations = []
            for data in datas:
                soup_proxy_content = bs(str(data), 'lxml')
                soup_proxy_data = soup_proxy_content.find_all(name='td')
                for i in range(len(soup_proxy_data)):
                    if i % 7 == 0:
                        ip = soup_proxy_data[i].string.strip()
                        ips.append(ip)
                        # print(soup_proxy_data[i].string.strip())
                    if i % 7 == 1:
                        port = soup_proxy_data[i].string.strip()
                        ports.append(port)
                        # print(soup_proxy_data[i].string.strip())
                    if i % 7 == 5:
                        AgentLocation = soup_proxy_data[i].string.strip()
                        AgentLocations.append(AgentLocation)
                        # print(soup_proxy_data[i].string.strip())


            for j in range(len(ips)):
                #print(ips[j] + ':' + ports[j])
                type = 'https'
                proxy = {}
                proxy[type.lower()] = '%s:%s' % (ips[j], ports[j])
                #print(proxy)
                headers = {
                    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:81.0) Gecko/20100101 Firefox/81.0',
                    'Connection': 'close'
                }

                try:#http://www.kxdaili.com
                    r = requests.get('http://www.kxdaili.com', headers=headers, proxies=proxy, timeout=5)
                    #print(r.status_code)
                    if r.status_code == 200:
                        self.filecontent.emit(str(ips[j]), str(ports[j]),1)
                    else:
                        self.filecontent.emit(str(ips[j]), str(ports[j]),0)
                except Exception as e:
                    print(str(ips[j]), str(ports[j]))
                    self.filetrail.emit(str(ips[j]), str(ports[j]), 2)
        self.filetrail.emit()
