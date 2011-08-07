import serial
import time

class BlinkMSerial:
    def __init__(self, port, ic2_address=0x09, 
            calibration={ 'brightness':1, 'color':{'r':1, 'g':1, 'b':1 } }):
        self.address = ic2_address
        self.port = port
        self.calibration = calibration

        try:
            self.ser = serial.Serial(port, 19200, timeout=1)
            print "connecting"
            while True:
            	serialline = self.ser.readline()
            	if (serialline):
            		print serialline.strip()
            	if ('ready' in serialline):
            		break
        except:
            self.ser = None
            print "error establishing connection to serial port '%s'" % port
            
    def _hex_to_rgb(self, hex_rgb):
        r = int('0x%s' % hex_rgb[0:2], 16)
        g = int('0x%s' % hex_rgb[2:4], 16)
        b = int('0x%s' % hex_rgb[4:6], 16)
        return {'r':r, 'g':g, 'b':b}
        
    def _calibrate_rgb(self, r, g, b):
        r = int(r * self.calibration['color']['r'] * self.calibration['brightness'])
        g = int(g * self.calibration['color']['g'] * self.calibration['brightness'])
        b = int(b * self.calibration['color']['b'] * self.calibration['brightness'])
        return {'r':r, 'g':g, 'b':b}
        
    def open(self):
        if self.ser:
            self.ser.open()
        return

    def close(self):
        if self.ser:
            self.ser.close()
        return
        
    def write(self, cmd):
        if self.ser:
            self.ser.write(cmd)
        return
        
    def send_command(self, payload, num_bytes_receive=0):
        start_byte = '01'
        address = '%02x' % self.address
        num_bytes_send = '%02x' % len(payload)
        num_bytes_receive = '%02x' % int(num_bytes_receive)
        cmd = [start_byte, address, num_bytes_send, num_bytes_receive]
        for item in payload:
            cmd.append('%02x' % item)
        cmd_str = ''.join(cmd)
        self.write(cmd_str.decode('hex'))
        time.sleep (.2)
        
    def stop_script(self):
        self.send_command([ord('o'), 0x6f])
        
    def go_to_rgb(self, r, g, b):
        calibrated = self._calibrate_rgb(r, g, b)
        self.stop_script()
        self.send_command([ord('n'), calibrated['r'], calibrated['g'], calibrated['b']])        
        
    def fade_to_rgb(self, r, g, b):
        calibrated = self._calibrate_rgb(r, g, b)
        self.stop_script()
        self.send_command([ord('c'), calibrated['r'], calibrated['g'], calibrated['b']])
        
    def fade_to_hsb(self, h, s, b):
        self.stop_script()
        self.send_command([ord('h'), h, s, b])
        
    def fade_random_rgb(self, r=0, g=0, b=0):
        calibrated = self._calibrate_rgb(r, g, b)
        self.stop_script()
        self.send_command([ord('C'), calibrated['r'], calibrated['g'], calibrated['b']])
        
    def fade_random_hsb(self, h=0, s=0, b=0):
        self.stop_script()
        self.send_command([ord('H'), h, s, b])
        
    def play_light_script(self, n, r=0, p=0):
        self.stop_script()
        self.send_command([ord('p'), n, r, p])
        
    def set_fade_speed(self, f):
        self.stop_script()
        self.send_command([ord('f'), f])
        
    def set_time_adjust(self, t):
        self.stop_script()
        self.send_command([ord('t'), t])
        
    def go_to_hex_rgb(self, hex_rgb):
        rgb_obj = self._hex_to_rgb(hex_rgb)
        self.go_to_rgb(rgb_obj['r'], rgb_obj['g'], rgb_obj['b'])
        
    def fade_to_hex_rgb(self, hex_rgb):
        rgb_obj = self._hex_to_rgb(hex_rgb)
        self.fade_to_rgb(rgb_obj['r'], rgb_obj['g'], rgb_obj['b'])