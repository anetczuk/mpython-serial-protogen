#
# File was automatically generated using 'mpyserialprotogen'
#
# Project website: https://github.com/anetczuk/mpython-serial-protogen
#


class SensorMessage:

    UNKNOWN_REQUEST_RSPNS = 0x01
    INTERNAL_TEMP_RSPNS = 0x02
    TEST_BYTES_RSPNS = 0x03
    TEST_TEXT_RSPNS = 0x04

    @staticmethod
    def get_id_from_value(value) -> str:
        if value == 0x01:
            return "UNKNOWN_REQUEST_RSPNS"
        if value == 0x02:
            return "INTERNAL_TEMP_RSPNS"
        if value == 0x03:
            return "TEST_BYTES_RSPNS"
        if value == 0x04:
            return "TEST_TEXT_RSPNS"

        # unhandled value
        return None
