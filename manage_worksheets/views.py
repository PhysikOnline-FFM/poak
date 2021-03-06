from django.shortcuts import render, get_object_or_404
from manage_worksheets.models import Tag, Worksheet
from manage_worksheets.forms import SubmissionForm, ChooseTagsForm
from django.http import HttpResponseRedirect
from django.core.urlresolvers import reverse
from poak.settings import POKAL_URL
from django.contrib.auth.decorators import login_required
from django.core.exceptions import PermissionDenied, SuspiciousOperation
import requests
from functions import get_POKAL_username


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
            # process the submission
            w = _save_worksheet(request, url)
            w.tags = tags
            # if there was no error, everything is fine
            return HttpResponseRedirect(
                        reverse('manage_worksheets:details',
                        args=[w.pk]))
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
            form = SubmissionForm(initial={"url":POKAL_URL+"/"+worksheet_id})
        except KeyError:
            form = SubmissionForm()

        return render(request, "manage_worksheets/submit.html", {
            'error': False,
            'pokal_url': POKAL_URL,
            'form': form,
            })

def _save_worksheet(request, url, worksheet_id=None, user=None):
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

    if Worksheet.objects.filter(worksheet_id=worksheet_id).exists():
        # worksheet is already in database
        raise PermissionDenied

    # get data from POKAL
    r = requests.get(url+'/worksheet_properties')

    # if the following fails, it raises a ValueError
    worksheet_properties = r.json()

    try:
        title = worksheet_properties['name']
        owner = worksheet_properties['worksheet_that_was_published'][0]
    except KeyError:
        raise ValueError # to make handling easier, make everything ValueErrors

    if user == None:
        user = request.user.username

    if owner != user:
        raise PermissionDenied

    # make new entry in the database
    w = Worksheet(worksheet_id=worksheet_id,
            title=title, owner=owner, author="")
    w.save()
    return w

def details(request, worksheet_pk):
    worksheet = get_object_or_404(Worksheet, pk=worksheet_pk)
    return render(request, "manage_worksheets/details.html", {
        'worksheet': worksheet,
        'pokal_url': POKAL_URL,
        })

@login_required
def loggedin_details(request, worksheet_pk):
    return HttpResponseRedirect(
                reverse('manage_worksheets:details',
                args=[worksheet_pk]))

@login_required
def delete(request, worksheet_pk):
    worksheet = get_object_or_404(Worksheet, pk=worksheet_pk)

    # see if user is allowed to delete
    if worksheet.owner != request.user.username:
        raise PermissionDenied

    worksheet.delete()
    return render(request, "manage_worksheets/delete_success.html", {
        'worksheet_pk': worksheet_pk,
    })

def sso_submit(request, worksheet_id):
    """
    two possibilies:
    1. called with post data from a submission
    2. called with a get parameter with an ID
    """
    user = get_POKAL_username(request)
    if user == None or user == "guest":
        raise PermissionDenied

    try:
        # save worksheet to the database
        url = POKAL_URL+"/"+worksheet_id
        w = _save_worksheet(request, url, worksheet_id=worksheet_id, user=user)
    except ValueError:
        raise SuspiciousOperation

    return render(request, "manage_worksheets/sso_submit_success.html", {
        'worksheet': w,
    })

@login_required
def choose_tags(request, worksheet_pk):
    worksheet = get_object_or_404(Worksheet, pk=worksheet_pk)

    # see if user is allowed to do this
    if worksheet.owner != request.user.username:
        raise PermissionDenied

    if request.method == 'POST': # tag were chosen

        form = ChooseTagsForm(request.POST)
        if not form.is_valid():
            raise SuspiciousOperation

        # get data
        tags = form.cleaned_data['tags']

        # add the chosen tags to the worksheet in the database
        worksheet.tags = tags

        return HttpResponseRedirect(
                    reverse('manage_worksheets:details',
                    args=[worksheet_pk]))
    else:
        # get the tags that are currently associated with the worksheet
        tagids = [tag.pk for tag in worksheet.tags.all()]

        # render form with these initial values
        form = ChooseTagsForm(initial={'tags':tagids})
        return render(request, "manage_worksheets/choose_tags.html", {
            'form': form,
            'worksheet': worksheet,
        })

def redirect_from_pid(request, worksheet_id):
    worksheet = get_object_or_404(Worksheet, worksheet_id=worksheet_id)
    return HttpResponseRedirect(
            reverse('manage_worksheets:details',
            args=[worksheet.pk])
            )
