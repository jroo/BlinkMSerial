import blinkm_serial

port = "/dev/tty.usbserial-A700fjEg"

calibration = {'brightness':0.6, 'color':{'r':1, 'g':1.35, 'b':0.5 }}
b = blinkm_serial.BlinkMSerial(port, calibration=calibration)
b.open()
b.fade_to_hex_rgb('fdfdfe')
b.close()