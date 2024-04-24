# MicroPython Serial Protocol Generator

Generate your message exchange protocol layer. Make your life easier and don't repeat yourself. Define your messages
and have code generated.

Generator is useful in case of communication between *Raspberry Pi Pico* (sensor) plugged into USB port of PC (host).
Generator properly handles corner cases such as keyboard interrupt character (`0x03`) and new line character (`\n`). In
first case interrupt handling have to be disabled. In second case new line causes read interrupt, so reading operation 
have to be resumed.

Main motivation of creating the project reluctance to do repetitive activities (copy-paste of code fragments to implement 
new messages) and error-prone defining of data frames.


## Raspberry Pi Pico example

In examples directory is simple use case of the generator. It consists of steering onboard LED and reading inner 
temperature sensor. More details [here](examples/pico-simple/README.md).

Example consists of following `JSON` config:

<!-- insertstart include="examples/pico-simple/pico-protocol.json" pre="\n\n```\n" post="\n```\n\n" -->

```
{
    "_description_": "Host side config",
    "device_a": {
        "class_name": "HostConnector",
        "class_template": "protocol.py.tmpl",
        "enum_name": "HostMessage",
        "enum_template": "message.py.tmpl"
    },

    "_description_": "Sensor side config",
    "device_b": {
        "class_name": "SensorConnector",
        "class_template": "protocol.py.tmpl",
        "enum_name": "SensorMessage",
        "enum_template": "message.py.tmpl"
    },

	"_description_": "Package name to place code into",
    "package_name": "picoserial",

    "_description_": "type of message identifier, allowed: str, int or hex",
    "message_id_type": "hex",

    "_description_": [
    	"definition of messages",
		"allowed field types: bool, byte, int16, bytearray, str",
        "allowed message direction:",
        "  <empty>   both directions",
        "  BOTH      both directions",
        "  TO_A      from MCU (RPi Pico) to Host (PC)",
        "  TO_B      from Host to MCU",
        "  DISABLED  skip item"
    ],
    "messages": [
        { "id": "SET_KBD_INTR_RQST",        "direction": "TO_B", "fields": [ {"id": "new_state", "type": "bool"} ] },
        { "id": "SET_INTERNAL_LED_RQST",    "direction": "TO_B", "fields": [ {"id": "new_state", "type": "bool"} ] },
        { "id": "INTERNAL_TEMP_RQST",       "direction": "TO_B", "fields": [] },
        { "id": "TEST_BYTES_RQST",          "direction": "TO_B", "fields": [ {"id": "data_bytes", "type": "bytearray"}, {"id": "transfer_num", "type": "int16"} ] },
        { "id": "TEST_TEXT_RQST",           "direction": "TO_B", "fields": [ {"id": "content", "type": "str"}, {"id": "transfer_num", "type": "int16"} ] },

        { "id": "UNKNOWN_REQUEST_RSPNS",    "direction": "TO_A", "fields": [ {"id": "message", "type": "byte"} ] },
        { "id": "INTERNAL_TEMP_RSPNS",      "direction": "TO_A", "fields": [ {"id": "temperature", "type": "int16"} ] },
        { "id": "TEST_BYTES_RSPNS",         "direction": "TO_A", "fields": [ {"id": "data_bytes", "type": "bytearray"} ] },
        { "id": "TEST_TEXT_RSPNS",          "direction": "TO_A", "fields": [ {"id": "content", "type": "str"} ] }
    ]
}
```

<!-- insertend -->


## Generating protocol

To generate protocol codes do following steps:
1. define configuration `.json` file (example: [examples/pico-simple/pico-protocol.json](examples/pico-simple/pico-protocol.json))
2. execute generator `python3 -m mpyserialprotogen` with config file passed as argument

Type `python3 -m mpyserialprotogen --help` for supported input arguemnts or open [help page](doc/cmdargs.md).


## Installation

Installation of package can be done by:
 - to install package from downloaded ZIP file execute: `pip3 install --user -I file:mpython-serial-protogen-master.zip#subdirectory=src`
 - to install package directly from GitHub execute: `pip3 install --user -I git+https://github.com/anetczuk/mpython-serial-protogen.git#subdirectory=src`
 - uninstall: `pip3 uninstall mpyserialprotogen`

Installation For development:
 - `src/install-deps.sh` to install package dependencies only (`requirements.txt`)
 - `src/install-package.sh` to install package in standard way through `pip` (with dependencies)
 - `src/install-package-dev.sh` to install package in developer mode using `pip` (with dependencies)


## MicroPython limitations

- no support for `enum` classes
- no support for `abc` module


## References

- [Texthon template processor](http://texthon.chipsforbrain.org/)
- [Raspberry Pi Pico documentation](https://www.raspberrypi.com/documentation/microcontrollers/raspberry-pi-pico.html)


## License

BSD 3-Clause License

Copyright (c) 2024, Arkadiusz Netczuk <dev.arnet@gmail.com>

Redistribution and use in source and binary forms, with or without
modification, are permitted provided that the following conditions are met:

1. Redistributions of source code must retain the above copyright notice, this
   list of conditions and the following disclaimer.

2. Redistributions in binary form must reproduce the above copyright notice,
   this list of conditions and the following disclaimer in the documentation
   and/or other materials provided with the distribution.

3. Neither the name of the copyright holder nor the names of its
   contributors may be used to endorse or promote products derived from
   this software without specific prior written permission.

THIS SOFTWARE IS PROVIDED BY THE COPYRIGHT HOLDERS AND CONTRIBUTORS "AS IS"
AND ANY EXPRESS OR IMPLIED WARRANTIES, INCLUDING, BUT NOT LIMITED TO, THE
IMPLIED WARRANTIES OF MERCHANTABILITY AND FITNESS FOR A PARTICULAR PURPOSE ARE
DISCLAIMED. IN NO EVENT SHALL THE COPYRIGHT HOLDER OR CONTRIBUTORS BE LIABLE
FOR ANY DIRECT, INDIRECT, INCIDENTAL, SPECIAL, EXEMPLARY, OR CONSEQUENTIAL
DAMAGES (INCLUDING, BUT NOT LIMITED TO, PROCUREMENT OF SUBSTITUTE GOODS OR
SERVICES; LOSS OF USE, DATA, OR PROFITS; OR BUSINESS INTERRUPTION) HOWEVER
CAUSED AND ON ANY THEORY OF LIABILITY, WHETHER IN CONTRACT, STRICT LIABILITY,
OR TORT (INCLUDING NEGLIGENCE OR OTHERWISE) ARISING IN ANY WAY OUT OF THE USE
OF THIS SOFTWARE, EVEN IF ADVISED OF THE POSSIBILITY OF SUCH DAMAGE.
