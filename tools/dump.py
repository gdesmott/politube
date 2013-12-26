#!/usr/bin/env python

import sys
import os
import os.path
import datetime
import multiprocessing

import urlparse
import urllib2

DIR = 'videos/wmv'
REPO = 'http://desmottes.be/~lachambre/' + DIR

MAX_PROCESS = 20

def now():
    return datetime.datetime.now().strftime('%d-%m-%Y %H:%M')

def dump(stream, out):
    cmd = 'mimms %s %s' % (stream, out)

    print "[START (%s)] %s" % (now(), out)
    print cmd
    result = os.system(cmd)
    if result == 0:
        print "[DONE] (%s) %s" % (now(), out)
    else:
        print "[FAIL] (%s) %s" % (now(), out)
        try:
            os.unlink(out)
        except:
            pass

def build_out_path(video):
    return os.path.join(DIR, video)

def url_exists(url):
    try:
        urllib2.urlopen(url)
    except:
        return False

    return True

def has_video(video):
    # local
    out = build_out_path(video)
    if os.path.exists(out):
        return True

    # remote
    url = urlparse.urljoin(REPO, video)
    if url_exists(url):
        return True

    return False

def dump_if_needed(stream):
    u = urlparse.urlparse(stream)
    video = u.path.split('/')[-1]

    if has_video(video):
        print "[SKIP] %s" % video
        return

    out = build_out_path(video)
    dump(stream, out)

def dump_all(f):
    try:
        os.makedirs(DIR)
    except:
        pass

    pool = multiprocessing.Pool(MAX_PROCESS)
    streams = [s.strip() for s in open(f)]

    r = pool.map_async(dump_if_needed, streams)
    try:
        r.wait()
    except KeyboardInterrupt:
        pool.terminate()

if __name__ == '__main__':
    dump_all(sys.argv[1])
