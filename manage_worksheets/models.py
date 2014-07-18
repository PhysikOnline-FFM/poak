from django.db import models

class Tag(models.Model):
    name = models.CharField(max_length=50)

class Worksheet(models.Model):
    ID = models.CharField(max_length=20)
    title = models.CharField(max_length=200)
    tags = models.ManyToManyField(Tag)
    pub_date = models.DateTimeField(auto_now_add=True)
    owner = models.CharField(max_length=20)
    upvotes = models.IntegerField(default=0)
    downvotes = models.IntegerField(default=0)
