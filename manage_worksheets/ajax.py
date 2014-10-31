from manage_worksheets.models import Tag, Worksheet
from poak.settings import POKAL_URL
from django.core.urlresolvers import reverse
from functions import get_POKAL_username
from django.http import JsonResponse

#
# This file contains the server side code for the AJAX on the frontpage
#

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
    return JsonResponse(tag_dict)

def worksheet_details(request, worksheet_pk):
    """
    returns the properties of the worksheet with the provided ID
    if no such worksheet exists, the response is empty
    """

    try:
        worksheet = Worksheet.objects.get(pk=worksheet_pk)
    except Worksheet.DoesNotExist:
        return JsonResponse({}) # empty response
    return JsonResponse(worksheet.data())

def worksheets_for_tag(request, tag_id):
    """
    returns all worksheets that are tagged with the given tag
    if no such tag exists, the response is empty
    """

    try:
        tag = Tag.objects.get(id=tag_id)
    except Tag.DoesNotExist:
        return JsonResponse({}) # empty response
    ws_list = [w.pk for w in tag.worksheet_set.all()]
    return JsonResponse({'worksheet_list':ws_list})

def worksheet_list(request):
    """
    returns the IDs of all worksheets and the POKAL base url to which
    the ID can be appended to get the complete URL of the worksheet
    """

    # details base url
    dbu = reverse('manage_worksheets:details', args=[''])

    ws_list = [w.pk for w in Worksheet.objects.all()]
    return JsonResponse({'worksheet_list':ws_list, 'pokal_url':POKAL_URL,
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
        return JsonResponse({}) # empty response


    ws_list = []

    for w in tag.worksheet_set.all():
        found = False
        for ch_tag in checked_tags:
            if ch_tag.worksheet_set.filter(pk=w.pk).exists():
                found = True
                break
        if not found:
            ws_list.append(w.pk)

    return JsonResponse({'worksheet_list':ws_list})

def move(request, from_id, to_id):
    try:
        worksheet = Worksheet.objects.get(worksheet_id=from_id)
    except Worksheet.DoesNotExist:
        return JsonResponse({'status':'failure', 'from_id':from_id})

    # test if the operation is allowed
    username = get_POKAL_username(request)
    if username != worksheet.owner:
        #return JsonResponse({'status':'failure'})
        pass

    worksheet.worksheet_id = to_id
    worksheet.save()
    return JsonResponse({'status':'OK', 'from_id':from_id, 'to_id':to_id})
