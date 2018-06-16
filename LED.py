# Import the WS2801 module.
import Adafruit_WS2801
import Adafruit_GPIO.SPI as SPI

import RPi.GPIO as GPIO

import time, datetime, threading, json

# Adafruit_WS2801.RGB_to_color(pos * 3, 255 - pos * 3, 0)
# pixels.count()
# pixels.set_pixel(i, wheel(((i * 256 // pixels.count())) % 256) )
# pixels.show()
# pixels.clear()
# pixels.get_pixel_rgb(i)
# reversed(range(i, pixels.count()))

class theLEDs(threading.Thread):

    # Configure the count of pixels:
    PIXEL_COUNT = 24

    runvar = True

    # Alternatively specify a hardware SPI connection on /dev/spidev0.0:
    SPI_PORT   = 0
    SPI_DEVICE = 0
    pixels = Adafruit_WS2801.WS2801Pixels(PIXEL_COUNT, spi=SPI.SpiDev(SPI_PORT, SPI_DEVICE), gpio=GPIO)

    comparesecond = 0
    t = 0

    nowdata = [1, 2, 3]

    config = {'state': None, 'brightness': None, 'show': None, 'r': None, 'g': None, 'b': None}

    def __init__(self):
        threading.Thread.__init__(self)
        with open('settings.json', 'r') as file:
            data = json.load(file)
            LED = data['LED']
            self.config['state'] = LED['state']
            self.config['brightness'] = float(LED['brightness'])
            self.config['show'] = LED['show']
            self.config['r'] = int(LED['r'])
            self.config['g'] = int(LED['g'])
            self.config['b'] = int(LED['b'])

    def config_led(self, config = {'state': None, 'brightness': None, 'show': None, 'r': None, 'g': None, 'b': None}):
        for c in self.config:
            if config[c] is not None:
                self.config[c] = config[c]

        with open('settings.json', 'w') as file:
            json.dump(self.config, file)

    def set_leds(self, number):
        highnumber = number/10
        lownumber = number%10

        leds = [[0, 0, 0, 0],[0, 0, 0, 0]]

        leds[0][3] = lownumber/8
        leds[0][2] = lownumber%8/4
        leds[0][1] = lownumber%8%4/2
        leds[0][0] = lownumber%8%4%2/1

        leds[1][0] = highnumber/8
        leds[1][1] = highnumber%8/4
        leds[1][2] = highnumber%8%4/2
        leds[1][3] = highnumber%8%4%2/1

        return leds

    def show(self, type, r, g, b, brightness):
        nowdata = [None, None, None]
        if type == 'time':
            now = datetime.datetime.now()
            nowdata = [now.second, now.minute, now.hour]

        elif type == 'date':
            now = datetime.datetime.now()
            nowdata = [now.year, now.month, now.day]

        else:
            return 0

        for k in range(len(nowdata)):
            leds = self.set_leds(nowdata[k])
            for i in range(len(leds)):
                for j in range(len(leds[i])):
                    if leds[i][j] == 1:
                        self.pixels.set_pixel(j+(k*8)+i*4, Adafruit_WS2801.RGB_to_color(int(r*brightness), int(g*brightness), int(b*brightness)))
                    else:
                        self.pixels.set_pixel(j+(k*8)+i*4, Adafruit_WS2801.RGB_to_color(0, 0, 0))

        self.pixels.show()

    def light(self):
        for i in range(self.PIXEL_COUNT):
            self.pixels.set_pixel(i, Adafruit_WS2801.RGB_to_color(150, 150, 150))
        self.pixels.show()
    def off(self):
        self.pixels.clear()
        self.pixels.show()

    def run(self):
        self.pixels.clear()
        self.pixels.show()

        while True:
            while self.config['status']:
                if self.config['show'] == "time":
                    while self.config['show'] == "time":
                        self.show('time', self.config['r'],self.config['g'], self.config['b'], self.config['brightness'])

                elif self.config['show'] == "date":
                    while self.config['show'] == "date":
                        self.show('date', self.config['r'],self.config['g'], self.config['b'], self.config['brightness'])

                elif self.config['show'] == "light":
                    self.light()
                    while self.config['show'] == "light":
                        pass

                elif self.config['show'] == "off":
                    self.off()
                    while self.config['show'] == "off":
                        pass