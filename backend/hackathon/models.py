from django.db import models

# Create your models here.
class Voice(models.Model):

    voice_id = models.CharField(max_length=15)
    file_name = models.CharField(max_length=100)
    voice_file = models.FileField(upload_to='', null=True, blank=True)