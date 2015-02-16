#!/usr/bin/env python
#License: GPL v2

import praw
import logging
import argparse
import re

user_agent = 'auto automoderator bot v0.1 by /u/mtux96 - modified version of rcssbot by /u/nath_schwarz'

username = ''
password = ''

subreddit = ''
page = 'automoderator'

setting1 = '["[META]", "[EVENT]", "[CLAIM]", "[EXPANSION]", "[CONFLICT]", "[MODPOST]", "[DATE]", "[DISCUSSION]"]'
setting2 = '["[META]", "[CLAIM]", "[NEWS]", "[MODPOST]", "[DATE]", "[DISCUSSION]"]'
automodstring = 'title:'

regex_date = 'title: (...*) #autoautomod'

months = [
        setting1,
        setting2
        ]

#globals
r = praw.Reddit(user_agent = user_agent)
logger = None

def login():
    """Logs in to reddit with given username and password."""
    global r
    try:
        r.login(username, password)
        logger.info('Login successful')
    except Exception as e:
        logger.error(e)

def replace(match):
    if not match:
        logger.error('Match not possible')
        return 'ERROR'
    else:
        #Assigns new month
        month = months[(months.index(match.group(1)) + 1) % 2]
        #Increments year if index of month is 0 (== tuesday)
        logger.info(month)
        return '{} {} #autoautomod'.format(automodstring, month)

def pull_stylesheet():
    logger.info('Pulling stylesheet')
    return r.get_wiki_page(subreddit, page).content_md

def push_stylesheet(stylesheet):
    logger.info('Uploading stylesheet')
    r.edit_wiki_page(subreddit, page, stylesheet)

def do():
    css = pull_stylesheet()
    css = re.sub(regex_date, replace, css)
    css = re.sub('&gt;', '>', css)
    css = re.sub('&lt;', '<', css)
    css = re.sub('&amp;', '&', css)
    push_stylesheet(css)

def updatea():
    r.send_message("automoderator", subreddit, "update", captcha=None)

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("-v", "--verbose", action="store_true", help="verbose output")
    parser.add_argument("--stdout", action="store_true", help="print log output to stdout")
    args = parser.parse_args()

    global logger
    if args.verbose:
        logging.basicConfig(level = logging.INFO)
    else:
        logging.basicConfig(level = logging.ERROR)
    if not args.stdout:
        logging.basicConfig(filename = 'autoautomod.log')
    logger = logging.getLogger('autoautomod')

    login()
    try:
        do()
	updatea()
    except Exception as e:
        logger.error(e)
    r.clear_authentication()

if __name__ == "__main__":
    main()
