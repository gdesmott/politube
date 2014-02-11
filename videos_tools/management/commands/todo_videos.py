from django.core.management.base import BaseCommand
from optparse import make_option

from videos_tools.models import Video

class Command(BaseCommand):
    option_list = BaseCommand.option_list + (
        make_option('--mms',
          action='store_true',
          dest='mms',
          default=False,
          help='Generate list of MMS stream'),
        make_option('--mp4',
          action='store_true',
          dest='mp4',
          default=False,
          help='Generate list of MP4 videos'),
        make_option('--webm',
          action='store_true',
          dest='webm',
          default=False,
          help='Generate list of WEBM videos'),
    )

    def handle(self, *args, **options):
        for video in Video.objects.all():
            if options['mms']:
                if not video.wmv_is_ok():
                    print video.plenary.stream
            elif options['mp4']:
                if video.wmv_is_ok() and not video.mp4_is_ok():
                    print "%s %s" % (video.plenary.getWmvStream(), video.plenary.getMp4Stream())
            elif options['webm']:
                if video.wmv_is_ok() and not video.webm_is_ok():
                    print "%s %s" % (video.plenary.getWmvStream(), video.plenary.getWebmStream())
