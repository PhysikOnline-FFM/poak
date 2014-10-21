from poak.settings import POKAL_UNAME_SCRIPT
import requests
import re
from django.http import HttpResponse
import json

def get_POKAL_username(request):
    url = POKAL_UNAME_SCRIPT
    r = requests.get(url, cookies=request.COOKIES)
    try:
        data = r.text
        # some regex magic
        m1 = re.search(r'username\s=\s"(\w+?)"', data)
        username = m1.group(1)
        #m2 = re.search(r'nickname\s=\s"(\w+?)"', data)
        #nickname = m2.group(1)
    except AttributeError:
        return None

    return username

def jsonify(dictionary):
    """
    Encodes dictionaries in JSON
    """
    return HttpResponse(json.dumps(dictionary), mimetype='application/json')
