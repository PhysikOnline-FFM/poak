from manage_worksheets.models import Tag, Worksheet
from django.http import HttpResponse
import json
from poak.settings import POKAL_URL
from django.core.urlresolvers import reverse

#
# This file contains the server side code for the AJAX on the frontpage
#

def jsonify(dictionary):
    """
    Encodes dictionaries in JSON
    """
    return HttpResponse(json.dumps(dictionary), mimetype='application/json')

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
    return jsonify(tag_dict)

def worksheet_details(request, worksheet_id):
    """
    returns the properties of the worksheet with the provided ID
    if no such worksheet exists, the response is empty
    """

    try:
        worksheet = Worksheet.objects.get(worksheet_id=worksheet_id)
    except Worksheet.DoesNotExist:
        return jsonify({}) # empty response
    return jsonify(worksheet.data())

def worksheets_for_tag(request, tag_id):
    """
    returns all worksheets that are tagged with the given tag
    if no such tag exists, the response is empty
    """

    try:
        tag = Tag.objects.get(id=tag_id)
    except Tag.DoesNotExist:
        return jsonify({}) # empty response
    ws_list = [w.worksheet_id for w in tag.worksheet_set.all()]
    return jsonify({'worksheet_list':ws_list})

def worksheet_list(request):
    """
    returns the IDs of all worksheets and the POKAL base url to which
    the ID can be appended to get the complete URL of the worksheet
    """

    # details base url
    dbu = reverse('manage_worksheets:details', args=[''])

    ws_list = [w.worksheet_id for w in Worksheet.objects.all()]
    return jsonify({'worksheet_list':ws_list, 'pokal_url':POKAL_URL,
                'details_base_url':dbu,
                })

def minus_tag(request, tag_id):
    """
    returns all worksheets that have to be removed from a list
    after unchecking the given tag
    """

    try:
        tag = Tag.objects.get(id=tag_id)
        # get the list of tags that are still checked
        checked_tags = [Tag.objects.get(id=ch_tag_id) for ch_tag_id in request.GET.getlist('checked_tags[]')]
    except Tag.DoesNotExist:
        return jsonify({}) # empty response


    ws_list = []

    for w in tag.worksheet_set.all():
        found = False
        for ch_tag in checked_tags:
            if ch_tag.worksheet_set.filter(pk=w.pk).exists():
                found = True
                break
        if not found:
            ws_list.append(w.worksheet_id)
                
    return jsonify({'worksheet_list':ws_list})

