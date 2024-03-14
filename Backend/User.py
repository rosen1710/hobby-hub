from django.db import models

class User (models.Model):
    # id = models.UUIDField ()
    email = models.EmailField (unique=True)
    fullname = models.TextField ()
    birthdate = models.DateField ()
    description = models.TextField ()
    is_admin = models.BooleanField ()
    created_at = models.DateTimeField ()

    def  __str__ (self):
        return self.fullname