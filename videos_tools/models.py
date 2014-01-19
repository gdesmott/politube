from django.db import models

from pleniere.models import Pleniere

class Video(models.Model):
    pleniere = models.ForeignKey(Pleniere)

    # len are in seconds
    mms_len = models.IntegerField(null=True)
    wmv_len = models.IntegerField(null=True)
    mp4_len = models.IntegerField(null=True)
    webm_len = models.IntegerField(null=True)

    def __unicode__(self):
        return "Videos of '%s'" % (self.pleniere.chambre_id)
