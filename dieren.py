import os
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "chambre.settings")

import urllib2
import json
from pleniere.models import Deputy

DEPUTIES_LIMIT = 200

def jsonToModel(j):
    v= {}

    v['dieren_id'] = j['id']
    v['lachambre_id'] = j['lachambre_id']
    v['current'] = j['current']
    v['cv_fr'] = j['cv']['fr']
    v['cv_nl'] = j['cv']['nl']
    v['email'] = j['emails'][0]
    v['first_name'] = j['first_name']
    v['full_name'] = j['full_name']
    v['language'] = j['language']
    v['last_name'] = j['last_name']
    v['sex'] = j['sex']
    v['website'] = j['websites'][0] if len(j['websites']) > 0 else None

    return v

def syncDeputies():
    url = "http://www.dierentheater.be/api/v1/deputy/?format=json&limit=%d" % (DEPUTIES_LIMIT)
    data = urllib2.urlopen(url).read()

    j = json.loads(data)
    for d in j['objects']:
        args = jsonToModel(d)
        try:
            deputy = Deputy.objects.get(dieren_id=d['id'])
            print "UPDATE", args['full_name']
            for k in args:
                setattr(deputy, k, args[k])
            deputy.save()

        except Deputy.DoesNotExist:
            print "CREATE", args['full_name']
            Deputy.objects.create(**args)

if __name__ == '__main__':
    syncDeputies()
