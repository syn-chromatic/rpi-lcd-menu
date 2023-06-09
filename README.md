# RPi LCD Menu

## `➢` Table of Contents
1. [Information](#-information)
2. [Installation (RPi)](#-installation-rpi)
3. [Parts](#-parts)
4. [Breadboard Diagram (RPi)](#-breadboard-diagram-rpi)
5. [Previews](#-previews)

___
## `➢` Information
* `rpi` for the Raspberry Pi 1/2/3/4
* `rp2040-pico` for the Raspberry Pi Pico (Untested)
* `rp2040-simulation` for Wowki Pico Simulation

___
## `➢` Installation (RPi)
Tested on Ubuntu 23.04 using a Raspberry Pi 4.

### `⤷` Installing Python Dependencies
* `pip install -r requirements.txt`

### `⤷` Installing PiGPIO
To install the PiGPIO library, run the following command:
* `sudo apt install python3-pigpio`

The library is not yet functional, as it requires a daemon to be running.

### `⤷` Installing PiGPIO Daemon (PiGPIOd)
```shell
wget https://github.com/joan2937/pigpio/archive/master.zip
unzip master.zip
cd pigpio-master
make
sudo make install
```

Those instructions are taken from [here](https://abyz.me.uk/rpi/pigpio/download.html).

To start the daemon, run the following command:
* `sudo pigpiod`

The daemon doesn't automatically start on boot.

___
## `➢` Parts
* x1 I2C LCD (16x2 OR 20x4)
* x4 1K Resistors
* x4 Momentary Push Buttons

___
## `➢` Breadboard Diagram (RPi)
![rpi-lcd-menu_bb](https://github.com/syn-chromatic/rpi-lcd-menu/assets/68112904/6937a6d6-2d49-41e1-a1cf-360e7b928617)

___
## `➢` Previews
### `⤷` RP2040 Pico Simulation
[Wowki Project](https://wokwi.com/projects/366452940481298433)

https://github.com/syn-chromatic/rpi-lcd-menu/assets/68112904/0871875d-3d89-42be-a493-d958d09ca745


