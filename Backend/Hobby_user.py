from typing import Any
from django.db import models

import User
import Hobby

class Hobby_user(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    hobby = models.ForeignKey(Hobby, on_delete=models.CASCADE)

    def __init__(self, user, hobby):
        self.user = user
        self.hobby = hobby