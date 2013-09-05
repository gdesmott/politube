#!/usr/bin/env python
# -*- coding: utf-8 -*-

from django.core.management import setup_environ
from chambre import settings

setup_environ(settings)

from pleniere.models import Pleniere, AgendaItem
from pleniere.scrapper import find_all_plenieres

def dropAll():
    Pleniere.objects.all().delete()
    AgendaItem.objects.all().delete()

def populatePlenieres():
    for p in find_all_plenieres():
        pleniere = Pleniere.objects.create(chambre_id=p.id,
                source=p.source, date=p.date, title=p.title, webm=p.webm,
                stream=p.stream)

        for a in p.agenda:
            AgendaItem.objects.create(pleniere=pleniere,
                time=a.time, speaker=a.name, section=a.section, subsection=a.subsection)


if __name__ == '__main__':
    dropAll()
    populatePlenieres()
