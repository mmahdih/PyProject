#!/usr/bin/env python3

import pyfirmata
import time

from anyio import sleep

if __name__ == '__main__':
    board = pyfirmata.Arduino('COM3')
    print("Communication Successfully started")


    button_old = 0
    button_new = 0

    led_state = 0


    iterator = pyfirmata.util.Iterator(board)
    iterator.start()

    button = board.get_pin('d:2:i')
    board.digital[2].mode = pyfirmata.INPUT
    time.sleep(5)


    while True:
        button_new = button.read()
        if button_new != button_old:
            if button_new == 1:
                led_state = not led_state
                board.digital[13].write(led_state)
            button_old = button_new

