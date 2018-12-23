# coding:GBK
from BaseHTTPServer import HTTPServer, BaseHTTPRequestHandler
import threading
from configfile import *
from multiprocessing import Process
from scanwebsite import *
from SftpClient import *
from httpclient import *

config = ConfigFile()


class myprocess(Process):

    def __init__(self, group=None, target=None, name=None, args=(), kwargs={}):
        super(myprocess, self).__init__(group, target, name, args, kwargs)

    def run(self):
        scanobj = ScanWebSite(scanUrl="http://wap.sn.10086.cn/h5/index/html/home.html")
        scanobj.start()


class handleThread(threading.Thread):

    def __init__(self, jsonParam,handleClass ):
        super(handleThread, self).__init__()#ע�⣺һ��Ҫ��ʽ�ĵ��ø���ĳ�ʼ��������
        self.param = jsonParam
        self.server = handleClass
        self.error = None
        print jsonParam
        print handleClass
        urlinfo = urlparse.urlparse(self.param)
        params = urlparse.parse_qs(urlinfo.query)
        if params.get("transid"):
            self.transid = params.get("transid")[0]
        else:
            self.error = "transid must not null"
        if params.get("scanurl"):
            self.scanurl = urllib.unquote(params.get("scanurl")[0])
        else:
            self.error = "scanurl must not null"
        if params.get("deep"):
            self.deep = params.get("deep")[0]
        else:
            self.deep = 1

    def checkparam(self):
        return self.error

    def run(self):
        print self.getName()+"�߳̿�ʼ��ɨ���ַΪ��"+str(self.scanurl)+" ɨ�����Ϊ��"+str(self.deep)+" ɨ����־Ϊ��"+str(self.transid)+".log"
        scanobj = ScanWebSite(scanUrl=self.scanurl, deep=int(self.deep), logname=str(self.transid)+".log")
        scanobj.start()
        ftptag = int(config.getvalue("ftptag"))
        if ftptag == 1:
            print "frpip="+config.getStringvalue("ftpip")
            print "ftppwd="+config.getStringvalue("ftppwd")
            print "ftpuser="+config.getStringvalue("ftpuser")
            sft = FtpClient(ftpip=config.getStringvalue("ftpip"),
                            ftppasswd=config.getStringvalue("ftppwd"),
                            ftpuser=config.getStringvalue("ftpuser")
                            )
            try:
                sft.connection()
                sft.upload(str(self.transid)+".log",config.getStringvalue("ftpdir")+"/"+str(self.transid)+".log")
                print(str(self.transid)+" �ļ��ϴ��ɹ��ϴ��ɹ�")
                httpurl = config.getvalue("ftpcallback")
                if httpurl:
                    httpclient = HttpClient(str(httpurl))
                    _params = {"transid": self.transid, "logfile": str(self.transid)+".log"}

                    if httpclient.do_get(_params):
                        print("�ص���"+self.transid+"�ɹ�")
            except Exception as e:
                print("[ERROR:] �����쳣", e)
            finally:
                if sft:
                    sft.close()


class handleClass(BaseHTTPRequestHandler):

    def _writeheads(self):
        print self.path
        print self.headers
        self.send_response(200)
        self.send_header('Content-type', 'text/html')
        self.end_headers()

    def do_GET(self):
        print 'dsdsds'
        path = self.path
        print 'path........'+path
        query = urllib.splitquery(path)
        print query[0]

        self._writeheads()
        if query[0].startswith('/scan'):
            thexecute = handleThread(path, self)
            checkinfo = thexecute.checkparam()
            if checkinfo:
                self.wfile.write(checkinfo)
                return
            self.wfile.write("ok")
            # p = myprocess()
            # p.start()
            thexecute.start()
            # self.send_response(200)
            # self.send_header('Content-type', 'text/html')
            # self.end_headers()
            # self.wfile.write("ok====="+query[1])
        else:
            self.wfile.write("hello===="+path)

if __name__ == '__main__':
    print '���������'

    ip = str(config.getvalue("bindip")).strip()
    port = config.getvalue("port")
    # ip = "127.0.0.1"

    print "���� http ���� ��ipΪ"+ip+"�󶨶˿�Ϊ��"+str(port)
    HOST, PORT = ip, int(port)
    httpserver = HTTPServer((HOST, PORT), handleClass)
    httpserver.serve_forever()

