from approxeng.input.selectbinder import ControllerResource
from approxeng.input.xboxone import WiredXBoxOneSPad
from time import sleep

while True:
    try:
        with ControllerResource() as controller:
            print('Found a controller and connected')
            while controller.connected:
                presses = controller.check_presses()
                #if controller.presses.cross:
                 #   print("A")
                if controller.presses.square:
                    print("X")
                if controller.presses.triangle:
                    print("Y")
                if controller.presses.circle:
                    print("B")
                if controller.presses.rs:
                    print("Right Stick")
                if controller.presses.ls:
                    print("Left Stick")
                if controller.presses.select:
                    print("View")
                if controller.presses.start:
                    print("Menu")
                if controller.presses.home:
                    print("Xbox")
                if controller.presses.l1:
                    print("LB")
                if controller.presses.r1:
                    print("RB")
                    
                if controller.presses.cross:
                    left_x, left_y = controller.l
                    right_x, right_y = controller.r
                    lt = controller.l2
                    rt = controller.r2
                    dleft = controller.dleft
                    dright = controller.dright
                    dup = controller.dup
                    ddown = controller.ddown
                    print("(rx, ry) = (", right_x, " ", right_y, ")")
                    print("(lx, ly) = (", left_x, " ", left_y, ")")
                    print("(lt, rt) = (", lt, " ", rt, ")")
                    print("(L, R, U, D) = (",dleft, " ", dright, " ", dup, " ", ddown,")")
                    print("*************")
                    
        # Joystick disconnected...
        print('Connection to controller lost')
    except IOError:
        # No joystick found
        print('Unable to find any controller')
        sleep(2)