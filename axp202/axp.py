
try:
    from struct import unpack as _unpack
except:
    from ustruct import unpack as _unpack

from .axp202_reg import *

_default_pin_scl = 22
_default_pin_sda = 21
_default_pin_intr = 35
_default_chip_type = AXP202_CHIP_ID


class AXP(object):
    def __init__(self, i2c: I2C, address: int = AXP202_SLAVE_ADDRESS, intr: Pin = None) -> None:
        self._intr = intr
        self._chip = AXP202_CHIP_ID
        self._address = address
        self._bus = i2c

        self._buffer = bytearray(16)
        self._bytebuf = memoryview(self._buffer[0:1])
        self._wordbuf = memoryview(self._buffer[0:2])
        self._irqbuf = memoryview(self._buffer[0:5])

        self._init_device()

    def write_byte(self, reg, val):
        self._bytebuf[0] = val
        self._bus.writeto_mem(self._address, reg, self._bytebuf)

    def read_byte(self, reg):
        self._bus.readfrom_mem_into(self._address, reg, self._bytebuf)
        return self._bytebuf[0]

    def read_word(self, reg):
        self._bus.readfrom_mem_into(self._address, reg, self._wordbuf)
        return _unpack('>H', self._wordbuf)[0]

    def read_word2(self, reg):
        self._bus.readfrom_mem_into(self._address, reg, self._wordbuf)
        return _unpack('>h', self._wordbuf)[0]

    def _init_device(self):
        print('* initializing mpu')
        self._chip = self.read_byte(AXP202_IC_TYPE_REG)
        if(self._chip == AXP202_CHIP_ID):
            print("Detect PMU Type is AXP202")
            self._chip = AXP202_CHIP_ID
        elif(self._chip == AXP192_CHIP_ID):
            print("Detect PMU Type is AXP192")
            self._chip = AXP192_CHIP_ID
        else:
            raise Exception("Invalid Chip ID!")

    def enablePower(self, ch):
        data = self.read_byte(AXP202_LDO234_DC23_CTL_REG)
        data = data | (1 << ch)
        self.write_byte(AXP202_LDO234_DC23_CTL_REG, data)

    def disablePower(self, ch):
        data = self.read_byte(AXP202_LDO234_DC23_CTL_REG)
        data = data & (~(1 << ch))
        self.write_byte(AXP202_LDO234_DC23_CTL_REG, data)

    def __BIT_MASK(self, mask):
        return 1 << mask

    def __get_h8_l5(self, regh8, regl5):
        hv = self.read_byte(regh8)
        lv = self.read_byte(regl5)
        return (hv << 5) | (lv & 0x1F)

    def __get_h8_l4(self, regh8, regl5):
        hv = self.read_byte(regh8)
        lv = self.read_byte(regl5)
        return (hv << 4) | (lv & 0xF)

    def isChargeing(self):
        data = self.read_byte(AXP202_MODE_CHGSTATUS_REG)
        return data & self.__BIT_MASK(6)

    def isBatteryConnect(self):
        data = self.read_byte(AXP202_MODE_CHGSTATUS_REG)
        return data & self.__BIT_MASK(5)

    def getAcinCurrent(self):
        data = self.__get_h8_l4(AXP202_ACIN_CUR_H8_REG, AXP202_ACIN_CUR_L4_REG)
        return data * AXP202_ACIN_CUR_STEP

    def getAcinVoltage(self):
        data = self.__get_h8_l4(AXP202_ACIN_VOL_H8_REG, AXP202_ACIN_VOL_L4_REG)
        return data * AXP202_ACIN_VOLTAGE_STEP

    def getVbusVoltage(self):
        data = self.__get_h8_l4(AXP202_VBUS_VOL_H8_REG, AXP202_VBUS_VOL_L4_REG)
        return data * AXP202_VBUS_VOLTAGE_STEP

    def getVbusCurrent(self):
        data = self.__get_h8_l4(AXP202_VBUS_CUR_H8_REG, AXP202_VBUS_CUR_L4_REG)
        return data * AXP202_VBUS_CUR_STEP

    def getTemp(self):
        hv = self.read_byte(AXP202_INTERNAL_TEMP_H8_REG)
        lv = self.read_byte(AXP202_INTERNAL_TEMP_L4_REG)
        data = (hv << 8) | (lv & 0xF)
        return data / 1000

    def getTSTemp(self):
        data = self.__get_h8_l4(AXP202_TS_IN_H8_REG, AXP202_TS_IN_L4_REG)
        return data * AXP202_TS_PIN_OUT_STEP

    def getGPIO0Voltage(self):
        data = self.__get_h8_l4(AXP202_GPIO0_VOL_ADC_H8_REG,
                                AXP202_GPIO0_VOL_ADC_L4_REG)
        return data * AXP202_GPIO0_STEP

    def getGPIO1Voltage(self):
        data = self.__get_h8_l4(AXP202_GPIO1_VOL_ADC_H8_REG,
                                AXP202_GPIO1_VOL_ADC_L4_REG)
        return data * AXP202_GPIO1_STEP

    def getBattInpower(self):
        h8 = self.read_byte(AXP202_BAT_POWERH8_REG)
        m8 = self.read_byte(AXP202_BAT_POWERM8_REG)
        l8 = self.read_byte(AXP202_BAT_POWERL8_REG)
        data = (h8 << 16) | (m8 << 8) | l8
        return 2 * data * 1.1 * 0.5 / 1000

    def getBattVoltage(self):
        data = self.__get_h8_l4(AXP202_BAT_AVERVOL_H8_REG, AXP202_BAT_AVERVOL_L4_REG)
        return data * AXP202_BATT_VOLTAGE_STEP

    def getBattChargeCurrent(self):
        data = 0
        if(self._chip == AXP202_CHIP_ID):
            data = self.__get_h8_l4(AXP202_BAT_AVERCHGCUR_H8_REG, AXP202_BAT_AVERCHGCUR_L4_REG) * AXP202_BATT_CHARGE_CUR_STEP
        elif (self._chip == AXP192_CHIP_ID):
            data = self.__get_h8_l5(AXP202_BAT_AVERCHGCUR_H8_REG, AXP202_BAT_AVERCHGCUR_L4_REG) * AXP202_BATT_CHARGE_CUR_STEP
        return data

    def getBattDischargeCurrent(self):
        data = self.__get_h8_l4(
            AXP202_BAT_AVERDISCHGCUR_H8_REG, AXP202_BAT_AVERDISCHGCUR_L5_REG) * AXP202_BATT_DISCHARGE_CUR_STEP
        return data

    def getSysIPSOUTVoltage(self):
        hv = self.read_byte(AXP202_APS_AVERVOL_H8_REG)
        lv = self.read_byte(AXP202_APS_AVERVOL_L4_REG)
        data = (hv << 4) | (lv & 0xF)
        return data

    def enableADC(self, ch, val):
        if(ch == 1):
            data = self.read_byte(AXP202_ADC_EN1_REG)
            data = data | (1 << val)
            self.write_byte(AXP202_ADC_EN1_REG, data)
        elif(ch == 2):
            data = self.read_byte(AXP202_ADC_EN2_REG)
            data = data | (1 << val)
            self.write_byte(AXP202_ADC_EN1_REG, data)
        else:
            return

    def disableADC(self, ch, val):
        if(ch == 1):
            data = self.read_byte(AXP202_ADC_EN1_REG)
            data = data & (~(1 << val))
            self.write_byte(AXP202_ADC_EN1_REG, data)
        elif(ch == 2):
            data = self.read_byte(AXP202_ADC_EN2_REG)
            data = data & (~(1 << val))
            self.write_byte(AXP202_ADC_EN1_REG, data)
        else:
            return

    def enableIRQ(self, val):
        if(val & 0xFF):
            data = self.read_byte(AXP202_INTEN1_REG)
            data = data | (val & 0xFF)
            self.write_byte(AXP202_INTEN1_REG, data)

        if(val & 0xFF00):
            data = self.read_byte(AXP202_INTEN2_REG)
            data = data | (val >> 8)
            self.write_byte(AXP202_INTEN2_REG, data)

        if(val & 0xFF0000):
            data = self.read_byte(AXP202_INTEN3_REG)
            data = data | (val >> 16)
            self.write_byte(AXP202_INTEN3_REG, data)

        if(val & 0xFF000000):
            data = self.read_byte(AXP202_INTEN4_REG)
            data = data | (val >> 24)
            self.write_byte(AXP202_INTEN4_REG, data)

    def disableIRQ(self, val):
        if(val & 0xFF):
            data = self.read_byte(AXP202_INTEN1_REG)
            data = data & (~(val & 0xFF))
            self.write_byte(AXP202_INTEN1_REG, data)

        if(val & 0xFF00):
            data = self.read_byte(AXP202_INTEN2_REG)
            data = data & (~(val >> 8))
            self.write_byte(AXP202_INTEN2_REG, data)

        if(val & 0xFF0000):
            data = self.read_byte(AXP202_INTEN3_REG)
            data = data & (~(val >> 16))
            self.write_byte(AXP202_INTEN3_REG, data)

        if(val & 0xFF000000):
            data = self.read_byte(AXP202_INTEN4_REG)
            data = data & (~(val >> 24))
            self.write_byte(AXP202_INTEN4_REG, data)
        pass

    def readIRQ(self):
        if(self._chip == AXP202_CHIP_ID):
            for i in range(5):
                self._irqbuf[i] = self.read_byte(AXP202_INTSTS1_REG + i)
        elif(self._chip == AXP192_CHIP_ID):
            for i in range(4):
                self._irqbuf[i] = self.read_byte(AXP192_INTSTS1 + i)
            self._irqbuf[4] = self.read_byte(AXP192_INTSTS5)

    def clearIRQ(self):
        if(self._chip == AXP202_CHIP_ID):
            for i in range(5):
                self.write_byte(AXP202_INTSTS1_REG + i, 0xFF)
                self._irqbuf[i] = 0
        elif(self._chip == AXP192_CHIP_ID):
            for i in range(4):
                self.write_byte(AXP192_INTSTS1 + i, 0xFF)
            self.write_byte(AXP192_INTSTS5, 0xFF)

    def isVBUSPlug(self):
        data = self.read_byte(AXP202_STATUS_REG)
        return data & self.__BIT_MASK(5)

    # Only can set axp192
    def setDC1Voltage(self, mv):
        if(self._chip != AXP192_CHIP_ID):
            return
        if(mv < 700):
            mv = 700
        elif(mv > 3500):
            mv = 3500
        val = (mv - 700) / 25
        self.write_byte(AXP192_DC1_VLOTAGE, int(val))

    def setDC2Voltage(self, mv):
        if(mv < 700):
            mv = 700
        elif(mv > 2275):
            mv = 2275
        val = (mv - 700) / 25
        self.write_byte(AXP202_DC2OUT_VOL_REG, int(val))

    def setDC3Voltage(self, mv):
        if(mv < 700):
            mv = 700
        elif(mv > 3500):
            mv = 3500
        val = (mv - 700) / 25
        self.write_byte(AXP202_DC3OUT_VOL_REG, int(val))

    def setLDO2Voltage(self, mv):
        if(mv < 1800):
            mv = 1800
        elif(mv > 3300):
            mv = 3300
        val = (mv - 1800) / 100
        prev = self.read_byte(AXP202_LDO24OUT_VOL_REG)
        prev &= 0x0F
        prev = prev | (int(val) << 4)
        self.write_byte(AXP202_LDO24OUT_VOL_REG, int(prev))

    def setLDO3Voltage(self, mv):
        if self._chip == AXP202_CHIP_ID and mv < 700:
            mv = 700
        elif self._chip == AXP192_CHIP_ID and mv < 1800:
            mv = 1800

        if self._chip == AXP202_CHIP_ID and mv > 3500:
            mv = 3500
        elif self._chip == AXP192_CHIP_ID and mv > 3300:
            mv = 3300

        if self._chip == AXP202_CHIP_ID:
            val = (mv - 700) / 25
            prev = self.read_byte(AXP202_LDO3OUT_VOL_REG)
            prev &= 0x80
            prev = prev | int(val)
            self.write_byte(AXP202_LDO3OUT_VOL_REG, int(prev))
            # self.write_byte(AXP202_LDO3OUT_VOL, int(val))
        elif self._chip == AXP192_CHIP_ID:
            val = (mv - 1800) / 100
            prev = self.read_byte(AXP192_LDO23OUT_VOL)
            prev &= 0xF0
            prev = prev | int(val)
            self.write_byte(AXP192_LDO23OUT_VOL, int(prev))

    def setLDO4Voltage(self, arg):
        if self._chip == AXP202_CHIP_ID and arg <= AXP202_LDO4_3300MV:
            data = self.read_byte(AXP202_LDO24OUT_VOL_REG)
            data = data & 0xF0
            data = data | arg
            self.write_byte(AXP202_LDO24OUT_VOL_REG, data)

    def setLDO3Mode(self, mode):
        if(mode > AXP202_LDO3_DCIN_MODE):
            return
        data = self.read_byte(AXP202_LDO3OUT_VOL_REG)
        if(mode):
            data = data | self.__BIT_MASK(7)
        else:
            data = data & (~self.__BIT_MASK(7))
        self.write_byte(AXP202_LDO3OUT_VOL_REG, data)

    def setStartupTime(self, val):
        startupParams = (
            0b00000000,
            0b01000000,
            0b10000000,
            0b11000000)
        if(val > AXP202_STARTUP_TIME_2S):
            return
        data = self.read_byte(AXP202_POK_SET_REG)
        data = data & (~startupParams[3])
        data = data | startupParams[val]
        self.write_byte(AXP202_POK_SET_REG, data)

    def setlongPressTime(self, val):
        longPressParams = (
            0b00000000,
            0b00010000,
            0b00100000,
            0b00110000)
        if(val > AXP202_LONGPRESS_TIME_2S5):
            return
        data = self.read_byte(AXP202_POK_SET_REG)
        data = data & (~longPressParams[3])
        data = data | longPressParams[val]
        self.write_byte(AXP202_POK_SET_REG, data)

    def setShutdownTime(self, val):
        shutdownParams = (
            0b00000000,
            0b00000001,
            0b00000010,
            0b00000011)
        if(val > AXP202_SHUTDOWN_TIME_10S):
            return
        data = self.read_byte(AXP202_POK_SET_REG)
        data = data & (~shutdownParams[3])
        data = data | shutdownParams[val]
        self.write_byte(AXP202_POK_SET_REG, data)

    def setTimeOutShutdown(self, en):
        data = self.read_byte(AXP202_POK_SET_REG)
        if(en):
            data = data | self.__BIT_MASK(3)
        else:
            data = data | (~self.__BIT_MASK(3))
        self.write_byte(AXP202_POK_SET_REG, data)

    def shutdown(self):
        data = self.read_byte(AXP202_OFF_CTL_REG)
        data = data | self.__BIT_MASK(7)
        self.write_byte(AXP202_OFF_CTL_REG, data)

    def getSettingChargeCurrent(self):
        data = self.read_byte(AXP202_CHARGE1_REG)
        data = data & 0b00000111
        curr = 300 + data * 100
        return curr

    def isChargeingEnable(self):
        data = self.read_byte(AXP202_CHARGE1_REG)
        if(data & self.__BIT_MASK(7)):
            return True
        return False

    def enableChargeing(self):
        data = self.read_byte(AXP202_CHARGE1_REG)
        data = data | self.__BIT_MASK(7)
        self.write_byte(AXP202_CHARGE1_REG, data)

    def setChargingTargetVoltage(self, val):
        targetVolParams = (
            0b00000000,
            0b00100000,
            0b01000000,
            0b01100000)
        if(val > AXP202_TARGET_VOL_4_36V):
            return
        data = self.read_byte(AXP202_CHARGE1_REG)
        data = data & (~targetVolParams[3])
        data = data | targetVolParams[val]
        self.write_byte(AXP202_CHARGE1_REG, data)

    def getBattPercentage(self):
        data = self.read_byte(AXP202_BATT_PERCENTAGE_REG)
        mask = data & self.__BIT_MASK(7)
        if(mask):
            return 0
        return data & (~self.__BIT_MASK(7))

    def setChgLEDChgControl(self):
        data = self.read_byte(AXP202_OFF_CTL_REG)
        data = data & 0b111110111
        self.write_byte(AXP202_OFF_CTL_REG, data)

    def setChgLEDMode(self, mode):
        data = self.read_byte(AXP202_OFF_CTL_REG)
        data |= self.__BIT_MASK(3)
        if(mode == AXP20X_LED_OFF):
            data = data & 0b11001111
        elif(mode == AXP20X_LED_BLINK_1HZ):
            data = data & 0b11001111
            data = data | 0b00010000
        elif(mode == AXP20X_LED_BLINK_4HZ):
            data = data & 0b11001111
            data = data | 0b00100000
        elif(mode == AXP20X_LED_LOW_LEVEL):
            data = data & 0b11001111
            data = data | 0b00110000
        self.write_byte(AXP202_OFF_CTL_REG, data)
