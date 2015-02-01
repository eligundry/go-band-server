import os
import sys
import inspect
import thread
import time
import requests as rekt

# Import the Leap Code
sys.path.insert(0, os.path.abspath(os.path.join('lib')))


SPARK = {
    'ID': '55ff6a065075555347441487',
    'ACCESS_TOKEN': '33fd66a97ab3f69a34c98298519c270058924680',
    'OAUTH_TOKEN': 'd5b7e5d72da4a18f7695f572e8e3270cc231e178',
    'URL': 'https://api.spark.io/v1/devices',
}

def issue_request(command_pattern):
    url = '%s/%s/twerk' % (SPARK['URL'], SPARK['ID'])
    data = {
        'access_token': SPARK['OAUTH_TOKEN'],
        'args': command_pattern,
    }

    print rekt.post(url, data=data)

import Leap
from Leap import CircleGesture, KeyTapGesture, ScreenTapGesture, SwipeGesture

class GoBandListener(Leap.Listener):

    def on_init(self, controller):
        self.init_list_commands()

        print "Initalized"

    def init_list_commands(self):
        self.commands = [
            SwipeUpLeftCommand(),
            SwipeDownLeftCommand(),
            SwipeUpRightCommand(),
            SwipeDownRightCommand(),
            SwipeRightCommand(),
            SwipeLeftCommand(),
            SwipeUpCommand(),
            SwipeDownCommand(),
            # ClockWiseCommand(),
            # CounterClockWiseCommand(),
        ]

    def on_connect(self, controller):
        print "Connected"
        # Register events
        controller.enable_gesture(Leap.Gesture.TYPE_CIRCLE)
        controller.enable_gesture(Leap.Gesture.TYPE_SWIPE)

        # Tweak the default speeds
        controller.config.set("Gesture.Swipe.MinLength", 100.0)
        controller.config.set("Gesture.Swipe.MinVelocity", 750)
        controller.config.save()

    def on_frame(self, controller):
        frame = controller.frame()

        if not frame.hands.is_empty:
            for command in self.commands:
                if command.applicable(frame):
                    print command
                    return

    def on_disconnect(self, controller):
        print "Exiting..."
        sys.exit(1)

class SwipeUpLeftCommand():
    def __init__(self):
        self.name = 'swipeupleft'
        self.swipe = None
        self.code = '1001'

    def __str__(self):
        return '%s (%s): [%s, %s, %s]' % (
            self.name, self.code, self.swipe.direction[0],
            self.swipe.direction[1], self.swipe.direction[2]
        )

    def applicable(self, frame):
        self.swipe = SwipeGesture(frame.gestures()[0])

        return (
            self.swipe.state == Leap.Gesture.STATE_STOP and
            self.swipe.type == Leap.Gesture.TYPE_SWIPE and
            self.swipe.direction[1] > 0 and
            self.swipe.direction[0] > 0
        )

    def execute(self):
        return issue_request(self.code)

class SwipeUpRightCommand():
    def __init__(self):
        self.name = 'swipeupright'
        self.swipe = None
        self.code = '1100'

    def __str__(self):
        return '%s (%s): [%s, %s, %s]' % (
            self.name, self.code, self.swipe.direction[0],
            self.swipe.direction[1], self.swipe.direction[2]
        )

    def applicable(self, frame):
        self.swipe = SwipeGesture(frame.gestures()[0])

        return (
            self.swipe.state == Leap.Gesture.STATE_STOP and
            self.swipe.type == Leap.Gesture.TYPE_SWIPE and
            self.swipe.direction[1] > 0 and
            self.swipe.direction[0] < 0
        )

    def execute(self):
        return issue_request(self.code)

class SwipeDownLeftCommand():
    def __init__(self):
        self.name = 'swipedownleft'
        self.swipe = None
        self.code = '0011'

    def __str__(self):
        return '%s (%s): [%s, %s, %s]' % (
            self.name, self.code, self.swipe.direction[0],
            self.swipe.direction[1], self.swipe.direction[2]
        )

    def applicable(self, frame):
        self.swipe = SwipeGesture(frame.gestures()[0])

        return (
            self.swipe.state == Leap.Gesture.STATE_STOP and
            self.swipe.type == Leap.Gesture.TYPE_SWIPE and
            self.swipe.direction[1] < 0 and
            self.swipe.direction[0] > 0
        )

    def execute(self):
        return issue_request(self.code)

