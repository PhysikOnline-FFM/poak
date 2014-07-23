from django.shortcuts import render, get_object_or_404
from manage_worksheets.models import Tag, Worksheet
from django.http import HttpResponse, HttpResponseRedirect
from django.core.urlresolvers import reverse
from django.utils import simplejson
from poak.settings import POKAL_URL

def json(dict):
    """
    Encodes dictionaries in JSON
    """
    return HttpResponse(simplejson.dumps(dict), mimetype='application/json')

def _tags():
    return [t.name for t in Tag.objects.all()]

def tags(request):
    tag_list = _tags()
    # endocde in JSON
    tag_dict ={'tags':tag_list}
    return json(tag_dict)

def worksheet_details(request, worksheet_id):
    try:
        worksheet = Worksheet.objects.get(worksheet_id=worksheet_id)
    except Worksheet.DoesNotExist:
        return json({}) # empty response
    return json(worksheet.data())

def worksheet_list(request):
    ws_list = [w.worksheet_id for w in Worksheet.objects.all()]
    return json({'worksheet_list':ws_list, 'pokal_url':POKAL_URL})

def main(request):
    return render(request, "manage_worksheets/index.html")

def submit(request):
    return render(request, "manage_worksheets/submit.html", {
        'tags':Tag.objects.all(),
        })

def takedata(request):
    """
    receive data from submit, if everything is ok, show the details page
    of the new entry
    """
    id = "0"
    return HttpResponseRedirect(reverse('manage_worksheets:details', args=id))

def details(request, worksheet_id):
    worksheet = get_object_or_404(Worksheet, worksheet_id=worksheet_id)
    return render(request, "manage_worksheets/details.html", {
        'worksheet': worksheet,
        'pokal_url': POKAL_URL,
        })
