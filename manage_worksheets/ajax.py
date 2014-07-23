from manage_worksheets.models import Tag, Worksheet
from django.http import HttpResponse
from django.utils import simplejson
from poak.settings import POKAL_URL

#
# This file contains the server side code for the AJAX on the frontpage
#

def json(dictionary):
    """
    Encodes dictionaries in JSON
    """
    return HttpResponse(simplejson.dumps(dictionary), mimetype='application/json')

def _tags():
    return [[t.id, t.name] for t in Tag.objects.all()]

def tags(request):
    """
    returns all tags in JSON
    """

    del request # unused argument
    tag_list = _tags()
    # endocde in JSON
    tag_dict ={'tags':tag_list}
    return json(tag_dict)

def worksheet_details(request, worksheet_id):
    """
    returns the properties of the worksheet with the provided ID
    if no such worksheet exists, the response is empty
    """

    try:
        worksheet = Worksheet.objects.get(worksheet_id=worksheet_id)
    except Worksheet.DoesNotExist:
        return json({}) # empty response
    return json(worksheet.data())

def worksheets_for_tag(request, tag_id):
    """
    returns all worksheets that are tagged with the given tag
    if no such tag exists, the response is empty
    """

    try:
        tag = Tag.objects.get(id=tag_id)
    except Tag.DoesNotExist:
        return json({}) # empty response
    ws_list = [w.worksheet_id for w in tag.worksheet_set.all()]
    return json({'worksheet_list':ws_list})

def worksheet_list(request):
    """
    returns the IDs of all worksheets and the POKAL base url to which
    the ID can be appended to get the complete URL of the worksheet
    """

    ws_list = [w.worksheet_id for w in Worksheet.objects.all()]
    return json({'worksheet_list':ws_list, 'pokal_url':POKAL_URL})
