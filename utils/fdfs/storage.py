import os

from django.core.files.storage import Storage
from fdfs_client.client import Fdfs_client
from Nchu_UTP.settings import FDFS_URL, FDFS_CLIENT_CONF


class FastDFS_Storage(Storage):
    '''fastdfs文件存储类'''
    def __init__(self, client_conf=None, base_url=None):
        '''初始化'''
        if client_conf is None:
            client_conf = FDFS_CLIENT_CONF
            self.client_conf = client_conf
        if base_url is None:
            base_url = FDFS_URL
            self.base_url = base_url

    def _open(self, name, mode='rb'):
        '''打开文件'''
        pass
    def _save(self, name, content):
        '''保存文件'''
        # name:选择上传文件的名字
        # content:包含你上传文件内容的File对象

        # 创建一个Fdfs_client对象
        client = Fdfs_client(self.client_conf)
        print(1111111)
        print(content)
        # 获取文件拓展名
        ext = str(content).split(".")[1]

        # 上传文件到fast_dfs系统中

        res = client.upload_by_buffer(content.read(), file_ext_name=ext)

        #return dict
        #{
        #    'Group name': group_name,
        #    'Remote file_id': remote_file_id,
        #    'Status': 'Upload successed.',
        #    'Local file name': local_file_name,
        #    'Uploaded size': upload_size,
        #    'Storage IP': storage_ip
        #} if success else None

        if res.get('Status') != 'Upload successed.':
            raise Exception('上传文件到FastDFS失败')

        # 获取返回的文件ID
        filename = res.get('Remote file_id')
        print(2222222)
        print(filename)
        return filename

    def exists(self, name):
        '''Django判断文件名是否可用'''
        return False

    def url(self, name):
        path = self.base_url + name
        return path