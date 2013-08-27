import datetime

from django.db import models

VIDEOS = 'http://urlab-srv0.ulb.ac.be/~cassidy/'

class Pleniere(models.Model):
    chambre_id = models.CharField(max_length=200)
    source = models.URLField()
    date = models.DateTimeField('date')
    title = models.CharField(max_length=200)
    webm = models.CharField(max_length=200)

    def __unicode__(self):
        return "%s - %s" % (self.chambre_id, self.title)

    def getWebmStream(self):
        return '%s/webm/%s' % (VIDEOS, self.webm)

class AgendaItem(models.Model):
    pleniere = models.ForeignKey(Pleniere)
    # time in seconds
    time = models.IntegerField()
    speaker = models.CharField(max_length=200)
    section = models.CharField(max_length=200, null=True)
    subsection = models.CharField(max_length=200, null=True)

    def __unicode__(self):
        return "%s - %s (%s)" % (self.speaker, self.pleniere.title, self.time)

    def displayTime(self):
        return str(datetime.timedelta(seconds=self.time))
