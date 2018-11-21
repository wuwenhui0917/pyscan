# coding:GBK
from BaseHTTPServer import HTTPServer, BaseHTTPRequestHandler
import threading
from configfile import *
from multiprocessing import Process
from scanwebsite import *


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
        scanobj = ScanWebSite(scanUrl=self.scanurl, logname=str(self.transid)+".log")
        scanobj.start()

        # print self.getName()
        # self.server.send_response(200)
        # self.server.send_header('Content-type', 'text/html')
        # self.server.end_headers()
        # self.server.end_headers()
        # self.send_response(200)

        # self.server.send_response(200,"hello")
        # self.server.finish()
        # self.server.wfile.write("hello====")


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
    print '����http'
    config = ConfigFile()
    ip = config.getvalue("bindip")
    port = config.getvalue("port")

    print "���� http ���� ��ipΪ"+str(ip)+"�󶨶˿�Ϊ��"+str(port)
    HOST, PORT = str("127.0.0.1"), int(port)

    httpserver = HTTPServer((HOST,PORT), handleClass)
    httpserver.serve_forever()

