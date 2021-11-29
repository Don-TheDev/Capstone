from django.db import models

# Create your models here.


# class Completion(models.Model):
#     sender = models.CharField(max_length=25)
#     message = models.CharField(max_length=200)
#     send_date = models.DateTimeField(auto_now=True)


class AiModel(models.Model):
    name = models.CharField(max_length=50)
    prompt = models.TextField()
    examples = models.TextField()
    # date = models.DateTimeField(auto_now=True)
