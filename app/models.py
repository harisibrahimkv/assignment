import uuid

from django.db import models


class Email(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    body = models.TextField(blank=True, null=True)
    sender = models.CharField(max_length=128, blank=True, null=True)
    receiver = models.CharField(max_length=128, blank=True, null=True)
    subject = models.CharField(max_length=256, blank=True, null=True)
    date = models.DateTimeField(null=True, blank=True)
    message_id = models.CharField(max_length=512, null=False)

    def __str__(self):
        return "Email {}".format(self.subject)
