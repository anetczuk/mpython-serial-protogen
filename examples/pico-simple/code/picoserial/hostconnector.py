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
            0x01: self._handle_unknown_request_rspns,  # UNKNOWN_REQUEST_RSPNS
            0x02: self._handle_internal_temp_rspns,  # INTERNAL_TEMP_RSPNS
            0x04: self._handle_test_bytes_rspns,  # TEST_BYTES_RSPNS
            0x05: self._handle_test_text_rspns,  # TEST_TEXT_RSPNS
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
    def _handle_unknown_request_rspns(self):
        message = self.channel.read_byte()
        return [0x01, message]

    # INTERNAL_TEMP_RSPNS
    ## parameters:
    ##    temperature: int16
    def _handle_internal_temp_rspns(self):
        temperature = self.channel.read_int(2)
        return [0x02, temperature]

    # TEST_BYTES_RSPNS
    ## parameters:
    ##    data_bytes: bytearray
    def _handle_test_bytes_rspns(self):
        data_size = self.channel.read_int(2)
        data_bytes = self.channel.read_bytes(data_size)
        return [0x04, data_bytes]

    # TEST_TEXT_RSPNS
    ## parameters:
    ##    content: str
    def _handle_test_text_rspns(self):
        content = self.channel.read_text()
        return [0x05, content]

    ## ============= send methods ===============

    ## send 'SET_KBD_INTR_RQST' message
    ## parameters:
    ##    new_state: bool
    def send_set_kbd_intr_rqst(self, new_state):
        self.channel.write_byte(0x01)  # "SET_KBD_INTR_RQST"
        self.channel.write_byte(new_state)

    ## send 'SET_INTERNAL_LED_RQST' message
    ## parameters:
    ##    new_state: bool
    def send_set_internal_led_rqst(self, new_state):
        self.channel.write_byte(0x02)  # "SET_INTERNAL_LED_RQST"
        self.channel.write_byte(new_state)

    ## send 'INTERNAL_TEMP_RQST' message
    def send_internal_temp_rqst(self):
        self.channel.write_byte(0x04)  # "INTERNAL_TEMP_RQST"

    ## send 'TEST_BYTES_RQST' message
    ## parameters:
    ##    data_bytes: bytearray
    ##    transfer_num: int16
    def send_test_bytes_rqst(self, data_bytes, transfer_num):
        self.channel.write_byte(0x05)  # "TEST_BYTES_RQST"
        self.channel.write_int(len(data_bytes), 2)
        self.channel.write_bytes(data_bytes)
        self.channel.write_int(transfer_num, 2)

    ## send 'TEST_TEXT_RQST' message
    ## parameters:
    ##    content: str
    ##    transfer_num: int16
    def send_test_text_rqst(self, content, transfer_num):
        self.channel.write_byte(0x06)  # "TEST_TEXT_RQST"
        self.channel.write_text(content)
        self.channel.write_int(transfer_num, 2)
