from django.core.management.base import BaseCommand
from optparse import make_option

from plenary.models import Plenary
from videos_tools.models import Video
from videos_tools.extract_len import extract_video_len

class Command(BaseCommand):
    option_list = BaseCommand.option_list + (
        make_option('--force-mms',
          action='store_true',
          dest='force-mms',
          default=False,
          help='Force a refresh of MMS stream'),
        make_option('--force-wmv',
          action='store_true',
          dest='force-wmv',
          default=False,
          help='Force a refresh of WMV videos'),
        make_option('--force-mp4',
          action='store_true',
          dest='force-mp4',
          default=False,
          help='Force a refresh of MP4 videos'),
        make_option('--force-webm',
          action='store_true',
          dest='force-webm',
          default=False,
          help='Force a refresh of WEBM videos'),
    )

    def _get_video_len(self, url):
        t = extract_video_len(url)
        return t.seconds

    def handle(self, *args, **options):
        for plenary in Plenary.objects.all():
            changed = False

            try:
                video = Video.objects.get(plenary=plenary)
            except Video.DoesNotExist:
                video = Video.objects.create(plenary=plenary)

            if video.mms_len is None or options['force-mms']:
                try:
                    video.mms_len = self._get_video_len(plenary.stream)
                    changed = True
                except ValueError:
                    pass

            if not video.wmv_is_ok() or options['force-wmv']:
                try:
                    video.wmv_len = self._get_video_len(plenary.getWmvStream())
                    changed = True
                except ValueError:
                    pass

            if not video.mp4_is_ok() or options['force-mp4']:
                try:
                    video.mp4_len = self._get_video_len(plenary.getMp4Stream())
                    changed = True
                except ValueError:
                    pass

            if not video.webm_is_ok() or options['force-webm']:
                try:
                    video.webm_len = self._get_video_len(plenary.getWebmStream())
                    changed = True
                except ValueError:
                    pass

            if changed:
                video.save()
