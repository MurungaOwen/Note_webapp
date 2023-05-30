from django.db import models
from django.contrib.auth.models import User

# Create your models here.
class Post(models.Model):
    created_by=models.ForeignKey(User,on_delete=models.CASCADE)#user akiwa deleted,hadi post zake zikue deleted
    title=models.CharField(max_length=200)
    note = models.TextField()
    created_at=models.DateTimeField(auto_now_add=True)
    updated_at=models.DateTimeField(auto_now=True)

    #tuciclick posts wat will we see
    def __str__(self):
        return self.name + "/n" +  self.note
    