from django.shortcuts import render, get_object_or_404
from manage_worksheets.models import Tag, Worksheet
from django.http import HttpResponseRedirect
from django.core.urlresolvers import reverse
from poak.settings import POKAL_URL


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
