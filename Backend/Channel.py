from django.db import models

import Hobby

class Message(models.Model):
    name = models.TextField()
    hobby = models.ForeignKey(Hobby, on_delete=models.SET_NULL)

    def __init__(self, name, hobby):
        self.name = name
        self.hobby = hobby

    def __str__(self):
        return self.name