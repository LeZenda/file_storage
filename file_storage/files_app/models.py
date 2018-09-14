from django.db import models
from django.utils.translation import ugettext_lazy as _
from core.models import User
from datetime import datetime, timezone, timedelta

# Create your models here.


class Source(models.Model):
    """
        Model to store sources of files
    """

    sid = models.CharField(_(u'SID'), unique=True, max_length=128)
    name = models.CharField(_(u'Name'), unique=True, max_length=256)
    url = models.URLField(_(u'Url'))

    def __str__(self):
        return '{0} - {1}'.format(self.name, self.sid)


class Document(models.Model):
    """
        Model to store documents
    """
    # time that the document can be edited in seconds
    TIME_FOR_EDITS = 1 * 60 * 60

    title = models.CharField(_(u'Title'), unique=True, max_length=128)
    text = models.TextField(_(u'Text'), unique=True)
    url = models.URLField(_(u'Url'))
    created = models.DateTimeField(_(u'Creation date'), auto_now_add=True)
    updated = models.DateTimeField(_(u'Last update date'), auto_now=True)
    date_added = models.DateTimeField(_(u'Date document was added'))

    source = models.ForeignKey(Source, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)

    def __str__(self):
        return '{0} - {1}'.format(self.title, self.url)

    def can_be_edited_by_owner(self):
        """
        :return: True if the time for edits has not yet expired
        """
        t_delta = timedelta(seconds=self.TIME_FOR_EDITS)
        return datetime.now(timezone.utc) - self.created < t_delta

    def can_be_edited_by_user(self, user):
        """
        :param user: user that is checked for the ability to edit this document
        :return: True if this document can be edited bu selected user, False if the action is forbidden
        """
        if user.is_superuser or (user == self.user and self.can_be_edited_by_owner()):
            return True
        return False
