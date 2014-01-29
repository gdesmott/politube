from django.core.management.base import BaseCommand
from optparse import make_option
from fuzzywuzzy import process, utils

import pleniere.scrapper
import pleniere.dieren
from pleniere.models import Pleniere, AgendaItem, Deputy,Party

IGNORED = ['voorzitter', 'einde', 'fin', 'reprise', 'volgende']
PREFIXES = ['min.', 'staatssecretaris', 'premier', '1m']
FUZZY_THRESHOLD = 90

class Command(BaseCommand):
    option_list = BaseCommand.option_list + (
        make_option('--force-update',
          action='store_true',
          dest='force-update',
          default=False,
          help='Force update of existing entries'),
    )

    def _clean_db(self):
        print "Clean DB"
        Pleniere.objects.all().delete()
        AgendaItem.objects.all().delete()
        Party.objects.all().delete()
        Deputy.objects.all().delete()

    def _update_pleniere(self):
        for i in pleniere.scrapper.find_pleniere_ids():
            try:
                Pleniere.objects.get(chambre_id=i)
            except Pleniere.DoesNotExist:
                sp = pleniere.scrapper.Pleniere(i)
                print "Add", sp

                p = Pleniere.objects.create(chambre_id=sp.id,
                        source=sp.source, date=sp.date, title=sp.title, video_id=sp.video_id,
                        stream=sp.stream)

                for a in sp.agenda:
                    AgendaItem.objects.create(pleniere=p,
                        time=a.time, speaker=a.name, section=a.section, subsection=a.subsection)

    def _strip_speaker_name(self, speaker):
        l = speaker.lower().strip()

        # TODO: special case the president
        for i in IGNORED:
            if l.startswith(i):
                return None

        # Remove useless prefixes about the function of the dude
        for prefix in PREFIXES:
            if l.startswith(prefix):
                l = l[len(prefix):]

        l = l.strip()

        if l.isspace():
            return None

        return l

    def _link_plenieres_deputies(self):
        queryset = Deputy.objects.all()

        # items = AgendaItem.objects.all()
        # Start from 2010 for now as we don't have old deputies anyway
        items = AgendaItem.objects.filter(pleniere__date__gt='2010-01-01', speaker_id=None)

        count = -1
        tot = len(items)

        # str -> Deputy
        cache = {}

        for a in items:
            count += 1
            stripped = self._strip_speaker_name(a.speaker)
            if stripped is None:
                #print "IGNORE %s (%d / %d)" % (a.speaker, count, tot)
                continue

            if cache.get(stripped) is not None:
                deputy = cache[stripped]
            else:
                match = process.extractOne(stripped, queryset, score_cutoff=FUZZY_THRESHOLD,
                        processor=lambda x: utils.full_process(x.full_name))

                if match is None:
                    deputy = None
                else:
                    deputy = match[0]
                    cache[stripped] = deputy

            if deputy is not None:
                print "MATCH %s with %s (%d / %d)" % (a.speaker, deputy.full_name, count, tot)
            else:
                print "FAILED %s (%d / %d)" % (a.speaker, count, tot)

            a.speaker_id = deputy
            a.save()

    def handle(self, *args, **options):
        if options['force-update']:
            self._clean_db()

        self._update_pleniere()
        pleniere.dieren.sync_parties()
        pleniere.dieren.sync_deputies()
        self._link_plenieres_deputies()
