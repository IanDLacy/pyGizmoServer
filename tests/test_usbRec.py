from controllers.testcube_usb_controller import *
from pyGizmoServer.utility import Utility
from tests.mock_variables import MockVars

class Test_usbRec():

    def checkmatch(self,md,pd,loc):

        if isinstance(md,list):
            idx=0
            for m,p in zip(md,pd):
                self.checkmatch(m,p,loc + f'[{idx}]')
                idx = idx + 1
        elif isinstance(md,dict):       
            for k,v in pd.items(): #the model can have more stuff than in the usb msg
                assert(k in md.keys()),f"usb parse to place not in model {loc=}/{k} {idx=}"
                self.checkmatch(md[k],v,loc + '/' + k)
        else:
            assert(md == pd),f"{loc=}"

    def processandcheck(self,msg):
        d = self.controller.recUsb(msg)
    
        for pd in d:
            results = Utility.parse_path_against_schema_and_model(path=pd['path'],schema=self.mockvars.mock_schema,model=self.mockvars.mock_model)
            self.checkmatch(results['model_data'],pd['data'],pd['path'])


    def setup(self):
        self.mockvars = MockVars()
        self.controller=TestCubeUSB()
        pass

    def test_usbmsg5(self): #pwm act and freq
        id,acthi,freqa,freqb = 0x5,0x555,0x1000,0xfff
        msg = f'{id:08x}{acthi:04x}{freqa:04x}{freqb:04x}'
        self.processandcheck(msg) 

    def test_usbmsg7(self):
        id,bank,mod,dcf,dce,dcd,dcc,dcb,dca = 7,0,0x3f,6,5,4,3,2,1
        msg = f"{id:08x}{bank:02x}{mod:02x}{dcf:02x}{dce:02x}{dcd:02x}{dcc:02x}{dcb:02x}{dca:02x}"       
        self.processandcheck(msg)
  
        id,bank,mod,dcf,dce,dcd,dcc,dcb,dca = 7,0x1,0x3f,12,11,10,9,8,7
        msg = f"{id:08x}{bank:02x}{mod:02x}{dcf:02x}{dce:02x}{dcd:02x}{dcc:02x}{dcb:02x}{dca:02x}"
        self.processandcheck(msg)

    def test_usbmsg9(self):
        id,enablemask = 9,0x555  
        msg = f"{id:08x}{enablemask:04x}"
        self.processandcheck(msg)

    def test_usbmsgb(self):
        id,di = 0xb,0x555
        msg = f"{id:08x}{di:04x}"
        self.processandcheck(msg)

    def test_usbmsgd(self): #act curr
        
        id,mask,a12,a11,a10 = 0xd,0xf0f,12,11,10
        msg = f"{id:08x}{mask:04x}{a12:04x}{a11:04x}{a10:04x}"
        self.processandcheck(msg)

        id,a9,a4,a3,a2 = 0x10d,9,4,3,2
        msg = f"{id:08x}{a9:04x}{a4:04x}{a3:04x}{a2:04x}"
        self.processandcheck(msg)        

        id,a1 = 0x20d,1
        msg = f"{id:08x}{a1:04x}"
        self.processandcheck(msg)  

    def test_usbmsgf(self): #speed
        id,mask,f4,f3,f2 = 0xf,0xf,4,3,2
        msg = f"{id:08x}{mask:04x}{f4:04x}{f3:04x}{f2:04x}"
        self.processandcheck(msg)
        
        id,f1 = 0x10f,1
        msg = f"{id:08x}{f1:04x}"
        self.processandcheck(msg)

    def test_usbmsg11(self): #adc
    
        id,mask,a8,a7,a6 = 0x11,0xff,8,7,6
        msg = f"{id:08x}{mask:04x}{a8:04x}{a7:04x}{a6:04x}"
        self.processandcheck(msg)

        id,a5,a4,a3,a2 = 0x111,5,4,3,2
        msg = f"{id:08x}{a5:04x}{a4:04x}{a3:04x}{a2:04x}"
        self.processandcheck(msg)

        id,a1 = 0x211,1
        msg = f"{id:08x}{a1:04x}"
        self.processandcheck(msg)

    def test_usbmsg13(self): #relay
        id,relays = 0x13,0x11
        msg = f"{id:08x}{relays:02x}"
        self.processandcheck(msg)

    def test_usbmsg1d(self): #act fault
        id,sync,faults = 0x1d,0,0x555
        msg = f"{id:08x}{sync:01x}{faults:03x}"
        self.processandcheck(msg)

    def test_usbmsg41(self): #version
        id,hi,lo,patch = 0x41,0xb,0xa,0xd
        msg = f"{id:08x}{hi:04x}{lo:04x}{patch:04x}"
        self.processandcheck(msg)
