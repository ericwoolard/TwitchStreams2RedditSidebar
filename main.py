# System imports
from time import time
# Third-party imports
import praw
from praw import exceptions as pExc
# Our imports
import cache
import config
import livestream_feed
import log

settings = config.readJson('settings.json')
account = config.readJson('accounts.json')

# Get the sidebar template
sidebar = config.read('sidebar.txt')

# Fix SSL issues by using pyOpenSSL
import urllib3.contrib.pyopenssl
urllib3.contrib.pyopenssl.inject_into_urllib3()

# Log into the main reddit account
r = praw.Reddit(client_id=account['primary_bot']['client_id'],
                client_secret=account['primary_bot']['client_secret'],
                username=account['primary_bot']['username'],
                password=account['primary_bot']['password'],
                user_agent=account['primary_bot']['user_agent'])


##################################################
#	             SIDEBAR PHASE                   #
##################################################

# Default values for the different sections of the sidebar
livestreams = {'markdown': '', 'spritesheet_path': None}

# Get the different components of the sidebar, but only if there is something
# in the sidebar markdown for them to replace!
if '__LIVESTREAMS__' in sidebar:
    # Returns spritesheet path and markdown
    livestreams = livestream_feed.build()

# Replace the placeholders with the retrieved values, or defaults if they
# were not retrieved
sidebar = (sidebar.replace('__LIVESTREAMS__', livestreams['markdown']))


##################################################
#	            UPLOADING PHASE                  #
##################################################

# Get the PRAW subreddit object
subreddit = r.subreddit(settings['subreddit'])

# Upload the new spritesheet if one was generated
if livestreams['spritesheet_path'] is not None:
    startTime = time()
    log.log('Uploading livestreams spritesheet...')
    sprite_name = settings['sidebar']['livestreams']['spritesheet_name']
    try:
        subreddit.stylesheet.upload(sprite_name, livestreams['spritesheet_path'])
    except pExc.APIException as e:
        print(e)
    log.log('\t... done! \BLUE(%s s)' % str(round(time() - startTime, 3)))

# TODO: Figure out exactly why the UTF-8 ignore conversion is necessary,
# 		i.e. why and how those strings are being converted to unicode in
#		the first place
#
#		In other words, the conversion is just a quick fix for an underlying
#		issue, which really sucks and needs to be rectified.

# Upload the new sidebar markdown if it's any different
if cache.read('sidebar_markdown.txt') != sidebar:
    startTime = time()
    log.log('Uploading sidebar markdown...')
    subreddit.mod.update(description=sidebar)
    cache.save('sidebar_markdown.txt', sidebar)
    log.log('\t... done! \BLUE(%s s)' % str(round(time() - startTime, 3)))
else:
    log.log('Not uploading sidebar -- it hasn\'t changed!')
