# -*- coding: utf-8 -*-
import copy
import os
import pickle

from future.utils import iteritems
from past.builtins import long
from PyQt5.QtWidgets import (QLabel, QRadioButton, QLineEdit, QCheckBox, QComboBox,
                             QListWidget,
                             QListWidgetItem, QTableView, QPushButton)


class Settings():
    compressable_types = [QLabel, QRadioButton, QLineEdit, QCheckBox, QComboBox,
                          QListWidget,
                          QTableView, QListWidgetItem]

    def __init__(self, filename):
        self.filename = filename

        self.settings = {}
        self.config = {'attributes': {}, 'objects': {}}
        self.config_name = ''

        try:
            with open(filename, 'rb') as handle:
                self.settings = pickle.load(handle)
        except:
            if os.path.isfile(filename):
                raise IOError(
                    'Configuration file "%s" could not be loaded. Delete '
                    'broken file and restart.' % filename)

        self.basicdtypes = [bool, str, float, int, long, complex]

    def load_config(self, config_name):
        if config_name in self.settings:
            # self.config = self.settings[config_name]
            self.config_name = config_name
            self.config = {'attributes': {}, 'objects': {}}
            # self.configchanged = False
            print('Loading config "%s"' % config_name)
        else:
            raise ValueError('Configuration %s does not exist' % config_name)

    def set_config_name(self, config_name):
        self.config_name = config_name

    def save_config(self):
        curr_config_simple = self.simplify_pyqt(self.config)
        self.settings[self.config_name] = curr_config_simple

        with open(self.filename, 'wb') as handle:
            pickle.dump(self.settings, handle)

    def delete_config(self, config_name):
        if config_name not in self.settings:
            raise ValueError('Configuration "%s" not'
                             'present in settings.' % config_name)
        else:
            self.settings.pop(config_name)
            with open(self.filename, 'wb') as handle:
                pickle.dump(self.settings, handle)

    def get_all_config_names(self):
        return [n for n in list(self.settings) if n != '']

    def register(self, name, obj, useconfig=True):
        if useconfig and self.config and (not self.is_registered(name)) and self.can_be_loaded(
                name):
            self.update_from_config(name, obj)

        if hasattr(obj, name):
            self.config['attributes'][name] = obj
        else:
            if type(obj) in [bool, str, float, int, long, complex]:
                raise TypeError(
                    'You should only register mutable objects as '
                    'non-attributes.')
            else:
                self.config['objects'][name] = obj

    def get_object(self, name):
        if name in self.config['attributes']:
            return getattr(self.config['attributes'][name], name)
        elif name in self.config['objects']:
            return self.config['objects'][name]
        else:
            raise ValueError('"%s" is not registered' % name)

    def can_be_loaded(self, name):
        if self.config_name:
            return ((name in self.settings[self.config_name]['attributes'])
                    or (name in self.settings[self.config_name]['objects']))
        else:
            return False

    def is_registered(self, name):
        return ((name in self.config['attributes'])
                or (name in self.config['objects']))

    def remove_object(self, name):
        if name in self.config['attributes']:
            return self.config['attributes'].pop(name)
        elif name in self.config['objects']:
            return self.config['objects'].pop(name)

    def simplify_pyqt(self, conf):
        simple_conf = {'attributes': {},
                       'objects': {}}
        for name, property in iteritems(conf['attributes']):
            simple_conf['attributes'][name] = self.simplifyprop(
                getattr(self.config['attributes'][name], name))
        for name, property in iteritems(conf['objects']):
            simple_conf['objects'][name] = self.simplifyprop(
                self.config['objects'][name])
        return simple_conf

    def simplifyprop(self, prop):
        if type(prop) == QPushButton:  # QPushButton
            return (str(prop.text()), str(prop.styleSheet()), str(type(prop)),
                    'pyqt')
        elif hasattr(prop, 'isChecked'):  # [QCheckBox,QRadioButton]:
            return (prop.isChecked(), str(type(prop)), 'pyqt')
        elif hasattr(prop, 'text'):  # QLabel, QLineEdit
            return (str(prop.text()), str(type(prop)), 'pyqt')
        elif hasattr(prop, 'count') and hasattr(prop, 'itemText') and hasattr(
                prop, 'currentIndex'):
            indexes = prop.currentIndex()
            if hasattr(indexes, 'row') and hasattr(indexes, 'column'):
                indexes = [(i.row(), i.column()) for i in indexes]
            return ([str(prop.itemText(c)) for c in list(range(prop.count()))], indexes,
                    str(type(prop)),'pyqt')
        elif hasattr(prop, 'count') and hasattr(prop,
                                                'selectedIndexes'):  #
            # QListWidget
            return ([str(prop.item(c).text()) for c in list(range(prop.count()))],
                    [(p.row(),p.column()) for p in prop.selectedIndexes()], str(type(prop)), 'pyqt')
        elif type(prop) in self.basicdtypes:  # Basic datatypes
            return (prop, str(type(prop)), 'basic')
        elif type(prop) == list:  # List of objects
            return [self.simplifyprop(item) for item in prop]
        elif type(prop) == dict:
            return {key: self.simplifyprop(value) for key, value in iteritems(prop)}
        else:
            raise ValueError('Can not simplify "%s"' % (prop))

    def _update_pyqt_object_from_config(self, obj, config_data, index=None):

        if index is not None:
            obj = obj[index]

        if type(obj) == QPushButton:  # QPushButton
            obj.setText(config_data[0])
            obj.setStyleSheet(config_data[1])
            # return obj
        elif hasattr(obj, 'isChecked'):  # [QCheckBox,QRadioButton]:
            obj.setChecked(config_data[0])
        elif hasattr(obj, 'text'):  # QLabel, QLineEdit
            obj.setText(config_data[0])
            # return obj
        elif hasattr(obj, 'count') and hasattr(obj, 'itemText') and hasattr(obj,
                                                                            'currentIndex'):  # QComboBox
            obj.clear()
            obj.addItems(config_data[0])
            obj.setCurrentIndex(config_data[1])
            # return obj
        elif hasattr(obj, 'count') and hasattr(obj,
                                               'selectedIndexes'):  #
            # QListWidget
            # removing old items
            obj.clear()
            for itemlabel in config_data[0]:
                item = QListWidgetItem()
                item.setText(itemlabel)
                obj.addItem(item)
            for itemid in list(range(obj.count())):
                if itemid in config_data[1]:
                    obj.item(itemid).setSelected(True)
                else:
                    obj.item(itemid).setSelected(False)

    def _update_basetype(self, parent, name, config_data, index=None):
        if config_data[1] not in [str(p) for p in
                                  self.basicdtypes]:  # Basic datatypes
            raise TypeError(
                'Attribute of type %s can not be recovered' % type(
                    config_data))
        elif index != None:
            if type(parent) == list and index >= len(parent):
                parent.append(config_data[0])
            else:
                parent[index] = config_data[0]
        else:
            setattr(parent, name, config_data[0])

    def _update_list(self, obj, prop, name, index=None):
        if any([p[-1] == 'pyqt' for p in prop]) and len(prop) != len(obj):
            raise IndexError('Wrong size of obj')
        else:
            if index:
                obj = obj[index]
            for i, _ in enumerate(prop):
                self.update_data(obj, prop[i], name, index=i)

    def _update_dict(self, obj, prop, index=None):
        if type(obj) != dict:
            raise TypeError('Wrong type of object')
        if any([p[-1] == 'pyqt' for p in prop]) and len(prop) != len(obj):
            # better: check if dict contain same keys
            raise IndexError('Wrong size of object')
        if index:
            if index not in obj:
                obj[index] = {}
            obj = obj[index]
        for key, value in iteritems(prop):
            self.update_data(obj, prop[key], name=key, index=key)

    def _get_saved_obj(self, name):
        prop = None
        if name not in list(self.settings[self.config_name]['attributes']) + \
                list(self.settings[self.config_name]['objects']):
            print('Object %s not present in saved config' % name)
        else:
            if name in self.settings[self.config_name]['attributes']:
                prop = self.settings[self.config_name]['attributes'][name]
            elif name in self.settings[self.config_name]['objects']:
                prop = self.settings[self.config_name]['objects'][name]
        return prop

    def update_from_config(self, name, obj):
        if not self.config_name:
            return

        prop = self._get_saved_obj(name)

        if hasattr(obj, name):
            o = getattr(obj, name)
        else:
            o = obj

        if type(o) != list and type(o) != dict and type(prop) != dict:
            if (name in self.settings[self.config_name]['attributes']) and \
                    (str(type(getattr(o, name))) != prop[-2]):
                raise TypeError('Object to fill has type %s but saved data '
                                'fits to type %s' % (type(o), prop[-2]))
            if (name in self.settings[self.config_name]['objects']) and \
                    (str(type(o)) != prop[-2]):
                raise TypeError('Object to fill has type %s but saved data '
                                'fits to type %s' % (type(o), prop[-2]))
        self.update_data(obj, prop, name)

    def update_data(self, obj, prop, name, index=None):
        # if this is an attribute, then consider the attribute as main object
        if hasattr(obj, name):
            obj = getattr(obj, name)

        if type(prop) == tuple and prop[-1] == 'pyqt':
            self._update_pyqt_object_from_config(obj, prop, index=index)
        elif type(prop) == tuple and prop[-1] == 'basic':
            self._update_basetype(obj, name, prop, index=index)
        elif type(prop) == list:
            self._update_list(obj, prop, name, index=index)
        elif type(prop) == dict:
            self._update_dict(obj, prop, index=index)

        else:
            raise ValueError(
                'Can not update object "%s" from config "%s"' % (obj, name))