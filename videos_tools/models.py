import datetime
from django.db import models

from plenary.models import Plenary

# in seconds
OK_THRESHOLD = 5

class Video(models.Model):
    plenary = models.ForeignKey(Plenary)

    # len are in seconds
    mms_len = models.IntegerField(null=True)
    wmv_len = models.IntegerField(null=True)
    mp4_len = models.IntegerField(null=True)
    webm_len = models.IntegerField(null=True)

    def __unicode__(self):
        return "Videos of '%s'" % (self.plenary.chambre_id)

    # format len
    def _format_len(self, l):
        return str(datetime.timedelta(seconds=l))

    def format_mms_len(self):
        return self._format_len(self.mms_len)

    def format_wmv_len(self):
        return self._format_len(self.wmv_len)

    def format_mp4_len(self):
        return self._format_len(self.mp4_len)

    def format_webm_len(self):
        return self._format_len(self.webm_len)

    # is the video considered as 'ok'
    def wmv_is_ok(self):
        if self.wmv_len is None:
            return False

        # WMV seems to be longer than MMS for some reason
        return self.wmv_len >= self.mms_len

    def mp4_is_ok(self):
        if self.mp4_len is None:
            return False

        return abs(self.mp4_len - self.mms_len) <= OK_THRESHOLD

    def webm_is_ok(self):
        if self.webm_len is None:
            return False

        return abs(self.webm_len - self.mms_len) <= OK_THRESHOLD

    class Meta:
        ordering = ["-plenary__date"]
