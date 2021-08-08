#!/usr/bin/python
#
import sys, os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from lib.get_mylogger import apllogger

import requests
import itertools



class ApolloAccoutAuth(object):
    def __init__(self, login_page='http://domain.com/signin', login_data={"username": 'apollo',"password": 'xxxxx', 'login-submit': '登录'}, headers=None):
        self.login_page = login_page
        self.login_data = login_data
        self.headers = headers

        self.__session = requests.session()
        self.__s = self.__session.post(url=self.login_page, data=self.login_data, headers=self.headers)

    '''url_args参数为字典'''
    def get_data(self, url, url_args=None, headers=None, method='get'):
        if method == 'get':
            data = self.__session.get(url=url, headers=headers)
            return data.json()
        else:
            data = self.__session.post(url=url, data=url_args, headers=headers)
            return data.json()


    def authHandle(self, url, user, headers={'Content-Type': 'text/plain'}):
        returnData = {}

        try:
            result = self.__session.post(url=url, data=user, headers=headers)

        except Exception as e:
            print(f"连接{url}失败，检查URL或网络连接...")
            sys.exit(111)

        else:
            if result.status_code == 200:
                apllogger.info(f"用户：{user} 授权到：{url}成功###")
            else:
                apllogger.error(f"用户：{user} 授权到：{url}失败！！！，失败原因：{result.json()}")


if __name__ == '__main__':
    productinit = input('输入要授权的产品 (xxx|xxx)：')
    product = 'domain.com' if productinit == 'xxx' else 'domian.com'
    login_page = 'http://domain.com/signin' if productinit == 'xxx' else 'http://domain.com/signin'

    appidinit = input('输入要授权的工程，以(,)分隔：')
    appidList = appidinit.split(',')

    userinit = input('输入要授权的用户，以(,)分隔，直接回车授权为授权运维部所有用户：')
    userList = userinit.split(',') if userinit else {}

    #env = ['DEV', 'FAT']
    env = ['UAT', 'PRO']
    urlinit = itertools.product(appidList, env)
    urlList = set()
    for U in urlinit:
        murl = f"http://{product}/apps/{U[0].strip()}/envs/{U[1]}/namespaces/application/roles/ModifyNamespace"
        rurl = f"http://{product}/apps/{U[0].strip()}/envs/{U[1]}/namespaces/application/roles/ReleaseNamespace"
        #murl = f"http://{product}/apps/{U[0].strip()}/envs/{U[1]}/namespaces/db.oracle/roles/ModifyNamespace"
        #rurl = f"http://{product}/apps/{U[0].strip()}/envs/{U[1]}/namespaces/db.oracle/roles/ReleaseNamespace"
        #murl = f"http://{product}/apps/{U[0].strip()}/envs/{U[1]}/namespaces/common/roles/ModifyNamespace"
        #rurl = f"http://{product}/apps/{U[0].strip()}/envs/{U[1]}/namespaces/common/roles/ReleaseNamespace"
        urlList.add(murl)
        urlList.add(rurl)

    # handle auth
    Apollo = ApolloAccoutAuth(login_page=login_page)

    for url in urlList:
        for user in userList:
            Apollo.authHandle(url, user.strip())

