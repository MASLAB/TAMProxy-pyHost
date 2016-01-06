TAMProxy Python Host
====================

Purpose
-------

TAMProxy (Totally A Microcontroller Proxy) is a microcontroller project offloads configuration, sampling, or setting of microcontroller devices/peripherals to a host computer through exchange USB packets.

For example, running the classic Arduino blink sketch using the python host software is as simple as:

	class Blink(Sketch):
	
	    def setup(self):
	        self.led = DigitalOutput(self.tamp, 13)
	        self.led_timer = Timer()
	        self.led_state = False
	
	    def loop(self):
	        if self.led_timer.millis() > 1000:
	            self.led_timer.reset()
	            self.led_state = not self.led_state
	            self.led.write(self.led_state)
	
    sketch = Blink()
    sketch.run()
    
With most similar libraries that control Arduino pins over USB, the communication is of a stop and wait nature. When the user sends a request, their program blocks while waiting for a response from the Arduino. With USB serial latency often in the millisecond range, this puts a big bottleneck on the user's code.

TAMProxy does things differently by having a formalized variable-length packet structure and implementing a sliding window protocol on the host side to send them. TAMProxy can release several packets and simultaneously listen for the responses of packets sent earlier, which significantly increases throughput. All the communcations code runs in another process, so the user's sketch never blocks. In preliminary testing, throughput reaches around 17,000 packets per second at maximum when running PyPy 4.0.1 on a 2013 MBP.

TAMProxy was designed for use in MIT's MASLAB 2016 competition (autonomous robotics). It currently only supports the Teensy 3.x boards, but support for Arduinos is probably possible if development continues.

### Limitations
Right now this firmware only works with the Teensy 3.x, with the support of the Teensyduino libraries available from PJRC

Communicating with certain peripherals that need high-speed or advanced features such as interrupts, SPI, or I2C will be difficult to use if support for that peripheral isn't built into TAMProxy yet.

Adding support for these peripherals is best done by extending the corresponding firmware ([TAMProxy-Firmware](https://github.com/mitchgu/TAMProxy-Firmware))

Supported Devices
-----------------
- [x] Digital input
- [x] Digital output
- [x] Analog input
- [ ] Analog output (PWM, or DAC on A14/40)
- [ ] Quadrature encoder
- [ ] Standard Motor (Cytron/Dago with PWM & dir)
- [ ] Feedback motor (Encoder feedback with PID for settable speed)
- [ ] Servo Motor
- [ ] Stepper Motor
- [ ] Analog Devices Gyroscope (SPI)
- [ ] Ultrasonic Distance Sensor
- [x] Short-range IR Distance Sensor (just an analog input)
- [x] Ultra-short range IR Distance Sensor (just a digital input)
- [ ] Color Sensor (SPI)


Dependencies
------------

- Python 2.7.x or PyPy 4.x.x
- PySerial 3.0 (2.x won't work, they changed some names)
- NumPy (Use the PyPy version if you're using PyPy)
- PyYAML (for configuration)

Unfortunately, getting the Makefile to work with an existing Teensyduino install is difficult on Windows, so the Makefile currently only works with OSX or Linux. Windows support is hopefully coming though.

Quick Start
-----------

- The `tamproxy/config.yaml` file has all the settings and constants and explanations for you to peruse/adjust before starting. Be warned that I've only tested on my OSX machine so far, so the best settings may vary significantly. I plan to document things better soon
- Compile the TAMProxy-Firmware repo and upload it to your Teensy. Follow the directions on that repo's readme.
- run `python blink.py` to try out the blink demo and go from there

Performance is greatly increased when using PyPy since the packet controlling is pretty CPU-bound and cpython is kinda slow. I recommend using pyenv to manage python installations if you want to go this route.