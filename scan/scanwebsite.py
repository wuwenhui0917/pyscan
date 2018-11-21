# coding:GBK

# ��վɨ�蹤�ߣ�ɨ����վ�ڲ������е�url��js����Դ
# author:wuwh
import Queue
import time
from selenium import webdriver
from selenium.webdriver.common.by import By
import urllib
import urlparse
# import LogFile
# import logfile
from logfile import *
from webmap import *


class ScanWebSite(object):


    def __init__(self,scanUrl,logname="scan.log",deep=2,domain="10086"):
        self.domain=domain
        # �Ѿ�ɨ��ĵ�ַ
        self.listhassacnaurl=[]
        self.htmllist=Queue.Queue()
        self.basedoamin=""
        self.scanurl = scanUrl
        self.logFile = LogFile(fileName=logname)
        map = WebsitrTree(startValue=scanUrl)
        self.webtree = map
        self.deep=deep
    def start(self):
        self.chrome = webdriver.Chrome()

        self.chrome.set_window_size(0, 0)
        if self.scanurl != None:
            self._startURL(self.scanurl)

    def _close(self):
        self.chrome.close()
        self.logFile.close()

    def _startURL(self,url):
        urlinfos = urlparse.urlparse(url)
        self.basedoamin = urlinfos.netloc
        self.htmllist.put(url)
        while not self.htmllist.empty():
            html = self.htmllist.get()
            if html not in self.listhassacnaurl:
                try:
                    print "#################################################################################"
                    print "��ʼɨ�裺" + html
                    print self.basedoamin
                    print "#################################################################################"

                    # ��ͬ������
                    if str(html).find(self.basedoamin) > -1:
                        self.execute(html)
                    else:
                        print "Ҫɨ���:"+str(html)+" ���Ǳ�վ���µ�url������ɨ��"
                    # �����Ѿ�ɨ�������
                    self.listhassacnaurl.append(html)
                except Exception as e:
                    print e
                    pass
                print "��ǰɨ����г���Ϊ ��"+str(self.htmllist.qsize())
            else:
                print str(html)+" �Ѿ�ɨ�����������ɨ��"

        self._close()

    def getRealUrl(self, url, currenturl):
        strurl = str(url)
        # if(strUrl.startswith("./")):
        #     return currentUrl+strUrl;
        # if(strUrl.startswith("..")):
        #     strUrl.split("")
        if strurl.startswith("http"):
            return strurl
        else:
            return urlparse.urljoin(currenturl, url)
            # if strUrl.startswith("/") or strUrl.startswith("."):
            #     return urlparse.urljoin(currentUrl,url);

            # return None


    def execute(self,baseurl):
        # chrome.get("http://service.sn.10086.cn/pch5/index/html/index.html")
        self.chrome.get(baseurl)
        time.sleep(1)
        # ����
        # parseUrl(baseurl)
        urlinfos = urlparse.urlparse(str(baseurl))
        if self.basedoamin != urlinfos.netloc:
            # print basedoamin + "============" + urlinfos.netloc
            print "����ͬһ�������µģ���ɨ��"
            return
        # strpasswprd = raw_input("��½�ɹ����밴�����: ");
        # print "Received input is : ", str
        # ����url��ȡdomain����Ϣ
        # parseUrl(baseurl)
        listurl = []
        list = self.chrome.find_elements(By.TAG_NAME, "a")
        print "a========="+str(len(list))
        for ele in list:
            url = ele.get_attribute("href")
            goodssrc = ele.get_attribute("goodsurl")
            # print url;
            strUrl = str(url)
            print strUrl
            # if not str(url).startswith("http") and str(url)!='' and url !=None :
            #     listurl.append(url)
            # if strUrl.startswith("http") :
            #     listurl.append(url)
            # if strUrl.startswith("/"):
            #     listurl(domain+strUrl);
            if not strUrl.startswith("java") and url != None and strUrl != '':
                childrenurl = self.getRealUrl(strUrl, baseurl)
                listurl.append(childrenurl)
                if childrenurl not in self.listhassacnaurl:
                    #������վ��ͼ��
                    self.webtree.addChild(childValue=childrenurl,paraentValue=baseurl)
                    deep = self.webtree.getDeep(childrenurl)
                    print ""+childrenurl+" �ǵ�"+str(deep)+"��  ,����ɨ��㼶Ϊ�� "+str(self.deep)
                    if deep <= self.deep:
                       print '��'+ childrenurl+" ��ӵ�ɨ������У���ǰɨ�����Ϊ: "+str(self.htmllist.qsize() )
                       self.htmllist.put(childrenurl)
                    # print "ɨ����г���Ϊ��" + str(len(self.htmllist))

            if goodssrc != None and goodssrc != '':
                listurl.append(self.getRealUrl(goodssrc, baseurl))
                if self.getRealUrl(goodssrc, baseurl) not in self.listhassacnaurl:
                    self.htmllist.put(self.getRealUrl(goodssrc, baseurl))

                # print 'goodsurl::::::::::::::' + goodssrc

        # ����ͼƬ
        imagess = self.chrome.find_elements(By.TAG_NAME, "img")
        for img in imagess:
            imgsrcurl = img.get_attribute("src")
            strImgsrc = str(imgsrcurl)
            if strImgsrc != None and strImgsrc != '':
                # print 'img:url' + strImgsrc
                listurl.append(self.getRealUrl(strImgsrc, baseurl))

        # css ɨ��
        links = self.chrome.find_elements(By.TAG_NAME, "link")
        for link in links:
            linksrcurl = link.get_attribute("href")
            strlinksrcurl = str(linksrcurl)
            if strlinksrcurl != None and strlinksrcurl != '':
                # print 'link:url' + strlinksrcurl
                listurl.append(self.getRealUrl(strlinksrcurl, baseurl))
        # ɨ��js
        scriptlinks = self.chrome.find_elements(By.TAG_NAME, "script")
        for jslink in scriptlinks:
            linksrcurl = jslink.get_attribute("src")
            strjssrcurl = str(linksrcurl)
            if strjssrcurl != None and strjssrcurl != '':
                # print 'script:url' + strjssrcurl
                listurl.append(self.getRealUrl(strjssrcurl, baseurl))

        # imglist  = chrome.find_elements(By.TAG_NAME,"a")
        # chrome.close();

        for visiturl in listurl:
            code = self.getPageContent(visiturl)
            self.logFile.writeLine(visiturl+"    "+str(code))

            # print str(visiturl) + "\t=============result========:" + str(code)
    #
    # ��ȡҳ����Ӧ��
    #
    def getPageContent(self,url):
        try:
            page = urllib.urlopen(url)
            if page.code != 200:
                print url + "\t" + str(page.code)
            return page.code;
        except IOError as e:
            print "errorurl==============================" + str(url)
            return -1

if __name__ == '__main__':
    scanobj = ScanWebSite(scanUrl="http://wap.sn.10086.cn/h5/index/html/home.html")
    scanobj.start()
