# -*- coding: utf-8 -*-
import os
import pickle
from PyQt4.QtGui import (QLabel, QRadioButton, QLineEdit, QCheckBox, QComboBox,QListWidget,
                         QListWidgetItem, QTableView)

class Settings():
    compressable_types = [QLabel, QRadioButton, QLineEdit, QCheckBox, QComboBox,QListWidget,
                         QListWidgetItem, QTableView]
    def __init__(self,filename):
        if os.path.isfile(filename):
            self.settings = pickle.load(filename)
        else:
            self.settings = {}
        self.config = {}
        self.config_name = 'new configuration'

    def load_config(self,config_name):
        if config_name in self.settings:
            self.config = self.settings[config_name]
            self.config_name = config_name
        else:
            raise ValueError('Configuration %s does not exist'%config_name)

    def save_config(self):
        self.settings[self.config_name] = self.config
        pickle.dump(self.settings)

    def register(self,name,obj):
        self.config[name] = obj

    def set_pageobjects(self, page):
        for name in self.config:
            if hasattr(page,name):
                setattr(page,name,self.config[name])
                # page_attr = getattr(page,name)

    def get_object(self, name):
        return self.config[name]

    def is_registered(self,name):
        return name in self.config