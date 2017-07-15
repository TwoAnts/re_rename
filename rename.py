#!/usr/bin/env python
#-*- coding:utf-8 -*-


import os, re, traceback
from ConfigParser import SafeConfigParser

CF_NAME = 'config.ini'
CUR_DIR = os.path.abspath(os.path.dirname(__file__))
CF_PATH = os.path.join(CUR_DIR, CF_NAME)

OS_CHARSET = None

SRC_PATTERN = None
DST_PATTERN = None

KEY_COLLECT = []
SRC_KEY_PATTERN = None
DST_KEY_PATTERN = None

WORK_DIR = None

def FULL_PATH(fname):
    return os.path.join(WORK_DIR, fname)
    
def parse_config():
    config_note = \
'''# -*- coding:utf-8 -*-

#Please fill this file first.
#This file's charset should be utf-8.
#
#OS_CHARSET: Charset of the os. For example, if you use it on windows in Chinese, use 'gbk'. 
#WORK_DIR: The dir contains the rename files.
#SRC_PATTERN: The fname's re pattern for getting the src file in WORK_DIR.
#             Please use (?P<name>) to specific the file name.
#DST_PATTERN: The fname's re pattern for getting the dst file in WORK_DIR.
#             Please use (?P<ext>) to specific the file name suffix. 
#The final file name will be '<name><ext>'
#
#KEY_COLLECT: Declare the key in KEY_PATTERN, e.g. key1,key2,key3
#SRC_KEY_PATTERN: The fname's re pattern to get the compare key of src file.
#DST_KEY_PATTERN: The fname's re pattern to get the compare key of dst file.

'''
    
    config = SafeConfigParser({k:'' for k in [
                        'OS_CHARSET', 'WORK_DIR', 'SRC_PATTERN', 'SRC_PATTERN',
                        'DST_PATTERN', 'KEY_COLLECT', 'SRC_KEY_PATTERN', 'DST_KEY_PATTERN']})
    config.set('DEFAULT', 'SRC_PATTERN', r'(?P<name>.+)\.mp4')
    config.set('DEFAULT', 'DST_PATTERN', r'[^\.]+(?P<ext>\.ass)')        
    config.set('DEFAULT', 'KEY_COLLECT', 'key')
    config.set('DEFAULT', 'SRC_KEY_PATTERN', r'\[(?P<key>\d{2})\]')
    config.set('DEFAULT', 'DST_KEY_PATTERN', r'\[(?P<key>\d{2})\]')
    if not os.path.isfile(CF_PATH):
        if os.path.exists(CF_PATH):
            raise Exception('Can\'t create the config file.', 'in parse_config()')
        
        with open(CF_PATH, 'w') as cf:
            cf.write(config_note)
            config.write(cf)
        print 'Please fill the %s first.' %CF_NAME
        exit()
        
    config.read(CF_PATH)
    try:
        global OS_CHARSET, WORK_DIR, SRC_PATTERN, DST_PATTERN, \
                    SRC_KEY_PATTERN, DST_KEY_PATTERN, KEY_COLLECT
        OS_CHARSET =  config.get('DEFAULT', 'OS_CHARSET')
        WORK_DIR = config.get('DEFAULT', 'WORK_DIR').decode('utf-8')
        SRC_PATTERN = re.compile(config.get('DEFAULT', 'SRC_PATTERN'))
        DST_PATTERN = re.compile(config.get('DEFAULT', 'DST_PATTERN'))
        SRC_KEY_PATTERN = re.compile(config.get('DEFAULT', 'SRC_KEY_PATTERN'))
        DST_KEY_PATTERN = re.compile(config.get('DEFAULT', 'DST_KEY_PATTERN'))
        KEY_COLLECT = [k.strip() for k in config.get('DEFAULT', 'KEY_COLLECT').split(',')]
    except Exception as e:
        print 'Please fill all options.'
        print traceback.format_exc()
        exit()
        
def get_key_by_pattern(pattern, data):
    m = pattern.search(data)
    if not m: return None
    key = (m.group(k) or '' for k in KEY_COLLECT)
    key = '_'.join(key)
    if key.count('_') == len(key): return None
    return key
        
def get_src_key(data):
    return get_key_by_pattern(SRC_KEY_PATTERN, data)
    
def get_dst_key(data):
    return get_key_by_pattern(DST_KEY_PATTERN, data)
    
def run_rename():
    print 'WORK_DIR: %s' %WORK_DIR
    flist = os.listdir(WORK_DIR.encode(OS_CHARSET))
    src_dict = {}
    dst_dict = {}
    todo_list = []
    dst_file_num = 0
    for fname in flist:
        #print 'test %s' %fname
        m = SRC_PATTERN.match(fname)
        if m: 
            src_key = get_src_key(fname)
            if not src_key: continue
            #print 'src_key %s' %src_key
            src_dict[src_key] = (fname, m.group('name'))
            continue
        
        m = DST_PATTERN.match(fname)
        if m:
            dst_key = get_dst_key(fname)
            if not dst_key: continue
            #print 'dst_key %s' %dst_key
            dst_dict.setdefault(dst_key, [])
            dst_dict[dst_key].append((fname, m.group('ext')))
            dst_file_num += 1
       
    print 'Found %s src file, %s dst file.' %(len(src_dict), dst_file_num)
    if len(src_dict) == 0 and len(dst_dict) == 0:
        print 'No file found, please modify PATTERN and KEY_PATTERN.'
        exit()
        
    for k,v in src_dict.iteritems():
        if k in dst_dict:
            for fname, ext in dst_dict[k]:
                todo_list.append((v[0], fname, v[1] + ext))
            
    todo_list.sort(key=lambda e: e[0])
    
    for data in todo_list:
        print '%s\n%s\n%s\n\n' %data
        
    if not todo_list: 
        print 'No file to rename.'
        exit()
    print 'File name no change will be skipped.'
    msg = raw_input('rename %s files?(Y/n) ' %len(todo_list))
    
    if msg not in ('Y', 'y'): return
    
    done = 0
    for data in todo_list:
        skip = '[skipped] '  if data[1] == data[2] else '' # if name no change, skip.
        print '%srename %s \nto %s\n' %(skip,
                                        FULL_PATH(data[1]).encode(OS_CHARSET),
                                        FULL_PATH(data[2]).encode(OS_CHARSET))
        if skip: continue
        os.rename(FULL_PATH(data[1]).encode(OS_CHARSET), FULL_PATH(data[2]).encode(OS_CHARSET))
        done += 1
        
    print 'Done! Total:%s Skipped:%s Rename:%s.' %(len(todo_list), len(todo_list) - done, done)
    
if __name__ == '__main__':
    parse_config()
    run_rename()

