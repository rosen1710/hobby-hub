from django.db import models
from datetime import datetime

import User

class Hobby(models.Model):
    name = models.TextField(unique = True)
    category = models.TextField()
    author = models.ForeignKey(User, on_delete = models.SET_NULL)
    created_at = models.DateTimeField(default=datetime.now())
    icon = models.FileField()
    approved = models.BooleanField()
    
    def __init__(self, name, category, author, icon):
        self.name = name
        self.category = category
        self.author = author
        self.icon = icon
        self.approved = False

    def  __str__(self):
        return self.name