# -*- coding: utf-8 -*-
from django.http import HttpResponse
import json

def jsonify(dictionary):
    """
    Encodes dictionaries in JSON
    """
    return HttpResponse(json.dumps(dictionary), mimetype='application/json')

def getlog(request, worksheet):
    """
    return the log for the worksheet
    """
    dic = {'messages':
            [
            {'content':'Hi, wie geht\'s?', 'datetime':'2014-08-05 16:54:14',
                'user':'Hans'},
            {'content':'Joa, ganz gut.', 'datetime':'2014-08-05 16:55:43',
                'user':'Peter'},
            {'content':'Das ist doch schön.', 'datetime':'2014-08-05 16:56:23',
                'user':'Hans'},
            ],}
    return jsonify(dic)
