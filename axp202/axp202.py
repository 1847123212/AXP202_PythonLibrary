'''
MIT License

Copyright (c) 2019 lewis he

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
SOFTWARE.

axp20x.py - MicroPython library for X-Power AXP202 chip.
Created by Lewis he on June 24, 2019.
github:https://github.com/lewisxhe/AXP202X_Libraries
'''

try:
    from struct import unpack as _unpack
except:
    from ustruct import unpack as _unpack

from micropython import schedule as _schedule
from .axp202_reg import *

__adc_channel = {
    AXP202_BATTERY_VOLTAGE_ADC      : (AXP202_ADC_EN1_REG, 7),
    AXP202_BATTERY_CURRENT_ADC      : (AXP202_ADC_EN1_REG, 6),
    AXP202_ACIN_VOLTAGE_ADC         : (AXP202_ADC_EN1_REG, 5),
    AXP202_ACIN_CURRENT_ADC         : (AXP202_ADC_EN1_REG, 4),
    AXP202_VBUS_VOLTAGE_ADC         : (AXP202_ADC_EN1_REG, 3),
    AXP202_VBUS_CURRENT_ADC         : (AXP202_ADC_EN1_REG, 2),
    AXP202_APS_VOLTAGE_ADC          : (AXP202_ADC_EN1_REG, 1),
    AXP202_BATTERY_TEMPERATURE_ADC  : (AXP202_ADC_EN1_REG, 0),
    AXP202_INTERNAL_TEMPERATURE_ADC : (AXP202_ADC_EN2_REG, 7),
    AXP202_GPIO0_FUNC_ADC           : (AXP202_ADC_EN2_REG, 3),
    AXP202_GPIO1_FUNC_ADC           : (AXP202_ADC_EN2_REG, 2)
}

__power_channel = {
    CH_EXTEN : (AXP202_LDO234_DC23_CTL_REG, 0),
    CH_DCDC2 : (AXP202_LDO234_DC23_CTL_REG, 4),
    CH_DCDC3 : (AXP202_LDO234_DC23_CTL_REG, 1),
    CH_LDO2  : (AXP202_LDO234_DC23_CTL_REG, 2),
    CH_LDO4  : (AXP202_LDO234_DC23_CTL_REG, 3),
    CH_LDO3  : (AXP202_LDO234_DC23_CTL_REG, 6)
}


__irq_channel = {
    0  : (AXP202_INTEN1_REG, 7),
    1  : (AXP202_INTEN1_REG, 6),
    2  : (AXP202_INTEN1_REG, 5),
    3  : (AXP202_INTEN1_REG, 4),
    4  : (AXP202_INTEN1_REG, 3),
    5  : (AXP202_INTEN1_REG, 2),
    6  : (AXP202_INTEN1_REG, 1),
    7  : (AXP202_INTEN1_REG, 0), # Reserved
    8  : (AXP202_INTEN2_REG, 7),
    9  : (AXP202_INTEN2_REG, 6),
    10 : (AXP202_INTEN2_REG, 5),
    11 : (AXP202_INTEN2_REG, 4),
    12 : (AXP202_INTEN2_REG, 3),
    13 : (AXP202_INTEN2_REG, 2),
    14 : (AXP202_INTEN2_REG, 1),
    15 : (AXP202_INTEN2_REG, 0),
    16 : (AXP202_INTEN3_REG, 7),
    17 : (AXP202_INTEN3_REG, 6),
    18 : (AXP202_INTEN3_REG, 5),
    19 : (AXP202_INTEN3_REG, 4),
    20 : (AXP202_INTEN3_REG, 3),
    21 : (AXP202_INTEN3_REG, 2), # Reserved
    22 : (AXP202_INTEN3_REG, 1),
    23 : (AXP202_INTEN3_REG, 0),
    24 : (AXP202_INTEN4_REG, 7),
    25 : (AXP202_INTEN4_REG, 6),
    26 : (AXP202_INTEN4_REG, 5),
    27 : (AXP202_INTEN4_REG, 4),
    28 : (AXP202_INTEN4_REG, 3),
    29 : (AXP202_INTEN4_REG, 2),
    30 : (AXP202_INTEN4_REG, 1),
    31 : (AXP202_INTEN4_REG, 0),
    32 : (AXP202_INTEN5_REG, 7),
    33 : (AXP202_INTEN5_REG, 6),
    34 : (AXP202_INTEN5_REG, 5),
    35 : (AXP202_INTEN5_REG, 4), # Reserved
    36 : (AXP202_INTEN5_REG, 3),
    37 : (AXP202_INTEN5_REG, 2),
    38 : (AXP202_INTEN5_REG, 1),
    39 : (AXP202_INTEN5_REG, 0)
}

