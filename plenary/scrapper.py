#!/usr/bin/env python

import datetime
import urllib2
import re
import warnings
from urlparse import urlparse

from bs4 import BeautifulSoup

INDEX = 'http://www.dekamer.be/kvvcr/showpage.cfm?section=none&rightmenu=right&language=fr&cfm=/site/wwwcfm/streaming/archive/video.cfm'

PAGE_URL = 'http://www.dekamer.be/kvvcr/showpage.cfm?section=none&leftmenu=none&language=%s&cfm=/site/wwwcfm/streaming/archive/viewarchivemeeting.cfm?meeting=%s'

class AgendaItem(object):
    def __init__(self, time, name, section, subsection):
        self.time = time
        self.name = name.encode('utf-8')

        def encode_or_none(txt):
            if txt is None:
                return None
            return txt.encode('utf-8')

        self.section = encode_or_none(section)
        self.subsection = encode_or_none(subsection)

class Plenary (object):
    def __init__(self, i):
        self.id = i

        self.source_fr = PAGE_URL % ('fr', self.id)
        page = urllib2.urlopen (self.source_fr)
        self.soup_fr = BeautifulSoup(page)

        self.source_nl = PAGE_URL % ('nl', self.id)
        page = urllib2.urlopen (self.source_nl)
        self.soup_nl = BeautifulSoup(page)

        self.date = self._extractDate()
        self.title_fr, self.title_nl = self._extractTitle(self.soup_fr), self._extractTitle(self.soup_nl)
        self.stream = self._extractStream()
        self.video_id = self._extract_video_id()
        self.agenda_fr, self.agenda_nl = self._extractAgenda(self.soup_fr), self._extractAgenda(self.soup_nl)

        assert len(self.agenda_fr) == len(self.agenda_nl)

    def _extractDate(self):
        font_fr = self.soup_fr.find('font', class_='txt')
        font_nl = self.soup_nl.find('font', class_='txt')
        assert (font_fr.text.strip() == font_nl.text.strip())

        return datetime.datetime.strptime(font_fr.text.strip(), '%d/%m/%Y - %H:%M')

    def _extractTitle(self, soup):
        h4 = soup.find_all('h4')
        # CRAP: use the 8th <h4>
        return h4[7].text.encode('utf-8')

    def _extractStream(self):
        e = self.soup_fr.find(href=re.compile("mms://"))
        if e is None:
            warnings.warn('No mms://')
            return

        return e['href']

    def _extractAgenda(self, soup):
        agenda = []

        section = None
        subsection = None

        a = soup.find(text='AGENDA')
        if a is None:
            return agenda

        table = a.find_parent('table')
        for td in table.find_all('td'):
            # section?
            b = td.find('b')
            if b is not None:
                section = b.text.strip()
                continue

            # subsection?
            font = td.find('font', color='#339933')
            if font is not None:
                subsection = font.text.strip()
                continue

            # Agenda Entry?
            a = td.find(href=re.compile("goTopic"))
            if a is not None:
                def getSec(s):
                    l = s.split(':')
                    return int(l[0]) * 3600 + int(l[1]) * 60 + int(l[2])

                agenda.append(AgendaItem(getSec(a['title']), a.text, section, subsection))
                continue

        return agenda

    def _extract_video_id(self):
        path = urlparse(self.stream).path
        f = path.split('/')[-1]
        base_name = f.split('.')[0]
        return base_name

def find_plenary_ids():
    soup = BeautifulSoup(urllib2.urlopen (INDEX))
    ids = []

    # We want only 'plenaries' sessions and yeah that's the only way to
    # identify the div containing them all...
    main_div = soup.find('div', style='width: auto; height:400px; overflow: auto; border: 1px solid gray')

    for e in main_div.find_all(href=re.compile("viewarchivemeeting.cfm")):
        ids.append(re.search('.*meeting=(.*)', e['href']).group(1))
    return ids

def generate_plenary():
    for i in find_plenary_ids():
        yield Plenary(i)

if __name__ == '__main__':
    for p in generate_plenary():
        print p.id, p.title_fr
