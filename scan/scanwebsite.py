# coding:GBK

# ��վɨ�蹤�ߣ�ɨ����վ�ڲ������е�url��js����Դ
# author:wuwh
import Queue
import time
from selenium import webdriver
from selenium.webdriver.common.by import By
import urllib2
import urlparse
# import LogFile
# import logfile
from logfile import *
from webmap import *
from ScanUrlThread import *
import sys



class ScanWebSite(object):

    def __init__(self,scanUrl,deep,logname="scan2.log",domain="10086",chromehandle=None,websitecode='utf-8'):
        # self.domain=domain
        # �Ѿ�ɨ��ĵ�ַ
        self.listhassacnaurl=[]
        #�Ѿ�ɨ��htmlҳ��
        self.hashtml=[]
        #��Ҫɨ��ĵ�ַ
        self.htmllist = Queue.Queue()
        self.basedoamin=urlparse.urlparse(str(scanUrl)).netloc;
        self.scanurl = scanUrl
        self.logFile = LogFile(fileName=logname)
        map = WebsitrTree(startValue=scanUrl)
        self.webtree = map
        if deep > 3:

            self.deep = 3
        else:
            self.deep=deep
        print "ɨ�����Ϊ��"+str(self.deep)
        print "ɨ������Ϊ��" + str(self.basedoamin)

        self.chrome = None
        self.chromehandle = chromehandle
        self.websitecode=websitecode

        self.threadcount=0
        self.mutex = threading.Lock()

    def addHasUrl(self,url):
        self.listhassacnaurl.append(url)

    def addhashtml(self,htmlurl):
        self.hashtml.append(htmlurl)

    def start(self):
        reload(sys)
        sys.setdefaultencoding(self.websitecode)
        option = webdriver.ChromeOptions()
        option.add_argument('headless')
        self.chrome = webdriver.Chrome(chrome_options=option)
        self.chrome.set_window_size(0, 0)
        # webdriver.PhantomJS.title.encode("utf-8")
        if self.scanurl:
            self._startURL(self.scanurl)


    def release(self):
        # self.mutex.acquire()
        self.threadcount=self.threadcount-1
        # self.mutex.release()

    def executeJs(self,parent):

        hh =  self.chrome.execute_script("return document.referrer")
        if hh :
            return 1


        print hh

    def  addthread(self):
        # self.mutex.acquire()
        self.threadcount = self.threadcount + 1
        # self.mutex.release()


    def _close(self):
        # while self.threadcount > 0:
        #     print "close"
        #     time.sleep(10)
        self.chrome.close()
        self.logFile.close()
        print "����ɨ�����"

    def gethost(self,html):
        return  urlparse.urlparse(str(html)).netloc


    def _startURL(self,url):
        urlinfos = urlparse.urlparse(url)
        self.htmllist.put(url)
        while not self.htmllist.empty():
            # print "��ǰ�߳���"+str(self.threadcount)
            html = self.htmllist.get()
            if html not in self.hashtml:
                try:
                    print "#################################################################################"
                    print "��ʼɨ�裺" + html
                    print self.basedoamin
                    print "#################################################################################"
                    urldomains = urlparse.urlparse(str(html)).netloc
                    # ��ͬ������
                    if urldomains == self.basedoamin:
                        self.execute(html)
                    else:
                        print "Ҫɨ���:"+str(html)+" ���Ǳ�վ���µ�url������ɨ��"
                    # �����Ѿ�ɨ�������
                    self.hashtml.append(html)
                except Exception as e:
                    print e
                    pass
                print "��ǰɨ����г���Ϊ ��"+str(self.htmllist.qsize())
            else:
                print str(html)+" �Ѿ�ɨ�����������ɨ��"


            # print "��ǰ�߳���::::::::::::::::::::::::" + str(self.threadcount)

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

    # def getDeep(self,url):{
    #     url =  self.chrome.execute_cdp_cmd("document.referrer");
    # }

    def execute(self,baseurl):

        urlinfos = urlparse.urlparse(str(baseurl))
        if self.basedoamin != urlinfos.netloc:
            # print basedoamin + "============" + urlinfos.netloc
            print "����ͬһ�������µģ���ɨ��"
            return
        # chrome.get("http://service.sn.10086.cn/pch5/index/html/index.html")
        self.chrome.get(baseurl)
        time.sleep(1)
        # ����
        # parseUrl(baseurl)

        # strpasswprd = raw_input("��½�ɹ����밴�����: ");
        # print "Received input is : ", str
        # ����url��ȡdomain����Ϣ
        # parseUrl(baseurl)
        listurl = []
        list = self.chrome.find_elements(By.TAG_NAME, "a")
        deep = self.webtree.getDeep(baseurl)
        for ele in list:
            url = ele.get_attribute("href")
            goodssrc = ele.get_attribute("goodsurl")
            # print url;
            strUrl = str(url)

            # if not str(url).startswith("http") and str(url)!='' and url !=None :
            #     listurl.append(url)
            # if strUrl.startswith("http") :
            #     listurl.append(url)
            # if strUrl.startswith("/"):
            #     listurl(domain+strUrl);
            if not strUrl.startswith("java") and url and strUrl != '':
                childrenurl = self.getRealUrl(strUrl, baseurl)
                #����ɨ�������ɨ��
                if childrenurl not in self.listhassacnaurl:
                    listurl.append(childrenurl)
                # listurl.append(childrenurl)
                #���html ����htmlɨ�����ʱɨ��
                if childrenurl not in self.hashtml:
                    urlinfos = urlparse.urlparse(str(childrenurl))
                    #����ͬһ������������
                    if self.basedoamin != urlinfos.netloc:
                        continue
                    #������վ��ͼ��
                    #��0��ʼ

                    #��ȡ�Լ��Ĳ㼶
                    if deep+1 < self.deep:
                        print "���tree"
                        self.webtree.addChild(childValue=childrenurl, paraentValue=baseurl)
                        # listurl.append(childrenurl)
                        print "����hmtlɨ��ɨ�����"
                        self.htmllist.put(childrenurl)
                    print ""+childrenurl+" �ǵ�"+str(deep+1)+"��  ,����ɨ��㼶Ϊ�� "+str(self.deep)

                       # code = self.getPageContent(childrenurl)
                       # if code == 200 :
                       #     urlinfos = urlparse.urlparse(str(childrenurl))
                       #     if self.basedoamin == urlinfos.netloc:
                       #         print '��' + childrenurl + " ��ӵ�ɨ������У���ǰɨ�����Ϊ: " + str(self.htmllist.qsize())
                       #         self.htmllist.put(childrenurl)
                       #       #listurl.append(childrenurl)
                       # else :
                       #     self.logFile.writeLine(str(childrenurl).strip() + "    " + str(code))

                           # print "ɨ����г���Ϊ��" + str(len(self.htmllist))

            #���a��ǩʱjava�ű�ʱ
            elif strUrl.startswith("java"):
                method = strUrl.split(":")[1]
                print "js======="+strUrl

            # if goodssrc != None and goodssrc != '':
            #     listurl.append(self.getRealUrl(goodssrc, baseurl))
            #     if self.getRealUrl(goodssrc, baseurl) not in self.listhassacnaurl:
            #         self.htmllist.put(self.getRealUrl(goodssrc, baseurl))

                # print 'goodsurl::::::::::::::' + goodssrc

        # ����ͼƬ
        imagess = self.chrome.find_elements(By.TAG_NAME, "img")
        for img in imagess:
            imgsrcurl = img.get_attribute("src")
            strImgsrc = str(imgsrcurl)
            if strImgsrc and strImgsrc != '':
                # print 'img:url' + strImgsrc
                imageurl = self.getRealUrl(strImgsrc, baseurl)
                if imgsrcurl not in self.listhassacnaurl:

                    listurl.append(imageurl)

        # css ɨ��
        links = self.chrome.find_elements(By.TAG_NAME, "link")
        for link in links:
            linksrcurl = link.get_attribute("href")
            strlinksrcurl = str(linksrcurl)
            if strlinksrcurl != None and strlinksrcurl != '':
                # print 'link:url' + strlinksrcurl
                cssurl = self.getRealUrl(strlinksrcurl, baseurl)
                if cssurl not in self.listhassacnaurl:
                   listurl.append(cssurl)
        # ɨ��js
        scriptlinks = self.chrome.find_elements(By.TAG_NAME, "script")
        for jslink in scriptlinks:
            linksrcurl = jslink.get_attribute("src")
            strjssrcurl = str(linksrcurl)
            if strjssrcurl and strjssrcurl != '':
                # print 'script:url' + strjssrcurl
                jsvar = self.getRealUrl(strjssrcurl, baseurl)
                if jsvar not in self.listhassacnaurl:
                    listurl.append(jsvar)

        # imglist  = chrome.find_elements(By.TAG_NAME,"a")
        # chrome.close();



        # for visiturl in listurl:
        #     code = self.getPageContent(visiturl)
        #     self.logFile.writeLine(str(visiturl).strip()+"    "+str(code))

        #���߳�ɨ��
        scanthread = ScanThread(self.logFile,listurl,self.htmllist,self.basedoamin,self,parenturl=baseurl)
        scanthread.run()

            # print str(visiturl) + "\t=============result========:" + str(code)
    #
    # ��ȡҳ����Ӧ��
    #
    # def getPageContent(self,url):
    #     try:
    #         page = urllib2.urlopen(url,timeout=5)
    #         if page.code != 200:
    #             print url + "\t" + str(page.code)
    #         return page.code
    #     except IOError as e:
    #         print "errorurl==============================" + str(url)
    #         return -1

if __name__ == '__main__':
    scanobj = ScanWebSite(scanUrl="http://www.ln.10086.cn/service/static/index.html",deep=1)
    scanobj.start()
    # if len(sys.argv) != 2:
    #     print "please useage: scan  url"
    #     print "forexample scan  http://wap.sn.10086.cn"
    # else :
    #     scanobj = ScanWebSite(scanUrl=sys.argv[1])
    #     scanobj.start()
