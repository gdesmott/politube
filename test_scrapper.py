# -*- coding: utf-8 -*-
import scrapper

def test_scrapper():
    p = scrapper.Pleniere('20130717-1')

    assert p.id == '20130717-1'
    assert p.title == 'P157 - Questions, projets et propositions de loi, votes'

    assert p.date.day == 17
    assert p.date.month == 07
    assert p.date.year == 2013
    assert p.date.hour == 14
    assert p.date.minute == 15

    assert p.stream == 'mms://193.191.129.52/Archive/20130717-1_bb_pl.wmv'
    assert p.webm == '20130717-1_bb_pl.webm'

    assert len(p.agenda) == 160

    def check_agenda(agenda, time, name, section=None, subsection=None):
        assert agenda.time == time
        assert agenda.name == name
        assert agenda.section == section
        assert agenda.subsection == subsection

    check_agenda(p.agenda[0], 87, 'Voorzitter - Président')
    check_agenda(p.agenda[2], 237, 'Benoît DRÈZE', None, 'prestation de serment')
    check_agenda(p.agenda[-1], 25033, 'Voorzitter - Président', 'votes: projets/propositions',
            '2945 - Convention travail maritime')
