#!/bin/python2.7
import cookielib
import requests, urllib2
import json
from get_cookies import get_cookies
from StringIO import StringIO

COOKIE, COOKIE_2 = get_cookies()
CLASS_SLUG       = "startup-001"
CALLBACK         = "some"

def get_page(url, use_cookie_2 = False):
    opener = urllib2.build_opener()

    if use_cookie_2:
        c = COOKIE_2
    else:
        c = COOKIE

    opener.addheaders.append(('Cookie', c))
    return opener.open(url)

forum_thread_template = "https://class.coursera.org/" + CLASS_SLUG + "/api/forum/threads/%d"
user_template = "https://www.coursera.org/maestro/api/user/profiles?user-ids=%d&callback=" + CALLBACK

uids = set()
thread_count = 1
there_are_more_threads = True

while there_are_more_threads and thread_count < 2:
    page_link = forum_thread_template % (thread_count, )
    try:
        data = get_page(page_link).read()
        j_d = json.loads(data)
        uids.add(j_d[u'user_id'])
        posts_and_comments = j_d['posts'] + j_d['comments']
        for entity in posts_and_comments:
            try:
                uids.add(entity[u'user_id'])
            except KeyError:
                pass
        thread_count += 1
    except urllib2.HTTPError:
        there_are_more_threads = False

# now we have all the uids let's get the user data

users = []

for uid in uids:
    print uid
    data = get_page(user_template % (uid,), True).read()
    user = data[len(CALLBACK)+2:len(data)-2].strip()
    if user:
        users.append(user)

print json.loads(users)