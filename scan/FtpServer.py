# coding:GBK

import os

from pyftpdlib.authorizers import DummyAuthorizer
from pyftpdlib.handlers import FTPHandler
from pyftpdlib.servers import FTPServer


def main():
    # ʵ�����û���Ȩ����
    authorizer = DummyAuthorizer()
    authorizer.add_user('user', '12345', 'C://', perm='elradfmwMT')  # ����û� ����:username,password,�����·��,Ȩ��
    authorizer.add_anonymous(os.getcwd())  # ���������������û�,���������ɾ�����м���

    # ʵ����FTPHandler
    handler = FTPHandler
    handler.authorizer = authorizer

    # �趨һ���ͻ�������ʱ�ı���
    handler.banner = "welcome I.am wwh."

    handler.masquerade_address = '151.25.42.11'#ָ��αװip��ַ
    handler.passive_ports = range(60000, 65535)#ָ������Ķ˿ڷ�Χ

    address = ("127.0.0.1", 21)  # FTPһ��ʹ��21,20�˿�
    server = FTPServer(address, handler)  # FTP������ʵ��

    # set a limit for connections
    server.max_cons = 256
    server.max_cons_per_ip = 5

    # ����������
    server.serve_forever()


if __name__ == '__main__':
    main()
