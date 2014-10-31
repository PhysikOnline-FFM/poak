from django.db import models
from django.core.urlresolvers import reverse
from threadedcomments.models import ThreadedComment

class Tag(models.Model):
    name = models.CharField(max_length=50)
    def __unicode__(self):
        return self.name

class Worksheet(models.Model):
    worksheet_id = models.CharField(max_length=20)
    title = models.CharField(max_length=200)
    tags = models.ManyToManyField(Tag)
    pub_date = models.DateTimeField(auto_now_add=True)
    # TODO: remove "author"
    owner = models.CharField(max_length=20)
    author = models.CharField(max_length=200)
    upvotes = models.IntegerField(default=0)
    downvotes = models.IntegerField(default=0)
    def __unicode__(self):
        return self.title

    def data(self):
        """
        Encode data of Worksheet in a dictionary
        """
        dictionary = {
            'worksheet_id': self.worksheet_id,
            'title': self.title,
            'tags': [t.name for t in self.tags.all()],
            'pub_date': self.pub_date.isoformat(),
            'owner': self.owner,
            'score': (self.upvotes-self.downvotes),
            'comments':
            ThreadedComment.objects.filter(object_pk=self.pk).count(),
            'pk': self.pk,
        }
        return dictionary

    def add_tags(self, tags):
        for tag in tags:
            self.tags.add(tag)

    def get_absolute_url(self):
        return reverse('manage_worksheets:details',
                    args=[self.pk])
