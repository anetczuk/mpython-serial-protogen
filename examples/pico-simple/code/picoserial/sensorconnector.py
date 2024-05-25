#
# File was automatically generated using 'mpyserialprotogen'
#
# Project website: https://github.com/anetczuk/mpython-serial-protogen
#

from picoserial.channel import AbstractChannel


# pylint: disable=C0103


class SensorConnector:
    def __init__(self, channel: AbstractChannel):
        self.channel: AbstractChannel = channel  # communication medium

        # under MicroPython lookup dict is significantly faster than if-else chain
        self.lookup_dict = {
            0x01: self._handle_set_kbd_intr_rqst,  # SET_KBD_INTR_RQST
            0x02: self._handle_set_internal_led_rqst,  # SET_INTERNAL_LED_RQST
            0x04: self._handle_internal_temp_rqst,  # INTERNAL_TEMP_RQST
            0x05: self._handle_test_bytes_rqst,  # TEST_BYTES_RQST
            0x06: self._handle_test_text_rqst,  # TEST_TEXT_RQST
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

    # SET_KBD_INTR_RQST
    ## parameters:
    ##    new_state: bool
    def _handle_set_kbd_intr_rqst(self):
        new_state = self.channel.read_byte()
        return [0x01, new_state]

    # SET_INTERNAL_LED_RQST
    ## parameters:
    ##    new_state: bool
    def _handle_set_internal_led_rqst(self):
        new_state = self.channel.read_byte()
        return [0x02, new_state]

    # INTERNAL_TEMP_RQST
    def _handle_internal_temp_rqst(self):
        # no fields
        return [0x04]

    # TEST_BYTES_RQST
    ## parameters:
    ##    data_bytes: bytearray
    ##    transfer_num: int16
    def _handle_test_bytes_rqst(self):
        data_size = self.channel.read_int(2)
        data_bytes = self.channel.read_bytes(data_size)
        transfer_num = self.channel.read_int(2)
        return [0x05, data_bytes, transfer_num]

    # TEST_TEXT_RQST
    ## parameters:
    ##    content: str
    ##    transfer_num: int16
    def _handle_test_text_rqst(self):
        content = self.channel.read_text()
        transfer_num = self.channel.read_int(2)
        return [0x06, content, transfer_num]

    ## ============= send methods ===============

    ## send 'UNKNOWN_REQUEST_RSPNS' message
    ## parameters:
    ##    message: byte
    def send_unknown_request_rspns(self, message):
        self.channel.write_byte(0x01)  # "UNKNOWN_REQUEST_RSPNS"
        self.channel.write_byte(message)

    ## send 'INTERNAL_TEMP_RSPNS' message
    ## parameters:
    ##    temperature: int16
    def send_internal_temp_rspns(self, temperature):
        self.channel.write_byte(0x02)  # "INTERNAL_TEMP_RSPNS"
        self.channel.write_int(temperature, 2)

    ## send 'TEST_BYTES_RSPNS' message
    ## parameters:
    ##    data_bytes: bytearray
    def send_test_bytes_rspns(self, data_bytes):
        self.channel.write_byte(0x04)  # "TEST_BYTES_RSPNS"
        self.channel.write_int(len(data_bytes), 2)
        self.channel.write_bytes(data_bytes)

    ## send 'TEST_TEXT_RSPNS' message
    ## parameters:
    ##    content: str
    def send_test_text_rspns(self, content):
        self.channel.write_byte(0x05)  # "TEST_TEXT_RSPNS"
        self.channel.write_text(content)
