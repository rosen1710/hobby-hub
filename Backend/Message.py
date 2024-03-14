from django.db import models
from datetime import datetime

import User
import Channel

class Message(models.Model):
    text = models.TextField()
    user = models.ForeignKey(User, on_delete=models.SET_NULL)
    channel = models.ForeignKey(Channel, on_delete=models.SET_NULL)
    created_at = models.DateTimeField(default=datetime.now())
    # updated_at = models.DateTimeField(default=datetime.now())

    def __init__(self, text, user, channel):
        self.text = text
        self.user = user
        self.channel = channel

    def __str__(self):
        return self.text