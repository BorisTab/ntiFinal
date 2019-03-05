from os import path

from threading import Event
from threading import Thread


class FileWaiter(object):

    def __init__(self, name):
        self.name = name

    def wait(self):
        event = Event()
        waiter = Thread(target=self.check, args=(event, ))
        waiter.start()
        waiter.join()

    def check(self, event):
        while not event.isSet():
            # ToDo: Add wait for i/o ending
            # ToDo: possibly can throw exception if file size is very big
            if path.isfile(self.name):
                print('found! ', self.name)
                event.set()
