#!/usr/bin/env python

import datetime
import urllib2
import re
import warnings
from urlparse import urlparse

from bs4 import BeautifulSoup

INDEX = 'http://www.dekamer.be/kvvcr/showpage.cfm?section=none&rightmenu=right&language=fr&cfm=/site/wwwcfm/streaming/archive/video.cfm'

PAGE_URL = 'http://www.dekamer.be/kvvcr/showpage.cfm?section=none&leftmenu=none&language=fr&cfm=/site/wwwcfm/streaming/archive/viewarchivemeeting.cfm?meeting=%s'

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

class Pleniere (object):
    def __init__(self, i):
        self.id = i

        self.source = PAGE_URL % self.id
        page = urllib2.urlopen (self.source)
        self.soup = BeautifulSoup(page)

        self.date = self._extractDate()
        self.title = self._extractTitle()
        self.stream = self._extractStream()
        self.webm = self._webM()
        self.agenda = self._extractAgenda()

    def _extractDate(self):
        font = self.soup.find('font', class_='txt')

        return datetime.datetime.strptime(font.text.strip(), '%d/%m/%Y - %H:%M')

    def _extractTitle(self):
        h4 = self.soup.find_all('h4')
        # CRAP: use the second <h4>
        return h4[1].text.encode('utf-8')

    def _extractStream(self):
        e = self.soup.find(href=re.compile("mms://"))
        if e is None:
            warnings.warn('No mms://')
            return

        return e['href']

    def _extractAgenda(self):
        agenda = []

        section = None
        subsection = None

        a = self.soup.find(text='AGENDA')
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

    def _webM(self):
        path = urlparse(self.stream).path
        f = path.split('/')[-1]
        base_name = f.split('.')[0]
        return '%s.webm' % base_name

def find_all_plenieres():
    soup = BeautifulSoup(urllib2.urlopen (INDEX))
    all = []

    for e in soup.find_all(href=re.compile("viewarchivemeeting.cfm")):
        i = re.search('.*meeting=(.*)', e['href']).group(1)

        all.append(Pleniere(i))

    return all

if __name__ == '__main__':
    for p in find_all_plenieres():
        print p.id
