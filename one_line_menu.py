#!/usr/bin/env micropython
"""
one_line_menu.py
menu with one line and three buttons
develop on micropython port on linux
plan to use on Trinket M0
"""

"""
# debug - shows that we are running micropython
import sys
print(sys.path)
"""

"""
design own menu system?
label (text), type (enum), value (text or num)

work, sublist, 10
software, sublist, 50
shopping, sublist, 100
bank, sublist, 150
...
work-local, sublist,

Would need OrderedDict to keep the order?
{work: {work_local: {linux: {user: rharolde, pw: xxxxx},
                    wallace: {user: rharolde, pw: xxxx}
                    },
        work_online: {umich: {user: rharolde, pw: xxxxx},
                    pci: {user: p-rharolde, pw: xxxxx}}
                    },
home: {home_local: {hpenvy: {user: rharold, pw: xxxxx},
                   fishtank: {user: mailman, pw: xxxxx}
                   }
       }
       {home_online: {github: {user: xxxx, pw: xxxxx}
                    }
       }
bank: {pnc: {user: rharold, pw: xxxxx},
       citi: {user: rharold99, pw: xxxxx}
       }
}

Or make them all lists, to keep the order,
and every second item if text string is data to decrypt and send

data=[
'work',['user','rharolde','pw','xxxxxx'],
'home',['user','rharold','pw','xxxxxx'],
]

Even simpler?
data=[
'work',['rharolde','xxxx','back',''],
'home',['rharold','yyyy','back',''],
'play',['dnsbob','zzzz','back','']
]
"""


# imports
import time
import sys

import board
import touchio
import board
import adafruit_dotstar as dotstar


# constants
tick = 0.1
bsp = chr(8) + " " + chr(8)  # backspace
# bsp='.'     # for testing


# One pixel connected internally!
dot = dotstar.DotStar(board.APA102_SCK, board.APA102_MOSI, 1, brightness=0.2)
dot[0] = (0, 255, 0)  # green

# variables
touch1 = touchio.TouchIn(board.D1)  # red, space
touch3 = touchio.TouchIn(board.D3)  # blue, dash
touch4 = touchio.TouchIn(board.D4)  # yellow, dot
buttons = [touch4, touch3, touch1]

action = ["up", "down", "enter"]

data = [
    "work",
    ["rharolde", "xxxx", "back", "back"],
    "home",
    ["rharold", "yyyy", "back", "back"],
    "play",
    ["minecraft", ["dnsbob", "zzzz", "back", ""], "back", ""],
    #'back',''   # should not be here, just testing
]

current = data
stack = []
i = 0
print(current[i], end="")
old = current[i]
button_num = 0
button = buttons[0]
while True:
    # print("wait for button")
    button_press = 0
    while not button_press:
        for button_num, button in enumerate(buttons):
            if button.value:
                button_press = 1
                dot[0] = (0, 0, 0)  # off
                break
        time.sleep(tick)  # only if no button
    dot[0] = (0, 255, 0)  # green
    """
    # temp use chars for buttons
    button_num = int(input())
    print('button:',action[button_num])
    """

    # print("act on button",button_num)
    c = current[i]
    if action[button_num] == "down":
        i = (i + 2) % len(current)  # wrap at ends
    elif action[button_num] == "up":
        i = (i - 2) % len(current)  # wrap
    elif action[button_num] == "enter":
        v = current[i + 1]
        if type(v) == type("string"):
            if c == "back":
                if stack:
                    i = stack.pop()
                    current = stack.pop()
                    c = current[i]
            else:
                print(v, end="")
                old = c
        elif type(v) == type(["list"]):
            old = current[i]
            stack.append(current)
            stack.append(i)
            current = v
            i = 0
    c = current[i]
    if c != old:  # only print if changed
        print("".join([bsp for x in range(len(old))]), end="")  # backspace to erase
        print(current[i], end="")
        old = c
    """
    else:
        print('no change, current[i]:',current[i])
    """
    # print('wait for release')
    while button.value:
        time.sleep(tick)  # wait for button release
