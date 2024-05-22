#!/usr/bin/env python3
#
# Copyright (c) 2024, Arkadiusz Netczuk <dev.arnet@gmail.com>
# All rights reserved.
#
# This source code is licensed under the BSD 3-Clause license found in the
# LICENSE file in the root directory of this source tree.
#

import sys
import time

import serial

from picoserial.hostconnector import HostConnector
from picoserial.sensormessage import SensorMessage
from picoserial.hostmessage import HostMessage
from host.serialchannel import SerialChannel
from host.printlogger import PrintLogger


def read_pico_temperature(connector: HostConnector):
    connector.send_INTERNAL_TEMP_RQST()
    message = connector.receive_message()
    temperature = message[1]
    if temperature is None:
        print("invalid data:", message)
        return
    temperature = temperature / 100.0
    print("current Pico temperature:", temperature)


def handle_message(connector: HostConnector, logger):
    command_data = connector.receive_message()

    if command_data is None:
        # no incoming message
        return

    command = command_data[0]

    if command is None:
        # unknown command
        # logger.info(f"unknown command: {command_data}")
        pass

    elif command == SensorMessage.UNKNOWN_REQUEST_RSPNS:
        message_value = command_data[1]
        message_id = HostMessage.get_id_from_value(message_value)
        logger.info(f"Pico does not know how to handle message '{message_value}'({message_id})")

    elif command == SensorMessage.INTERNAL_TEMP_RSPNS:
        temperature = command_data[1] / 100.0
        logger.info(f"Pico internal temperature: {temperature}")

    else:
        # unhandled command
        command_id = SensorMessage.get_id_from_value(command)
        logger.warn(f"unhandled command: {command_data}, '{command_id}'")


def main():
    print("connecting")

    # open a serial connection
    with serial.Serial(
        port="/dev/ttyACM0", parity=serial.PARITY_EVEN, stopbits=serial.STOPBITS_ONE, timeout=1
    ) as medium:
        logger = PrintLogger()
        medium.flush()
        channel = SerialChannel(medium)
        connector = HostConnector(channel)

        # disable keyboard interrupts (allow value 0x03)
        logger.info("disabling Pico keyboard interrupt")
        connector.send_SET_KBD_INTR_RQST(0)
        time.sleep(0.1)  # wait a bit to propagate the request

        connector.send_SET_INTERNAL_LED_RQST(1)

        try:
            while True:
                connector.send_INTERNAL_TEMP_RQST()
                handle_message(connector, logger)
                time.sleep(1)

        except KeyboardInterrupt:
            logger.info("enabling Pico keyboard interrupt")
            connector.send_SET_INTERNAL_LED_RQST(0)
            # enable keyboard interrupt
            connector.send_SET_KBD_INTR_RQST(1)
            raise

    return 0


if __name__ == "__main__":
    EXIT_CODE = main()
    sys.exit(EXIT_CODE)
