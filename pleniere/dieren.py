import urllib2
import json
from pleniere.models import Deputy, Party

LIMIT = 200

def party_json_to_model(j):
    v= {}

    v['dieren_id'] = j['id']
    v['name'] = j['name']

    return v

def sync_parties():
    url = "http://www.dierentheater.be/api/v1/party/?format=json&limit=%d" % (LIMIT)
    data = urllib2.urlopen(url).read()

    j = json.loads(data)
    for d in j['objects']:
        args = party_json_to_model(d)
        try:
            party = Party.objects.get(dieren_id=d['id'])
            print "UPDATE", args['name']
            for k in args:
                setattr(party, k, args[k])
            party.save()

        except Party.DoesNotExist:
            print "CREATE", args['name']
            Party.objects.create(**args)

def deputy_json_to_model(j):
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
    v['photo_uri'] = j['photo_uri']

    if len(j['party']):
        party_id = j['party'].split('/')[-2]
        v['party'] = Party.objects.get(pk=party_id)
    else:
        v['party'] = None

    return v

def sync_deputies():
    url = "http://www.dierentheater.be/api/v1/deputy/?format=json&limit=%d" % (LIMIT)
    data = urllib2.urlopen(url).read()

    j = json.loads(data)
    for d in j['objects']:
        args = deputy_json_to_model(d)
        try:
            deputy = Deputy.objects.get(dieren_id=d['id'])
            print "UPDATE", args['full_name']
            for k in args:
                setattr(deputy, k, args[k])
            deputy.save()

        except Deputy.DoesNotExist:
            print "CREATE", args['full_name']
            Deputy.objects.create(**args)
