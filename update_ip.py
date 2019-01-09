#!/usr/bin/python3
import requests
import json
import os

configdir = os.path.dirname(os.path.realpath(__file__))

with open(configdir + '/config.json', 'r') as fp:
    config = json.load(fp)

ipdir = config['ipdir']
new_ip = requests.get('http://ifconfig.co/ip').content.decode('utf-8')

with open(ipdir + '/current_ip.txt', 'r') as fp:
        current_ip = fp.read()

if new_ip != current_ip:
    ses = requests.session()
    ses.headers = {'X-Auth-Email': config['email'], 'X-Auth-Key': config['key'], 'Content-Type': 'application/json'}
    records = json.loads(ses.get('https://api.cloudflare.com/client/v4/zones/%s/dns_records' % config['zone']).content.decode('utf8'))['result']
    id_list = []
    for e in records:
        if e['content'] == current_ip:
            id_list.append({ 'id' : e['id'], 'type' : e['type'], 'name': e['name'], 'content' : e['content']})
    for e in id_list:
        result = ses.put('https://api.cloudflare.com/client/v4/zones/%s/dns_records/%s' % (config['zone'], e['id']),
                                '{"type": "%s", "name": "%s", "content": "%s"}' % (e['type'], e['name'], new_ip[0:-1]))
        print(result.content.decode('utf8'))
    ses.close()
    with open(ipdir + '/current_ip.txt', 'w') as fp:
        fp.write(new_ip)


