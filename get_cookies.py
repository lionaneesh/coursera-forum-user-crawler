#!/bin/python2.7

def get_cookies():
    fd1 = open("cookie.txt")
    fd2 = open("cookie2.txt")

    COOKIE   = fd1.read()
    COOKIE_2 = fd2.read()

    fd1.close()
    fd2.close()

    return COOKIE, COOKIE_2