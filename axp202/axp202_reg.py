
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
    from micropython import const as const
except:
    def const(expr):
        return expr

# Chip Address
AXP202_SLAVE_ADDRESS = const(0x35)

# Chip ID
AXP202_CHIP_ID = const(0x41)
AXP192_CHIP_ID = const(0x03)

# REG MAP
# Group 1: Power Control
'''Power status register'''
AXP202_STATUS_REG          = const(0x00)
'''Power mode/ charge state register'''
AXP202_MODE_CHGSTATUS_REG  = const(0x01)
'''OTG VBUS state register'''
AXP202_OTG_STATUS_REG      = const(0x02)
AXP202_IC_TYPE_REG         = const(0x03)
'''Data buffer register'''
AXP202_DATA_BUFFER1_REG    = const(0x04)
AXP202_DATA_BUFFER2_REG    = const(0x05)
AXP202_DATA_BUFFER3_REG    = const(0x06)
AXP202_DATA_BUFFER4_REG    = const(0x07)
AXP202_DATA_BUFFER5_REG    = const(0x08)
AXP202_DATA_BUFFER6_REG    = const(0x09)
AXP202_DATA_BUFFER7_REG    = const(0x0A)
AXP202_DATA_BUFFER8_REG    = const(0x0B)
AXP202_DATA_BUFFER9_REG    = const(0x0C)
AXP202_DATA_BUFFERA_REG    = const(0x0D)
AXP202_DATA_BUFFERB_REG    = const(0x0E)
AXP202_DATA_BUFFERC_REG    = const(0x0F)
'''DC-DC2/3 & LDO2/3/4&EXTEN control register'''
AXP202_LDO234_DC23_CTL_REG = const(0x12)
'''DC-DC2 voltage setting register'''
AXP202_DC2OUT_VOL_REG      = const(0x23)
'''DC-DC2/LDO3 voltage ramp parameter setting register'''
AXP202_LDO3_DC2_DVM_REG    = const(0x25)
'''DC-DC3 voltage setting register'''
AXP202_DC3OUT_VOL_REG      = const(0x27)
'''LDO2/3 voltage setting register'''
AXP202_LDO24OUT_VOL_REG    = const(0x28)
AXP202_LDO3OUT_VOL_REG     = const(0x29)
'''VBUS-IPSOUT channel setting register'''
AXP202_IPS_SET_REG         = const(0x30)
'''VOFF shutdown voltage setting register'''
AXP202_VOFF_SET_REG        = const(0x31)
'''Shutdown, battery detection, CHGLED control register'''
AXP202_OFF_CTL_REG         = const(0x32)
AXP202_CHARGE1_REG         = const(0x33)
AXP202_CHARGE2_REG         = const(0x34)
AXP202_BACKUP_CHG_REG      = const(0x35)
AXP202_POK_SET_REG         = const(0x36)
AXP202_DCDC_FREQSET_REG    = const(0x37)
AXP202_VLTF_CHGSET_REG     = const(0x38)
AXP202_VHTF_CHGSET_REG     = const(0x39)
AXP202_APS_WARNING1_REG    = const(0x3A)
AXP202_APS_WARNING2_REG    = const(0x3B)
AXP202_TLTF_DISCHGSET_REG  = const(0x3C)
AXP202_THTF_DISCHGSET_REG  = const(0x3D)
AXP202_DCDC_MODESET_REG    = const(0x80)
AXP202_ADC_EN1_REG         = const(0x82)
AXP202_ADC_EN2_REG         = const(0x83)
AXP202_ADC_SPEED_REG       = const(0x84)
AXP202_ADC_INPUTRANGE_REG  = const(0x85)
AXP202_ADC_IRQ_RETFSET_REG = const(0x86)
AXP202_ADC_IRQ_FETFSET_REG = const(0x87)
AXP202_TIMER_CTL_REG       = const(0x8A)
AXP202_VBUS_DET_SRP_REG    = const(0x8B)
AXP202_HOTOVER_CTL_REG     = const(0x8F)

# Group 2 GPIO control
AXP202_GPIO0_CTL_REG      = const(0x90)
AXP202_GPIO0_VOL_REG      = const(0x91)
AXP202_GPIO1_CTL_REG      = const(0x92)
AXP202_GPIO2_CTL_REG      = const(0x93)
AXP202_GPIO012_SIGNAL_REG = const(0x94)
AXP202_GPIO3_CTL_REG      = const(0x95)

# Group3 Interrupt control
AXP202_INTEN1_REG  = const(0x40)
AXP202_INTEN2_REG  = const(0x41)
AXP202_INTEN3_REG  = const(0x42)
AXP202_INTEN4_REG  = const(0x43)
AXP202_INTEN5_REG  = const(0x44)
AXP202_INTSTS1_REG = const(0x48)
AXP202_INTSTS2_REG = const(0x49)
AXP202_INTSTS3_REG = const(0x4A)
AXP202_INTSTS4_REG = const(0x4B)
AXP202_INTSTS5_REG = const(0x4C)

