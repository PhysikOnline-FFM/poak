from django.shortcuts import render, get_object_or_404
from manage_worksheets.models import Tag, Worksheet
from manage_worksheets.forms import SubmissionForm, ChooseTagsForm
from django.http import HttpResponseRedirect, Http404
from django.core.urlresolvers import reverse
from poak.settings import POKAL_URL
from django.contrib.auth.decorators import login_required
from django.core.exceptions import PermissionDenied, SuspiciousOperation
import requests
import re


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

    if request.method == 'POST':
        # form was submitted
        form = SubmissionForm(request.POST)
        if not form.is_valid():
            return render(request, "manage_worksheets/submit.html", {
                'form': SubmissionForm(),
                'error': True,
            })

        url = form.cleaned_data['url']
        tags = form.cleaned_data['tags']

        try:
            worksheet_id = _process_submission(request, url, tags)
            # if there was no error, everything is fine
            return HttpResponseRedirect(
                        reverse('manage_worksheets:details',
                        args=[worksheet_id]))
        except ValueError:
            # there was an error
            return render(request, "manage_worksheets/submit.html", {
                'tags': Tag.objects.all(),
                'form': SubmissionForm(),
                'error': True,
            })
    else: # no post data
        try:
            # see if there is get data
            worksheet_id = request.GET['id']
        except KeyError:
            worksheet_id = ""

        return render(request, "manage_worksheets/submit.html", {
            'error': False,
            'worksheet_id': worksheet_id,
            'pokal_url': POKAL_URL,
            'form': SubmissionForm(),
            })

def _process_submission(request, url, tags, worksheet_id=None, owner=None):
    """
    creates a new database entry for the given worksheet

    the URL is checked for being a valid POKAL-URL. But only if worksheet_id
    is not given.

    if no owner is given, set the currently logged-in user as the owner
    """
    if worksheet_id == None: # url has to be checked
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

    if owner == None:
        owner = request.user.username

    if owner != author:
        raise ValueError

    # make new entry in the database
    w = Worksheet(worksheet_id=worksheet_id,
            title=title, owner=owner, author=author)
    w.save() # has to be saved before we can add the tags

    # now add the tags
    for tag in tags:
        w.tags.add(tag)

    return w.worksheet_id

def details(request, worksheet_id):
    worksheet = get_object_or_404(Worksheet, worksheet_id=worksheet_id)
    return render(request, "manage_worksheets/details.html", {
        'worksheet': worksheet,
        'pokal_url': POKAL_URL,
        })

@login_required
def loggedin_details(request, worksheet_id):
    return HttpResponseRedirect(
                reverse('manage_worksheets:details',
                args=[worksheet_id]))

@login_required
def delete(request, worksheet_id):
    worksheet = get_object_or_404(Worksheet, worksheet_id=worksheet_id)

    # see if user is allowed to delete
    if worksheet.owner != request.user.username:
        raise Http404

    worksheet.delete()
    return render(request, "manage_worksheets/delete_success.html", {
        'worksheet_id': worksheet_id,
    })

def choose_tags(request):
    """
    two possibilies:
    1. called with post data from a submission
    2. called with a get parameter with an ID
    """
    owner = _get_POKAL_username(request)
    if owner == None:
        raise PermissionDenied

    if request.method == 'POST':
        form = ChooseTagsForm(request.POST)
        if not form.is_valid():
            raise SuspiciousOperation

        # process data
        worksheet_id = form.cleaned_data['worksheet_id']
        url = POKAL_URL+"/"+worksheet_id
        tags = form.cleaned_data['tags']

        try:
            _process_submission(request, url, tags,
                                worksheet_id=worksheet_id, owner=owner)
            # if there was no error, everything is fine
            return HttpResponseRedirect(
                        reverse('manage_worksheets:details',
                        args=[worksheet_id]))
        except ValueError:
            # there was an error
            raise Http404
    else:
        try:
            # see if there is get data
            worksheet_id = request.GET['id']
            form = ChooseTagsForm(initial={'worksheet_id':worksheet_id})
            return render(request, "manage_worksheets/choose_tags.html", {
                'form': form,
            })
        except KeyError:
            raise Http404

def _get_POKAL_username(request):
    url = POKAL_URL+"/javascript/dynamic/username.js"
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
