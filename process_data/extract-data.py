# -*- coding: utf-8 -*-
import os
import json

def new_repo():
    return {'access_rules': []}

def extract_data(filename):
    if os.path.exists(filename):
        with open(filename, 'r') as f:
            content = f.readlines()
            users = set()
            ret = {'groups': [], 'repos': []}
            cur_repo = ''
            repo = new_repo()
            for line in content:
                if line.strip():
                    line = line.strip()
                    if line[0] == '[':
                        item = line[1:-1]
                        if item == 'groups':
                            cur_repo = ''
                        else:
                            if cur_repo:
                                ret['repos'].append(repo.copy())
                                repo = new_repo()
                            repo['name'] = item
                            cur_repo = item
                    elif cur_repo:
                        unit, priv = line.split('=')
                        repo['access_rules'].append(('g' if unit.strip()[0]=='@' else 'u', unit.lstrip('@').strip(), priv))
                    else:
                        group_name, user_str = line.split('=')
                        group_name = group_name.strip()
                        # TODO: may be user or group
                        users = [user.strip() for user in user_str.split(',')]
                        ret['groups'].append((group_name, users))
            return ret
    else:
        raise Exception('file not found!')

filename = '../data/access-rules.txt'

result = extract_data(filename)

print([g for g,u_list in result['groups']])

with open('../data/parsed-data.json', 'w') as f:
    f.write(json.dumps(result))
