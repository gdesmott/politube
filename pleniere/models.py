import datetime

from django.db import models

VIDEOS = 'http://urlab-srv0.ulb.ac.be/~cassidy/'

class Pleniere(models.Model):
    chambre_id = models.CharField(max_length=200)
    source = models.URLField()
    date = models.DateTimeField('date')
    title = models.CharField(max_length=200)
    webm = models.CharField(max_length=200)
    stream = models.URLField()

    def __unicode__(self):
        return "%s - %s" % (self.chambre_id, self.title)

    def getWebmStream(self):
        return '%s/webm/%s' % (VIDEOS, self.webm)

    class Meta:
        ordering = ["-date"]

class Deputy(models.Model):
    dieren_id = models.CharField(max_length=200, primary_key=True)

    current = models.BooleanField()
    cv_fr = models.TextField()
    cv_nl = models.TextField()
    email = models.EmailField() # FIXME: get all emails?
    first_name = models.CharField(max_length=100)
    full_name = models.CharField(max_length=200)
    lachambre_id = models.CharField(max_length=200)
    language = models.CharField(max_length=200)
    last_name = models.CharField(max_length=100)
    sex = models.CharField(max_length=1)
    website = models.URLField(null=True) # FIXME: get all websites?

    def __unicode__(self):
        return self.full_name

    class Meta:
        ordering = ["full_name"]

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

    class Meta:
        ordering = ["time"]
