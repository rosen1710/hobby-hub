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
        self.name = self.is_valid_name(name)
        self.category = self.is_valid_name(category)
        self.author = author
        self.icon = icon
        self.approved = False

    def  __str__(self):
        return self.name
    
    def is_valid_name (self, name):
        if name == "":
            raise ValueError ("Not a valid name!")
        
        return name