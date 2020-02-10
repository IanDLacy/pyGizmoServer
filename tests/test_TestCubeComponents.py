from TestCubeUSB.TestCubeComponents.actuators import *
from TestCubeUSB.TestCubeComponents.adc import *
from TestCubeUSB.TestCubeComponents.di import *
from TestCubeUSB.TestCubeComponents.frequency import *
from TestCubeUSB.TestCubeComponents.pwm import *
from TestCubeUSB.TestCubeComponents.relay import *
from TestCubeUSB.TestCubeComponents.usb import *
from TestCubeUSB.TestCubeComponents.version import *


def test_init():
    rm = RelayMessage()
    assert rm.get_relay_messages() == []


def test_relay0on():
    rm = RelayMessage()
    rm.setRelay(0, True)
    assert rm.get_relay_messages() == ["000000120101"]


def test_relay1on0off():
    rm = RelayMessage()
    assert rm.get_relay_messages() == []
    rm.setRelay(0, False)
    assert rm.get_relay_messages() == ["000000120100"]
    rm.setRelay(1, True)
    assert rm.get_relay_messages() == ["000000120302"]


def test_pwmfreq():
    pm = PwmMessage()
    assert pm.get_pwm_messages() == []
    pm.setPwmFrequencyA(100)
    assert pm.get_pwm_messages() == ["000000048000000000640000"]
    pm.setPwmFrequencyB(0x1234)
    assert pm.get_pwm_messages() == ["00000004c000000000641234"]


def test_pwmhiconf():
    pm = PwmMessage()
    pm.sethiconf(0, True)
    pm.sethiconf(8, False)
    assert pm.get_pwm_messages() == ["000000040101000100000000"]


def test_pwmduty():
    pm = PwmMessage()
    pm.setPwmDutyCycle(0, 50)
    pm.setPwmDutyCycle(4, 50)
    assert pm.get_pwm_messages() == ["000000060011320000003200"]
    pm.setPwmDutyCycle(6, 50)
    assert pm.get_pwm_messages() == [
        "000000060011320000003200",
        "000000060101320000000000",
    ]


def test_pwmenable():
    pm = PwmMessage()
    assert pm.get_pwm_messages() == []
    pm.setPwmEnabled(0, True)
    pm.setPwmEnabled(8, False)
    assert pm.get_pwm_messages() == ["0000000801010001"]


def test_dirate():
    dm = DiMessage()
    assert dm.get_di_messages() == []
    dm.setDiMonitorUpdateRate(1)
    assert dm.get_di_messages() == ["0000000a01"]


def test_actCur():
    am = ActCurMessage()
    am.setPwmCurrentMonitorUpdateRate(1)
    am.setPwmCurrentMonitorChannels(0x555)
    am.setPwmFaultThreshold(0x22)
    assert am.get_actcur_messages() == ["0000000c05550122"]


def test_sendUsbMsg():
    um = UsbMessage()
    um.sendrawusb("1234")
    assert um.get_sendusb_messages() == ["1234"]


def test_freq():
    fm = FrequencyMessage()
    fm.setFrequencyInputEnabled(0x5)
    fm.setFrequencyMonitorRate(0x1)
    assert fm.get_freq_messages() == ["0000000e0501"]


def test_adcrequest():
    am = AdcMessage()
    # am.setAdcEnabled(True,0x5)
    # default changed to all on
    am.setAdcMonitorUpdateRate(0x11 * 50)
    assert am.get_adc_messages() == ["000000103f11"]


def test_version():
    vm = VersionMessage()
    vm.ask = True
    vm.get_version_messages()
    assert vm.get_version_messages() == ["00000040"]
