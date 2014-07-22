from django.shortcuts import render
from manage_worksheets.models import Tag
from django.http import HttpResponse
from django.utils import simplejson

def json(dict):
    """
    Encodes dictionaries in JSON
    """
    return HttpResponse(simplejson.dumps(dict), mimetype='application/json')

def tags(request):
    tag_list = [t.name for t in Tag.objects.all()]
    # endocde in JSON
    tag_dict ={'tags':tag_list}
    return json(tag_dict)


def main(request):
    return render(request, "manage_worksheets/index.html")
