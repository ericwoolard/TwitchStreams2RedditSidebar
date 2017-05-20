# System imports
from time import time
# Third-party imports
import praw
# Project imports
import file_manager

r = None
config_path = 'cfg/'  # Root of all configuration files
settings_root = ''  # Full path to profile folder relative to bot root
last_updated = 0
cached_returns = {}  # Used to, well, cache function returns. Not wildly
# used in the configuration files, but a handy
# option nonetheless.
# TODO: Look into streamlining the caching process
authed_account = ''  # The current authenticated account


# Aliases of the file_manager functions to control the relative path
def read(relative_path):
    global config_path
    return file_manager.read(config_path + relative_path)


def readJson(relative_path):
    global config_path
    return file_manager.readJson(config_path + relative_path)


def save(relative_path, data):
    global config_path
    return file_manager.save(config_path + relative_path, data)


def saveJson(relative_path, data):
    global config_path
    return file_manager.saveJson(config_path + relative_path, data)


def getConfigPath():
    global config_path
    return file_manager.ensureAbsPath(config_path)


# Bot account OAuth information // These don't follow the profile,
# keep all bots in the same accounts.json file
def getAccounts():
    global config_root
    return file_manager.readJson(config_root + 'accounts.json')


def setAccounts(newAccounts):
    global config_root
    file_manager.saveJson(config_root + 'accounts.json', newAccounts)
