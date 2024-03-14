from django.db import models
import User
import Hobby

class Hobby_user (models.Model):
    user = models.ForeignKey (User, on_delete = models.SET_NULL)
    hobby = models.ForeignKey (Hobby, on_delete = models.SET_NULL)