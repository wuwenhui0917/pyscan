#coding=GBK
import threading
import urllib2
from configfile import *
import urlparse


class ScanThread(threading.Thread):
    def __init__(self,LogFile,listurl,htmllist,basedomain,scansite,parenturl):

        threading.Thread.__init__(self)
        self.logfile = LogFile
        self.data = listurl
        self.basedoamin = basedomain
        self.scansite = scansite
        self.scansite.addthread()
        self.parentUrl = parenturl
        print 'init thread....'
        config = ConfigFile()
        #ʹ�ô�����
        proxy = config.getvalue("proxy")
        if proxy ==None :
            proxy='-1'

        if proxy == "true":
            #���ô���
            #proxyConfig = 'http://%s:%s@%s' % ('userName', 'password', 'proxy')
            proxyconfig = 'http://%s:%s@%s' % (config.getStringvalue("proxyuserName"), config.getStringvalue("proxypassword"), config.getStringvalue("proxyUrl"))
            opener = urllib2.build_opener(urllib2.ProxyHandler({'http': proxyconfig}))
            urllib2.install_opener(opener)
            print "���ô���ɹ� ����Ϊ��"+proxyconfig

    def getPageContent(self, url):
        try:
            page = urllib2.urlopen(url, timeout=3)
            if page.code != 200:
                print url + "\t" + str(page.code)
            return page.code
        except IOError as e:
            print "errorurl==============================" + str(url)
            return -1


    def run(self):

        #print "ɨ���߳�"+self.getName()+"��ʼ...."

        print 'run data==='
        print self.data
        if self.data:
            for visiturl in self.data:
                code = self.getPageContent(visiturl)
                if self.logfile:

                    self.logfile.writeLine(str(visiturl).strip() + "    " + str(code)+"    "+str(self.parentUrl))
                else:
                    print(str(visiturl).strip() + "    " + str(code))
                #�����Ѿ�ɨ�����
                self.scansite.addHasUrl(visiturl)

                    # code = self.getPageContent(childrenurl)
                # if code == 200 :
                #     urlinfos = urlparse.urlparse(str(visiturl))
                #     if self.basedoamin == urlinfos.netloc:
                #         pagename = str(visiturl);
                #         if pagename.endswith("html") or pagename.endswith("jsp"):
                #
                #             print '��' + visiturl + " ��ӵ�ɨ������У���ǰɨ�����Ϊ: " + str(self.htmllist.qsize())
                #             self.htmllist.put(pagename)
                #         else:
                            #�����Ѿ�ɨ���



                            # listurl.append(childrenurl)
                        # else :
                        #   self.logFile.writeLine(str(childrenurl).strip() + "    " + str(code))

        else :
            print "nodata"
        print "ɨ�裺"+self.getName()+" ����"
        self.scansite.release()
