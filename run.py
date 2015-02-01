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
from Leap import CircleGesture, SwipeGesture

class GoBandListener(Leap.Listener):

    def on_init(self, controller):
        self.init_list_commands()

        print "Initalized"

    def init_list_commands(self):
        self.commands = [
            SwipeUpCommand(),
            SwipeRightCommand(),
            SwipeDownCommand(),
            SwipeLeftCommand(),
            SwipeUpLeftCommand(),
            SwipeDownLeftCommand(),
            SwipeUpRightCommand(),
            SwipeDownRightCommand(),
            ClockWiseCommand(),
        ]

    def on_connect(self, controller):
        print "Connected"
        # Register events
        controller.enable_gesture(Leap.Gesture.TYPE_CIRCLE)
        controller.enable_gesture(Leap.Gesture.TYPE_SWIPE)

        # Tweak the default speeds
        controller.config.set("Gesture.Swipe.MinLength", 10.0)
        controller.config.set("Gesture.Swipe.MinVelocity", 1)
        controller.config.save()

    def on_frame(self, controller):
        frame = controller.frame()

        if not frame.hands.is_empty:
            for command in self.commands:
                if command.applicable(frame):
                    print command
                    return command.execute()

    def on_disconnect(self, controller):
        print "Exiting..."
        sys.exit(1)

class BaseSwipeCommand():
    name = None
    swipe = None
    code = None
    min_y_val = -0.2
    max_y_val = 0.2
    min_x_val = -0.3
    max_x_val = 0.3

    def __str__(self):
        return '%s (%s): [%s, %s, %s]' % (
            self.name, self.code, self.swipe.direction[0],
            self.swipe.direction[1], self.swipe.direction[2]
        )

    def has_stopped(self):
        return (
            self.swipe.state == Leap.Gesture.STATE_STOP and
            self.swipe.type == Leap.Gesture.TYPE_SWIPE
        )

    def execute(self):
        return issue_request(self.code)

class SwipeUpLeftCommand(BaseSwipeCommand):
    name = 'swipe_up_left'
    code = '1001'

    def applicable(self, frame):
        self.swipe = SwipeGesture(frame.gestures()[0])

        return (
            self.has_stopped() and
            self.min_x_val > self.swipe.direction[0] and
            self.min_y_val < self.swipe.direction[1]
        )

class SwipeUpRightCommand(BaseSwipeCommand):
    name = 'swipe_up_right'
    code = '1100'

    def applicable(self, frame):
        self.swipe = SwipeGesture(frame.gestures()[0])

        return (
            self.has_stopped() and
            self.min_x_val < self.swipe.direction[0] > self.max_x_val and
            self.min_y_val < self.swipe.direction[1] > self.max_y_val
        )

class SwipeDownLeftCommand(BaseSwipeCommand):
    name = 'swipe_down_left'
    code = '0011'

    def applicable(self, frame):
        self.swipe = SwipeGesture(frame.gestures()[0])

        return (
            self.has_stopped() and
            self.min_x_val > self.swipe.direction[0] and
            self.min_y_val > self.swipe.direction[1]
        )

class SwipeDownRightCommand(BaseSwipeCommand):
    name = 'swipe_down_right'
    code = '0110'

    def applicable(self, frame):
        self.swipe = SwipeGesture(frame.gestures()[0])

        return (
            self.has_stopped() and
            self.min_y_val > self.swipe.direction[1] > self.max_y_val and
            self.min_x_val < self.swipe.direction[0] < self.max_x_val
        )

class SwipeUpCommand(BaseSwipeCommand):
    name = 'swipe_up'
    code = '1000'

    def applicable(self, frame):
        self.swipe = SwipeGesture(frame.gestures()[0])

        return (
            self.has_stopped() and
            self.min_x_val <= self.swipe.direction[0] <= self.max_x_val and
            self.swipe.direction[1] > 0
        )

class SwipeDownCommand(BaseSwipeCommand):
    name = 'swipe_down'
    code = '0010'

    def applicable(self, frame):
        self.swipe = SwipeGesture(frame.gestures()[0])

        return (
            self.has_stopped() and
            self.min_x_val <= self.swipe.direction[0] <= self.max_x_val and
            self.swipe.direction[1] < 0
        )

class SwipeRightCommand(BaseSwipeCommand):
    name = 'swipe_right'
    code = '0100'

    def applicable(self, frame):
        self.swipe = SwipeGesture(frame.gestures()[0])

        return (
            self.has_stopped() and
            self.min_y_val <= self.swipe.direction[1] <= self.max_y_val and
            self.swipe.direction[0] > 0
        )

class SwipeLeftCommand(BaseSwipeCommand):
    name = 'swipe_left'
    code = '0001'

    def applicable(self, frame):
        self.swipe = SwipeGesture(frame.gestures()[0])

        return (
            self.has_stopped() and
            self.min_y_val <= self.swipe.direction[1] <= self.max_y_val and
            self.swipe.direction[0] < 0
        )

class ClockWiseCommand():
    name = 'clockwisecommand'
    code = '1111'

    def __str__(self):
        return '%s (%s)' % (self.name, self.code)

    def applicable(self, frame):
        self.circle = CircleGesture(frame.gestures()[0])

        return (
            self.circle.state == Leap.Gesture.STATE_STOP and
            self.circle.type == Leap.Gesture.TYPE_CIRCLE
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
