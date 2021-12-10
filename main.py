def on_button_pressed_a():
    global led2
    led2 += 1
    basic.show_icon(IconNames.YES)
input.on_button_pressed(Button.A, on_button_pressed_a)

def on_button_pressed_b():
    global led2
    led2 += 0
    basic.show_icon(IconNames.NO)
input.on_button_pressed(Button.B, on_button_pressed_b)

led2 = 0
ESP8266_IoT.init_wifi(SerialPin.P8, SerialPin.P12, BaudRate.BAUD_RATE115200)
ESP8266_IoT.connect_wifi("WIFIDUINO", "12345678")
if ESP8266_IoT.wifi_state(True):
    OLED.init(128, 64)
    OLED.clear()
    OLED.write_string_new_line("Conectado")
    RTC_DS1307.set_time(RTC_DS1307.TimeType.HOUR, 14)
    RTC_DS1307.set_time(RTC_DS1307.TimeType.MINUTE, 15)
    RTC_DS1307.set_time(RTC_DS1307.TimeType.SECOND, 0)
else:
    OLED.clear()
    OLED.write_string_new_line("No conectado")

def on_forever():
    ESP8266_IoT.connect_thing_speak()
    ESP8266_IoT.set_data("7TE3L53GOU1FH9RZ",
        Environment.read_light_intensity(AnalogPin.P1),
        Environment.octopus_BME280(Environment.BME280_state.BME280_TEMPERATURE_C),
        Environment.octopus_BME280(Environment.BME280_state.BME280_HUMIDITY),
        led2)
    ESP8266_IoT.upload_data()
    basic.pause(1000)
basic.forever(on_forever)

def on_forever2():
    global led2
    OLED.clear()
    OLED.write_string("Intensidad: ")
    OLED.write_num(Environment.read_light_intensity(AnalogPin.P1))
    OLED.new_line()
    OLED.write_string("Temperatura: ")
    OLED.write_num(Environment.octopus_BME280(Environment.BME280_state.BME280_TEMPERATURE_C))
    OLED.new_line()
    OLED.write_string("Humedad: ")
    OLED.write_num(Environment.octopus_BME280(Environment.BME280_state.BME280_HUMIDITY))
    if Environment.read_light_intensity(AnalogPin.P1) < 10:
        pins.servo_write_pin(AnalogPin.P13, 90)
        led2 += 1
    else:
        pins.servo_write_pin(AnalogPin.P13, 0)
        basic.pause(1000)
        led2 = 0
    basic.pause(1000)
basic.forever(on_forever2)
