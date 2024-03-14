from django.db import models
from datetime import datetime
import bcrypt

class User(models.Model):
    email = models.EmailField(unique=True, null=False)
    password_hash = models.TextField()
    fullname = models.TextField()
    age = models.PositiveIntegerField()
    description = models.TextField()
    is_admin = models.BooleanField()
    created_at = models.DateTimeField(defiault=datetime.now())
    
    def  __init__(self, email, password, fullname, age, description):
        self.email = self.is_valid_email(email)
        self.password_hash = bcrypt.hashpw(self.is_valid_password(password), bcrypt.gensalt())
        self.fullname = self.is_valid_fullname(fullname)
        self.age = self.is_valid_age(age)
        self.description = description
        self.is_admin = False

    def  __str__(self):
        return self.fullname

    def is_valid_email (self, email):
        regex = "^[a-z0-9]+[\._]?[a-z0-9]+[@]\w+[.]\w{2,3}$"

        if not regex.match(regex, email):
            raise ValueError("It's not an email address.")
        
        return email
    
    def is_valid_password (self, password):
        regex = "^(?=.*[a-z])(?=.*[A-Z])(?=.*\d)(?=.*[@$!%*#?&])[A-Za-z\d@$!#%*?&]{6,20}$"

        if not regex.match (regex, password):
            raise ValueError("Password is not valid!")
        
        return password

    def is_valid_fullname (self, fullname):
        regex = "\b([A-ZÀ-ÿ][-,a-z. ']+[ ]*)+"

        if not regex.match (regex, fullname):
            raise ValueError("Name is not valid!")

        return fullname
    
    def is_valid_age (self, age):
        if (age < 14) or (age > 150):
            raise ValueError("Age is not valid!")

        return age