import zoomeye.sdk as zoom
import requests
import json
import os
import re
import time
from bs4 import BeautifulSoup as bs
from PyQt5.QtCore import QDateTime
from PyQt5.QtCore import *
from PyQt5.QtGui import *
from PyQt5.QtWidgets import *
from PyQt5.QtWidgets import QMainWindow,QApplication,QHeaderView,QTableWidgetItem

class startCollectZoomeye(QObject):
    collectZoomeye = pyqtSignal(str,str,str,str,str)
    overZoomeye = pyqtSignal()
    def __init__(self,jwt,q):
        super(startCollectZoomeye,self).__init__()
        self.jwt = jwt
        self.q = q
    def __del__(self):
        print(">>>__del-CollectZoomeye__")
        #self.wait()

    def run(self):#   传入jwt,搜索关键词#,jwt,q
        header = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:81.0) Gecko/20100101 Firefox/81.0',
            'Cube-Authorization': '%s'%self.jwt,
            'Referer': 'https://www.zoomeye.org/'
        }
        q = "%s"%self.q
        url = "https://www.zoomeye.org/search?q=%s&page=1&pageSize=20" % q
        r = requests.get(url, headers=header)
        r_decoded = json.loads(r.text)
        sum = int(r_decoded['total'])
        page = int(sum / 20) + 2
        result = []
        for i in range(1, int("%s" % page)):

            url = "https://www.zoomeye.org/search?q=%s&page=%i&pageSize=20" % (q, i)
            r = requests.get(url, headers=header)
            r_decoded = json.loads(r.text)
            ip = None
            port = None
            service = None
            rdns = None
            timestamp = None
            title = None
            for k in range(0, len(r_decoded['matches'])):
                # print(k)
                singel = r_decoded['matches'][k]
                ipReady = singel["ip"]  # 添加ip
                if "[" in str(ipReady):
                    ip = ipReady[0]
                else:
                    ip = ipReady
                #print(ip)
                #print(singel)
                singelKeys = singel.keys()
                singelKey = []
                for key in singelKeys:
                    singelKey.append(str(key))
                if "rdns" in singelKey:
                    rdns = singel["rdns"]  # 添加rdns
                else:
                    rdns = None
                if "portinfo" in singelKey:
                    portinfo = singel["portinfo"]  # 添加portinfo
                    port = portinfo["port"]  # 添加port
                    portinfoKeys = singel['portinfo'].keys()
                    portinfoKey = []
                    for pkey in portinfoKeys:
                        portinfoKey.append(str(pkey))
                    if "port" in portinfoKey:
                        port = singel["portinfo"]["port"]  # 添加port
                    else:
                        port = None
                    if "service" in portinfoKey:
                        service = singel["portinfo"]["service"]  # 添加service
                    else:
                        service = None
                else:
                    pass
                if "title" in singelKey:
                    title = singel["title"]  # 添加title
                else:
                    if "title" in portinfoKey:
                        title = singel["portinfo"]["title"]  # 添加title
                    else:
                        title = None
                if "timestamp" in singelKey:
                    timestamp = singel["timestamp"]  # 添加timeStamp
                else:
                    timestamp = None

                if "%s://%s:%s" % (service, ip, port) not in result:
                    result.append("%s://%s:%s" % (service, ip, port))
                    if port == None:
                        self.collectZoomeye.emit(str(timestamp),str(title), str(rdns), "http://%s" % ip,"服务:http" )
                        print(timestamp, title, rdns, "http://%s" % ip)
                    elif str(port) == "443" and str(service) == "https":
                        self.collectZoomeye.emit(str(timestamp), str(title), str(rdns), "https://%s" % ip, "服务:%s，端口:%s" % (service, port))
                        print(timestamp, title, rdns, "https://%s" % ip)
                    elif str(port) == "80" and str(service) == "http":
                        self.collectZoomeye.emit(str(timestamp), str(title), str(rdns), "http://%s" % ip, "服务:%s，端口:%s" % (service, port))
                        print(timestamp, title, rdns, "http://%s" % ip)
                    elif "https" not in str(service) and "http" not in str(service):
                        self.collectZoomeye.emit(str(timestamp), str(title), str(rdns), str(ip), "服务:%s，端口:%s" % (service, port))
                        print(timestamp, title, rdns, ip, "服务:%s，端口:%s" % (service, port))
                    elif ("https" in str(service) or "http" in str(service)) and "/" in str(service):
                        self.collectZoomeye.emit(str(timestamp), str(title), str(rdns), "%s://%s:%s" % (service, ip, port), "服务:%s，端口:%s" % (service, port))
                        print(timestamp, title, rdns, "%s://%s:%s" % (service, ip, port), "服务:%s，端口:%s" % (service, port))
                    elif ("https" in str(service) or "http" in str(service)) and "/" not in str(service):
                        self.collectZoomeye.emit(str(timestamp), str(title), str(rdns), "%s://%s:%s" % (service, ip, port), "服务:%s，端口:%s" % (service, port))
                        print(timestamp, title, rdns, "%s://%s:%s" % (service, ip, port))
                else:
                    print("%s://%s:%s" % (service, ip, port))
            time.sleep(2)
        self.overZoomeye.emit()




