#!/usr/bin/env python3
#-*- coding:utf-8 -*-

import os
import sys
import io
import re
import traceback
from configparser import SafeConfigParser
from tkinter import *
from tkinter.scrolledtext import ScrolledText
import tkinter.filedialog
from tkinter.font import Font

CF_NAME = 'config.txt'
CUR_DIR = os.path.abspath(os.path.dirname(__file__))
CF_PATH = os.path.join(CUR_DIR, CF_NAME)

class Application:

    CONFIG_ITEMS = ['os_charset', 'work_dir', 'src_pattern', 'dst_pattern',
                            'src_key_pattern', 'dst_key_pattern', 'key_collect']
    CONFIG_ITEM_DEFAULT_VALS = {
        'src_pattern': r'(?P<name>.+)\.mp4',
        'dst_pattern': r'.+(?P<ext>\.ass)',
        'src_key_pattern': r'-\s(?P<key>\d{2})\s\(',
        'dst_key_pattern': r'-\s(?P<key>\d{2})\s\(',
        'key_collect': 'key',
        'os_charset': 'utf-8',
    }
                            
    def init_config(self):
        self.config = SafeConfigParser({k:'' for k in self.CONFIG_ITEMS})

    def save_config(self):
        for item in self.CONFIG_ITEMS:
            value = getattr(self, item).get()
            self.config.set('DEFAULT', item, value)
        with open(CF_PATH, 'w', encoding='utf-8') as cf:
            self.config.write(cf)
    
    def load_config(self):
        if not os.path.isfile(CF_PATH):
            self.save_config()

        self.config.read(CF_PATH, encoding='utf-8')
        for item in self.CONFIG_ITEMS:
            value = self.config.get('DEFAULT', item)
            if not value:
                value = self.CONFIG_ITEM_DEFAULT_VALS.get(item, '')
            getattr(self, item).set(value)
    
    def on_exit(self):
        try:
            self.save_config()
        except:
            print((traceback.format_exc()))
        finally:
            self.root.after(1, self.root.destroy)
    
    def create_widgets(self):
        self.normal_font = Font(size=10)
        self.bold_font = Font(size=10, weight="bold")
        
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
        self.work_dir_button = Button(self.work_dir_frame, text='Browse', height=1, 
                                        font=self.normal_font)
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
        Label(self.pattern_frame, text='OS charset:').grid(row=2, column=0)
        self.charset_entry.grid(row=2, column=1, sticky=W)
        self.charset_entry.config(state='disabled')
        
        self.log_frame = Frame(self.root, bd=2.5)
        self.log_frame.pack(fill=X)
        
        self.log_text = ScrolledText(self.log_frame, bd=0, height=35)
        self.log_text.tag_config('red', foreground='red', font=self.bold_font)
        self.log_text.tag_config('blue', foreground='blue')
        self.log_text.pack(fill=X, side=TOP)
        
        self.action_frame = Frame(self.log_frame, bd=0)
        self.action_frame.pack(fill=X, side=BOTTOM, expand=True)
        button_width = 10
        self.src_match_button = Button(self.action_frame, text='Src Match', 
                                        width=button_width, font=self.normal_font)
        self.src_match_button.grid(row=0, column=0)
        self.dst_match_button = Button(self.action_frame, text='Dst Match', 
                                        width=button_width, font=self.normal_font)
        self.dst_match_button.grid(row=0, column=1)
        self.list_todo_button = Button(self.action_frame, text='List Todo', 
                                        width=button_width, font=self.normal_font)
        self.list_todo_button.grid(row=0, column=2)
        self.run_button = Button(self.action_frame, text='Run', width=button_width,
                                        foreground='red', font=self.bold_font)
        self.run_button.grid(row=0, column=3)
        self.run_button.configure(state='disabled')
        for i in range(0, 4):
            self.action_frame.grid_columnconfigure(i, weight=1)
            
    def msg_clear(self):
        self.log_text.configure(state='normal')
        self.log_text.delete(1.0, END)
        self.log_text.configure(state='disabled')
        
    def msg_print(self, msg, tag=None, end='\n'):
        self.log_text.configure(state='normal')
        self.log_text.insert(END, msg+end, tag)
        self.log_text.configure(state='disabled')
        
    def msg_print_x(self, msg_list, end='\n'):
        self.log_text.configure(state='normal')
        for msg in msg_list:
            if isinstance(msg, str):
                self.log_text.insert(END, msg)
            else:
                text, tags = msg
                self.log_text.insert(END, text, tags)
        self.log_text.insert(END, end)
        self.log_text.configure(state='disabled')
        
    def select_work_dir(self):
        work_dir = tkinter.filedialog.askdirectory() #get unicode string here.
        if work_dir:
            self.work_dir.set(work_dir)
            
    def init_vars(self):
        self.todo_list = []
        self.src_dict = {}
        self.dst_dict = {}
        self.dst_file_num = 0
        
    def reset_vars(self):
        self.todo_list[:] = []
        self.src_dict.clear()
        self.dst_dict.clear()
        self.dst_file_num = 0
        
    def check_vars(self):
        for var in ('os_charset', 'work_dir', 'key_collect'):
            if not getattr(self, var).get():
                self.msg_print_x((
                    (var, ('red',)), ' can\'t be empty!',
                ))
                return False
        return True
    
    def get_key_by_pattern(self, pattern, data):
        key_collect = self.key_collect.get()
        m = pattern.search(data)
        if not m or not key_collect: return None
        key_collect = [k.strip() for k in key_collect.split(',')]
        key = (m.group(k) or '' for k in key_collect)
        key = '_'.join(key)
        if key.count('_') == len(key): return None
        return key
        
    def get_src_key(self, data):
        src_key_pattern = re.compile(self.src_key_pattern.get())
        return self.get_key_by_pattern(src_key_pattern, data)
        
    def get_dst_key(self, data):
        dst_key_pattern = re.compile(self.dst_key_pattern.get())
        return self.get_key_by_pattern(dst_key_pattern, data)
        
    def get_full_path(self, fname):
        return os.path.join(self.work_dir.get(), fname)
        
    def _load_todo_list_handler(self):
        self.reset_vars()
        self.run_button.configure(state='disabled')
        self.msg_clear()
        
        if not self.check_vars():
            return
        
        work_dir = self.work_dir.get()
        src_pattern = re.compile(self.src_pattern.get())
        dst_pattern = re.compile(self.dst_pattern.get())
        for de in os.scandir(work_dir):
            if not de.is_file():
                continue
            fname = de.name
            #print 'test %s' %fname
            m = src_pattern.match(fname)
            if m: 
                src_key = self.get_src_key(fname)
                if not src_key: continue
                #print 'src_key %s' %src_key
                self.src_dict[src_key] = (fname, m.group('name'))
                continue
            
            m = dst_pattern.match(fname)
            if m:
                dst_key = self.get_dst_key(fname)
                if not dst_key: continue
                #print 'dst_key %s' %dst_key
                self.dst_dict.setdefault(dst_key, [])
                self.dst_dict[dst_key].append((fname, m.group('ext')))
                self.dst_file_num += 1
        msg_list = (
            'Found ', (str(len(self.src_dict)), ('red', )), ' src file, ',
            (str(self.dst_file_num), ('red', )), ' dst file.\n',
        )
        self.msg_print_x(msg_list)
        if len(self.src_dict) == 0 and len(self.dst_dict) == 0:
            msg_list = (
                'No file found, please modify ',
                ('src_pattern', ('red', )), ', ',
                ('dst_pattern', ('red', )), ', ',
                ('src_key_pattern', ('red', )), ', ',
                ('dst_key_pattern', ('red', )), '.',
            )
            self.msg_print_x(msg_list)
            return 
            
        for k,v in self.src_dict.items():
            if k in self.dst_dict:
                for fname, ext in self.dst_dict[k]:
                    self.todo_list.append((v[0], fname, v[1] + ext))
                
        self.todo_list.sort(key=lambda e: e[0])
        
        for data in self.todo_list:
            msg_list = (
                ('[src file] ', ('blue', )), '%s\n' %data[0],
                ('[dst old ] ', ('blue', )), '%s\n' %data[1],
                ('[dst new ] ', ('blue', )), '%s\n' %data[2]
            )
            self.msg_print_x(msg_list)
            
        if not self.todo_list:
            self.msg_print('No file to rename.', tag=('red', ))
            return
            
        self.msg_print('Filenames with no change will be skipped.')
        msg_list =(
            'Please click ', ('Run', ('red', )) ,' button to rename ', 
            (str(len(self.todo_list)), ('red', )),
            ' files.'
        )
        self.msg_print_x(msg_list)
        self.run_button.configure(state='normal')
        
        self.log_text.focus()
        
        
    def _match_handler(self, action_name):
        self.reset_vars()
        self.run_button.configure(state='disabled')
        self.msg_clear()
        
        work_dir = self.work_dir.get()
        if not self.check_vars():
            return
        if action_name not in('src', 'dst'):
            return
        
        _pattern = getattr(self, action_name+'_pattern').get()
        if not _pattern:
            self.msg_print((
                'Fill ', ('%s pattern' %action_name, ('red',)), ' firstly!',
            ))
            return
        
        pattern = re.compile(_pattern)
        flist = os.listdir(work_dir)
        counter = 0
        for de in os.scandir(work_dir):
            if not de.is_file():
                continue
            fname = de.name
            if pattern.match(fname):
                counter += 1
                self.msg_print_x((
                    ('[%3s]' %counter, ('blue', )), '\t%s' %fname,
                ))
        self.msg_print_x((
            'Match ', (str(counter), ('red', )), ' files.'
        ))
        
        self.log_text.focus()
        
    def _run_handler(self):
        self.msg_clear()
        
        done = 0
        for data in self.todo_list:
            path_old = self.get_full_path(data[1])
            path_new = self.get_full_path(data[2])
            if data[1] == data[2]:
                self.msg_print_x((
                    ('[skipped]', ('red', )),
                    (' rename\n', ('blue', )), path_old, '\n',
                    ('to\n', ('blue', )), path_new, '\n'
                ))
            else:
                self.msg_print_x((
                    ('rename\n', ('blue', )), path_old, '\n',
                    ('to\n', ('blue', )), path_new, '\n'
                ))
                os.rename(path_old, path_new)
                done += 1
        
        self.msg_print_x((
            'Done! Total:', (str(len(self.todo_list)), ('red', )),
            ' Skipped:', (str(len(self.todo_list) - done), ('red', )),
            ' Rename:', (str(done), ('red', ))
        ))

    def src_match_handler(self):
        self._match_handler('src')
    
    def dst_match_handler(self):
        self._match_handler('dst')
        
    def list_todo_handler(self):
        self._load_todo_list_handler()
        
    def run_handler(self):
        self._run_handler()
        
    def on_work_dir_changed(self):
        if self.old_work_dir != self.work_dir.get():
            self.run_button.config(state='disabled')
            self.reset_vars()
            self.msg_clear()
        return True
        
    def bind_action(self):
        self.root.protocol('WM_DELETE_WINDOW', self.on_exit)
        self.work_dir_button.config(command=self.select_work_dir)
        self.src_match_button.config(command=self.src_match_handler)
        self.dst_match_button.config(command=self.dst_match_handler)
        self.list_todo_button.config(command=self.list_todo_handler)
        self.run_button.config(command=self.run_handler)
        self.work_dir_entry.config(validate='focusout', validatecommand=self.on_work_dir_changed)
        self.old_work_dir = self.work_dir.get()

    def __init__(self, root):
        self.root = root
        self.init_vars()
        self.create_widgets()
        self.init_config()
        self.load_config()
        self.bind_action()

root = Tk()
root.title("Rename Subtitle For Video [ By lzmyhzy (lzmyhzy@gmail.com) ]")
app = Application(root)
root.mainloop()