from django.db import models
import User

class Hobby (models.Model):
    name = models.TextField (unique = True)
    category = models.TextField ()
    author = models.ForeignKey (User, on_delete = models.SET_NULL)
    created_at = models.DateTimeField ()
    icon = models.FileField ()
    # approved = models.BooleanField ()  # TODO: Add approval process?

    def  __str__ (self):
        return self.name