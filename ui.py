#!/usr/bin/env python2
#-*- coding:utf-8 -*-

import os
import sys
import io
import re
import traceback
from ConfigParser import SafeConfigParser
from Tkinter import *
from ScrolledText import ScrolledText
import tkFileDialog

CF_NAME = 'config.txt'
CUR_DIR = os.path.abspath(os.path.dirname(__file__))
CF_PATH = os.path.join(CUR_DIR, CF_NAME)

class Application:

    CONFIG_ITEMS = ['os_charset', 'work_dir', 'src_pattern', 'dst_pattern',
                            'src_key_pattern', 'dst_key_pattern', 'key_collect']
                            
    def init_config(self):
        self.config = SafeConfigParser({k:'' for k in self.CONFIG_ITEMS})

    def save_config(self):
        for item in self.CONFIG_ITEMS:
            value = getattr(self, item).get()
            self.config.set('DEFAULT', item, value)
        with open(CF_PATH, 'w') as cf:
            self.config.write(cf)
    
    def load_config(self):
        if not os.path.isfile(CF_PATH):
            self.save_config()
            return
        self.config.read(CF_PATH)
        for item in self.CONFIG_ITEMS:
            value = self.config.get('DEFAULT', item)
            if isinstance(value, bytes):
                value = value.decode(sys.getdefaultencoding())
            getattr(self, item).set(value)
            
        if not self.os_charset.get():
            self.os_charset.set(sys.getdefaultencoding())
    
    def on_exit(self):
        try:
            self.save_config()
        except:
            print(traceback.format_exc())
        finally:
            self.root.after(1, self.root.destroy)
    
    def create_widgets(self):
        self.work_dir = StringVar()
        self.src_pattern = StringVar()
        self.dst_pattern = StringVar()
        self.src_key_pattern = StringVar()
        self.dst_key_pattern = StringVar()
        self.key_collect = StringVar()
        self.os_charset = StringVar()
        
        self.entry_frame = Frame(self.root, width=30, bd=2.5)
        self.entry_frame.pack(fill=X, side=TOP)
        
        self.work_dir_frame = Frame(self.entry_frame, bd=0)
        self.work_dir_frame.pack(fill=X, side=TOP)
        self.work_dir_entry = Entry(self.work_dir_frame, textvariable=self.work_dir)
        Label(self.work_dir_frame, text='Work dir:').pack(side=LEFT)
        self.work_dir_button = Button(self.work_dir_frame, text='Browser', height=1)
        self.work_dir_button.pack(side=RIGHT)
        self.work_dir_entry.pack(fill=X, expand=True)
        
        
        self.pattern_frame = Frame(self.entry_frame, bd=0)
        self.pattern_frame.pack(fill=X, side=TOP)
        
        self.src_pattern_entry = Entry(self.pattern_frame, width=40, textvariable=self.src_pattern)
        self.dst_pattern_entry = Entry(self.pattern_frame, width=40, textvariable=self.dst_pattern)
        Label(self.pattern_frame, text='Src pattern:').grid(row=0, column=0)
        self.src_pattern_entry.grid(row=0, column=1)
        Label(self.pattern_frame, text='Dst pattern:').grid(row=1, column=0)
        self.dst_pattern_entry.grid(row=1, column=1)
        
        self.src_key_pattern_entry = Entry(self.pattern_frame, width=40, textvariable=self.src_key_pattern)
        self.dst_key_pattern_entry = Entry(self.pattern_frame, width=40, textvariable=self.dst_key_pattern)
        Label(self.pattern_frame, text='Src key pattern:').grid(row=0, column=2)
        self.src_key_pattern_entry.grid(row=0, column=3)
        Label(self.pattern_frame, text='Dst key pattern:').grid(row=1, column=2)
        self.dst_key_pattern_entry.grid(row=1, column=3)

        self.key_collect_entry = Entry(self.pattern_frame, textvariable=self.key_collect)
        self.charset_entry = Entry(self.pattern_frame, width=8, textvariable=self.os_charset)
        Label(self.pattern_frame, text='Key collect:').grid(row=2, column=2)
        self.key_collect_entry.grid(row=2, column=3, sticky=W)
        Label(self.pattern_frame, text='OS Charset:').grid(row=2, column=0)
        self.charset_entry.grid(row=2, column=1, sticky=W)
        self.charset_entry.config(state='disabled')
        
        self.log_frame = Frame(self.root, bd=2.5)
        self.log_frame.pack(fill=X)
        
        self.log_text = ScrolledText(self.log_frame, bd=0, height=20)
        self.log_text.pack(fill=X, side=TOP)
        
        self.action_frame = Frame(self.log_frame, bd=0)
        self.action_frame.pack(fill=X, side=BOTTOM, expand=True)
        button_width = 10
        self.src_match_button = Button(self.action_frame, text='Src Match', width=button_width)
        self.src_match_button.grid(row=0, column=0)
        self.dst_match_button = Button(self.action_frame, text='Dst Match', width=button_width)
        self.dst_match_button.grid(row=0, column=1)
        self.list_todo_button = Button(self.action_frame, text='List Todo', width=button_width)
        self.list_todo_button.grid(row=0, column=2)
        self.run_button = Button(self.action_frame, text='Run', width=button_width)
        self.run_button.grid(row=0, column=3)
        for i in range(0, 4):
            self.action_frame.grid_columnconfigure(i, weight=1)
            
    def msg_clear(self):
        self.log_text.configure(state='normal')
        self.log_text.delete(1.0, END)
        self.log_text.configure(state='disabled')
            
    def msg_print(self, msg, end='\n'):
        self.log_text.configure(state='normal')
        self.log_text.insert(END, msg+end)
        self.log_text.configure(state='disabled')
            
    def select_work_dir(self):
        work_dir = tkFileDialog.askdirectory() #get unicode string here.
        if work_dir:
            self.work_dir.set(work_dir)
            
    def _match_handler(self, action_name):
        os_charset = self.os_charset.get()
        work_dir = self.work_dir.get()
        if not work_dir:
            self.msg_clear()
            self.msg_print('Fill work_dir firstly!')
            return
        if action_name not in('src', 'dst'):
            return
        
        _pattern = getattr(self, action_name+'_pattern').get()
        if not _pattern:
            self.msg_clear()
            self.msg_print('Fill %s_pattern firstly!' %action_name)
            return
        
        pattern = re.compile(_pattern)
        flist = os.listdir(work_dir.encode(os_charset))
        self.msg_clear()
        counter = 0
        for fname in flist:
            if pattern.match(fname):
                counter += 1
                self.msg_print('%3s %s' %(counter, fname))
        self.msg_print('Match %s files.' %counter)
        
        self.log_text.focus()
        
    def src_match_handler(self):
        self._match_handler('src')
    
    def dst_match_handler(self):
        self._match_handler('dst')
        
    def bind_action(self):
        self.root.protocol('WM_DELETE_WINDOW', self.on_exit)
        self.work_dir_button.config(command=self.select_work_dir)
        self.src_match_button.config(command=self.src_match_handler)
        self.dst_match_button.config(command=self.dst_match_handler)

    def __init__(self, root):
        self.root = root
        self.create_widgets()
        self.init_config()
        self.load_config()
        self.bind_action()

root = Tk()
app = Application(root)
root.mainloop()