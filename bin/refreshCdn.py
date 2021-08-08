#/usr/bin/python
#
import sys, os

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from lib.get_config import get_config, Base_Dir
from lib.supplier_api import *
from lib.cdn_api import *
#from lib.get_mylogger import mylogger


select_product = sys.argv[1]
refresh_url = sys.argv[2]


def main():
    Aconfig = get_config('Ali')
    Tconfig = get_config('Tencent')
    Cconfig = get_config('Cloudflare')
    Qconfig = get_config('Quansuyun')
    Uconfig = get_config('UDomain')


    # 阿里云
    if select_product == 'ali':
        A = Ali_Api(refresh_url, 'RefreshObjectCaches', 'version', Aconfig['accessKeyId'], Aconfig['accessSecret'])
        print(A.refresh_cdn(Aconfig['refresh_type'], refresh_url))


    # 腾讯云
    elif select_product == 'tx':
        xxxList1 = Tconfig['domain_list']['']
        xxxList2 = Tconfig['domain_list']['']
        url = 'https://cdn.api.qcloud.com/v2/index.php'

        if refresh_url in xxxList1:
            T = Tencent_Api(action='RefreshCdnDir', url=url, secretId=Tconfig['']['SecretId'], secretKey=Tconfig['']['SecretKey'])
        elif refresh_url in xxxList2:
            T = Tencent_Api(action='RefreshCdnDir', url=url, secretId=Tconfig['']['SecretId'], secretKey=Tconfig['']['SecretKey'])
        else:
            T = Tencent_Api(action='RefreshCdnDir', url=url, secretId=Tconfig['']['SecretId'], secretKey=Tconfig['']['SecretKey'])

        print(T.refresh_cdn(refresh_url))


    # Cloudflare
    elif select_product == 'cf':
        C = Cloudflare_Api_Purge(Cconfig['mainUrl'], Cconfig['recordUrl'], Cconfig['purgeUrl'], Cconfig['headers'])
        print(C.purge_everything(refresh_url))


    # 网宿云
    elif select_product == 'wx':
        Q = QuansuCloud_Api(Qconfig['mainUrl'], Qconfig['username'], Qconfig['apikey'])
        print(Q.refresh_cdn(refresh_url))


    # UDomain
    elif select_product == 'ud':
        url_list = []
        url_list.append(refresh_url)

        U = UdomainCacheUrl(Uconfig)
        print(U.purge_cache_url(url_list))


    else:
        print('产品选择错误，请确认!!!')
        sys.exit(111)


if __name__ == '__main__':
    main()
