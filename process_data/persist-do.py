# -*- coding: utf-8 -*-


import pymysql
import os
import json
from dbconnection import get_connection_config
from uuid import uuid4

class Path():
  def __init__(self, dir_name, repo_name, par_path_id=None):
    self.dir_name = dir_name
    self.repo_name = repo_name
    self.par_path_id = par_path_id
    self._id = uuid4()
    self.par_path_db_id = None
    self._db_id = None
    self.access_rules = None

recreate_db = True

data_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), os.pardir, 'data'))
source = os.path.join(data_dir, 'parsed-data.json')

with open(source, 'r') as f:
  data = json.load(f)
  path_settings = data['paths']
  group_settings = data['groups']

def get_paths(raw_paths):
  paths = []
  # raw path name, access rules
  for rpn,ars in raw_paths:
      if not rpn == '/':
        repo_name = rpn.split(':')[0]
        repo_found = [p for p in paths if p.repo_name == repo_name]
        if not repo_found:
          repo_root_path = Path(repo_name=repo_name, dir_name='/')
          paths.append(repo_root_path)
        else:
          repo_root_path = repo_found[0]
        if rpn.lstrip(repo_name + ':/'):
          sub_path_id = None
          sub_dirs = rpn.lstrip(repo_name + ':/').split('/')
          for index,sub_dir in enumerate(sub_dirs):
            par_path_id = repo_root_path._id if not sub_path_id else sub_path_id
            sub_path_found = [p for p in paths if p.repo_name == repo_name and p.par_path_id == par_path_id and p.dir_name == sub_dir]
            if sub_path_found:
              sub_path_id = sub_path_found[0]._id
            else:
              sub_path = Path(dir_name=sub_dir, par_path_id=par_path_id, repo_name=repo_name)
              paths.append(sub_path)
              sub_path_id = sub_path._id
              if index == len(sub_dirs) - 1:
                sub_path.access_rules = ars
        else:
          repo_root_path.access_rules = ars
  return paths

c = get_connection_config()
conn = pymysql.connect(**c)

INSERT_ACCESS_PATH_SQL = '''
  INSERT INTO access_path (repo_name, dir_name, par_path_id)
  VALUES (%s, %s, %s)
'''

INSERT_ACCESS_RULE_SQL = '''
  INSERT INTO access_rule (path_id, unit, ref, priv)
  VALUES (%s, %s, %s, %s)
'''

def store_path_by_par_path_id(par_path_id, par_path_db_id=None):
  sub_paths = [path for path in paths if path.par_path_id == par_path_id]
  if sub_paths:
    for p in sub_paths:
        cur.execute(INSERT_ACCESS_PATH_SQL, (p.repo_name, p.dir_name, par_path_db_id))
        conn.commit()
        path_db_id = cur.lastrowid
        p._db_id = path_db_id
        if p.access_rules:
          for rule in p.access_rules:
            cur.execute(INSERT_ACCESS_RULE_SQL, (path_db_id, rule[0], rule[1], rule[2]))
          conn.commit()
        store_path_by_par_path_id(p._id, path_db_id)

try:
  groups = set()
  raw_paths = [(rp['name'].encode('utf-8'), rp['access_rules']) for rp in path_settings]
  paths = get_paths(raw_paths)
  with conn.cursor() as cur:
    # check if database recreation is preferred
    # if recreate_db blahhh

    cur.execute('use svn;')
    conn.commit()

    cur.execute(INSERT_ACCESS_PATH_SQL, (None, '/', None))
    conn.commit()
    root_path_db_id = cur.lastrowid
    store_path_by_par_path_id(par_path_id=None, par_path_db_id=root_path_db_id)

    sql = '''
      INSERT INTO access_group (group_code_name, sub_groups, group_users)
      VALUES (%s, %s, %s)
    '''
    for gcn,subs in group_settings:
      # sub groups
      sgs = set([g for g in subs if g[0] == '@'])
      # group users
      gus = set(subs) - sgs
      cur.execute(sql, (gcn, json.dumps(list(sgs)) if sgs else '', json.dumps(list(gus)) if gus else ''))
      gid = cur.lastrowid
      groups.add((gcn, gid))
    conn.commit()
    # print groups
finally:
  conn.close()

