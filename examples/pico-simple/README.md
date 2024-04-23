# Simple Raspberry Pi Pico protocol

Following example presents code generated for RPi Pico (MicroPython) and for host PC (Python).


## Content

- `pico-protocol.json` configuration file for the generator
- `generate.sh` script executing the generator with proper JSON
- `code/picoserial` generated protocol code
- `code/boot` MicroPython bootloader for Pico
- `code/pico` sample application for RPi
- `code/host` sample application for PC
- `code/connect-pico.sh` connecting to Pico using `rshell`
- `code/send-pico-code.sh` uploading to device and execution of Pico sample application
- `code/run-host.sh` running PC sample application


## How to use

1. connect RPi Pico to PC using USB
2. upload bootloader from `code/boot` and reset the board (only first time)
3. upload Pico application by following command: `send-pico-code.sh --upload` and reset the board (after every change in code)
4. run host application on PC: `run-host.sh`

If everything works properly, then there should be similar output:
```
connecting
2024-04-23 18:59:29.364730 INFO:  disabling Pico keyboard interrupt
2024-04-23 18:59:29.466729 INFO:  Pico internal temperature: 24.7
2024-04-23 18:59:30.469023 INFO:  Pico internal temperature: 24.23
2024-04-23 18:59:31.471347 INFO:  Pico internal temperature: 24.7
2024-04-23 18:59:32.473276 INFO:  Pico internal temperature: 24.7
```

In case of problems use `connect-pico.sh` to connect to the board and investigate log file `/pyboard/log.txt`.