class AXP202():
    IRQ_ACIN_OVER_VOLTAGE           = const(0)
    IRQ_ACIN_PLUGIN                 = const(1)
    IRQ_ACIN_REMOVAL                = const(2)
    IRQ_VBUS_OVER_VOLTAGE           = const(3)
    IRQ_VBUS_PLUGIN                 = const(4)
    IRQ_VBUS_REMOVAL                = const(5)
    IRQ_VBUS_VOLTAGE_LOWER          = const(6)
    IRQ_BATTERY_PLUGIN              = const(8)
    IRQ_BATTERY_REMOVAL             = const(9)
    IRQ_BATTERY_ENTER_ACTIVATE_MODE = const(10)
    IRQ_BATTERY_EXIT_ACTIVATE_MODE  = const(11)
    IRQ_BATTERY_CHARGING            = const(12)
    IRQ_BATTERY_CHARGE_DONE         = const(13)
    IRQ_BATTERY_TEMP_TOO_HIGH       = const(14)
    IRQ_BATTERY_TEMP_TOO_LOW        = const(15)
    IRQ_TEMP_HIGH                   = const(16)
    IRQ_CHARGE_CURRENT_INSUFFICIENT = const(17)
    IRQ_DC1_VOLTAGE_LOWER           = const(18)
    IRQ_DC2_VOLTAGE_LOWER           = const(19)
    IRQ_DC3_VOLTAGE_LOWER           = const(20)
    IRQ_PEK_SHORT_PRESS             = const(22)
    IRQ_PEK_LONG_PRESS              = const(23)
    IRQ_POWER_ON                    = const(24)
    IRQ_POWER_OFF                   = const(25)
    IRQ_VBUS_VALID                  = const(26)
    IRQ_VBUS_INVALID                = const(27)
    IRQ_VBUS_SESSION_VALID          = const(28)
    IRQ_VBUS_SESSION_END            = const(29)
    IRQ_LOW_POWER_LEVEL1            = const(30)
    IRQ_LOW_POWER_LEVEL2            = const(31)
    IRQ_TIMER                       = const(32)
    IRQ_PEK_RISING_EDGE             = const(33)
    IRQ_PEK_FALLING_EDGE            = const(34)
    IRQ_GPIO3_INPUT_EDGE_TRIGGER    = const(36)
    IRQ_GPIO2_INPUT_EDGE_TRIGGER    = const(37)
    IRQ_GPIO1_INPUT_EDGE_TRIGGER    = const(38)
    IRQ_GPIO0_INPUT_EDGE_TRIGGER    = const(39)

    CH_EXTEN = CH_EXTEN
    CH_DCDC2 = CH_DCDC2
    CH_DCDC3 = CH_DCDC3
    CH_LDO2  = CH_LDO2
    CH_LDO4  = CH_LDO4
    CH_LDO3  = CH_LDO3

    ADC_BATTERY_VOLTAGE     = AXP202_BATTERY_VOLTAGE_ADC
    ADC_BATTERY_CURRENT     = AXP202_BATTERY_CURRENT_ADC
    ADC_ACIN_VOLTAGE        = AXP202_ACIN_VOLTAGE_ADC
    ADC_ACIN_CURRENT        = AXP202_ACIN_CURRENT_ADC
    ADC_VBUS_VOLTAGE        = AXP202_VBUS_VOLTAGE_ADC
    ADC_VBUS_CURRENT        = AXP202_VBUS_CURRENT_ADC
    ADC_APS_VOLTAGE         = AXP202_APS_VOLTAGE_ADC
    ADC_BATTERY_TEMPERATURE = AXP202_BATTERY_TEMPERATURE_ADC

    def __init__(self, i2c: I2C, address: int = AXP202_SLAVE_ADDRESS, intr: Pin = None) -> None:
        self._intr = intr
        self._chip = AXP202_CHIP_ID
        self._address = address
        self._bus = i2c

        self._buffer  = bytearray(16)
        self._bytebuf = memoryview(self._buffer[0:1])
        self._wordbuf = memoryview(self._buffer[0:2])
        self._irqbuf  = memoryview(self._buffer[0:5])

        self._handler_list = [ None for _ in range(0, 40) ]

        self.__init_device()
        if self._intr is not None:
            self._intr.irq(handler=self.__callback, trigger=self._intr.IRQ_FALLING)
            if self._intr.value() == 0:
                _schedule(self.__handler_irq, self)

    def is_chargeing(self) -> bool:
        data = self.__read_byte(AXP202_MODE_CHGSTATUS_REG)
        return bool(data & (1 << 6))

    def is_battery_connect(self) -> bool:
        data = self.__read_byte(AXP202_MODE_CHGSTATUS_REG)
        return bool(data & (1 << 5))

    def is_vbus_plug(self) -> bool:
        data = self.__read_byte(AXP202_STATUS_REG)
        return bool(data & 1 << 5)

    def dump_power(self) -> None:
        self._bus.readfrom_mem_into(self._address, AXP202_LDO234_DC23_CTL_REG, self._bytebuf)
        print("+--------+--------+--------+")
        print("| Power  | Enable | Value  |")
        print("+========+========+========+")
        print("| EXTEN  |   %d    | n/a    |" % (bool(self._bytebuf[0] & (1 << __power_channel.get(CH_EXTEN)[1]))))
        print("+--------+--------+--------+")
        print("| DCDC2  |   %d    | %04x   |" % (bool(self._bytebuf[0] & (1 << __power_channel.get(CH_DCDC2)[1])), self.__read_byte(AXP202_DC2OUT_VOL_REG) & 0x3F))
        print("+--------+--------+--------+")
        print("| DCDC3  |   %d    | %04x   |" % (bool(self._bytebuf[0] & (1 << __power_channel.get(CH_DCDC3)[1])), self.__read_byte(AXP202_DC3OUT_VOL_REG) & 0x7F))
        print("+--------+--------+--------+")
        print("| LDO2   |   %d    | %04x   |" % (bool(self._bytebuf[0] & (1 << __power_channel.get(CH_LDO2)[1])), self.__read_byte(AXP202_DC2OUT_VOL_REG) & 0x3F))
        print("+--------+--------+--------+")
        print("| LDO3   |   %d    | %04x   |" % (bool(self._bytebuf[0] & (1 << __power_channel.get(CH_LDO3)[1])), self.__read_byte(AXP202_DC3OUT_VOL_REG) & 0x7F))
        print("+--------+--------+--------+")
        print("| LDO4   |   %d    | %04x   |" % (bool(self._bytebuf[0] & (1 << __power_channel.get(CH_LDO4)[1])), self.__read_byte(AXP202_LDO24OUT_VOL_REG) & 0x0F))
        print("+--------+--------+--------+")

    def power_enable(self, ch) -> None:
        channel = __power_channel.get(ch)
        if channel is not None:
            data = self.__read_byte(channel[0])
            data = data | (1 << channel[1])
            self.__write_byte(channel[0], data)

    def power_disable(self, ch) -> None:
        channel = __power_channel.get(ch)
        if channel is not None:
            data = self.__read_byte(channel[0])
            data = data & (~(1 << channel[1]))
            self.__write_byte(channel[0], data)

    @property
    def dc2_voltage(self) -> int:
        data = self.__read_byte(AXP202_DC2OUT_VOL_REG) & 0x3F
        return int(700 + data * 25)

    @dc2_voltage.setter
    def dc2_voltage(self, mv: int) -> None:
        mv = 700 if mv < 700 else mv
        mv = 2275 if mv > 2275 else mv
        val = (mv - 700) / 25
        self.__write_byte(AXP202_DC2OUT_VOL_REG, int(val))

    @property
    def dc3_voltage(self) -> int:
        data = self.__read_byte(AXP202_DC3OUT_VOL_REG) & 0x7F
        return int(700 + data * 25)

    @dc3_voltage.setter
    def dc3_voltage(self, mv: int) -> None:
        mv = 700 if mv < 700 else mv
        mv = 3500 if mv > 3500 else mv
        val = (mv - 700) / 25
        self.__write_byte(AXP202_DC3OUT_VOL_REG, int(val))

    @property
    def ldo2_voltage(self) -> int:
        data = self.__read_byte(AXP202_LDO24OUT_VOL_REG) >> 4
        return int(1800 + data * 100)

    @ldo2_voltage.setter
    def ldo2_voltage(self, mv: int) -> None:
        mv = 1800 if mv < 1800 else mv
        mv = 3300 if mv > 3300 else mv
        val = (mv - 1800) / 100
        prev = self.__read_byte(AXP202_LDO24OUT_VOL_REG) & 0x0F
        prev = prev | (int(val) << 4)
        self.__write_byte(AXP202_LDO24OUT_VOL_REG, prev)

    def set_ldo3_mode(self, mode):
        if(mode > AXP202_LDO3_DCIN_MODE):
            return
        data = self.__read_byte(AXP202_LDO3OUT_VOL_REG)
        if(mode):
            data = data | (1 << 7)
        else:
            data = data & (~(1 << 7))
        self.__write_byte(AXP202_LDO3OUT_VOL_REG, data)

    @property
    def ldo3_voltage(self) -> int:
        data = self.__read_byte(AXP202_LDO3OUT_VOL_REG) & 0x7F
        return int(700 + data * 25)

    @ldo3_voltage.setter
    def ldo3_voltage(self, mv: int) -> None:
        mv = 700 if mv < 700 else mv
        mv = 3500 if mv > 3500 else mv
        val = (mv - 700) / 25
        prev = self.__read_byte(AXP202_LDO3OUT_VOL_REG) & 0x80
        prev = prev | int(val)
        self.__write_byte(AXP202_LDO3OUT_VOL_REG, prev)

    @property
    def ldo4_voltage(self) -> int:
        voltage = (1250, 1300, 1400, 1500, 1600, 1700, 1800, 1900,
                   2000, 2500, 2700, 2800, 3000, 3100, 3200, 3300)
        data = self.__read_byte(AXP202_LDO24OUT_VOL_REG) & 0x0F
        return voltage[data]

    @ldo4_voltage.setter
    def ldo4_voltage(self, mv: int) -> None:
        voltage = (1250, 1300, 1400, 1500, 1600, 1700, 1800, 1900,
                   2000, 2500, 2700, 2800, 3000, 3100, 3200, 3300)
        try:
            val = voltage.index(mv)
        except:
            # todo
            print("The voltage is not within the setting range.")
            return
        data = self.__read_byte(AXP202_LDO24OUT_VOL_REG) & 0xF0
        data = data | (val & 0x0F)
        self.__write_byte(AXP202_LDO24OUT_VOL_REG, data)

    def __callback(self, intr):
        _schedule(self.__handler_irq, self)

    def dump_irq(self):
        buf1 = bytearray(5)
        self._bus.readfrom_mem_into(self._address, AXP202_INTEN1_REG, buf1)
        buf2 = bytearray(5)
        self._bus.readfrom_mem_into(self._address, AXP202_INTSTS1_REG, buf2)
        print("+-------------------------------+--------+--------+")
        print("| IRQ                           | Enable | Status |")
        print("+===============================+========+========+")
        print("| ACIN Over voltage             |   %d    |   %d    |" % (bool(buf1[0] & (1 << 7)), bool(buf2[0] & (1 << 7))))
        print("+-------------------------------+--------+--------+")
        print("| ACIN plug in                  |   %d    |   %d    |" % (bool(buf1[0] & (1 << 6)), bool(buf2[0] & (1 << 6))))
        print("+-------------------------------+--------+--------+")
        print("| ACIN removal                  |   %d    |   %d    |" % (bool(buf1[0] & (1 << 5)), bool(buf2[0] & (1 << 5))))
        print("+-------------------------------+--------+--------+")
        print("| VBUS Over voltage             |   %d    |   %d    |" % (bool(buf1[0] & (1 << 4)), bool(buf2[0] & (1 << 4))))
        print("+-------------------------------+--------+--------+")
        print("| VBUS plug in                  |   %d    |   %d    |" % (bool(buf1[0] & (1 << 3)), bool(buf2[0] & (1 << 3))))
        print("+-------------------------------+--------+--------+")
        print("| VBUS removal                  |   %d    |   %d    |" % (bool(buf1[0] & (1 << 2)), bool(buf2[0] & (1 << 2))))
        print("+-------------------------------+--------+--------+")
        print("| VBUS voltage lower than VHOLD |   %d    |   %d    |" % (bool(buf1[0] & (1 << 1)), bool(buf2[0] & (1 << 1))))
        print("--------------------------------+--------+--------+")
        print("| Battery plugin                |   %d    |   %d    |" % (bool(buf1[1] & (1 << 7)), bool(buf2[1] & (1 << 7))))
        print("+-------------------------------+--------+--------+")
        print("| Battery Removal               |   %d    |   %d    |" % (bool(buf1[1] & (1 << 6)), bool(buf2[1] & (1 << 6))))
        print("+-------------------------------+--------+--------+")
        print("| Enter battery activate mode   |   %d    |   %d    |" % (bool(buf1[1] & (1 << 5)), bool(buf2[1] & (1 << 5))))
        print("+-------------------------------+--------+--------+")
        print("| Exit battery activate mode    |   %d    |   %d    |" % (bool(buf1[1] & (1 << 4)), bool(buf2[1] & (1 << 4))))
        print("+-------------------------------+--------+--------+")
        print("| charging                      |   %d    |   %d    |" % (bool(buf1[1] & (1 << 3)), bool(buf2[1] & (1 << 3))))
        print("+-------------------------------+--------+--------+")
        print("| Charge Done                   |   %d    |   %d    |" % (bool(buf1[1] & (1 << 2)), bool(buf2[1] & (1 << 2))))
        print("+-------------------------------+--------+--------+")
        print("| Battery temp toor high        |   %d    |   %d    |" % (bool(buf1[1] & (1 << 1)), bool(buf2[1] & (1 << 1))))
        print("+-------------------------------+--------+--------+")
        print("| Battery temp too low          |   %d    |   %d    |" % (bool(buf1[1] & (1 << 0)), bool(buf2[1] & (1 << 0))))
        print("+-------------------------------+--------+--------+")
        print("| Die Temp too high             |   %d    |   %d    |" % (bool(buf1[2] & (1 << 7)), bool(buf2[2] & (1 << 7))))
        print("+-------------------------------+--------+--------+")
        print("| Charge current insufficient   |   %d    |   %d    |" % (bool(buf1[2] & (1 << 6)), bool(buf2[2] & (1 << 6))))
        print("+-------------------------------+--------+--------+")
        print("| DCDC1voltage too long         |   %d    |   %d    |" % (bool(buf1[2] & (1 << 5)), bool(buf2[2] & (1 << 5))))
        print("+-------------------------------+--------+--------+")
        print("| DCDC2 voltage too long        |   %d    |   %d    |" % (bool(buf1[2] & (1 << 4)), bool(buf2[2] & (1 << 4))))
        print("+-------------------------------+--------+--------+")
        print("| DCDC3 voltage too long        |   %d    |   %d    |" % (bool(buf1[2] & (1 << 3)), bool(buf2[2] & (1 << 3))))
        print("--------------------------------+--------+--------+")
        print("| PEKshort-press                |   %d    |   %d    |" % (bool(buf1[2] & (1 << 1)), bool(buf2[2] & (1 << 1))))
        print("+-------------------------------+--------+--------+")
        print("| PEK long-press                |   %d    |   %d    |" % (bool(buf1[2] & (1 << 0)), bool(buf2[2] & (1 << 0))))
        print("+-------------------------------+--------+--------+")
        print("| N_OE Power on                 |   %d    |   %d    |" % (bool(buf1[3] & (1 << 7)), bool(buf2[3] & (1 << 7))))
        print("+-------------------------------+--------+--------+")
        print("| N_OEPower off                 |   %d    |   %d    |" % (bool(buf1[3] & (1 << 6)), bool(buf2[3] & (1 << 6))))
        print("+-------------------------------+--------+--------+")
        print("| VBUS Valid                    |   %d    |   %d    |" % (bool(buf1[3] & (1 << 5)), bool(buf2[3] & (1 << 5))))
        print("+-------------------------------+--------+--------+")
        print("| VBUS Invalid                  |   %d    |   %d    |" % (bool(buf1[3] & (1 << 4)), bool(buf2[3] & (1 << 4))))
        print("+-------------------------------+--------+--------+")
        print("| VBUS Session Valid            |   %d    |   %d    |" % (bool(buf1[3] & (1 << 3)), bool(buf2[3] & (1 << 3))))
        print("+-------------------------------+--------+--------+")
        print("| VBUS Session End              |   %d    |   %d    |" % (bool(buf1[3] & (1 << 2)), bool(buf2[3] & (1 << 2))))
        print("+-------------------------------+--------+--------+")
        print("| Low power LEVEL1              |   %d    |   %d    |" % (bool(buf1[3] & (1 << 1)), bool(buf2[3] & (1 << 1))))
        print("+-------------------------------+--------+--------+")
        print("| Low power LEVEL2              |   %d    |   %d    |" % (bool(buf1[3] & (1 << 0)), bool(buf2[3] & (1 << 0))))
        print("+-------------------------------+--------+--------+")
        print("| Timer interrupt               |   %d    |   %d    |" % (bool(buf1[4] & (1 << 7)), bool(buf2[4] & (1 << 7))))
        print("+-------------------------------+--------+--------+")
        print("| PEK rising edge               |   %d    |   %d    |" % (bool(buf1[4] & (1 << 6)), bool(buf2[4] & (1 << 6))))
        print("+-------------------------------+--------+--------+")
        print("| PEK falling edge              |   %d    |   %d    |" % (bool(buf1[4] & (1 << 5)), bool(buf2[4] & (1 << 5))))
        print("--------------------------------+--------+--------+")
        print("| GPIO3 input edge trigger      |   %d    |   %d    |" % (bool(buf1[4] & (1 << 3)), bool(buf2[4] & (1 << 3))))
        print("+-------------------------------+--------+--------+")
        print("| GPIO2 input edge trigger      |   %d    |   %d    |" % (bool(buf1[4] & (1 << 2)), bool(buf2[4] & (1 << 2))))
        print("+-------------------------------+--------+--------+")
        print("| GPIO1 input edge trigger      |   %d    |   %d    |" % (bool(buf1[4] & (1 << 1)), bool(buf2[4] & (1 << 1))))
        print("+-------------------------------+--------+--------+")
        print("| GPIO0 input edge trigger      |   %d    |   %d    |" % (bool(buf1[4] & (1 << 0)), bool(buf2[4] & (1 << 0))))
        print("+-------------------------------+--------+--------+")

    def irq(self, handler=None, trigger: int=None) -> None:
        channel = __irq_channel.get(trigger)
        if channel is None:
            return
        if handler is None:
            data = self.__read_byte(channel[0])
            data = data & (~(1 << channel[1]))
            self.__write_byte(channel[0], data)
        else:
            data = self.__read_byte(channel[0])
            data = data | (1 << channel[1])
            self.__write_byte(channel[0], data)
        self._handler_list[trigger] = handler

    @staticmethod
    def __handler_irq(self):
        print("__handler_irq")
        buf = bytearray(5)
        self._bus.readfrom_mem_into(self._address, AXP202_INTSTS1_REG, buf)
        data = buf[0] << 32 | \
               buf[1] << 24 | \
               buf[2] << 16 | \
               buf[3] << 8  | \
               buf[4]
        for i in range(0, 40):
            if data & (1 << (39 - i)) and self._handler_list[i] is not None:
                self._handler_list[i](self)
        for i in range(AXP202_INTSTS1_REG, AXP202_INTSTS5_REG + 1):
            self._bus.writeto_mem(self._address, i, b'\xFF')

    def __write_byte(self, reg, val):
        self._bytebuf[0] = val
        self._bus.writeto_mem(self._address, reg, self._bytebuf)

    def __read_byte(self, reg):
        self._bus.readfrom_mem_into(self._address, reg, self._bytebuf)
        return self._bytebuf[0]

    def __init_device(self):
        print('* initializing mpu')
        self._chip = self.__read_byte(AXP202_IC_TYPE_REG)
        if(self._chip == AXP202_CHIP_ID):
            print("Detect PMU Type is AXP202")
            self._chip = AXP202_CHIP_ID
        elif(self._chip == AXP192_CHIP_ID):
            print("Detect PMU Type is AXP192")
            self._chip = AXP192_CHIP_ID
        else:
            raise Exception("Invalid Chip ID!")

    def adc_enable(self, ch):
        '''
        AXP202_BATTERY_VOLTAGE_ADC      = _const(0)
        AXP202_BATTERY_CURRENT_ADC      = _const(1)
        AXP202_ACIN_VOLTAGE_ADC         = _const(2)
        AXP202_ACIN_CURRENT_ADC         = _const(3)
        AXP202_VBUS_VOLTAGE_ADC         = _const(4)
        AXP202_VBUS_CURRENT_ADC         = _const(5)
        AXP202_APS_VOLTAGE_ADC          = _const(6)
        AXP202_BATTERY_TEMPERATURE_ADC  = _const(7)
        AXP202_INTERNAL_TEMPERATURE_ADC = _const(8)
        AXP202_GPIO0_FUNC_ADC           = _const(9)
        AXP202_GPIO1_FUNC_ADC           = _const(10)
        '''
        val = __adc_channel.get(ch)
        if val is not None:
            data = self.__read_byte(val[0])
            data = data | (1 << val[1])
            self.__write_byte(val[0], data)

    def adc_disable(self, ch):
        val = __adc_channel.get(ch)
        if val is not None:
            data = self.__read_byte(val[0])
            data = data & (~(1 << val[1]))
            self.__write_byte(val[0], data)

    @property
    def acin_current(self) -> int:
        '''读取 ACIN 的电流'''
        self._bus.readfrom_mem_into(self._address, AXP202_ACIN_CUR_H8_REG, self._wordbuf)
        data = _unpack('>h', self._wordbuf)[0] >> 4
        return int(data * AXP202_ACIN_CUR_STEP)

    @property
    def acin_voltage(self) -> int:
        '''读取 ACIN 的电压'''
        self._bus.readfrom_mem_into(self._address, AXP202_ACIN_VOL_H8_REG, self._wordbuf)
        data = _unpack('>h', self._wordbuf)[0] >> 4
        return int(data * AXP202_ACIN_VOLTAGE_STEP)

    @property
    def vbus_voltage(self) -> int:
        '''读取 VBUS 的电压'''
        self._bus.readfrom_mem_into(self._address, AXP202_VBUS_VOL_H8_REG, self._wordbuf)
        data = _unpack('>H', self._wordbuf)[0] >> 4
        return int(data * AXP202_VBUS_VOLTAGE_STEP)

    @property
    def vbus_current(self) -> int:
        '''读取 VBUS 的电流'''
        self._bus.readfrom_mem_into(self._address, AXP202_VBUS_CUR_H8_REG, self._wordbuf)
        data = _unpack('>H', self._wordbuf)[0] >> 4
        return int(data * AXP202_VBUS_CUR_STEP)

    @property
    def temperature(self) -> float:
        '''芯片内部的温度'''
        self._bus.readfrom_mem_into(self._address, AXP202_INTERNAL_TEMP_H8_REG, self._wordbuf)
        data = _unpack('>H', self._wordbuf)[0] >> 4
        return (-144.7 + data * 0.1)

    @property
    def battery_temperature(self) -> float:
        '''电池的温度
        这是错误的
        '''
        self._bus.readfrom_mem_into(self._address, AXP202_TS_IN_H8_REG, self._wordbuf)
        data = _unpack('>H', self._wordbuf)[0] >> 4
        return data * AXP202_TS_PIN_OUT_STEP

    def getGPIO0Voltage(self) -> float:
        self._bus.readfrom_mem_into(self._address, AXP202_GPIO0_VOL_ADC_H8_REG, self._wordbuf)
        data = _unpack('>H', self._wordbuf)[0] >> 4
        return data * AXP202_GPIO0_STEP

    def getGPIO1Voltage(self) -> float:
        self._bus.readfrom_mem_into(self._address, AXP202_GPIO1_VOL_ADC_H8_REG, self._wordbuf)
        data = _unpack('>H', self._wordbuf)[0] >> 4
        return data * AXP202_GPIO1_STEP

    @property
    def battery_power(self) -> float:
        '''电池瞬时功率'''
        h8 = self.__read_byte(AXP202_BAT_POWERH8_REG)
        m8 = self.__read_byte(AXP202_BAT_POWERM8_REG)
        l8 = self.__read_byte(AXP202_BAT_POWERL8_REG)
        data = (h8 << 16) | (m8 << 8) | l8
        return (2 * data * 1.1 * 0.5 / 1000)

    @property
    def battery_voltage(self) -> int:
        '''读取电池电压'''
        self._bus.readfrom_mem_into(self._address, AXP202_BAT_AVERVOL_H8_REG, self._wordbuf)
        data = _unpack('>H', self._wordbuf)[0] >> 4
        return int(data * AXP202_BATT_VOLTAGE_STEP)

    @property
    def battery_charge_current(self) -> int:
        '''读取电池的充电电流'''
        self._bus.readfrom_mem_into(self._address, AXP202_BAT_AVERCHGCUR_H8_REG, self._wordbuf)
        data = _unpack('>H', self._wordbuf)[0] >> 4
        return int(data * AXP202_BATT_CHARGE_CUR_STEP)

    @property
    def battery_current(self) -> int:
        '''读取电池的电流'''
        self._bus.readfrom_mem_into(self._address, AXP202_BAT_AVERDISCHGCUR_H8_REG, self._wordbuf)
        data = _unpack('>H', self._wordbuf)[0] >> 3
        return int(data * AXP202_BATT_DISCHARGE_CUR_STEP)

    @property
    def ipsout_voltage(self) -> int:
        '''System IPSOUT voltage'''
        self._bus.readfrom_mem_into(self._address, AXP202_APS_AVERVOL_H8_REG, self._wordbuf)
        data = _unpack('>H', self._wordbuf)[0] >> 4
        return data

    def dump_adc(self):
        buf = bytearray(2)
        self._bus.readfrom_mem_into(self._address, AXP202_ADC_EN1_REG, buf)
        print("+--------------------+--------+-------+")
        print("| ADC Channel        | Enable | Value |")
        print("+====================+========+=======+")
        self._bus.readfrom_mem_into(self._address, AXP202_BAT_AVERVOL_H8_REG, self._wordbuf)
        data = _unpack('>H', self._wordbuf)[0] >> 4
        print("| Battery voltage    |   %d    | %04x  |" % (bool(buf[0] & (1 << 7)), data))
        print("+--------------------+--------+-------+")
        self._bus.readfrom_mem_into(self._address, AXP202_BAT_AVERCHGCUR_H8_REG, self._wordbuf)
        data = _unpack('>H', self._wordbuf)[0] >> 4
        print("| Battery current    |   %d    | %04x  |" % (bool(buf[0] & (1 << 6)), data))
        print("+--------------------+--------+-------+")
        self._bus.readfrom_mem_into(self._address, AXP202_ACIN_VOL_H8_REG, self._wordbuf)
        data = _unpack('>H', self._wordbuf)[0] >> 4
        print("| ACIN voltage       |   %d    | %04x  |" % (bool(buf[0] & (1 << 5)), data))
        print("+--------------------+--------+-------+")
        self._bus.readfrom_mem_into(self._address, AXP202_ACIN_CUR_H8_REG, self._wordbuf)
        data = _unpack('>H', self._wordbuf)[0] >> 4
        print("| ACIN current       |   %d    | %04x  |" % (bool(buf[0] & (1 << 4)), data))
        print("+--------------------+--------+-------+")
        self._bus.readfrom_mem_into(self._address, AXP202_VBUS_VOL_H8_REG, self._wordbuf)
        data = _unpack('>H', self._wordbuf)[0] >> 4
        print("| VBUS voltage       |   %d    | %04x  |" % (bool(buf[0] & (1 << 3)), data))
        print("+--------------------+--------+-------+")
        self._bus.readfrom_mem_into(self._address, AXP202_VBUS_CUR_H8_REG, self._wordbuf)
        data = _unpack('>H', self._wordbuf)[0] >> 4
        print("| VBUS current       |   %d    | %04x  |" % (bool(buf[0] & (1 << 2)), data))
        print("+--------------------+--------+-------+")
        self._bus.readfrom_mem_into(self._address, AXP202_APS_AVERVOL_H8_REG, self._wordbuf)
        data = _unpack('>H', self._wordbuf)[0] >> 4
        print("| APS voltage        |   %d    | %04x  |" % (bool(buf[0] & (1 << 1)), data))
        print("+--------------------+--------+-------+")
        self._bus.readfrom_mem_into(self._address, AXP202_TS_IN_H8_REG, self._wordbuf)
        data = _unpack('>H', self._wordbuf)[0] >> 4
        print("| TS temperature     |   %d    | %04x  |" % (bool(buf[0] & (1 << 0)), data))
        print("+--------------------+--------+-------+")
        self._bus.readfrom_mem_into(self._address, AXP202_INTERNAL_TEMP_H8_REG, self._wordbuf)
        data = _unpack('>H', self._wordbuf)[0] >> 4
        print("| AXP202 temperature |   %d    | %04x  |" % (bool(buf[1] & (1 << 7)), data))
        print("+--------------------+--------+-------+")
        self._bus.readfrom_mem_into(self._address, AXP202_GPIO0_VOL_ADC_H8_REG, self._wordbuf)
        data = _unpack('>H', self._wordbuf)[0] >> 4
        print("| GPIO0 ADC          |   %d    | %04x  |" % (bool(buf[1] & (1 << 3)), data))
        print("+--------------------+--------+-------+")
        self._bus.readfrom_mem_into(self._address, AXP202_GPIO1_VOL_ADC_H8_REG, self._wordbuf)
        data = _unpack('>H', self._wordbuf)[0] >> 4
        print("| GPIO1 ADC          |   %d    | %04x  |" % (bool(buf[1] & (1 << 3)), data))
        print("+--------------------+--------+-------+")

    def setStartupTime(self, val):
        startupParams = (
            0b00000000,
            0b01000000,
            0b10000000,
            0b11000000)
        if(val > AXP202_STARTUP_TIME_2S):
            return
        data = self.__read_byte(AXP202_POK_SET_REG)
        data = data & (~startupParams[3])
        data = data | startupParams[val]
        self.__write_byte(AXP202_POK_SET_REG, data)

    def setlongPressTime(self, val):
        longPressParams = (
            0b00000000,
            0b00010000,
            0b00100000,
            0b00110000)
        if(val > AXP202_LONGPRESS_TIME_2S5):
            return
        data = self.__read_byte(AXP202_POK_SET_REG)
        data = data & (~longPressParams[3])
        data = data | longPressParams[val]
        self.__write_byte(AXP202_POK_SET_REG, data)

    def setShutdownTime(self, val):
        shutdownParams = (
            0b00000000,
            0b00000001,
            0b00000010,
            0b00000011)
        if(val > AXP202_SHUTDOWN_TIME_10S):
            return
        data = self.__read_byte(AXP202_POK_SET_REG)
        data = data & (~shutdownParams[3])
        data = data | shutdownParams[val]
        self.__write_byte(AXP202_POK_SET_REG, data)

    def setTimeOutShutdown(self, en):
        data = self.__read_byte(AXP202_POK_SET_REG)
        if(en):
            data = data | (1 << 3)
        else:
            data = data | (~(1 << 3))
        self.__write_byte(AXP202_POK_SET_REG, data)

    def shutdown(self):
        '''disable the AXP202 output'''
        data = self.__read_byte(AXP202_OFF_CTL_REG)
        data = data | (1 << 7)
        self.__write_byte(AXP202_OFF_CTL_REG, data)


    '''Charging control'''
    def charging(self, en: bool | None = None) -> bool | None:
        data = self.__read_byte(AXP202_CHARGE1_REG)
        if en is None:
            return bool(data & (1 << 7))
        if en is True:
            data = data | (1 << 7)
            self.__write_byte(AXP202_CHARGE1_REG, data)
        if en is False:
            data = data & (~(1 << 7))
            self.__write_byte(AXP202_CHARGE1_REG, data)

    @property
    def charge_target_voltage(self) -> int:
        target_voltage = {
            0b00000000: 4100,
            0b00100000: 4150,
            0b01000000: 4200,
            0b01100000: 4360
        }
        data = self.__read_byte(AXP202_CHARGE1_REG)
        target_voltage.get(data & 0b01100000)

    @charge_target_voltage.setter
    def charge_target_voltage(self, val: int) -> int:
        target_voltage = {
            4100: 0b00000000,
            4150: 0b00100000,
            4200: 0b01000000,
            4360: 0b01100000
        }
        params = target_voltage.get(val)
        if params is not None:
            data = self.__read_byte(AXP202_CHARGE1_REG)
            data = data & 0b11001111
            data = data & params
            self.__write_byte(AXP202_CHARGE1_REG, data)

    @property
    def charge_target_current(self) -> int:
        data = self.__read_byte(AXP202_CHARGE1_REG)
        data = data & 0x0F
        return (300 + data * 100)

    @charge_target_current.setter
    def charge_target_current(self, val: int) -> None:
        target_current = (300, 400, 500, 600, 700, 800, 900, 1000, 1100, 1200,
            1300, 1400, 1500, 1600, 1700, 1800)
        try:
            target_current.index(val)
            data = self.__read_byte(AXP202_CHARGE1_REG)
            data &= 0xF0
            data &= int((val - 300) / 100)
            self.__write_byte(AXP202_CHARGE1_REG, data)
        except:
            return

    def chgled_mode(self, mode: int) -> None:
        '''
        ``CHGLED_ALWAYS_BRIGHT``: 0
        ``CHGLED_FLICKER``: 1
        '''
        data = self.__read_byte(AXP202_CHARGE2_REG)
        if mode == 0:
            data = data & (~(1 << 4))
            self.__write_byte(AXP202_CHARGE2_REG, data)
        if mode == 1:
            data = data | (1 << 4)
            self.__write_byte(AXP202_CHARGE2_REG, data)

    '''库仑计'''
    def getBattPercentage(self):
        data = self.__read_byte(AXP202_BATT_PERCENTAGE_REG)
        mask = data & (1 << 7)
        if(mask):
            return 0
        return data & (~(1 << 7))
