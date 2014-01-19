from extract_len import *

def test_extract_video_len():
    t = extract_video_len('mms://193.191.129.52/Archive/20131219-1_bb_pl.wmv')
    assert (str(t) == '5:43:17.820000')

    t = extract_video_len('http://agot.be/~lachambre/videos/wmv/20131219-1_bb_pl.wmv')
    assert (str(t) == '5:46:57.020000')
