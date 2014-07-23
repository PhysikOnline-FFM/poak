from django.db import models

class Tag(models.Model):
    name = models.CharField(max_length=50)
    def __unicode__(self):
        return self.name

class Worksheet(models.Model):
    worksheet_id = models.CharField(max_length=20)
    title = models.CharField(max_length=200)
    tags = models.ManyToManyField(Tag)
    pub_date = models.DateTimeField(auto_now_add=True)
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
        dict = {
            'worksheet_id': self.worksheet_id,
            'title': self.title,
            'tags': [t.name for t in self.tags.all()],
            'pub_date': self.pub_date.isoformat(),
            'author': self.author,
            'score': (self.upvotes-self.downvotes),
        }
        return dict