class SwipeDownRightCommand():
    def __init__(self):
        self.name = 'swipedownright'
        self.swipe = None
        self.code = '0110'

    def __str__(self):
        return '%s (%s): [%s, %s, %s]' % (
            self.name, self.code, self.swipe.direction[0],
            self.swipe.direction[1], self.swipe.direction[2]
        )

    def applicable(self, frame):
        self.swipe = SwipeGesture(frame.gestures()[0])

        return (
            self.swipe.state == Leap.Gesture.STATE_STOP and
            self.swipe.type == Leap.Gesture.TYPE_SWIPE and
            self.swipe.direction[1] < 0 and
            self.swipe.direction[0] < 0
        )

    def execute(self):
        return issue_request(self.code)

class SwipeUpCommand():
    def __init__(self):
        self.name = 'swipeup'
        self.swipe = None
        self.code = '1000'

    def __str__(self):
        return '%s (%s): [%s, %s, %s]' % (
            self.name, self.code, self.swipe.direction[0],
            self.swipe.direction[1], self.swipe.direction[2]
        )

    def applicable(self, frame):
        self.swipe = SwipeGesture(frame.gestures()[0])

        return (
            self.swipe.state == Leap.Gesture.STATE_STOP and
            self.swipe.type == Leap.Gesture.TYPE_SWIPE and
            self.swipe.direction[1] > 0
        )

    def execute(self):
        return issue_request(self.code)

class SwipeDownCommand():
    def __init__(self):
        self.name = 'swipedown'
        self.swipe = None
        self.code = '0010'

    def __str__(self):
        return '%s (%s): [%s, %s, %s]' % (
            self.name, self.code, self.swipe.direction[0],
            self.swipe.direction[1], self.swipe.direction[2]
        )

    def applicable(self, frame):
        self.swipe = SwipeGesture(frame.gestures()[0])

        return (
            self.swipe.state == Leap.Gesture.STATE_STOP and
            self.swipe.type == Leap.Gesture.TYPE_SWIPE and
            self.swipe.direction[1] < 0
        )

    def execute(self):
        return issue_request(self.code)

class SwipeRightCommand():
    def __init__(self):
        self.name = 'swiperight'
        self.swipe = None
        self.code = '0100'

    def __str__(self):
        return '%s (%s): [%s, %s, %s]' % (
            self.name, self.code, self.swipe.direction[0],
            self.swipe.direction[1], self.swipe.direction[2]
        )

    def applicable(self, frame):
        self.swipe = SwipeGesture(frame.gestures()[0])

        return (
            self.swipe.state == Leap.Gesture.STATE_STOP and
            self.swipe.type == Leap.Gesture.TYPE_SWIPE and
            self.swipe.direction[0] < 0
        )

    def execute(self):
        return issue_request(self.code)

class SwipeLeftCommand():
    def __init__(self):
        self.name = 'swipeleft'
        self.swipe = None
        self.code = '0001'

    def __str__(self):
        return '%s (%s): [%s, %s, %s]' % (
            self.name, self.code, self.swipe.direction[0],
            self.swipe.direction[1], self.swipe.direction[2]
        )

    def applicable(self, frame):
        self.swipe = SwipeGesture(frame.gestures()[0])

        return (
            self.swipe.state == Leap.Gesture.STATE_STOP and
            self.swipe.type == Leap.Gesture.TYPE_SWIPE and
            self.swipe.direction[0] > 0
        )

    def execute(self):
        return issue_request(self.code)

class ClockWiseCommand():
    def __init__(self):
        self.name = 'clockwisecommand'
        self.circle = None
        self.code = '1111'

    def __str__(self):
        return '%s (%s): [%s, %s, %s]' % (
            self.name, self.code, self.circle.direction[0],
            self.circle.direction[1], self.circle.direction[2]
        )

    def applicable(self, frame):
        self.circle = CircleGesture(frame.gestures()[0])

        return (
            self.circle.state == Leap.Gesture.STATE_STOP and
            self.circle.type == Leap.Gesture.TYPE_CIRCLE and
            self.circle.pointable.direction.angle_to(self.circle.normal) <= Leap.PI/4
        )

    def execute(self):
        return issue_request(self.code)

class CounterClockWiseCommand():
    def __init__(self):
        self.name = 'counterclockwisecommand'
        self.circle = None
        self.code = '1111'

    def __str__(self):
        return '%s (%s): [%s, %s, %s]' % (
            self.name, self.code, self.circle.direction[0],
            self.circle.direction[1], self.circle.direction[2]
        )

    def applicable(self, frame):
        self.circle = CircleGesture(frame.gestures()[0])

        return (
            self.circle.state == Leap.Gesture.STATE_STOP and
            self.circle.type == Leap.Gesture.TYPE_CIRCLE and
            self.circle.pointable.direction.angle_to(self.circle.normal) > Leap.PI/4
        )

    def execute(self):
        return issue_request(self.code)

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
