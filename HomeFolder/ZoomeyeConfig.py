#import ZoomeyeConfig_ui
import ZoomeyeConfigToken_ui
from PyQt5 import *
from PyQt5 import QtWidgets
from PyQt5.QtCore import *
from PyQt5.QtGui import *
from PyQt5.QtWidgets import *
from PyQt5.QtWidgets import QMainWindow,QApplication,QHeaderView,QTableWidgetItem
import sys,os,cv2
import requests,datetime,time

class ZoomeyeConfig(QtWidgets.QDialog):
    def __init__(self):
        QtWidgets.QWidget.__init__(self)
        # self.ui = ZoomeyeConfig_ui.Ui_ZoomeyeConfig()
        self.ui = ZoomeyeConfigToken_ui.Ui_ZoomeyeConfig()
        self.ui.setupUi(self)
        self.trans = QTranslator()
        self.setWindowIcon(QIcon("../img/main_icon.jpg"))
        self.ui.message.setVisible(False)
        self.ZoomeyeToken = None
        # self.gif = QMovie('ZoomVerify.gif')
        # self.ui.graphicsView.setMovie(self.gif)
        # self.gif.start()
        # self.ui.changeVer.clicked.connect(self.getVerify)

        self.jwt = None
        self.csrfmiddlewaretoken = None
        self.__jsluid_s = None
        self.sessionid = None
        self.Referer = "https://sso.telnet404.com/cas/login?service=https%3A%2F%2Fwww.zoomeye.org%2Flogin"

        # self.ui.Login.clicked.connect(self.Login)
        # self.ui.Grammar.clicked.connect(self.Grammar)

        if os.path.exists("../common/ZoomeyeKeyword.txt"):
            with open("../common/ZoomeyeKeyword.txt" , "r", encoding="utf-8") as f:
                self.ui.Keyword.setText(f.readline().replace("\n",''))
                self.ZoomeyeToken = f.readline().replace("\n",'')
                valid = f.readline().replace("\n",'')
                f.close()
        if self.ZoomeyeToken != None:
            if os.path.exists("../common/%s.txt"%self.ZoomeyeToken):
                if int(time.time())-int(valid) <= 10800:
                    with open("../common/%s.txt"%self.ZoomeyeToken, "r", encoding="utf-8") as f:
                        self.ui.ZoomToken.setText(f.readline())
                        f.close()
                else:
                    self.ui.ZoomToken.setText("")

        self.accepted.connect(self._accepted)


    # def Login(self):
    #     if self.csrfmiddlewaretoken == None:
    #         QMessageBox.information(self, '提示', '请先获取新的验证码登录~')
    #     else:
    #         url = "https://sso.telnet404.com/cas/login?service=https%3A%2F%2Fwww.zoomeye.org%2Flogin"
    #         header = {
    #             "Host": "sso.telnet404.com",
    #             "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:94.0) Gecko/20100101 Firefox/94.0",
    #             "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,*/*;q=0.8",
    #             "Accept-Language": "zh-CN,zh;q=0.8,zh-TW;q=0.7,zh-HK;q=0.5,en-US;q=0.3,en;q=0.2",
    #             "Accept-Encoding": "gzip, deflate",
    #             "Content-Type": "application/x-www-form-urlencoded",
    #             "Origin": "https://sso.telnet404.com",
    #             "Referer": "%s"%self.Referer,
    #             "Connection": "close",
    #             "Cookie": "csrftoken=%s; __jsluid_s=%s; __jsluid_h=24d92bb8df728be4bf5961fca4f1c96a; sessionid=%s"%(self.csrfmiddlewaretoken,self.__jsluid_s,self.sessionid),
    #             "Upgrade-Insecure-Requests": "1",
    #             "Sec-Fetch-Dest": "document",
    #             "Sec-Fetch-Mode": "navigate",
    #             "Sec-Fetch-Site": "cross-site",
    #             "Sec-Fetch-User": "?1"
    #         }
    #
    #         username = self.ui.Zoomname.text().replace("@","%40")
    #         data = "csrfmiddlewaretoken=%s&email=%s&password=%s&captcha=%s"%(self.csrfmiddlewaretoken,username,self.ui.Zoompwd.text(),self.ui.ZoomVerification.text())
    #         print(data)
    #         r = requests.post(url=url,data=data,headers=header)
    #         print(r,r.headers)
    #     print("Login")

    def Grammar(self):
        QDesktopServices.openUrl(QUrl('file:///' +
                                      os.path.abspath(
                                          '../document/ZoomeyeSearch.docx').replace('\\', '/')))
        print("Grammar")

    # def getVerify(self):
    #     url1 = "https://sso.telnet404.com/cas/login?service=https%3A%2F%2Fwww.zoomeye.org%2Flogin"
    #     header1 = {
    #         "Host": "sso.telnet404.com",
    #         "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:94.0) Gecko/20100101 Firefox/94.0",
    #         "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,*/*;q=0.8",
    #         "Accept-Language": "zh-CN,zh;q=0.8,zh-TW;q=0.7,zh-HK;q=0.5,en-US;q=0.3,en;q=0.2",
    #         "Accept-Encoding": "gzip, deflate",
    #         "Referer": "https://www.zoomeye.org/",
    #         "Connection": "close",
    #         "Upgrade-Insecure-Requests": "1",
    #         "Sec-Fetch-Dest": "document",
    #         "Sec-Fetch-Mode": "navigate",
    #         "Sec-Fetch-Site": "cross-site",
    #         "Sec-Fetch-User": "?1",
    #         "If-Modified-Since": "Tue, 23 Nov 2021 01:08:39 GMT",
    #         "Cache-Control": "max-age=0",
    #     }
    #     header2 = {
    #         "Host": "sso.telnet404.com",
    #         "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:94.0) Gecko/20100101 Firefox/94.0",
    #         "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,*/*;q=0.8",
    #         "Accept-Language": "zh-CN,zh;q=0.8,zh-TW;q=0.7,zh-HK;q=0.5,en-US;q=0.3,en;q=0.2",
    #         "Accept-Encoding": "gzip, deflate",
    #         "Referer": "%s"%self.Referer,
    #         "Connection": "close",
    #         "Cookie": "csrftoken=%s; __jsluid_s=%s; __jsluid_h=24d92bb8df728be4bf5961fca4f1c96a;" % (self.csrfmiddlewaretoken,self.__jsluid_s),
    #         "Upgrade-Insecure-Requests": "1",
    #         "Sec-Fetch-Dest": "document",
    #         "Sec-Fetch-Mode": "navigate",
    #         "Sec-Fetch-Site": "cross-site",
    #         "Sec-Fetch-User": "?1",
    #         "If-Modified-Since": "Tue, 23 Nov 2021 01:08:39 GMT",
    #         "Cache-Control": "max-age=0",
    #     }
    #     if self.csrfmiddlewaretoken == None:
    #         r1 = requests.get(url1, headers=header1)
    #     else:
    #         r1 = requests.get(url1, headers=header2)
    #     #print(r.headers["Set-Cookie"])
    #     csrftoken = r1.headers["Set-Cookie"].split(";")[0].split("=")[1]
    #     if self.__jsluid_s == None:
    #         __jsluid_s = r1.headers["Set-Cookie"].split(";")[3].split(",")[1].split("=")[1]
    #         self.__jsluid_s = __jsluid_s
    #     self.csrfmiddlewaretoken = csrftoken
    #     print("csrfyoken: "+self.csrfmiddlewaretoken)
    #     print("__jsluid_s: "+self.__jsluid_s)
    #
    #     url2 = "https://sso.telnet404.com/captcha/"
    #
    #     r2 = requests.get(url2, headers=header2)
    #     sessionid = r2.headers["Set-Cookie"].split(";")[0].split("=")[1]
    #     self.sessionid = sessionid
    #     with open("ZoomVerify.gif", "wb") as f:
    #         f.write(r2.content)
    #         f.close()
    #
    #     self.gif.stop()
    #     self.gif = QMovie('ZoomVerify.gif')
    #     self.ui.graphicsView.setMovie(self.gif)
    #     self.gif.start()
    #     print("验证码更换了")

    def _accepted(self):
        nowTime = "%s%s%s%s" % (
            datetime.datetime.now().year, datetime.datetime.now().month, datetime.datetime.now().day,
            datetime.datetime.now().hour)
        try:
            if self.ui.Keyword.text() != "" :
                with open("../common/ZoomeyeKeyword.txt" , "w", encoding="utf-8") as f:
                    f.write(self.ui.Keyword.text())
                    f.write("\n")
                    f.write(nowTime)
                    f.write("\n")
                    f.write("%s"%int(time.time()))
                    f.close()
            if self.ui.ZoomToken.text() != "" :
                with open("../common/%s.txt"%nowTime , "w", encoding="utf-8") as f:
                    f.write(self.ui.ZoomToken.text())
                    f.close()
        except Exception as e:
            print("文件创建出现问题")
        print("接受了")

    @property
    def keyword(self):
        return self.ui.Keyword.text()

    @property
    def jwtResult(self):
        #return self.jwt
        return self.ui.ZoomToken.text()