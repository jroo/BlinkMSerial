import blinkm_serial

port = "/dev/tty.usbserial-A700607d"

b = blinkm_serial.BlinkMSerial(port)
b.open()
b.fade_to_hex_rgb('00ff00')
b.close()