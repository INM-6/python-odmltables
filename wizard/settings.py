# -*- coding: utf-8 -*-
import os
import pickle
import copy
from PyQt4.QtGui import (QLabel, QRadioButton, QLineEdit, QCheckBox, QComboBox,QListWidget,
                         QListWidgetItem, QTableView, QPushButton)

class Settings():
    compressable_types = [QLabel, QRadioButton, QLineEdit, QCheckBox, QComboBox,QListWidget,
                         QTableView,QListWidgetItem]
    def __init__(self,filename):
        self.filename = filename

        self.settings = {}
        self.config = {'attributes':{},'objects':{}}
        self.config_name = ''

        try:
            with open(filename, 'rb') as handle:
                self.settings = pickle.load(handle)
        except:
            if os.path.isfile(filename):
                raise IOError('Configuration file "%s" could not be loaded. Delete broken file and restart.'%filename)

        self.basicdtypes = [bool,str,float,int,long,complex]


    def load_config(self,config_name):
        if config_name in self.settings:
            # self.config = self.settings[config_name]
            self.config_name = config_name
            # self.configchanged = False
            print 'Loading config "%s"'%config_name
        else:
            raise ValueError('Configuration %s does not exist'%config_name)

    def set_config_name(self,config_name):
        self.config_name = config_name

    def save_config(self):
        curr_config_simple = self.simplify_pyqt(self.config)
        self.settings[self.config_name] = curr_config_simple

        with open(self.filename, 'wb') as handle:
            pickle.dump(self.settings,handle)

    def delete_config(self,config_name):
        if config_name not in self.settings:
            raise ValueError('Configuration "%s" not'
                             'present in settings.'%config_name)
        else:
            self.settings.pop(config_name)
            with open(self.filename, 'wb') as handle:
                pickle.dump(self.settings,handle)

    def get_all_config_names(self):
        return [n for n in self.settings.keys() if n!='']

    def register(self,name,obj,useconfig=True):
        if (useconfig and self.config): #TODO: Go on here. Consistent data reconstruction.
            self.update_from_config(name,obj)

        if hasattr(obj,name):
            self.config['attributes'][name] = obj
        else:
            if type(obj) in [bool,str,float,int,long,complex]:
                raise TypeError('You should only register mutable objects as non-attributes.')
            else:
                self.config['objects'][name] = obj

        # self.configchanged = True



    # def set_pageobjects(self, page):
    #     for name in self.config:
    #         if hasattr(page,name):
    #             setattr(page,name,self.config[name])
    #             # page_attr = getattr(page,name)

    def get_object(self, name):
        if name in self.config['attributes']:
            return getattr(self.config['attributes'][name],name)
        elif name in self.config['objects']:
            return self.config['objects'][name]
        else:
            raise ValueError('"%s" is not registered'%name)

    def is_registered(self,name):
        return ((name in self.config['attributes'])
                or (name in self.config['objects']))

    def simplify_pyqt(self,conf):
        conf = copy.deepcopy(conf)
        for name, property in conf['attributes'].iteritems():
            conf['attributes'][name] = self.simplifyprop(getattr(self.config['attributes'][name], name))
        for name, property in conf['objects'].iteritems():
            conf['objects'][name] = self.simplifyprop(self.config['objects'][name])
        return conf

    def simplifyprop(self, prop):
        if type(prop) == QPushButton: #QPushButton
            return (str(prop.text()),str(prop.styleSheet()),str(type(prop)))
        elif hasattr(prop,'isChecked'): #[QCheckBox,QRadioButton]:
            return (prop.isChecked(),str(str(type(prop))))
        elif hasattr(prop,'text'): # QLabel, QLineEdit
            return (str(prop.text()),str(str(type(prop))))
        elif hasattr(prop,'count') and hasattr(prop,'itemText') and hasattr(prop,'currentIndex'): # QComboBox
            return ([str(prop.itemText(c)) for c in range(prop.count())],prop.currentIndex(),str(type(prop)))
        elif hasattr(prop,'count') and hasattr(prop,'selectedIndexes'): #QListWidget
            return ([str(prop.item(c).text()) for c in range(prop.count())],prop.selectedIndexes(),str(type(prop)))
        elif type(prop) in self.basicdtypes: # Basic datatypes
            return (prop,str(type(prop)))
        elif hasattr(prop,'__iter__'): # List of objects
            return [self.simplifyprop(item) for item in prop]
        else:
            raise ValueError('Can not simplify "%s"'%(prop))

    def update_from_config(self,name,obj,index=None):
        if not self.config_name:
            # print 'Can not get %s from config. No config loaded.'%name
            return

        # # break criteria: not a saved tuple
        # if (type(self.get_object(name)) not in [tuple,list] or
        #     len(self.get_object(name))==0 or
        #     type(self.get_object(name)[0]) in self.basicdtypes):
        #     print 'Exiting update_from_config, because of invalid input %s'%(str(self.get_object(name)))
        #     return

        if name not in self.settings[self.config_name]['attributes'].keys() + self.settings[self.config_name]['objects'].keys():
            print 'Object %s not present in saved config'%name
            return

        if name in self.settings[self.config_name]['attributes']:
            prop = self.settings[self.config_name]['attributes'][name]
        elif name in self.settings[self.config_name]['objects']:
            prop = self.settings[self.config_name]['objects'][name]
        # prop = self.get_object(name)
        if index != None:
            prop = prop[index]

        if type(obj)!= list:
            if (name in self.settings[self.config_name]['attributes']) and (str(type(getattr(obj,name))) != prop[-1]):
                raise TypeError('Object to fill has type %s but saved data fits to type %s'%(type(getattr(obj,name)),prop[-1]))
            if (name in self.settings[self.config_name]['objects']) and (str(type(obj)) != prop[-1]):
                raise TypeError('Object to fill has type %s but saved data fits to type %s'%(type(obj),prop[-1]))

        # if name in self.settings[self.config_name]['attributes']:
        #     prop = self.settings[self.config_name]['attributes'][name]
        # elif name in self.settings[self.config_name]['objects']:
        #     prop = self.settings[self.config_name]['objects'][name]
        # else:
        #     raise ValueError('"%s" is not registered'%name)

        if type(obj) == QPushButton: #QPushButton
            obj.setText(prop[0])
            obj.setStyleSheet(prop[1])
            # return obj
        elif hasattr(obj,'isChecked'): #[QCheckBox,QRadioButton]:
            obj.setChecked(prop[0])
        elif hasattr(obj,'text'): # QLabel, QLineEdit
            obj.setText(prop[0])
            # return obj
        elif hasattr(obj,'count') and hasattr(obj,'itemText') and hasattr(obj,'currentIndex'): #QComboBox
            obj.clear()
            obj.addItems(prop[0])
            obj.setCurrentIndex(prop[1])
            # return obj
        elif hasattr(obj,'count') and hasattr(obj,'selectedIndexes'): #QListWidget
            # removing old items
            obj.clear()
            for itemlabel in prop[0]:
                item = QListWidgetItem()
                item.setText(itemlabel)
                obj.addItem(item)
            for itemid in range(obj.count()):
                if itemid in prop[1]:
                    obj.item(itemid).setSelected(True)
                else:
                    obj.item(itemid).setSelected(False)
            # return obj
        elif hasattr(obj,name):
            if prop[1] not in [str(p) for p in self.basicdtypes]: # Basic datatypes
                raise TypeError('Attribute of type %s can not be recovered'%type(prop))
            else:
                setattr(obj,name,prop[0])
            # return (prop,type(prop))
        elif hasattr(obj,'__iter__'): # List of objects
            if len(obj) == len(prop):
                for i,item in enumerate(obj):
                    self.update_from_config(name,item,index=i)
        else:
            raise ValueError('Can not update object "%s" from config "%s"'%(obj,name))

    # def reinflate_pyqt(self,conf):
    #     conf = copy.deepcopy(conf)
    #     for name, property in conf['attributes'].iteritems():
    #         conf['attributes'][name] = self.reinflateprop(getattr(self.config['attributes'][name], name))
    #     for name, property in conf['objects'].iteritems():
    #         conf['objects'][name] = self.reinflateprop(self.config['objects'][name])
    #     return conf