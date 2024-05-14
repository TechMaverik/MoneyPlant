from machine import Pin, I2C
import time
from dht import DHT11, InvalidChecksum
from lcd_api import LcdApi
from i2c_lcd import I2cLcd


class MoneyPlant:

    def __init__(self):
        self.enable = Pin(13, Pin.OUT)
        self.motor_p = Pin(14, Pin.OUT)
        self.motor_n = Pin(15, Pin.OUT)
        self.led = Pin(25, Pin.OUT)

    def get_dh11_readings(self):
        self.led.value(0)
        time.sleep(2)
        pin = Pin(12, Pin.OUT, Pin.PULL_DOWN)
        sensor = DHT11(pin)
        temp = sensor.temperature
        humidity = sensor.humidity
        self.led.value(1)
        return (temp, humidity)

    def get_delay(self, temperature):
        if temperature < 35.0 and temperature > 30.0:
            set_delay = 10
        elif temperature > 35.0 and temperature < 40.0:
            set_delay = 900
        elif temperature < 30.0:
            set_delay = 3600
        else:
            set_delay = 450
        return set_delay

    def activate_pump_motor(self):
        self.motor_p.value(1)
        self.motor_n.value(0)
        self.enable.value(1)
        print("Pump ON")
        time.sleep(20)
        self.motor_p.value(0)
        self.motor_n.value(0)
        self.enable.value(0)
        print("Pump OFF")
        count = 0
        self.led.value(0)
        return count

    def messages(self, lcd):
        lcd.move_to(0, 0)
        lcd.putstr("HL Robotics")
        lcd.move_to(0, 1)
        lcd.putstr("Loading ...")
        time.sleep(3)
        lcd.clear()
        lcd.move_to(0, 0)
        lcd.putstr("Money Plant")
        lcd.move_to(0, 1)
        lcd.putstr("Project")
        time.sleep(3)


count = 0
print("HL Robotics Money Plant Project")

I2C_ADDR = 0x27
I2C_NUM_ROWS = 2
I2C_NUM_COLS = 16
i2c = I2C(1, sda=Pin(2), scl=Pin(3), freq=400000)
lcd = I2cLcd(i2c, I2C_ADDR, I2C_NUM_ROWS, I2C_NUM_COLS)
MoneyPlant().messages(lcd)

while True:

    temperature, humidity = MoneyPlant().get_dh11_readings()
    print(temperature, humidity)
    generated_delay = MoneyPlant().get_delay(temperature)
    lcd.move_to(0, 0)
    lcd.putstr(
        "Temp:"
        + str(temperature)
        + " "
        + "Trigger in: "
        + str(count)
        + "/"
        + str(generated_delay)
    )
    lcd.move_to(0, 1)
    lcd.putstr("Humidity:" + str(humidity))
    if count == generated_delay:
        lcd.clear()
        lcd.move_to(0, 0)
        lcd.putstr("Water Pumping")
        lcd.move_to(0, 1)
        lcd.putstr("In Progress ....")
        count = MoneyPlant().activate_pump_motor()
    else:
        count = count + 1
        print(temperature, humidity, str(count) + "/" + str(generated_delay))
