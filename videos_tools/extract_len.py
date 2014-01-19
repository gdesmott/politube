import subprocess
import datetime

def extract_video_len(url):
    if 'mms' in url:
        url = url.replace('mms', 'rtsp')

        output, err = subprocess.Popen(['ffprobe', '-rtsp_transport', 'tcp', url], stdout=subprocess.PIPE, stderr=subprocess.PIPE).communicate()
    else:
        output, err = subprocess.Popen(['ffprobe', url], stdout=subprocess.PIPE, stderr=subprocess.PIPE).communicate()

    for l in err.split('\n'):
        if 'Duration' in l:
            l = l.strip()
            _, l = l.split('Duration: ')
            duration = l.split(',')[0]
            # duration is something like '05:43:17.82'
            s = duration.split(':')
            return datetime.timedelta(hours=int(s[0]), minutes=int(s[1]), seconds=float(s[2]))

    raise ValueError
