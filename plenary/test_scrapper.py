# -*- coding: utf-8 -*-

import scrapper

from collections import Counter

def test_scrapper_20130717():
    p = scrapper.Plenary('20130717-1')

    assert p.id == '20130717-1'
    assert p.title_fr == 'P157 - Questions, projets et propositions de loi, votes'
    assert p.title_nl == 'P157 - Vragen, wetsontwerpen en voorstellen, stemmingen'

    assert p.source_fr == 'http://www.dekamer.be/kvvcr/showpage.cfm?section=none&leftmenu=none&language=fr&cfm=/site/wwwcfm/streaming/archive/viewarchivemeeting.cfm?meeting=20130717-1'
    assert p.source_nl == 'http://www.dekamer.be/kvvcr/showpage.cfm?section=none&leftmenu=none&language=nl&cfm=/site/wwwcfm/streaming/archive/viewarchivemeeting.cfm?meeting=20130717-1'

    assert p.date.day == 17
    assert p.date.month == 07
    assert p.date.year == 2013
    assert p.date.hour == 14
    assert p.date.minute == 15

    assert p.stream == 'mms://193.191.129.52/Archive/20130717-1_bb_pl.wmv'
    assert p.video_id == '20130717-1_bb_pl'

    assert len(p.agenda_fr) == 160
    assert len(p.agenda_nl) == 160

    def check_agenda(agenda, time, name, section=None, subsection=None):
        assert agenda.time == time
        assert agenda.name == name
        assert agenda.section == section
        assert agenda.subsection == subsection

    check_agenda(p.agenda_fr[0], 87, 'Voorzitter - Président')
    check_agenda(p.agenda_fr[2], 237, 'Benoît DRÈZE', None, 'prestation de serment')
    check_agenda(p.agenda_fr[-1], 25033, 'Voorzitter - Président', 'votes: projets/propositions',
            '2945 - Convention travail maritime')

    check_agenda(p.agenda_nl[0], 87, 'Voorzitter - Président')
    check_agenda(p.agenda_nl[2], 237, 'Benoît DRÈZE', None, 'eedaflegging')
    check_agenda(p.agenda_nl[-1], 25033, 'Voorzitter - Président', 'stemmingen: ontwerpen/voorstellen',
            '2945 - Verdrag maritieme arbeid')

def test_scrapper_20130307():
    p = scrapper.Plenary('20130307-1')

    assert p.id == '20130307-1'
    assert p.title_fr == 'P 134 - questions, projets de loi et propositions, votes'
    assert p.title_nl == 'P 134 - vragen, wetsontwerpen en voorstellen, stemmingen'

    assert p.date.day == 7
    assert p.date.month == 3
    assert p.date.year == 2013
    assert p.date.hour == 14
    assert p.date.minute == 15

    assert p.stream == 'mms://193.191.129.52/Archive/20130307-1_bb_pl.wmv'
    assert p.video_id == '20130307-1_bb_pl'

    assert len(p.agenda_fr) == 0
    assert len(p.agenda_nl) == 0

def test_scrapper_20121122():
    p = scrapper.Plenary('20121122-2')

    assert p.id == '20121122-2'
    assert p.title_fr == 'P114 - Discussion de la déclaration du gouvernement'
    assert p.title_nl == 'P114 - Bespreking van de verklaring van de regering'

    assert p.date.day == 22
    assert p.date.month == 11
    assert p.date.year == 2012
    assert p.date.hour == 16
    assert p.date.minute == 15

    assert p.stream == 'mms://193.191.129.52/Archive/20121122-2_bb_pl.wmv'
    assert p.video_id == '20121122-2_bb_pl'

def test_ignore_not_plenay():
    # make sure we ignore not plenay sessions
    ids = scrapper.find_plenary_ids()

    assert '20140123-1' in ids
    assert '20081008-1' not in ids

def test_chambre_ids_unique():
    # check that each chambre-id is unique
    ids = scrapper.find_plenary_ids()
    c = Counter(ids)

    for i in c:
        assert c[i] == 1, i
