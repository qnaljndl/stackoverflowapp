from django.db import models


class Search(models.Model):
    search_time = models.DateTimeField(auto_now_add=True)
    user_id = models.IntegerField(max_length=10, blank=False)
    query = models.CharField(max_length=256)

# Create your models here.
