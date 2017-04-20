#!/usr/bin/env python
#-*- coding:utf-8 -*-


import os, re

SRC_PATTERN = re.compile(r'^(?P<name>.+?)\.mp4$', flags=re.M)
DST_PATTERN = re.compile(r'^.+?(?P<ext>\.ass)$', flags=re.M)

SRC_KEY_PATTERN = re.compile(r'\[(?P<key>\d{2})\]')
DST_KEY_PATTERN = SRC_KEY_PATTERN

WORK_DIR = r'I:\animation\[异域-11番小队][噬血狂袭Strike the Blood][BDRIP][1-24+SP][720P][X264-10bit_AAC]'.decode('utf-8')

def FULL_PATH(fname):
    return os.path.join(WORK_DIR, fname)

def get_src_key(data):
    m = SRC_KEY_PATTERN.search(data)
    if not m: raise Exception('No src key found.')
    key = int(m.group('key'))
    return key
    
def get_dst_key(data):
    m = DST_KEY_PATTERN.search(data)
    if not m: raise Exception('No dst key found.')
    key = int(m.group('key'))
    return key
    
def run_rename():
    flist = os.listdir(WORK_DIR.encode('gbk'))
    src_dict = {}
    dst_dict = {}
    todo_list = []
    for fname in flist:
        try:
            m = SRC_PATTERN.match(fname)
            if m: 
                src_dict[get_src_key(fname)] = (fname, m.group('name'))
                continue
            m = DST_PATTERN.match(fname)
            if m:
                dst_dict[get_dst_key(fname)] = (fname, m.group('ext'))
        except :
            continue

    for k,v in src_dict.iteritems():
        if k in dst_dict:
            todo_list.append((v[0], dst_dict[k][0], v[1] + dst_dict[k][1]))
            
    todo_list.sort(key=lambda e: e[0])
    
    for data in todo_list:
        print '%s\n%s\n%s\n\n' %data
        
    msg = raw_input('rename %s files?' %len(todo_list))
    
    if msg not in ('Y', 'y'): return
    
    for data in todo_list:
        print 'rename %s \nto %s\n' %(FULL_PATH(data[1]).encode('gbk'), FULL_PATH(data[2]).encode('gbk'))
        os.rename(FULL_PATH(data[1]).encode('gbk'), FULL_PATH(data[2]).encode('gbk'))
        
    print 'Done!'
    
if __name__ == '__main__':
    run_rename()

