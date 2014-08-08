from django.shortcuts import render, get_object_or_404
from manage_worksheets.models import Tag, Worksheet
from django.http import HttpResponseRedirect
from django.core.urlresolvers import reverse
from poak.settings import POKAL_URL
from django.contrib.auth.decorators import login_required
import requests


def main(request):
    return render(request, "manage_worksheets/index.html")

@login_required
def submit(request):
    """
    three possibilies:
    1. called with post data from a submission
    2. called with a get parameter with an ID
    3. called without any parameters
    """
    try:
        url = request.POST['url']
        postdata = True
    except KeyError:
        # no post data there
        postdata = False

    if postdata:
        try:
            tag_ids = request.POST.getlist('tag')
        except KeyError:
            tag_ids = []

        try:
            worksheet_id = _process_submission(request, url, tag_ids)
            # if there was no error, everything is fine
            return HttpResponseRedirect(
                        reverse('manage_worksheets:details',
                        args=worksheet_id))
        except ValueError:
            # there was an error
            return render(request, "manage_worksheets/submit.html", {
                'tags': Tag.objects.all(),
                'error': True,
            })
    else: # no post data
        try:
            # see if there is get data
            worksheet_id = request.GET['id']
        except KeyError:
            worksheet_id = ""

        return render(request, "manage_worksheets/submit.html", {
            'tags':Tag.objects.all(),
            'error': False,
            'worksheet_id': worksheet_id,
            'pokal_url': POKAL_URL,
            })

def _process_submission(request, url, tag_ids):
    # the pattern is "base_url/worksheet_id/"
    if url[-1] == '/':
        url = url[:-1] # get rid of the last slash
    base_url, worksheet_id = url.rsplit('/', 1) # split in two parts

    # test if the base url ist correct
    if (base_url != POKAL_URL
        and base_url != POKAL_URL.replace("https://", "http://", 1)):
        raise ValueError

    # get data from POKAL
    r = requests.get(url+'/worksheet_properties')

    # if the following fails, it raises a ValueError
    worksheet_properties = r.json()
    try:
        title = worksheet_properties['name']
        author = worksheet_properties['worksheet_that_was_published'][0]
    except KeyError:
        raise ValueError # to make handling easier, make everything ValueErrors

    # make new entry in the database
    w = Worksheet(worksheet_id=worksheet_id,
            title=title, owner=request.user.username, author=author)
    w.save() # has to be saved before we can add the tags

    # see if we can decode the tags
    for tag_id in tag_ids:
        try:
            w.tags.add(Tag.objects.get(id=tag_id))
        except Tag.DoesNotExist:
            # the input data is corrupt
            # abort the process
            w.delete()
            raise ValueError # maybe it should be another error

    return w.worksheet_id

def details(request, worksheet_id):
    worksheet = get_object_or_404(Worksheet, worksheet_id=worksheet_id)
    return render(request, "manage_worksheets/details.html", {
        'worksheet': worksheet,
        'pokal_url': POKAL_URL,
        })
