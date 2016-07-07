#-*-coding:utf-8-*-
__author__ = 'lixin'
import win32api,win32con,win32process
import ctypes

from time import sleep
import threading

class Work():
    def __init__(self):
        self.point = []
        self.delay = []
        self.num = 0
        self.tid = None


    def addPoint(self, x, y, ad, delay = 1000):
        self.point.insert(ad, [x, y])
        self.delay.insert(ad, delay)
        self.num += 1

    def delPoint(self, ad):
        self.point.pop(ad)
        self.delay.pop(ad)
        self.num -= 1


    def end(self):
        terminate_thread(int(self.tid))
        self.tid = None

    def start(self):
        self.handle, self.tid = win32process.beginthreadex(None, 0, self.run, (), 0)

    def run(self):
        print 'Begin!'
        for x in xrange(100):
            for i in xrange(self.num):
                win32api.mouse_event(win32con.MOUSEEVENTF_MOVE|win32con.MOUSEEVENTF_ABSOLUTE,
                                     self.point[i][0], self.point[i][1], 0, 0)
                win32api.mouse_event(win32con.MOUSEEVENTF_LEFTDOWN, 0, 0, 0, 0)
                win32api.mouse_event(win32con.MOUSEEVENTF_LEFTUP, 0, 0, 0, 0)
                sleep(self.delay[i]/1000)
            print x
        print 'Stop!'



def terminate_thread(tid):
	"""Terminates a python thread from another thread.

	:param thread: a threading.Thread instance
	"""

	exc = ctypes.py_object(KeyboardInterrupt)
	res = ctypes.pythonapi.PyThreadState_SetAsyncExc(
		ctypes.c_long(tid), exc)
	if res == 0:
		# raise ValueError("nonexistent thread id")
		print "nonexistent thread id"
	elif res > 1:
		"""if it returns a number greater than one, you're in trouble,
		and you should call it again with exc=NULL to revert the effect"""
		ctypes.pythonapi.PyThreadState_SetAsyncExc(tid, None)
		# raise SystemError("PyThreadState_SetAsyncExc failed")
		print "PyThreadState_SetAsyncExc failed"
