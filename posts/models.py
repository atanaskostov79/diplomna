from django.db import models

class Posts(models.Model):
    title = models.CharField(max_length=100)
    entry_title = models.CharField(max_length=200, default="N/A")
    content = models.TextField()
