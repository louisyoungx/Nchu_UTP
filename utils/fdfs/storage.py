from django.core.files.storage import Storage
from fdfs_client.client import Fdfs_client

from Nchu_UTP.settings import FDFS_URL


class FastDFS_Storage(Storage):
    '''fastdfsw文件存储类'''
    def _open(self, name, mode='rb'):
        '''打开文件'''
        pass
    def _save(self, name, content):
        '''保存文件'''
        # name:选择上传文件的名字
        # content:包含你上传文件内容的File对象

        # 创建一个Fdfs_client对象
        client = Fdfs_client('./utils/fdfs/client.conf')

        # 上传文件到fast_dfs系统中
        res = client.upload_by_buffer(content.read())

        print(res.get('Storage IP'))
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

        return filename

    def exists(self, name):
        '''Django判断文件名是否可用'''
        return False

    def url(self, name):
        path = FDFS_URL+name
        return path