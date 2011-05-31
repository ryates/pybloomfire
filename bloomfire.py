import json
from urllib import urlencode
import urllib2

class API(object):
    """
        API object that provides a Python binding to the Bloomfire REST API: http://bloomfire.com
    """
    
    def __init__(self, subdomain, api_key, auth_email, auth_password):
        self._api_key = api_key
        self._endpoint_prefix = 'https://%s.bloomfire.com/api/' % subdomain
        
        self._authenticate(auth_email, auth_password)
        
        
    
    def _authenticate(self, auth_email, auth_password):
        passman = urllib2.HTTPPasswordMgrWithDefaultRealm()
        passman.add_password(None, self._endpoint_prefix, auth_email, auth_password)
        authhandler = urllib2.HTTPBasicAuthHandler(passman)
        opener = urllib2.build_opener(authhandler)
        urllib2.install_opener(opener)
    
    def get(self, api_name, kwargs=None):
        if kwargs:
            endpoint_query = '?%s' % urlencode(kwargs)
        else:
            endpoint_query = ''
        return self._call('%s%s.json%s' % (self._endpoint_prefix, api_name, endpoint_query))
    
    def post(self, api_name, kwargs=None):
        req = urllib2.Request(url='%s%s.json' % (self._endpoint_prefix, api_name), data=urlencode(kwargs))
        return self._call(req)
    
    def _call(self, request):
        
        try:
            result = urllib2.urlopen(request)
            response_dict = json.loads(result.read())
        except urllib2.HTTPError as http_error:
            response_dict = json.loads(http_error.read())
        return response_dict

