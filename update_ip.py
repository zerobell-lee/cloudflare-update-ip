#!/usr/bin/python3
import requests
import json
import os
import sys

configdir = os.path.dirname(os.path.realpath(__file__))

if len(sys.argv) == 1:

    try:
        fp = open(configdir + '/config.json', 'r')
        config = json.load(fp)
        fp.close()
    except FileNotFoundError:
        print('Cannot find %s/config.json \nPlease make your own config.json from config-sample.json'%configdir)
        exit(-1)

    new_ip = requests.get('http://ifconfig.co/ip').content.decode('utf-8')[0:-1]

    if 'current_ip' in config.keys():
        current_ip = config['current_ip']
    else:
        print('Current Ip is not defined. Use new Ip as current Ip.')
        current_ip = new_ip
        config['current_ip'] = current_ip
        try:
            fp = open(configdir + '/config.json', 'w')
            json.dump(config, fp)
            fp.close()
        except PermissionError:
            print('Permission Error Occured. Cannot write %s/config.json'%configdir)

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
                                '{"type": "%s", "name": "%s", "content": "%s"}' % (e['type'], e['name'], new_ip))
            print(result.content.decode('utf8'))
        ses.close()

        config['current_ip'] = new_ip

        try:
            fp = open(configdir + '/config.json', 'w')
            json.dump(config, fp)
            fp.close()
        except PermissionError:
            print('Permission Error Occured. Cannot write %s/config.json.'%configdir)



