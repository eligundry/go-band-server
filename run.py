import os
import sys
import inspect
import thread
import time

# Import the Leap Code
sys.path.insert(0, os.path.join('/', 'lib', 'Leap'))

import Leap
from Leap import CircleGesture, KeyTapGesture, ScreenTapGesture, SwipeGesture

class GoBandListener(Leap.Listener):

    def on_connect(self, controller):
        print "Connected"

    def on_frame(self, controller):
        print "Frame available"

def main():
    listener = GoBandListener()
    controller = Leap.Controller()

    controller.add_listener(listener)

    print "Press <Enter> to quit..."

    try:
        sys.stdin.readline()
    except KeyboardInterrupt:
        pass

if __name__ == "__main__":
    main()
