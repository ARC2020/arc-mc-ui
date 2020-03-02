from approxeng.input.selectbinder import bind_controllers
from approxeng.input.selectbinder import find_matching_controllers, ControllerRequirement
from time import sleep


class XboxCtrl():
    def __init__(self):
        self.controller = None
        self.unbind_function = None
        self.connect()

    def get_steering_position(self):
        """ Returns the left joystick x position.

        """
        return self.controller.lx

    def get_throttle_position(self):
        """ Returns the right joystick y position.

        """
        return self.controller.ry

    def check_brake(self):
        """ Returns the number of seconds for which RB is held.
            Returns zero if RB is not pressed.

        """
        return self.controller['r1']

    def connect(self):
        """ Try to connect to a controller that has LeftStick, RightStick and RBbutton.
            Returns TRUE if successful, FALSE otherwise.

        """
        try:
            discovery = find_matching_controllers(ControllerRequirement(
                require_snames=['lx', 'ly', 'rx', 'ry', 'r1']))[0]
            self.controller = discovery.controller
            self.unbind_function = bind_controllers(discovery, print_events=False)
            if discovery.controller.connected:
                return True
            else:
                return False
        except IOError:
            return False

    def reconnect(self):
        """ If controller is disconnected, then try to reconnect.
            Retruns TRUE if successful, FALSE otherwise.

        """
        if self.controller is None or (not self.controller.connected):
            return self.connect()
        else:
            return True

    def is_connected(self):
        """ Retruns TRUE if connected, FALSE otherwise.

        """
        if self.controller is None:
            return False

        return self.controller.connected

    def deinit(self):
        if self.unbind_function is not None:
            self.unbind_function()
        self.controller = None


if __name__ == '__main__':
    my_controller = XboxCtrl()
    reconnect_attempts = 10
    while True:
        if my_controller.is_connected():
            print(my_controller.get_throttle_position())
            print(my_controller.get_steering_position())
            print(my_controller.check_brake())
            sleep(2)
        else:
            temp = my_controller.reconnect()
            reconnect_attempts += -1
            print('trying to reconnect ')
            sleep(2)

        if reconnect_attempts == 0:
            my_controller.deinit()
            break
