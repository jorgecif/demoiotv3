input.onButtonPressed(Button.A, function () {
    led2 += 1
    basic.showIcon(IconNames.Yes)
})
input.onButtonPressed(Button.B, function () {
    led2 += 0
    basic.showIcon(IconNames.No)
})
let led2 = 0
ESP8266_IoT.initWIFI(SerialPin.P8, SerialPin.P12, BaudRate.BaudRate115200)
ESP8266_IoT.connectWifi("WIFIDUINO", "12345678")
if (ESP8266_IoT.wifiState(true)) {
    OLED.init(128, 64)
    OLED.clear()
    OLED.writeStringNewLine("Conectado")
    RTC_DS1307.setTime(RTC_DS1307.TimeType.HOUR, 14)
    RTC_DS1307.setTime(RTC_DS1307.TimeType.MINUTE, 15)
    RTC_DS1307.setTime(RTC_DS1307.TimeType.SECOND, 0)
} else {
    OLED.clear()
    OLED.writeStringNewLine("No conectado")
}
basic.forever(function () {
    basic.showIcon(IconNames.Heart)
    ESP8266_IoT.connectThingSpeak()
    ESP8266_IoT.setData(
    "7TE3L53GOU1FH9RZ",
    Environment.ReadLightIntensity(AnalogPin.P1),
    Environment.octopus_BME280(Environment.BME280_state.BME280_temperature_C),
    Environment.octopus_BME280(Environment.BME280_state.BME280_humidity),
    led2
    )
    ESP8266_IoT.uploadData()
    basic.pause(1000)
})
basic.forever(function () {
    OLED.clear()
    OLED.writeString("Intensidad: ")
    OLED.writeNum(Environment.ReadLightIntensity(AnalogPin.P1))
    OLED.newLine()
    OLED.writeString("Temperatura: ")
    OLED.writeNum(Environment.octopus_BME280(Environment.BME280_state.BME280_temperature_C))
    OLED.newLine()
    OLED.writeString("Humedad: ")
    OLED.writeNum(Environment.octopus_BME280(Environment.BME280_state.BME280_humidity))
    if (Environment.ReadLightIntensity(AnalogPin.P1) < 10) {
        pins.servoWritePin(AnalogPin.P13, 90)
        led2 += 1
    } else {
        pins.servoWritePin(AnalogPin.P13, 0)
        basic.pause(1000)
        led2 = 0
    }
    basic.pause(1000)
})
