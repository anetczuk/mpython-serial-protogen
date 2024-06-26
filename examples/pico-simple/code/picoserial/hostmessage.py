#
# File was automatically generated using 'mpyserialprotogen'
#
# Project website: https://github.com/anetczuk/mpython-serial-protogen
#


class HostMessage:

    SET_KBD_INTR_RQST = 0x01
    SET_INTERNAL_LED_RQST = 0x02
    INTERNAL_TEMP_RQST = 0x04
    TEST_BYTES_RQST = 0x05
    TEST_TEXT_RQST = 0x06

    @staticmethod
    def get_id_from_value(value) -> str:
        if value == 0x01:
            return "SET_KBD_INTR_RQST"
        if value == 0x02:
            return "SET_INTERNAL_LED_RQST"
        if value == 0x04:
            return "INTERNAL_TEMP_RQST"
        if value == 0x05:
            return "TEST_BYTES_RQST"
        if value == 0x06:
            return "TEST_TEXT_RQST"

        # unhandled value
        return None
