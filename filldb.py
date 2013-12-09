#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "chambre.settings")

from fuzzywuzzy import process, utils

from pleniere.models import Pleniere, AgendaItem, Deputy
from pleniere.scrapper import find_all_plenieres
import dieren

def dropPlenieres():
    Pleniere.objects.all().delete()
    AgendaItem.objects.all().delete()

def dropDeputies():
    Deputy.objects.all().delete()

def populatePlenieres():
    for p in find_all_plenieres():
        pleniere = Pleniere.objects.create(chambre_id=p.id,
                source=p.source, date=p.date, title=p.title, webm=p.webm,
                stream=p.stream)

        for a in p.agenda:
            AgendaItem.objects.create(pleniere=pleniere,
                time=a.time, speaker=a.name, section=a.section, subsection=a.subsection)

IGNORED = ['voorzitter', 'einde', 'fin', 'reprise', 'volgende']
PREFIXES = ['min.', 'staatssecretaris', 'premier', '1m']
FUZZY_THRESHOLD = 90

def stripSpeakerName(speaker):
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

def linkPlenieresDeputies():
    queryset = Deputy.objects.all()

    items = AgendaItem.objects.all()

    count = -1
    tot = len(items)

    for a in items:
        count += 1
        stripped = stripSpeakerName(a.speaker)
        if stripped is None:
            print "IGNORE %s (%d / %d)" % (a.speaker, count, tot)
            continue

        match = process.extractOne(stripped, queryset, score_cutoff=FUZZY_THRESHOLD,
                processor=lambda x: utils.full_process(x.full_name))

        if match is None:
            deputy = None
        else:
            deputy = match[0]

        if deputy is not None:
            print "MATCH %s with %s (%d / %d)" % (a.speaker, deputy.full_name, count, tot)
        else:
            print "FAILED %s (%d / %d)" % (a.speaker, count, tot)

        a.speaker_id = deputy
        a.save()

if __name__ == '__main__':
    dropPlenieres()
    populatePlenieres()

    dropDeputies()
    dieren.syncDeputies()

    linkPlenieresDeputies()
