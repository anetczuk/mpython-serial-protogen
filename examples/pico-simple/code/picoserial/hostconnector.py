#
# File was automatically generated using 'mpyserialprotogen'
#
# Project website: https://github.com/anetczuk/mpython-serial-protogen
#

from picoserial.channel import AbstractChannel


# pylint: disable=C0103


class HostConnector:
    def __init__(self, channel: AbstractChannel):
        self.channel: AbstractChannel = channel  # communication medium

        # under MicroPython lookup dict is significantly faster than if-else chain
        self.lookup_dict = {
            0x01: self._handle_UNKNOWN_REQUEST_RSPNS,  # UNKNOWN_REQUEST_RSPNS
            0x02: self._handle_INTERNAL_TEMP_RSPNS,  # INTERNAL_TEMP_RSPNS
            0x04: self._handle_TEST_BYTES_RSPNS,  # TEST_BYTES_RSPNS
            0x05: self._handle_TEST_TEXT_RSPNS,  # TEST_TEXT_RSPNS
        }

    def wait_message(self):
        while True:
            message = self.receive_message()
            if message is None:
                # no message
                continue
            if message[0] is None:
                # unknown message
                continue
            return message

    def wait_message_type(self, message_type):
        while True:
            message = self.receive_message()
            if message is None:
                # no message
                continue
            if message[0] is not message_type:
                # message type not match
                continue
            return message

    def receive_message(self):
        command = self.channel.read_byte()

        callback = self.lookup_dict.get(command)
        if callback is not None:
            return callback()

        self._handle_unknown_command(command)

        # unknown message
        return [None, command]

    def _handle_unknown_command(self, command):
        # override if needed
        pass

    # UNKNOWN_REQUEST_RSPNS
    ## parameters:
    ##    message: byte
    def _handle_UNKNOWN_REQUEST_RSPNS(self):
        message = self.channel.read_byte()
        return [0x01, message]

    # INTERNAL_TEMP_RSPNS
    ## parameters:
    ##    temperature: int16
    def _handle_INTERNAL_TEMP_RSPNS(self):
        temperature = self.channel.read_int(2)
        return [0x02, temperature]

    # TEST_BYTES_RSPNS
    ## parameters:
    ##    data_bytes: bytearray
    def _handle_TEST_BYTES_RSPNS(self):
        data_size = self.channel.read_int(2)
        data_bytes = self.channel.read_bytes(data_size)
        return [0x04, data_bytes]

    # TEST_TEXT_RSPNS
    ## parameters:
    ##    content: str
    def _handle_TEST_TEXT_RSPNS(self):
        content = self.channel.read_text()
        return [0x05, content]

    ## ============= send methods ===============

    ## send 'SET_KBD_INTR_RQST' message
    ## parameters:
    ##    new_state: bool
    def send_SET_KBD_INTR_RQST(self, new_state):
        self.channel.write_byte(0x01)  # "SET_KBD_INTR_RQST"
        self.channel.write_byte(new_state)

    ## send 'SET_INTERNAL_LED_RQST' message
    ## parameters:
    ##    new_state: bool
    def send_SET_INTERNAL_LED_RQST(self, new_state):
        self.channel.write_byte(0x02)  # "SET_INTERNAL_LED_RQST"
        self.channel.write_byte(new_state)

    ## send 'INTERNAL_TEMP_RQST' message
    def send_INTERNAL_TEMP_RQST(self):
        self.channel.write_byte(0x04)  # "INTERNAL_TEMP_RQST"

    ## send 'TEST_BYTES_RQST' message
    ## parameters:
    ##    data_bytes: bytearray
    ##    transfer_num: int16
    def send_TEST_BYTES_RQST(self, data_bytes, transfer_num):
        self.channel.write_byte(0x05)  # "TEST_BYTES_RQST"
        self.channel.write_int(len(data_bytes), 2)
        self.channel.write_bytes(data_bytes)
        self.channel.write_int(transfer_num, 2)

    ## send 'TEST_TEXT_RQST' message
    ## parameters:
    ##    content: str
    ##    transfer_num: int16
    def send_TEST_TEXT_RQST(self, content, transfer_num):
        self.channel.write_byte(0x06)  # "TEST_TEXT_RQST"
        self.channel.write_text(content)
        self.channel.write_int(transfer_num, 2)
