import axp202

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
pmu.dump_irq()

def callback(pmu):
    print('ACIN plug in')

pmu.irq(handler=callback, trigger=pmu.IRQ_VBUS_PLUGIN)
