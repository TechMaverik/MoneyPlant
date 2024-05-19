from machine import Pin, I2C
from i2c_lcd import I2cLcd
from lcd_api import LcdApi
import communications
import time


motor_p = Pin(12, Pin.OUT)
motor_n = Pin(13, Pin.OUT)
light_p = Pin(14, Pin.OUT)
light_n = Pin(15, Pin.OUT)
led = Pin(25, Pin.OUT)
I2C_ADDR = 0x27
I2C_NUM_ROWS = 2
I2C_NUM_COLS = 16
i2c = I2C(1, sda=Pin(2), scl=Pin(3), freq=400000)
lcd = I2cLcd(i2c, I2C_ADDR, I2C_NUM_ROWS, I2C_NUM_COLS)
buzzer = Pin(25, Pin.OUT)
com_protocol = communications.initialize_communications()


def activate(time_data):
    rtc = machine.RTC()
    rtc.datetime(time_data)
    while True:
        (year, month, day, weekday, hour, minute, second, _) = rtc.datetime()
        lcd.move_to(0, 0)
        lcd.putstr(f"{hour:02d}:{minute:02d}:{second:02d}")
        lcd.move_to(0, 1)
        lcd.putstr(f"{day:02d}/{month:02d}/{year}")
        time.sleep(1)
        water_hour = 8
        water_hour2 = 16
        light_on_hour = 18
        light_off_hour = 6
        if hour == water_hour and minute == 0 and second == 10:
            activate_pump_motor()
        if hour == water_hour2 and minute == 0 and second == 10:
            activate_pump_motor()
        if hour == light_on_hour and minute == 0 and second == 10:
            activate_light()
        if hour == light_off_hour and minute == 0 and second == 10:
            deactivate_light()


def messages(lcd):
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


def activate_pump_motor():
    motor_p.value(1)
    motor_n.value(0)
    print("PUMP ON")
    time.sleep(60)
    motor_p.value(0)
    motor_n.value(0)
    print("PUMP OFF")
    count = 0
    led.value(0)
    return count


def activate_light():
    light_p.value(1)
    light_n.value(0)
    print("LIGHTS ON")
    time.sleep(1)


def deactivate_light():
    light_p.value(0)
    light_n.value(0)
    print("LIGHTS OFF")
    time.sleep(1)


messages(lcd)
menu = ["Y ", "M ", "D ", "W ", "H ", "M ", "S"]
time_data = []
lcd.clear()
lcd.move_to(0, 0)
for item in menu:
    lcd.putstr(item)
com_protocol.write("Enter Time Details in the Format:")
com_protocol.write("Year, Month, Date , Week, Hour, Minute, Second")

while True:
    if com_protocol.any():
        command = com_protocol.read()
        data = str(command.decode()).lower()
        data = data.strip()
        time_data.append(int(data))
        if len(time_data) == 0:
            com_protocol.write("Year:")
        if len(time_data) == 1:
            com_protocol.write("Month:")
        if len(time_data) == 2:
            com_protocol.write("Date:")
        if len(time_data) == 3:
            com_protocol.write("Week:")
        if len(time_data) == 4:
            com_protocol.write("Hour:")
        if len(time_data) == 5:
            com_protocol.write("Minute:")
        if len(time_data) == 6:
            com_protocol.write("Second:")
        if len(time_data) == 7:
            com_protocol.write("MilliSecond:")

        if len(time_data) == 8:
            data = tuple(time_data)
            print(data)
            lcd.clear()
            activate(data)
