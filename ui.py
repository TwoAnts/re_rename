#!/usr/bin/env python2
#-*- coding:utf-8 -*-

from Tkinter import *

class Application:

    def createWidgets(self):
        self.entry_frame = Frame(self.root, width=30, bd=2.5)
        self.entry_frame.pack(fill=X, side=TOP)
        
        self.work_dir_frame = Frame(self.entry_frame, bd=0)
        self.work_dir_frame.pack(fill=X, side=TOP)
        self.work_dir_entry = Entry(self.work_dir_frame)
        Label(self.work_dir_frame, text='Work dir:').pack(side=LEFT)
        self.work_dir_button = Button(self.work_dir_frame, text='Browser', height=1)
        self.work_dir_button.pack(side=RIGHT)
        self.work_dir_entry.pack(fill=X, expand=True)
        
        
        self.pattern_frame = Frame(self.entry_frame, bd=0)
        self.pattern_frame.pack(fill=X, side=TOP)
        
        self.src_pattern_entry = Entry(self.pattern_frame, width=40)
        self.dst_pattern_entry = Entry(self.pattern_frame, width=40)
        Label(self.pattern_frame, text='Src pattern:').grid(row=0, column=0)
        self.src_pattern_entry.grid(row=0, column=1)
        Label(self.pattern_frame, text='Dst pattern:').grid(row=1, column=0)
        self.dst_pattern_entry.grid(row=1, column=1)
        
        self.src_key_pattern_entry = Entry(self.pattern_frame, width=40)
        self.dst_key_pattern_entry = Entry(self.pattern_frame, width=40)
        Label(self.pattern_frame, text='Src key pattern:').grid(row=0, column=2)
        self.src_key_pattern_entry.grid(row=0, column=3)
        Label(self.pattern_frame, text='Dst key pattern:').grid(row=1, column=2)
        self.dst_key_pattern_entry.grid(row=1, column=3)

        self.key_collect_entry = Entry(self.pattern_frame)
        self.charset_entry = Entry(self.pattern_frame, width=8)
        Label(self.pattern_frame, text='Key collect:').grid(row=2, column=2)
        self.key_collect_entry.grid(row=2, column=3, sticky=W)
        Label(self.pattern_frame, text='Charset:').grid(row=2, column=0)
        self.charset_entry.grid(row=2, column=1, sticky=W)
        
        

    def __init__(self, root):
        self.root = root
        self.createWidgets()

root = Tk()
app = Application(root)
root.mainloop()