# Group4 ADC data
AXP202_ACIN_VOL_H8_REG          = const(0x56)
AXP202_ACIN_VOL_L4_REG          = const(0x57)
AXP202_ACIN_CUR_H8_REG          = const(0x58)
AXP202_ACIN_CUR_L4_REG          = const(0x59)
AXP202_VBUS_VOL_H8_REG          = const(0x5A)
AXP202_VBUS_VOL_L4_REG          = const(0x5B)
AXP202_VBUS_CUR_H8_REG          = const(0x5C)
AXP202_VBUS_CUR_L4_REG          = const(0x5D)
AXP202_INTERNAL_TEMP_H8_REG     = const(0x5E)
AXP202_INTERNAL_TEMP_L4_REG     = const(0x5F)
AXP202_TS_IN_H8_REG             = const(0x62)
AXP202_TS_IN_L4_REG             = const(0x63)
AXP202_GPIO0_VOL_ADC_H8_REG     = const(0x64)
AXP202_GPIO0_VOL_ADC_L4_REG     = const(0x65)
AXP202_GPIO1_VOL_ADC_H8_REG     = const(0x66)
AXP202_GPIO1_VOL_ADC_L4_REG     = const(0x67)
AXP202_BAT_POWERH8_REG          = const(0x70)
AXP202_BAT_POWERM8_REG          = const(0x71)
AXP202_BAT_POWERL8_REG          = const(0x72)
AXP202_BAT_AVERVOL_H8_REG       = const(0x78)
AXP202_BAT_AVERVOL_L4_REG       = const(0x79)
AXP202_BAT_AVERCHGCUR_H8_REG    = const(0x7A)
AXP202_BAT_AVERCHGCUR_L4_REG    = const(0x7B)
AXP202_BAT_AVERDISCHGCUR_H8_REG = const(0x7C)
AXP202_BAT_AVERDISCHGCUR_L5_REG = const(0x7D)
AXP202_APS_AVERVOL_H8_REG       = const(0x7E)
AXP202_APS_AVERVOL_L4_REG       = const(0x7F)
AXP202_BAT_CHGCOULOMB3_REG      = const(0xB0)
AXP202_BAT_CHGCOULOMB2_REG      = const(0xB1)
AXP202_BAT_CHGCOULOMB1_REG      = const(0xB2)
AXP202_BAT_CHGCOULOMB0_REG      = const(0xB3)
AXP202_BAT_DISCHGCOULOMB3_REG   = const(0xB4)
AXP202_BAT_DISCHGCOULOMB2_REG   = const(0xB5)
AXP202_BAT_DISCHGCOULOMB1_REG   = const(0xB6)
AXP202_BAT_DISCHGCOULOMB0_REG   = const(0xB7)
AXP202_COULOMB_CTL_REG          = const(0xB8)
AXP202_BATT_PERCENTAGE_REG      = const(0xB9)

# unknown register
'''
AXP202_BAT_VOL_H8           = 0x50
AXP202_BAT_VOL_L4           = 0x51
AXP202_INT_BAT_CHGCUR_H8    = 0xA0
AXP202_INT_BAT_CHGCUR_L4    = 0xA1
AXP202_EXT_BAT_CHGCUR_H8    = 0xA2
AXP202_EXT_BAT_CHGCUR_L4    = 0xA3
AXP202_INT_BAT_DISCHGCUR_H8 = 0xA4
AXP202_INT_BAT_DISCHGCUR_L4 = 0xA5
AXP202_EXT_BAT_DISCHGCUR_H8 = 0xA6
AXP202_EXT_BAT_DISCHGCUR_L4 = 0xA7
AXP202_VREF_TEM_CTRL        = 0xF3
'''

# AXP202   bit definitions for AXP events irq event
AXP202_IRQ_USBLO = 1
AXP202_IRQ_USBRE = 2
AXP202_IRQ_USBIN = 3
AXP202_IRQ_USBOV = 4
AXP202_IRQ_ACRE  = 5
AXP202_IRQ_ACIN  = 6
AXP202_IRQ_ACOV  = 7

AXP202_IRQ_TEMLO   = 8
AXP202_IRQ_TEMOV   = 9
AXP202_IRQ_CHAOV   = 10
AXP202_IRQ_CHAST   = 11
AXP202_IRQ_BATATOU = 12
AXP202_IRQ_BATATIN = 13
AXP202_IRQ_BATRE   = 14
AXP202_IRQ_BATIN   = 15

