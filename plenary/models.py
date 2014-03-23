import datetime

from django.db import models

VIDEOS_WMV = 'http://wmv.politu.be'
VIDEOS_MP4 = 'http://mp4.politu.be'
VIDEOS_WEBM = 'http://politu.be/~lachambre/videos/webm'

class Plenary(models.Model):
    chambre_id = models.CharField(max_length=200)
    source = models.URLField()
    date = models.DateTimeField('date')
    title = models.CharField(max_length=200)
    video_id = models.CharField(max_length=200)
    stream = models.URLField()

    def __unicode__(self):
        return "%s - %s" % (self.chambre_id, self.title)

    def get_wmv_stream(self):
        return '%s/%s.%s' % (VIDEOS_WMV, self.video_id, 'wmv')

    def get_webm_stream(self):
        return '%s/%s.%s' % (VIDEOS_WEBM, self.video_id, 'webm')

    def get_mp4_stream(self):
        return '%s/%s.%s' % (VIDEOS_MP4, self.video_id, 'mp4')

    def get_title(self):
        return self.title

    def get_source(self):
        return self.source

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

    def getSortedItems(self):
        return self.agendaitem_set.all().order_by('plenary', 'time')

class AgendaItem(models.Model):
    plenary = models.ForeignKey(Plenary)
    # time in seconds
    time = models.IntegerField()
    speaker = models.CharField(max_length=200)
    section = models.CharField(max_length=200, null=True)
    subsection = models.CharField(max_length=200, null=True)
    speaker_id = models.ForeignKey(Deputy, null=True)

    def __unicode__(self):
        return "%s - %s (%s)" % (self.speaker, self.plenary.title, self.time)

    def displayTime(self):
        return str(datetime.timedelta(seconds=self.time))

    class Meta:
        ordering = ["time"]
