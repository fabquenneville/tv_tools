#!/usr/bin/env python3

import json
import os
import inspect

from pathlib import Path

# Built-in dict(): ['__class__', '__class_getitem__', '__contains__', '__delattr__', '__delitem__', '__dict__', '__dir__', '__doc__', '__eq__', '__format__', '__ge__', '__getattribute__', '__getitem__', '__gt__', '__hash__', '__init__', '__init_subclass__', '__ior__', '__iter__', '__le__', '__len__', '__lt__', '__module__', '__ne__', '__new__', '__or__', '__reduce__', '__reduce_ex__', '__repr__', '__reversed__', '__ror__', '__setattr__', '__setitem__', '__sizeof__', '__str__', '__subclasshook__', '__weakref__', 'clear', 'copy', 'fromkeys', 'get', 'items', 'keys', 'pop', 'popitem', 'setdefault', 'update', 'values']

class AppConfig(dict):
    def __init__(self, *args, **kwargs):
        dict.__init__(self, *args, **kwargs)

        self.load_config()

    def __str__(self):
        return json.dumps(self, indent=4)

    def load_config(self):
        filepath = AppConfig.get_filepath()
        if os.path.exists(filepath):
            with open(filepath, 'r') as configfile:
                config_file_data = json.load(configfile)
                for section_name, section_config in self.items():
                    if section_name in config_file_data:
                        for config_key, setting in self[section_name].items():
                            if config_key in config_file_data[section_name]:
                                self[section_name][config_key] = config_file_data[section_name][config_key]

    def save_config(self):
        with open(AppConfig.get_filepath(True), 'w') as configfile:
            json.dump(self, configfile, indent=4)

    @staticmethod
    def get_appname():
        filename = inspect.stack()[-1].filename 
        return Path(filename).stem
    
    @staticmethod
    def get_folderpath(create = False):
        home = str(Path.home())

        config_folder = os.path.join(home, ".config")
        if not os.path.isdir(config_folder) and create:
            os.mkdir(config_folder)
        
        app_config_folder = os.path.join(config_folder, AppConfig.get_appname())
        if not os.path.isdir(app_config_folder) and create:
            os.mkdir(app_config_folder)

        return app_config_folder
    
    @staticmethod
    def get_filepath(create = False):
        return os.path.join(AppConfig.get_folderpath(create), "config.json")