AXP202_IRQ_POKLO    = 16
AXP202_IRQ_POKSH    = 17
AXP202_IRQ_LDO3LO   = 18
AXP202_IRQ_DCDC3LO  = 19
AXP202_IRQ_DCDC2LO  = 20
AXP202_IRQ_CHACURLO = 22
AXP202_IRQ_ICTEMOV  = 23

AXP202_IRQ_EXTLOWARN2    = 24
AXP202_IRQ_EXTLOWARN1    = 25
AXP202_IRQ_SESSION_END   = 26
AXP202_IRQ_SESS_AB_VALID = 27
AXP202_IRQ_VBUS_UN_VALID = 28
AXP202_IRQ_VBUS_VALID    = 29
AXP202_IRQ_PDOWN_BY_NOE  = 30
AXP202_IRQ_PUP_BY_NOE    = 31

AXP202_IRQ_GPIO0TG = 32
AXP202_IRQ_GPIO1TG = 33
AXP202_IRQ_GPIO2TG = 34
AXP202_IRQ_GPIO3TG = 35
AXP202_IRQ_PEKFE   = 37
AXP202_IRQ_PEKRE   = 38
AXP202_IRQ_TIMER   = 39


# Signal Capture
AXP202_BATT_VOLTAGE_STEP       = 1.1
AXP202_BATT_DISCHARGE_CUR_STEP = 0.5
AXP202_BATT_CHARGE_CUR_STEP    = 0.5
AXP202_ACIN_VOLTAGE_STEP       = 1.7
AXP202_ACIN_CUR_STEP           = 0.625
AXP202_VBUS_VOLTAGE_STEP       = 1.7
AXP202_VBUS_CUR_STEP           = 0.375
AXP202_INTENAL_TEMP_STEP       = 0.1
AXP202_APS_VOLTAGE_STEP        = 1.4
AXP202_TS_PIN_OUT_STEP         = 0.8
AXP202_GPIO0_STEP              = 0.5
AXP202_GPIO1_STEP              = 0.5

# axp202 power channel
CH_EXTEN = const(0)
CH_DCDC2 = const(1)
CH_DCDC3 = const(2)
CH_LDO2  = const(3)
CH_LDO4  = const(4)
CH_LDO3  = const(5)


# axp202 adc1 args
AXP202_BATTERY_VOLTAGE_ADC     = const(0)
AXP202_BATTERY_CURRENT_ADC     = const(1)
AXP202_ACIN_VOLTAGE_ADC        = const(2)
AXP202_ACIN_CURRENT_ADC        = const(3)
AXP202_VBUS_VOLTAGE_ADC        = const(4)
AXP202_VBUS_CURRENT_ADC        = const(5)
AXP202_APS_VOLTAGE_ADC         = const(6)
AXP202_BATTERY_TEMPERATURE_ADC = const(7)

# axp202 adc2 args
AXP202_INTERNAL_TEMPERATURE_ADC = const(8)
AXP202_GPIO0_FUNC_ADC           = const(9)
AXP202_GPIO1_FUNC_ADC           = const(10)


# AXP202 IRQ1
AXP202_VBUS_VHOLD_LOW_IRQ = 1 << 1
AXP202_VBUS_REMOVED_IRQ   = 1 << 2
AXP202_VBUS_CONNECT_IRQ   = 1 << 3
AXP202_VBUS_OVER_VOL_IRQ  = 1 << 4
AXP202_ACIN_REMOVED_IRQ   = 1 << 5
AXP202_ACIN_CONNECT_IRQ   = 1 << 6
AXP202_ACIN_OVER_VOL_IRQ  = 1 << 7

# AXP202 IRQ2
AXP202_BATT_LOW_TEMP_IRQ      = 1 << 8
AXP202_BATT_OVER_TEMP_IRQ     = 1 << 9
AXP202_CHARGING_FINISHED_IRQ  = 1 << 10
AXP202_CHARGING_IRQ           = 1 << 11
AXP202_BATT_EXIT_ACTIVATE_IRQ = 1 << 12
AXP202_BATT_ACTIVATE_IRQ      = 1 << 13
AXP202_BATT_REMOVED_IRQ       = 1 << 14
AXP202_BATT_CONNECT_IRQ       = 1 << 15

# AXP202 IRQ3
AXP202_PEK_LONGPRESS_IRQ  = 1 << 16
AXP202_PEK_SHORTPRESS_IRQ = 1 << 17
AXP202_LDO3_LOW_VOL_IRQ   = 1 << 18
AXP202_DC3_LOW_VOL_IRQ    = 1 << 19
AXP202_DC2_LOW_VOL_IRQ    = 1 << 20
AXP202_CHARGE_LOW_CUR_IRQ = 1 << 21
AXP202_CHIP_TEMP_HIGH_IRQ = 1 << 22

