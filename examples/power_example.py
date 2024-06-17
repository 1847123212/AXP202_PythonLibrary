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

# pmu.power_enable(axp202.AXP202_DCDC2)
# pmu.power_enable(axp202.AXP202_DCDC3)
pmu.power_enable(axp202.AXP202_LDO2)
# pmu.power_enable(axp202.AXP202_LDO3)
# pmu.power_enable(axp202.AXP202_LDO4)

# pmu.dc2_voltage = 2000
# pmu.dc3_voltage = 3300

pmu.ldo2_voltage = 3300
# pmu.ldo3_voltage = 3300
# pmu.ldo4_voltage = 3300


