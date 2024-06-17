import axp202
import time
from machine import I2C
from machine import Pin

'''
t-watch 2020 v3
    scl: 22
    sda: 21
    intr: 35
'''
i2c0 = I2C(0, scl=Pin(22), sda=Pin(21))
pmu = axp202.AXP202(i2c0, intr=Pin(35, mode=Pin.IN))

pmu.adc_enable(axp202.AXP202_VBUS_VOLTAGE_ADC)
pmu.adc_enable(axp202.AXP202_VBUS_CURRENT_ADC)
pmu.adc_enable(axp202.AXP202_ACIN_VOLTAGE_ADC)
pmu.adc_enable(axp202.AXP202_ACIN_CURRENT_ADC)
pmu.adc_enable(axp202.AXP202_BATTERY_VOLTAGE_ADC)
pmu.adc_enable(axp202.AXP202_BATTERY_CURRENT_ADC)
pmu.adc_enable(axp202.AXP202_APS_VOLTAGE_ADC)
pmu.adc_enable(axp202.AXP202_INTERNAL_TEMPERATURE_ADC)
pmu.dump_adc()

while True:
    print("VBUS:")
    print("  voltage: %dmv" % pmu.vbus_voltage)
    print("  current: %dma" % pmu.vbus_current)

    print("ACIN:")
    print("  voltage: %dmv" % pmu.acin_voltage)
    print("  current: %dma" % pmu.acin_current)

    print("Battery")
    print("  voltage: %dmv" % pmu.battery_voltage)
    print("  current: %dma" % pmu.battery_current)
    print("  charge current: %dma" % pmu.battery_charge_current)

    print("APS:")
    print("  current: %dmv" % pmu.ipsout_voltage)

    print("CHIP:")
    print("  temperature: %.2f℃" % pmu.temperature)
    time.sleep(1)