# AXP202 IRQ4
AXP202_APS_LOW_VOL_LEVEL2_IRQ = 1 << 24
APX202_APS_LOW_VOL_LEVEL1_IRQ = 1 << 25
AXP202_VBUS_SESSION_END_IRQ   = 1 << 26
AXP202_VBUS_SESSION_AB_IRQ    = 1 << 27
AXP202_VBUS_INVALID_IRQ       = 1 << 28
AXP202_VBUS_VAILD_IRQ         = 1 << 29
AXP202_NOE_OFF_IRQ            = 1 << 30
AXP202_NOE_ON_IRQ             = 1 << 31

# AXP202 IRQ5
AXP202_GPIO0_EDGE_TRIGGER_IRQ = 1 << 32
AXP202_GPIO1_EDGE_TRIGGER_IRQ = 1 << 33
AXP202_GPIO2_EDGE_TRIGGER_IRQ = 1 << 34
AXP202_GPIO3_EDGE_TRIGGER_IRQ = 1 << 35

# Reserved and unchangeable BIT 4
AXP202_PEK_FALLING_EDGE_IRQ   = 1 << 37
AXP202_PEK_RISING_EDGE_IRQ    = 1 << 38
AXP202_TIMER_TIMEOUT_IRQ      = 1 << 39

AXP202_ALL_IRQ = 0xFFFFFFFFFF


# AXP202 LDO3 Mode
AXP202_LDO3_LDO_MODE  = 0
AXP202_LDO3_DCIN_MODE = 1

# AXP202 LDO4 voltage setting args
AXP202_LDO4_1250MV = 0
AXP202_LDO4_1300MV = 1
AXP202_LDO4_1400MV = 2
AXP202_LDO4_1500MV = 3
AXP202_LDO4_1600MV = 4
AXP202_LDO4_1700MV = 5
AXP202_LDO4_1800MV = 6
AXP202_LDO4_1900MV = 7
AXP202_LDO4_2000MV = 8
AXP202_LDO4_2500MV = 9
AXP202_LDO4_2700MV = 10
AXP202_LDO4_2800MV = 11
AXP202_LDO4_3000MV = 12
AXP202_LDO4_3100MV = 13
AXP202_LDO4_3200MV = 14
AXP202_LDO4_3300MV = 15


# Boot time setting
AXP202_STARTUP_TIME_128MS = 0
AXP202_STARTUP_TIME_3S    = 1
AXP202_STARTUP_TIME_1S    = 2
AXP202_STARTUP_TIME_2S    = 3


# Long button time setting
AXP202_LONGPRESS_TIME_1S  = 0
AXP202_LONGPRESS_TIME_1S5 = 1
AXP202_LONGPRESS_TIME_2S  = 2
AXP202_LONGPRESS_TIME_2S5 = 3


# Shutdown duration setting
AXP202_SHUTDOWN_TIME_4S  = 0
AXP202_SHUTDOWN_TIME_6S  = 1
AXP202_SHUTDOWN_TIME_8S  = 2
AXP202_SHUTDOWN_TIME_10S = 3


# REG 33H: Charging control 1 Charging target-voltage setting
AXP202_TARGET_VOL_4_1V  = 0
AXP202_TARGET_VOL_4_15V = 1
AXP202_TARGET_VOL_4_2V  = 2
AXP202_TARGET_VOL_4_36V = 3

# AXP202 LED CONTROL
AXP20X_LED_OFF       = 0
AXP20X_LED_BLINK_1HZ = 1
AXP20X_LED_BLINK_4HZ = 2
AXP20X_LED_LOW_LEVEL = 3

AXP202_LDO5_1800MV = 0
AXP202_LDO5_2500MV = 1
AXP202_LDO5_2800MV = 2
AXP202_LDO5_3000MV = 3
AXP202_LDO5_3100MV = 4
AXP202_LDO5_3300MV = 5
AXP202_LDO5_3400MV = 6
AXP202_LDO5_3500MV = 7

# LDO3 OUTPUT MODE
AXP202_LDO3_MODE_LDO  = 0
AXP202_LDO3_MODE_DCIN = 1

AXP_POWER_OFF_TIME_4S  = 0
AXP_POWER_OFF_TIME_65  = 1
AXP_POWER_OFF_TIME_8S  = 2
AXP_POWER_OFF_TIME_16S = 3

AXP_LONGPRESS_TIME_1S  = 0
AXP_LONGPRESS_TIME_1S5 = 1
AXP_LONGPRESS_TIME_2S  = 2
AXP_LONGPRESS_TIME_2S5 = 3

AXP202_STARTUP_TIME_128MS = 0
AXP202_STARTUP_TIME_3S    = 1
AXP202_STARTUP_TIME_1S    = 2
AXP202_STARTUP_TIME_2S    = 3
