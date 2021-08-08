#!/usr/bin/env python3.6
# -*- coding: utf-8 -*-

import os, sys,json

import smtplib
from email.mime.text import MIMEText
from email.header import Header

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from lib.get_config import get_config, Base_Dir
from lib.supplier_api import *
from lib.get_mylogger import mylogger



no_recharge = '无需充值'
need_recharge = '需要充值!!!!!'
get_data_except = '获取数据异常!!!'


def getTencentData(secretId, secretKey, checkData, minimumBal=5000, minimumCdn=1000):
    returnData = {}

    if checkData == 'balance':
        try:
            t = Tencent_Api(action='DescribeAccountBalance', url='https://xxx.com', secretId=secretId, secretKey=secretKey)
            bal_result = t.check_accout_balance()

            returnData['bal'] = bal_result['Balance']
            returnData['recharge'] = no_recharge if int(str(bal_result['Balance']).split('.')[0]) > minimumBal else need_recharge
            returnData['minimumBal'] = minimumBal
            mylogger.info(f"获取腾讯云余额成功，本次操作返回结果：{returnData}")
            return returnData

        except Exception as e:
            returnData['bal'] = get_data_except
            returnData['recharge'] = get_data_except
            returnData['minimumBal'] = get_data_except
            mylogger.error(f"获取腾讯云余额异常，具体异常为：{e}, {bal_result}")
            return returnData


    elif checkData == 'cdn':
        try:
            t = Tencent_Api(action='GetPackage', url='https://xxx.com/v2/index.php', secretId=secretId, secretKey=secretKey)
            cdn_result = t.check_cdn_balance(offset=0, limit=10)

            t_cdn_all = 0
            t_cdn_use = 0
            for c in cdn_result['data']:
                t_cdn_all += c['flux_byte']
                t_cdn_use += c['flux_used']
            t_cdn_bal_str = str((t_cdn_all - t_cdn_use) / 1000000000)
            t_cdn_bal = float(f"{t_cdn_bal_str.split('.')[0]}.{t_cdn_bal_str.split('.')[1][:2]}")

            returnData['bal'] = f"{t_cdn_bal}"
            returnData['recharge'] = no_recharge if int(str(returnData['bal']).split('.')[0]) > minimumCdn else need_recharge
            returnData['minimumCdn'] = minimumCdn
            mylogger.info(f"获取腾讯云CDN流量包余额成功，本次操作返回结果：{returnData}")
            return returnData

        except Exception as e:
            returnData['bal'] = get_data_except
            returnData['recharge'] = get_data_except
            returnData['minimumCdn'] = get_data_except
            mylogger.error(f"获取腾讯云CDN流量包余额异常，具体异常为：{e}, {cdn_result}")
            return returnData
    else:
        return None



def getAliData(accessKeyId, accessSecret, checkData):
    returnData = {}

    if checkData == 'balance':
        try:
            a = Ali_Api('business.ap-southeast-1.aliyuncs.com', 'QueryAccountBalance', '2017-12-14', accessKeyId, accessSecret)

            bal_result = a.check_accout_balance()
            returnData['bal'] = bal_result['data']['AvailableAmount']
            returnData['recharge'] = no_recharge if int(returnData['bal'].split('.')[0].replace(',', '')) > 1000 else need_recharge
            mylogger.info(f"获取阿里云余额成功，本次操作返回结果：{returnData}")
            return returnData

        except Exception as e:
            returnData['bal'] = get_data_except
            returnData['recharge'] = get_data_except
            mylogger.error(f"获取阿里云余额异常，具体异常为：{e}, {bal_result}")
            return returnData


    elif checkData == 'cdn':
        try:
            a = Ali_Api('cdn.aliyuncs.com', 'DescribeCdnUserResourcePackage', '2018-05-10', accessKeyId, accessSecret)

            cdn_result = a.check_cdn_balance()
            a_cdn_all = 0
            for c in cdn_result['data']:
                a_cdn_all += int(c['CurrCapacity'])
            a_cdn_bal_str = str(a_cdn_all / 1000000000)
            a_cdn_bal = float(f"{a_cdn_bal_str.split('.')[0]}.{a_cdn_bal_str.split('.')[1][:2]}")

            returnData['bal'] = f"{a_cdn_bal}"
            returnData['recharge'] = no_recharge if int(returnData['bal'].split('.')[0]) > 500 else need_recharge
            mylogger.info(f"获取阿里云CDN流量包余额成功，本次操作返回结果：{returnData}")
            return returnData

        except Exception as e:
            returnData['bal'] = get_data_except
            returnData['recharge'] = get_data_except
            mylogger.error(f"获取阿里云CDN流量包余额异常，具体异常为：{e}, {cdn_result}")
            return returnData
    else:
        return None



def getYunpianData(mainUrl, headers, apikey):
    returnData = {}

    try:
        y = YunPian_Api(mainUrl, headers, apikey)

        y_result = y.check_accout_balance()
        returnData['bal'] = str(y_result['data']['balance'])
        returnData['recharge'] = no_recharge if int(returnData['bal'].split('.')[0]) > 1000 else need_recharge
        mylogger.info(f"获取云片余额成功，本次操作返回结果：{returnData}")
        return returnData

    except Exception as e:
        returnData['bal'] = get_data_except
        returnData['recharge'] = get_data_except
        mylogger.error(f"获取云片余额异常，具体异常为：{e}, {y_result}")
        return returnData



