import datetime

from django.utils.translation import get_language
from django.db import models

VIDEOS_WMV = 'http://wmv.politu.be'
VIDEOS_MP4 = 'http://mp4.politu.be'
VIDEOS_WEBM = 'http://politu.be/~lachambre/videos/webm'

def use_nl():
    l = get_language()
    return l == 'nl' or l.startswith('nl-')

class Plenary(models.Model):
    chambre_id = models.CharField(max_length=200)
    source_fr = models.URLField()
    source_nl = models.URLField()
    date = models.DateTimeField('date')
    title_fr = models.CharField(max_length=200)
    title_nl = models.CharField(max_length=200)
    video_id = models.CharField(max_length=200)
    stream = models.URLField()

    def __unicode__(self):
        return "%s - %s" % (self.chambre_id, self.title_fr)

    def get_wmv_stream(self):
        return '%s/%s.%s' % (VIDEOS_WMV, self.video_id, 'wmv')

    def get_webm_stream(self):
        return '%s/%s.%s' % (VIDEOS_WEBM, self.video_id, 'webm')

    def get_mp4_stream(self):
        return '%s/%s.%s' % (VIDEOS_MP4, self.video_id, 'mp4')

    def get_title(self):
        if use_nl():
            return self.title_nl
        else:
            return self.title_fr

    def get_source(self):
        if use_nl():
            return self.source_nl
        else:
            return self.source_fr

    class Meta:
        ordering = ["-date"]
        get_latest_by = "date"

class Party(models.Model):
    dieren_id = models.CharField(max_length=200, primary_key=True)
    name = models.CharField(max_length=100)

    def __unicode__(self):
        return self.name

    class Meta:
        ordering = ["name"]

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
    sex = models.CharField(max_length=1, null=True)
    website = models.URLField(null=True) # FIXME: get all websites?
    party = models.ForeignKey(Party, null=True)
    photo_uri = models.URLField(null=True)

    def __unicode__(self):
        return self.full_name

    class Meta:
        ordering = ["party", "full_name"]

    def get_cv(self):
        if use_nl():
            return self.cv_nl
        else:
            return self.cv_fr

    def getSortedItems(self):
        return self.agendaitem_set.all().order_by('plenary', 'time')

class AgendaItem(models.Model):
    plenary = models.ForeignKey(Plenary)
    # time in seconds
    time = models.IntegerField()
    speaker = models.CharField(max_length=200)
    section_fr = models.CharField(max_length=200, null=True)
    section_nl = models.CharField(max_length=200, null=True)
    subsection_fr = models.CharField(max_length=200, null=True)
    subsection_nl = models.CharField(max_length=200, null=True)
    speaker_id = models.ForeignKey(Deputy, null=True)

    def __unicode__(self):
        return "%s - %s (%s)" % (self.speaker, self.plenary.title_fr, self.time)

    def displayTime(self):
        return str(datetime.timedelta(seconds=self.time))

    def get_section(self):
        if use_nl():
            return self.section_nl
        else:
            return self.section_fr

    def get_subsection(self):
        if use_nl():
            return self.subsection_nl
        else:
            return self.subsection_fr

    class Meta:
        ordering = ["time"]
