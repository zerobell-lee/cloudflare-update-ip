#!/usr/bin/python3
import requests
import json
import os
import sys

configdir = os.path.dirname(os.path.realpath(__file__))

if len(sys.argv) == 1:

    try:
        fp1 = open(configdir + '/config.json', 'r')
        config = json.load(fp1)
        fp1.close()
    except FileNotFoundError:
        print('Cannot find %s/config.json \nPlease make your own config.json from config-sample.json'%configdir)
        exit(-1)

    ipdir = config['ipdir']
    new_ip = requests.get('http://ifconfig.co/ip').content.decode('utf-8')

    try:
        fp1 = open(ipdir + '/current_ip.txt', 'r')
        current_ip = fp1.read()
        fp1.close()
    except FileNotFoundError:
        print('%s/current_ip.txt Not Found. Creating new current_ip.txt'%ipdir)
        try:
            current_ip = new_ip
            fp2 = open(ipdir + '/current_ip.txt', 'w')
            fp2.write(new_ip)
            fp2.close()
            print('Wrote %s/current_ip.txt'%ipdir)
        except PermissionError:
            print('Cannot Write! Please check permission settings')
            exit(-1)

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


