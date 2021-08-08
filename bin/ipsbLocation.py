#!/usr/bin/python
#
import sys, os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
#from lib.get_mylogger import mylogger
from lib.get_config import get_config, Base_Dir
from lib.color import *
import requests
from bs4 import BeautifulSoup



ip_init = input(f"{yellow}请输入要查询的IP(已,为分隔符),留空则从文件 {Base_Dir}/bin/ip.txt 读入IP：{end}")
with open(f"{Base_Dir}/bin/ip.txt", 'r') as f:
    ips = ip_init.split(',') if ip_init else f.read().splitlines()

url = 'https://ip.sb/ip/'
urls = map(lambda x: f"{url}{x}", ips)

finally_params = dict(zip(ips, urls))


def ipsbRequest(ip, url):
    returnData = {}
    try:
        result = requests.get(url=url)
        html = result.text
        soup = BeautifulSoup(html, features="lxml")
        td = soup.find('table', class_='table').find_all('td')

        returnData['result'] = 'successful'
        returnData['IP'] = ip
        returnData['ISP'] = td[2].string
        lctf = td[-1].string.split(',')
        returnData['Location'] = f"{lctf[0].strip()} , {lctf[1].strip()}"

    except Exception as e:
        returnData['result'] = 'failed'

    finally:
        return returnData


def ipCheck(finally_params):
    for ip in finally_params.keys():
        ipinfo = ipsbRequest(ip, finally_params[ip])
        if ipinfo['result'] == 'successful':
            #print(f"{green}IP：{ip}\tISP: {ipinfo['ISP']}\tLocation：{ipinfo['Location']}{end}\n")
            print("{0}{1:<30}{2:<50}{3:<30}{4}\n".format(green, f"IP：{ip}", f"ISP: {ipinfo['ISP']}", f"Location：{ipinfo['Location']}", end))
        else:
            print(f"{red}IP：{ip}\t 获取数据异常\n{end}")


if __name__ == '__main__':
    ipCheck(finally_params)

