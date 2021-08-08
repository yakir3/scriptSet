#!/usr/bin/env python3.6
# -*- coding: utf-8 -*-
import requests
import json


__all__ = [
    'UdomainSubdomain',
    'UdomainConfiguration',
    'UdomainCacheUrl',
    'UdomainCertificate'
]


UDOMAIN_API_HOST = ''
GREY_API_HOST = ''


class _ApiBase(object):

    def __init__(self, auth_header, api_host=None):
        self.auth_header = auth_header
        self.api_host = api_host if api_host else UDOMAIN_API_HOST
        self.endpoint = ''

    def _do(self, method, relative_path=None, **kwargs):
        """
        method:: put, get, post, delete

        """
        try:
            url = self.api_host + self.endpoint + (relative_path if relative_path else '')
            res = requests.request(method,
                                   url,
                                   headers=self.auth_header,
                                   **kwargs)

            return res

        except Exception as e:
            return_data = {}
            return_data['code'] = 111
            return_data['msg'] = f"请求{url}失败，检查网络！"
            return return_data



class UdomainSubdomain(_ApiBase):
    """
    CDN Domain --> create, delete, change status, domain info
    """
    def __init__(self, auth_header, api_host=None):
        super(UdomainSubdomain, self).__init__(auth_header, api_host)
        self.endpoint = '/c/v1/subdomain'
        # self.domainName = domainName


    def create_cdn(self, subdomainName, httpOrigin, httpsOrigin, originPolicy='FOLLOW'):
        """
        Parameters
        ----------
        origin:  dict  -->  key need originPolicy and httpOrigin and httpsOrigin
            originPolicy: string -->  HTTP or HTTPS or FOLLOW
            httpOrigin: list
              example:
                [
                  {"address": "1.1.1.1","port": "80"},
                  {"address": "2.2.2.2","port": "80"}
                ]
            httpsOrigin: list like httpOrigin (port is 443)
        """
        data = json.dumps({
            'subdomainName': subdomainName,
            'origin': {
                'originPolicy': originPolicy,
                'httpOrigin': httpOrigin,
                'httpsOrigin': httpsOrigin
            }
        })

        resp = self._do('POST', data=data)
        return resp.json()


    def delete_cdn(self):
        pass


    def change_status(self):
        pass


    def get_info(self, domainId=None, getAll=None):
        """
        Returns
        -------
        customerID: UDomain unique customer identifier
        subdomainCNAME: The CNAME system created for the CDN domain
        ...

        """
        if getAll:
            resp = self._do('GET')
        else:
            resp = self._do('GET', relative_path=f"/{domainId}")
        return resp.json()



class UdomainConfiguration(_ApiBase):
    pass



class UdomainCacheUrl(_ApiBase):
    def __init__(self, auth_header, api_host=None):
        super(UdomainCacheUrl, self).__init__(auth_header, api_host)
        self.endpoint = '/c/v1/cache'


    def get_cache_list(self):
        """
        Returns
        -------
        type:: PUSH or PURGE
        status:: NEW or PROCESSING or APPLIED

        """
        resp = self._do('GET')
        return resp.json()


    def purge_cache_url(self, purge_url_list):
        data = json.dumps({'url': purge_url_list})

        resp = self._do('POST', '/purge', data=data)
        return resp.json()


    def push_cache_url(self, push_url_list):
        """
        ::params push_url_list::  domain list, type must be list
        """
        data = json.dumps({'url': push_url_list})

        resp = self._do('POST', '/push', data=data)
        return resp.json()



class UdomainCertificate(_ApiBase):
    """
    Certificate:  upload,delete,info
    """
    def __init__(self, auth_header, api_host=None):
        super(UdomainCertificate, self).__init__(auth_header, api_host)
        self.endpoint = '/c/v1/certificate'
        #self.domainName = domainName


    def get_certificate_list(self):
        """get all certificate info"""
        resp = self._do('GET')

        return resp.json()


    def upload_certificate(self, domainName, privateKey, publicKey):
        """
        ::domainName::  string  certificate name
        ::privateKey::  string  read key certificate to string
        ::publicKey::   string  read crt certificate to string
        """
        data = json.dumps({
            'certificateName': domainName,
            'privateKey': privateKey,
            'publicKey': publicKey
        })

        resp = self._do('POST', data=data)

        return resp.json()


    def delete_certificate(self):
        pass


class GreyCacheApi(_ApiBase):

    def __init__(self, auth_header, api_host=GREY_API_HOST):
        super(GreyCacheApi, self).__init__(auth_header, api_host)
        self.auth_header = auth_header
        #self.endpoint = endpoint


    def get_all_site_info(self):
        """
        Returns
        -------
        """
        resp = self._do('POST', '/api/v1/site/list/all')
        return resp.json()


    def purge_cache_site(self, uid):
        #data = json.dumps({'uid': uid})
        parms = {'uid': uid}

        resp = self._do('POST', '/api/v1/cache/purge/by-site', params=parms)
        return resp.json()


    def purge_cache_uri(self, uid, uri):
        """
        ::params
        """
        parms = {'uid': uid}
        data = json.dumps({'uri': uri})

        resp = self._do('POST', '/api/v1/cache/purge/by-site-uri', params=parms, data=data)
        return resp.json()



if __name__ == '__main__':
    pass

