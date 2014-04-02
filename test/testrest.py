import json
import requests
newrecord = {'site_id':11112,'site_name':u'testtest2','country':u'China','province':u'Shanghai','city':u'Shanghai','latitude':120.1,'longitude':71.9,'owner_id':1003}
r = requests.post('http://192.168.1.106:5000/api/site',data=json.dumps(newrecord),headers={'content-type':'application/json'})
print r.status_code, r.content
#newid = json.loads(r.content)['site_id']
#r = requests.get('http://192.168.2.112:5000/api/site/%d' % newid, headers={'content-type':'application/json'})
r = requests.get('http://192.168.1.106:5000/api/site', headers={'content-type':'application/json'})
print r.content

#r = requests.put('http://192.168.2.112:5000/api/site/')