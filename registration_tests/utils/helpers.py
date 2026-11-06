import time


def unique_email():
    # new email every run so "already registered" doesn't break the test
    return "qauser" + str(int(time.time())) + "@mailinator.com"