def getNamecheapData(mainUrl, apiuser, apikey, username, clientip, command):
    returnData = {}

    try:
        n = Namecheap_Api(mainUrl, apiuser, apikey, username, clientip, command)

        n_result = n.get_balances()
        returnData['bal'] = str(n_result['data'])
        returnData['recharge'] = no_recharge if int(returnData['bal'].split('.')[0]) > 3000 else need_recharge
        mylogger.info(f"获取余额成功，本次操作返回结果：{returnData}")
        return returnData

    except Exception as e:
        returnData['bal'] = get_data_except
        returnData['recharge'] = get_data_except
        mylogger.error(f"获取余额异常，具体异常为：{e}, {n_result}")
        return returnData


def get_mxt_bal(bal_url, user_id, account_info):
    returnData = {}

    req_data_list = [{'UserID': user_id, 'Account': k, 'Password': v} for i in range(len(account_info)) for k,v in account_info[i].items()]
    for reqdata in req_data_list:
        m = MxtBalApi(bal_url, reqdata)
        m_result = m.get_info()

        tmp_data = {}
        tmp_ac = reqdata['Account']
        minimum_bal = 10000 if 'product' in tmp_ac else 3000

        if m_result['status'] == 'Success':
            tmp_data['bal'] = m_result['data']
            tmp_data['recharge'] = no_recharge if int(m_result['data']) > minimum_bal else need_recharge
            mylogger.info(f"获取账号{tmp_ac}余量成功，本次操作返回结果：{m_result}")
        else:
            tmp_data['bal'] = get_data_except
            tmp_data['recharge'] = get_data_except
            mylogger.error(f"获取账号{tmp_ac}余量失败，具体返回异常为：{m_result}")

        returnData[tmp_ac] = tmp_data

    return returnData


def sendMail(sendmessage):
    try:
        sender = 'xxx.com'
        receivers = ['xxx.comm', 'xxx.com']   # 邮件接收人
        send_message = sendmessage

        message = MIMEText(send_message, 'html', 'utf-8')
        message['From'] = Header("xxx.com")
        message['To'] = Header("xxx.com>; xxx.com")
        message['Subject'] = Header("腾讯云、阿里云、云片、Namecheap 查询", 'utf-8')

        smtpobj = smtplib.SMTP('mail.xxx.com')
        smtpobj.sendmail(sender, receivers, message.as_string())
    except Exception as e:
        mylogger.error(f"发送邮件失败，异常原因：{e}")
        sys.exit(111)



if __name__ == '__main__':
    #1.get all config
    Tconfig = get_config('')
    Aconfig = get_config('')
    Yconfig = get_config('')
    Nconfig = get_config('')

    #2.get all data
    #Tencent
    productTencentAccountBal = getTencentData(Tconfig['product']['SecretId'], Tconfig['product']['SecretKey'], 'balance')
    productTencentCdnBal = getTencentData(Tconfig['product']['SecretId'], Tconfig['product']['SecretKey'], 'cdn')
    productTencentAccountBal = getTencentData(Tconfig['product']['SecretId'], Tconfig['product']['SecretKey'], 'balance', minimumBal=1000)
    productTencentCdnBal = getTencentData(Tconfig['product']['SecretId'], Tconfig['product']['SecretKey'], 'cdn', minimumCdn=500)
    productTencentAccountBal = getTencentData(Tconfig['product']['SecretId'], Tconfig['product']['SecretKey'], 'balance', minimumBal=1000)
    productTencentCdnBal = getTencentData(Tconfig['product']['SecretId'], Tconfig['product']['SecretKey'], 'cdn', minimumCdn=500)
    #Aliyun
    aliAccountBal = getAliData(Aconfig['accessKeyId'], Aconfig['accessSecret'], 'balance')
    aliCdnBal = getAliData(Aconfig['accessKeyId'], Aconfig['accessSecret'], 'cdn')
    #Yunpian
    yunpianAccoutBal = getYunpianData(Yconfig['mainUrl'], Yconfig['headers'], Yconfig['apikey'])
    productyunpianAccoutBal = getYunpianData(Yconfig['mainUrl'], Yconfig['headers'], Yconfig['productApiKey'])
    #Namecheap
    ncAccoutBal = getNamecheapData(Nconfig['mainUrl'], Nconfig['apiuser'], Nconfig['apikey'], Nconfig['username'], Nconfig['clientip'], Nconfig['command'])
    #MXT
    MxtBal = get_mxt_bal(MxtConfig['BalUrl'], MxtConfig['UserID'], MxtConfig['AccountInfo'])

    #3.send email to SA
    allProductInfo = list()
    allProductInfo.append(productTencentAccountBal)
    allProductInfo.append(productTencentCdnBal)
    allProductInfo.append(productTencentAccountBal)
    allProductInfo.append(productTencentCdnBal)
    allProductInfo.append(productTencentAccountBal)
    allProductInfo.append(productTencentCdnBal)
    allProductInfo.append(aliAccountBal)
    allProductInfo.append(aliCdnBal)
    allProductInfo.append(yunpianAccoutBal)
    allProductInfo.append(productyunpianAccoutBal)
    allProductInfo.append(ncAccoutBal)
    allProductInfo.append(MxtBal)

    from lib.balance_message_html import BalMegHtml
    send_message = BalMegHtml(*allProductInfo)

    sendMail(send_message)

