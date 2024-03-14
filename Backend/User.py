from django.db import models
from datetime import datetime
import bcrypt

class User(models.Model):
    email = models.EmailField(unique=True, null=False)
    password_hash = models.TextField()
    fullname = models.TextField()
    birthdate = models.DateField()
    description = models.TextField()
    is_admin = models.BooleanField()
    created_at = models.DateTimeField(defiault=datetime.now())
    
    def  __init__(self, email, password, fullname, birthdate, description):
        self.email = email
        self.password_hash = bcrypt.hashpw(password, bcrypt.gensalt())
        self.fullname = fullname
        self.birthdate = birthdate
        self.description = description
        self.is_admin = False

    def  __str__(self):
        return self.fullname