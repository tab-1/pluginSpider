# coding:utf-8

from pluginManager import DirectoryPluginManager
import os

if __name__ == '__main__':
    plugin_manager = DirectoryPluginManager()
    plugin_manager.loadPlugins()
    plugins = plugin_manager.getPlugins("sencondPlugin")


    print("**" * 50)
    print (plugins[0].scan())