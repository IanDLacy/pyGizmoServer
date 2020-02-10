import usb.core
from usb.backend import libusb1
import usb.util
import time, threading, time, logging
import asyncio, json
from TestCubeUSB.TestCubeComponents.adc import AdcMessage
from TestCubeUSB.TestCubeComponents.pwm import PwmMessage
from TestCubeUSB.TestCubeComponents.relay import RelayMessage
from TestCubeUSB.TestCubeComponents.di import DiMessage
from TestCubeUSB.TestCubeComponents.actuators import ActCurMessage
from TestCubeUSB.TestCubeComponents.frequency import FrequencyMessage
from TestCubeUSB.TestCubeComponents.usb import UsbMessage
from TestCubeUSB.TestCubeComponents.can import CanDatabaseMessage

class TestCubeUSB(
    RelayMessage,
    PwmMessage,
    DiMessage,
    ActCurMessage,
    UsbMessage,
    FrequencyMessage,
    AdcMessage,
    CanDatabaseMessage
    ):
    
    def callParentInits(self):
        RelayMessage.__init__(self)
        PwmMessage.__init__(self)
        DiMessage.__init__(self)
        ActCurMessage.__init__(self)
        UsbMessage.__init__(self)
        FrequencyMessage.__init__(self)
        
    
    def __init__(self,):
        self.logger = logging.getLogger('gizmoLogger')
        self.logger.debug("TescubeUSB()")
        self.callParentInits()
        self.callback = None
        self.version = None
        self.ask = None
        AdcMessage.__init__(self)
        self.usbidparsers = {
            '00000005':self.recusb_5_pwmfreq,
            '00000007':self.recusb_7_pwmdutycycle,
            '00000009':self.recusb_9_pwmenable,
            '0000000b':self.recusb_b_digitalinputs,
            '0000000d':self.recusb_00d_actcurrent,
            '0000010d':self.recusb_10d_actcurrent,
            '0000020d':self.recusb_20d_actcurrent,
            '0000030d':self.recusb_30d_actcurrent,
            '0000000f':self.recusb_00f_speed,
            '0000010f':self.recusb_10f_speed,
            '00000011':self.recusb_011_adc,
            '00000111':self.recusb_111_adc,
            '00000211':self.recusb_211_adc,
            '00000013':self.recusb_13_relay,
            '0000001d':self.recusb_1d_actfault,
            '00000041':self.recusb_41_version,
        }
        self.actcurrent_listinfirstmsg = None
        self.adc_listinfirstmsg = []
        with open("TestCubeUSB/schema.json") as f:
            self.schema = json.load(f)

    def setcallback(self, callback):
        if not callable(callback):
            raise ValueError("callback must be a function")
        self.callback = callback

    def start(self):
        if self.callback is None:
            raise RuntimeError('controller callback not set')
        self.dev = usb.core.find(idVendor=0x2B87,idProduct=0x0001)
        if self.dev is None:
            raise ValueError('Device not found')

    def finished(self):
        self.logger.debug(f"TescubeUSB.finished")
        msgs = (self.get_relay_messages()
            + self.get_pwm_messages()
            + self.get_di_messages()
            + self.get_actcur_messages()
            + self.get_sendusb_messages()
            + self.get_freq_messages()
            + self.get_adc_messages()
            + self.get_version_messages()
        )
        for msg in msgs:
            self.logger.debug(f"TescubeUSB.finished: write({msg})")
            self.dev.write(2, msg)
        self.callParentInits()
    
    async def listen(self):
        await self.usbrxhandler()

    async def usbrxhandler(self):
        self.logger.debug("TescubeUSB.usbrxhandler")
        while 1: 
            await asyncio.sleep(0.001)
            try:
                msg = self.dev.read(130,24,100)
            except usb.core.USBError as e:
                if "time" not in str(e):
                    self.logger.error(f"ERROR: {e}")
                continue
            msg = ''.join([chr(x) for x in msg])
            d = self.recUsb(msg)
            if len(d) > 0:
                await self.callback(d)
            
    def recUsb(self,msg):
        _id, payload = msg[:8], msg[8:]
        try:
            f = self.usbidparsers.get(_id)
            if f is None:
                self.logger.error(f"TescubeUSB: ID not found in {self.usbidparsers}")
                return []
        except Exception as e:
            self.logger.error(f"ERROR: {e}")
        result = f(payload)
        return result

    def recusb_5_pwmfreq(self,payload):
        acthi,freqa,freqb = payload[:4],payload[4:8],payload[8:12]
        #self.logger.debug(acthi,freqa,freqb)
        d = []
        path = '/pwmController/bankA/frequency'
        data = int(freqa,16)
        d.append({'path':path,'data':data})
        path = '/pwmController/bankB/frequency'
        data = int(freqb,16)
        d.append({'path':path,'data':data})
        path = '/pwmController/pwms'
        data = [{'activeConfiguration':"high"} if (int(acthi,16) & (1<<x)) else {'activeConfiguration':"low"} for x in range(12)]
        d.append({'path':path,'data':data})
        return d
    def recusb_7_pwmdutycycle(self,payload):
        ret = [{}]*12
        bank,mo,dcf,dce,dcd,dcc,dcb,dca = (
            int(payload[:2],16),
            int(payload[2:4],16),
            int(payload[4:6],16),
            int(payload[6:8],16),
            int(payload[8:10],16),
            int(payload[10:12],16),
            int(payload[12:14],16),
            int(payload[14:16],16)
        )
        ret[6*bank+0] = {'dutyCycle': dca}
        ret[6*bank+1] = {'dutyCycle': dcb}
        ret[6*bank+2] = {'dutyCycle': dcc}
        ret[6*bank+3] = {'dutyCycle': dcd}
        ret[6*bank+4] = {'dutyCycle': dce}
        ret[6*bank+5] = {'dutyCycle': dcf}
        path = '/pwmController/pwms'
        return [{'path': path, 'data': ret}]

    def recusb_9_pwmenable(self,payload):
        d = []
        enabled = int(payload[:4],16)
        data = [{'enabled': True} if (enabled & (1<<x)) else {'enabled': False} for x in range(12)]
        path = '/pwmController/pwms'
        d.append({'path':path,'data':data})
        return d

    def recusb_b_digitalinputs(self,payload):
        d = []
        high = int(payload[:4],16)
        data = [{'high': True} if (high & (1<<x)) else {'high': False} for x in range(12)]
        path = '/digitalInputController/digitalInputs'
        d.append({'path':path,'data':data})
        return d        

    def recusb_00d_actcurrent(self,payload):
        ret = [{}]*12
        payload = payload + "0"*16  #pad to avoid errors
        channels,cc,cb,ca = (
            int(payload[:4],16),
            int(payload[4:8],16),
            int(payload[8:12],16),
            int(payload[12:16],16)
        )
        #this first msg defines which channels are in subsequent msgs
        self.actcurrent_listinfirstmsg = [i for i in [11,10,9,8,7,6,5,4,3,2,1,0] if (channels & (1<<(i)))]
        thismsg = self.actcurrent_listinfirstmsg[0:3]
        
        for ch,v in zip(thismsg,[cc,cb,ca]):
            if isinstance(ch,int):
                ret[ch] = {'currentMonitor':{'measuredCurrent': v}}
        path = '/pwmController/pwms'
        return [{'path': path, 'data': ret}]                

    def recusb_10d_actcurrent(self,payload):
        ret = [{}]*12
        payload = payload + "0"*16  #pad to avoid errors
        cd,cc,cb,ca = (
            int(payload[:4],16),
            int(payload[4:8],16),
            int(payload[8:12],16),
            int(payload[12:16],16)
        )        
        thismsg = self.actcurrent_listinfirstmsg[3:7]
        for ch,v in zip(thismsg,[cd,cc,cb,ca]):
            if isinstance(ch,int):
                ret[ch] = {'currentMonitor':{'measuredCurrent': v}}
        path = '/pwmController/pwms'
        return [{'path': path, 'data': ret}]        

    def recusb_20d_actcurrent(self,payload):
        ret = [{}]*12
        payload = payload + "0"*16  #pad to avoid errors
        cd,cc,cb,ca = (
            int(payload[:4],16),
            int(payload[4:8],16),
            int(payload[8:12],16),
            int(payload[12:16],16)
        )        
        thismsg = self.actcurrent_listinfirstmsg[7:11]
        for ch,v in zip(thismsg,[cd,cc,cb,ca]):
            if isinstance(ch,int):
                ret[ch] = {'currentMonitor':{'measuredCurrent': v}}
        path = '/pwmController/pwms'
        return [{'path': path, 'data': ret}]                
   
    def recusb_30d_actcurrent(self,payload):
        ret = [{}]*12
        payload = payload + "0"*16  #pad to avoid errors
        cd = (
            int(payload[:4],16),
        )        
        thismsg = self.actcurrent_listinfirstmsg[12:]
        for ch,v in zip(thismsg,[cd]):
            if isinstance(ch,int):
                ret[ch] = {'currentMonitor':{'measuredCurrent': v}}
        path = '/pwmController/pwms'
        return [{'path': path, 'data': ret}]                

    def recusb_00f_speed(self,payload):
        ret = [{}]*4
        payload = payload + "0"*16  #pad to avoid errors
        channels,cc,cb,ca = (
            int(payload[:4],16),
            int(payload[4:8],16),
            int(payload[8:12],16),
            int(payload[12:16],16)
        )
        #this first msg defines which channels are in subsequent msgs
        self.speed_listinfirstmsg = [i for i in [3,2,1,0] if (channels & (1<<(i)))]
        thismsg = self.speed_listinfirstmsg[0:3]
        
        for ch,v in zip(thismsg,[cc,cb,ca]):
            if isinstance(ch,int):
                ret[ch] = {'measuredFrequency': v}
        path = '/frequencyInputController/frequencyInputs'
        return [{'path': path, 'data': ret}]                
        

    def recusb_10f_speed(self,payload):
        ret = [{}]*4
        payload = payload + "0"*16  #pad to avoid errors
        cd = int(payload[:4],16)

        thismsg = self.speed_listinfirstmsg[3:]
        
        for ch,v in zip(thismsg,[cd]):
            if isinstance(ch,int):
                ret[ch] = {'measuredFrequency': v}
        path = '/frequencyInputController/frequencyInputs'
        return [{'path': path, 'data': ret}]               
        
    def recusb_011_adc(self,payload):
        ret = [{}]*8
        payload = payload + "0"*16  #pad to avoid errors
        channels,cc,cb,ca = (
            int(payload[:4],16),
            int(payload[4:8],16),
            int(payload[8:12],16),
            int(payload[12:16],16)
        )
        #this first msg defines which channels are in subsequent msgs
        self.adc_listinfirstmsg = [i for i in [7,6,5,4,3,2,1,0] if (channels & (1<<(i)))]
        thismsg = self.adc_listinfirstmsg[0:3]
        
        for ch,v in zip(thismsg,[cc,cb,ca]):
            if isinstance(ch,int):
                ret[ch] = {'measuredVoltage': v}
        path = '/adcInputController/adcInputs'
        return [{'path': path, 'data': ret}]         
        
    def recusb_111_adc(self,payload):
        ret = [{}]*8
        payload = payload + "0"*16  #pad to avoid errors
        cd,cc,cb,ca = (
            int(payload[:4],16),
            int(payload[4:8],16),
            int(payload[8:12],16),
            int(payload[12:16],16)
        )
        #this first msg defines which channels are in subsequent msgs
        thismsg = self.adc_listinfirstmsg[3:7]
        
        for ch,v in zip(thismsg,[cd,cc,cb,ca]):
            if isinstance(ch,int):
                ret[ch] = {'measuredVoltage': v}
        path = '/adcInputController/adcInputs'
        return [{'path': path, 'data': ret}]
            
    def recusb_211_adc(self,payload):
        ret = [{}]*8
        payload = payload + "0"*16  #pad to avoid errors
        cd,cc,cb,ca = (
            int(payload[:4],16),
            int(payload[4:8],16),
            int(payload[8:12],16),
            int(payload[12:16],16)
        )
        #this first msg defines which channels are in subsequent msgs
        thismsg = self.adc_listinfirstmsg[7:]
        
        for ch,v in zip(thismsg,[cd,cc,cb,ca]):
            if isinstance(ch,int):
                ret[ch] = {'measuredVoltage': v}
        path = '/adcInputController/adcInputs'
        return [{'path': path, 'data': ret}]        
    
    def recusb_13_relay(self,payload):
        enabled = (
            int(payload[:2],16)
        )
        data = [{'enabled': True} if (enabled & (1<<x)) else {'enabled': False} for x in range(6)]

        path = '/relayController/relays'
        return [{'path': path, 'data': data}]

    def recusb_1d_actfault(self,payload):
        sync,faults = (
            int(payload[:1],16),
            int(payload[1:4],16)
        )
        data = [{'currentMonitor':{'faulty': True}} if (faults & (1<<x)) else {'currentMonitor':{'faulty': False}} for x in range(12)]

        path = '/pwmController/pwms'
        return [{'path': path, 'data': data}]  
                      
    def recusb_41_version(self,payload):
        print("GOTIT")
        hi,lo,patch = (
            int(payload[:4],16),
            int(payload[4:8],16),
            int(payload[8:12],16)
        )
        self.version = f"{hi}.{lo}.{patch}"
        data = self.version

        path = '/version'
        return [{'path': path, 'data': data}]

    async def getFirmwareVersion(self):
        self.ask = True
        data = await self.wait_for_version()
        path = '/version'
        return [{'path': path, 'data': data}]

    def get_version_messages(self):
        if self.ask == None:
            return []
        return [f"{0x40:08x}"]

    async def wait_for_version(self):
        while self.version is None:
            await asyncio.sleep(1)
        return self.version