from django.db import models
from django.contrib.auth.models import User

class ClusterImage(models.Model):
    title = models.CharField(max_length=50)
    image = models.TextField()
    date = models.DateTimeField(auto_now=True, null=True, blank=True)
    createdBy = models.ForeignKey(User, on_delete=models.CASCADE, null=True, blank=True)

    def __str__(self):
        return self.title

class RegressionImage(models.Model):
    title = models.CharField(max_length=50)
    image = models.TextField()
    date = models.DateTimeField(auto_now=True, null=True, blank=True)
    createdBy = models.ForeignKey(User, on_delete=models.CASCADE, null=True, blank=True)

    
    def __str__(self):
        return self.title
    