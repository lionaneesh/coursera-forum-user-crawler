#!/bin/python2.7
import urllib2
import json
from get_cookies import get_cookies
from StringIO import StringIO

COOKIE, COOKIE_2 = get_cookies()
CLASS_SLUG       = "startup-001"
CALLBACK         = "some"
OUT_FILE         = "user_data.json"

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

while there_are_more_threads:
    print "Scanning thread ", thread_count
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
    except urllib2.HTTPError, e:
        if e.read() == "Unexpected API error":
            there_are_more_threads = False
        else:
            thread_count += 1

# now we have all the uids let's get the user data
users = []

number_of_users = len(uids)
count = 1

print "Crawling %d user profiles." % (number_of_users,)

for uid in uids:
    print count, " / ", number_of_users
    data = get_page(user_template % (uid,), True).read()
    data = data[len(CALLBACK)+2:len(data)-2].strip()
    if data:
        user = json.loads(data)
        users.append(user)
    count += 1

fp = open(OUT_FILE, "w")
fp.write(json.dumps(users))
fp.close()
