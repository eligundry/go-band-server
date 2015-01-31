import os
import sys
import inspect
import thread
import time
import requests as rekt

from commands import *

# Import the Leap Code
sys.path.insert(0, os.path.abspath(os.path.join('lib')))


SPARK = {
    'ID': '55ff6a065075555347441487',
    'ACCESS_TOKEN': '12a5efa1c98bdd36dc87ea7521aae623bae61e98',
    'OAUTH_TOKE': 'd93e8ecdbf83b689cade259dec1c886ef03f8f32',
}

SPARK_END_POINT = 'https://api.spark.io/v1/devices/%s' % SPARK['ID']

import Leap
from Leap import CircleGesture, KeyTapGesture, ScreenTapGesture, SwipeGesture

class GoBandListener(Leap.Listener):

    def on_init(self, controller):
        self.init_list_commands()

        print "Initalized"

    def init_list_commands(self):
        self.commands = [
            SwipeRightCommand(),
            SwipeLeftCommand(),
            SwipeForwardCommand(),
            SwipeBackCommand(),
            ClockWiseCommand(),
            CounterClockWiseComman(),
        ]

    def on_connect(self, controller):
        print "Connected"
        controller.enable_gesture(Leap.Gesture.TYPE_CIRCLE)
        controller.enable_gesture(Leap.Gesture.TYPE_SWIPE)

    def on_frame(self, controller):
        frame = controller.frame()

        if not frame.hands.is_empty:
            print "Handsy"

    def on_disconnect(self, controller):
        print "Exiting..."
        sys.exit(1)

class SwipeUpCommand():
    def __init__(self):
        self.name = 'swipeup'

    def applicable(self, frame):
        swipe = SwipeGesture(frame.gestures()[0])

        return(
            swipe.state == Leap.Gesture.STATE_STOP and
            swipe.type == Leap.Gesture.TYPE_CIRCLE and
            swipe.direction[1] > 0
        )

class SwipeDownCommand():
    def __init__(self):
        self.name = 'swipedown'

    def applicable(self, frame):
        swipe = SwipeGesture(frame.gestures()[0])

        return(
            swipe.state == Leap.Gesture.STATE_STOP and
            swipe.type == Leap.Gesture.TYPE_CIRCLE and
            swipe.direction[1] < 0
        )

class SwipeRightCommand():
    def __init__(self):
        self.name = 'swiperight'

    def applicable(self, frame):
        swipe = SwipeGesture(frame.gestures()[0])

        return(
            swipe.state == Leap.Gesture.STATE_STOP and
            swipe.type == Leap.Gesture.TYPE_CIRCLE and
            swipe.direction[0] < 0
        )

class SwipeLeftCommand():
    def __init__(self):
        self.name = 'swipeleft'

    def applicable(self, frame):
        swipe = SwipeGesture(frame.gestures()[0])

        return(
            swipe.state == Leap.Gesture.STATE_STOP and
            swipe.type == Leap.Gesture.TYPE_CIRCLE and
            swipe.direction[0] > 0
        )

class ClockWiseCommand():
    def __init__(self):
        self.name = 'clockwisecommand'

    def applicable(self, frame):
        circle = CircleGesture(frame.gestures()[0])

        return (
            circle.state == Leap.Gesture.STATE_STOP and
            circle.type == Leap.Gesture.TYPE_CIRCLE and
            circle.pointable.direction.angle_to(circle.normal) <= Leap.PI/4
        )

class CounterClockWiseCommand():
    def __init__(self):
        self.name = 'counterclockwisecommand'

    def applicable(self, frame):
        circle = CircleGesture(frame.gestures()[0])

        return (
            circle.state == Leap.Gesture.STATE_STOP and
            circle.type == Leap.Gesture.TYPE_CIRCLE and
            circle.pointable.direction.angle_to(circle.normal) > Leap.PI/4
        )

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
