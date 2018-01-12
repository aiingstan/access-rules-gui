# -*- coding: utf-8 -*-
import os
import json

def new_path():
    return {'access_rules': []}

def extract_data(filename):
    if os.path.exists(filename):
        with open(filename, 'r') as f:
            content = f.readlines()
            users = set()
            ret = {'groups': [], 'paths': []}
            cur_path = ''
            path = new_path()
            for line in content:
                if line.strip():
                    line = line.strip()
                    if line[0] == '[':
                        item = line[1:-1]
                        if item == 'groups':
                            cur_path = ''
                        else:
                            if cur_path:
                                ret['paths'].append(path.copy())
                                path = new_path()
                            path['name'] = item
                            cur_path = item
                    elif cur_path:
                        unit, priv = line.split('=')
                        path['access_rules'].append(('g' if unit.strip()[0]=='@' else 'u', unit.lstrip('@').strip(), priv))
                    else:
                        group_name, user_str = line.split('=')
                        group_name = group_name.strip()
                        # TODO: may be user or group
                        users = [user.strip() for user in user_str.split(',') if user.strip()]
                        ret['groups'].append((group_name, users))
            return ret
    else:
        raise Exception('file not found!')

data_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), os.pardir, 'data'))
filename = os.path.join(data_dir, 'access-rules.txt')
output = os.path.join(data_dir, 'parsed-data.json')
print(filename)
result = extract_data(filename)

print([g for g,u_list in result['groups']])

with open(output, 'w') as f:
    f.write(json.dumps(result, encoding='utf-8'))
