# -*- coding: utf-8 -*-
"""
Created on Mon Sep  9 12:02:44 2024

@author: Yann Parot
"""

#Enumérations
from enum import Enum

class Z_IN(Enum):
    Z_1MEG = 1e6
    Z_50 = 50
    
class ACQ_MODE(Enum):
    SAMPLE = "SAMple"
    PEAKDETECT ="PEAKdetect"
    HIRES = "HIRes"
    AVERAGE = "AVErage"
    ENVELOPE = "ENVelope"
    
class EXTREM_VAL(Enum):
    MAX_BW = 1e9 #Hz
    MIN_BW = 20e6 #Hz
    MAX_SCALE = 1 #V/div
    MIN_SCALE = 1e-3 #V/div
    HDIV = 10 #div
    VDIV = 10 #div
    NBCHAN  = 4
    
class MEAS_TYPE(Enum):
    ACCOMMONMODE='ACCOMMONMODE'
    ACPRACRMS='ACPRACRMS'
    AMPLITUDE='AMPLITUDE'
    AREA='AREA'
    BASE='BASE'
    BITAMPLITUDE='BITAMPLITUDE'
    BITHIGH='BITHIGH'
    BITLOW='BITLOW'
    BURSTWIDTH='BURSTWIDTH'
    CCJITTER='CCJITTER'
    COMMONMODE='COMMONMODE'
    CPOWER='CPOWER'
    DATARATE='DATARATE'
    DCD='DCD'
    DDJ='DDJ'
    DDRAOS='DDRAOS'
    DDRAOSPERUI='DDRAOSPERUI'
    DDRAUS='DDRAUS'
    DDRAUSPERTCK='DDRAUSPERTCK'
    DDRAUSPERUI='DDRAUSPERUI'
    DDRHOLDDIFF='DDRHOLDDIFF'
    DDRSETUPDIFF='DDRSETUPDIFF'
    DDRTCHABS='DDRTCHABS'
    DDRTCLABS='DDRTCLABS'
    DDRTCLAVERAGE='DDRTCLAVERAGE'
    DDRTERRMN='DDRTERRMN'
    DDRTERRN='DDRTERRN'
    DDRTJITCC='DDRTJITCC'
    DDRTJITDUTY='DDRTJITDUTY'
    DDRTJITPER='DDRTJITPER'
    DDRTPST='DDRTPST'
    DDRTRPRE='DDRTRPRE'
    DDRTWPRE='DDRTWPRE'
    DDRVIXAC='DDRVIXAC'
    DDRTDQSCK='DDRTDQSCK'
    DELAY='DELAY'
    DJ='DJ'
    DJDIRAC='DJDIRAC'
    DPMPSIJ='DPMPSIJ'
    EYEHIGH='EYEHIGH'
    EYELOW='EYELOW'
    FALLSLEWRATE='FALLSLEWRATE'
    FALLTIME='FALLTIME'
    FREQUENCY='FREQUENCY'
    F2='F2'
    F4='F4'
    F8='F8'
    HEIGHT='HEIGHT'
    HEIGHTBER='HEIGHTBER'
    HIGH='HIGH'
    HIGHTIME='HIGHTIME'
    HOLD='HOLD'
    IMDAANGLE='IMDAANGLE'
    IMDADIRECTION='IMDADIRECTION'
    IMDADQ0='IMDADQ0'
    IMDAEFFICIENCY='IMDAEFFICIENCY'
    IMDAHARMONICS='IMDAHARMONICS'
    IMDAMECHPWR='IMDAMECHPWR'
    IMDAPOWERQUALITY='IMDAPOWERQUALITY'
    IMDASPEED='IMDASPEED'
    IMDASYSEFF='IMDASYSEFF'
    IMDATORQUE='IMDATORQUE'
    JITTERSUMMARY='JITTERSUMMARY'
    J2='J2'
    J9='J9'
    LOW='LOW'
    LOWTIME='LOWTIME'
    MAXIMUM='MAXIMUM'
    MEAN='MEAN'
    MINIMUM='MINIMUM'
    NDUty='NDUty'
    NOVERSHOOT='NOVERSHOOT'
    NPERIOD='NPERIOD'
    NPJ='NPJ'
    NWIDTH='NWIDTH'
    OBW='OBW'
    PDUTY='PDUTY'
    PERIOD='PERIOD'
    PHASE='PHASE'
    PHASENOISE='PHASENOISE'
    PJ='PJ'
    PK2Pk='PK2Pk'
    POVERSHOOT='POVERSHOOT'
    PWIDTH='PWIDTH'
    QFACTOR='QFACTOR'
    RISESLEWRATE='RISESLEWRATE'
    RISETIME='RISETIME'
    RJ='RJ'
    RJDIRAC='RJDIRAC'
    RMS='RMS'
    SETUP='SETUP'
    SKEW='SKEW'
    SRJ='SRJ'
    SSCFREQDEV='SSCFREQDEV'
    SSCMODRATE='SSCMODRATE'
    TIE='TIE'
    TIMEOUTSIDELEVEL='TIMEOUTSIDELEVEL'
    TIMETOMAX='TIMETOMAX'
    TIMETOMIN='TIMETOMIN'
    TJBER='TJBER'
    TNTRATIO='TNTRATIO'
    TOP='TOP'
    UNITINTERVAL='UNITINTERVAL'
    VDIFFXOVR='VDIFFXOVR'
    WBGDDT='WBGDDT'
    WBGDIODEDDT='WBGDIODEDDT'
    WBGEOFF='WBGEOFF'
    WBGEON='WBGEON'
    WBGERR='WBGERR'
    WBGIPEAK='WBGIPEAK'
    WBGIRRM='WBGIRRM'
    WBGQOSS='WBGQOSS'
    WBGQRR='WBGQRR'
    WBGTDOFF='WBGTDOFF'
    WBGTDON='WBGTDON'
    WBGTF='WBGTF'
    WBGTON='WBGTON'
    WBGTOFF='WBGTOFF'
    WBGTR='WBGTR'
    WBGTRR='WBGTRR'
    WBGTDT='WBGTDT'
    WBGVPEAK='WBGVPEAK'
    WIDTH='WIDTH'
    WIDTHBER='WIDTHBER'


#Classe principale
import socket

class OscClient:
    
    def __init__(self,IPaddress="10.120.1.86",Port=4000):      
        self._IPaddress = ""
        self._Port = 0
        self._Socket = 0        
        self._BufferLength=4096
        
        self.IPaddress=IPaddress
        self.Port=Port
        
#getters et setters        
    @property
    def IPaddress(self):
        return self._IPaddress
    
    @IPaddress.setter
    def IPaddress(self,IPaddress):
        if not isinstance(IPaddress, str):
            print('Adresse IP invalide: n\'est pas un str')
            return
        self._IPaddress = IPaddress
    
    
    @property
    def Port(self):
        return self._Port
    
    @Port.setter
    def Port(self,Port):
        if not isinstance(Port, int):
            print('Port invalide: n\'est pas un int')
            return
        self._Port = Port
        
    @property
    def Connection(self):
        return self._Socket
    
    @property
    def BufferLength(self):
        return self._BufferLength
    
    @BufferLength.setter
    def BufferLength(self,BufferLength):
        if not isinstance(BufferLength, int):
            print('Erreur: n\'est pas un int')
            return
        
        if BufferLength%2 != 0:
            print('Erreur: n\'est pas une puissance de 2')
            return
        
        self._BufferLength = BufferLength
        
    def SetTimeOut(self,timeout):
        if not isinstance(timeout, float):
            print('Erreur: n\'est pas de type float')
            return
        self._Socket.settimeout(timeout)
        
#Commandes basiques    
    def OpenCom(self):
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        s.settimeout(10.0) #timeout general à 10 secondes
        s.connect((self._IPaddress,self._Port))
        self._Socket = s
        return s #permet l'utilisation de context manager with closing
    
        
    def CloseCom(self):
        self._Socket.close()
        
    def Command(self,command):
        return self._Socket.send(f'{command}\n'.encode())
        
    def Query(self,Query):
        self._Socket.send(f'{Query}\n'.encode())
        data = self._Socket.recv(self._BufferLength) #A tuner en fonction de la datasheet oscillo
        return data.decode()

        
    def ClearOutputQueue(self):
        self.Command("DCL\n") #Device Clear Function (Pas utile car l'oscillo fait un clear à chaque requête/commande)

        
#Commandes avancées classiques

#Acquisition

    def SetAcqMode(self,Mode=ACQ_MODE.SAMPLE):
        self.Command(f"ACQuire:MODe {Mode.value}")
        
    def GetAcqMode(self):
        return self.Query("ACQuire:MODe")
    
    def RunAcq(self):
        self.Command("ACQuire:STATE RUN")
        
    def StopAcq(self):
        self.Command("ACQuire:STATE STOP")  
        
    def GetNAcq(self):
        data = self.Query("ACQuire:NUMACq?")
        if data.strip():
            return int(data.strip())
        else:
            return 0
        
    def WaitForAnAcquisition(self):
        n_acq = 0
        self.RunAcq()
        while n_acq == 0:
            n_acq = self.GetNAcq()
            
        self.StopAcq()

#Horizontal

    def SetManualHorizontalMode(self,manual=True):
        if manual:
            mode="MANual"
        else:
            mode="AUTO"
        self.Command(f"HORizontal:MODe {mode}")

    def AdjustRLWhenSRMove(self,status=False):
        if status:
            mode = "RECORDLength"
        else:
            mode = "HORIZontalscale"
        
        self.Command(f"HORIZONTAL:MODE:MANUAL:CONFIGURE {mode}")

    def SetSampleRate(self,SR):
        self.Command(f"HORizontal:MODe:SAMPLERate {SR}")
        
    def GetSampleRate(self):
        data = self.Query("HORizontal:MODe:SAMPLERate?")
        return float(data.strip())
        
    def SetRecordLength(self,RL):
        self.Command(f"HORizontal:RECOrdlength {RL}")
        
    def GetRecordLength(self):
        data = self.Query("HORizontal:RECOrdlength?")
        return float(data.strip())
    
#Vertical

    def IsClipping(self,Channel=1):
        data = self.Query(f"CH{Channel}:CLIPping?")
        return bool(int(data))
    
    def SetScale(self,Channel=1,Scale=EXTREM_VAL.MAX_SCALE.value):
        self.Command(f"CH{Channel}:Scale {Scale}")
        
    def GetScale(self,Channel=1):
        data = self.Query(f"CH{Channel}:Scale?")
        return float(data.strip())
    
    def SetPosition(self,Channel=1,Position=0.0): #Position est en nombre de divisions
        self.Command(f"CH{Channel}:POSition {Position}")
        
    def GetPosition(self,Channel=1):
        data = self.Query(f"CH{Channel}:POSition?")
        return float(data.strip())
        
#Channel

    def SetBandwidth(self,Channel=1,BW=EXTREM_VAL.MAX_BW.value):
        self.Command(f"CH{Channel}:BANdwidth {BW}")
        
    def GetBandwidth(self,Channel=1):
        data = self.Query(f"CH{Channel}:BANdwidth?")
        return float(data.strip()) 
    
    def SetLabel(self,Channel=1,Label="No Label"):
        self.Command(f"CH{Channel}:LABel:NAMe \"{Label}\"")
        
    def GetLabel(self,Channel=1):
        return self.Query(f"CH{Channel}:LABel:NAMe?")
    
    def SetInputZ(self,Channel=1,InputZ=Z_IN.Z_50):
        if not isinstance(InputZ,Z_IN):
            print("Erreur: Veuillez passer par la classe d'enumeration Z_IN")
            return
        self.Command(f"CH{Channel}:TERmination {InputZ.value}")
        
    def GetInputZ(self,Channel=1):
        data = self.Query(f"CH{Channel}:TERmination?")
        return float(data.strip())
    
    def SetChannelState(self,Channel=1,State=True): #1 = ON 0=Off
        self.Command(f"SELect:CH{Channel} {int(State)}")
        
    def IsChannelActive(self,Channel=1):
        data = self.Query(f"SELect:CH{Channel}")
        return bool(int(data.strip()))
    
    def GetAllChannelState(self):
        ch_state=[]
        for i in range(1,EXTREM_VAL.NBCHAN.value+1):
            ch_state.append(self.IsChannelActive(i))
        return ch_state
    
    def SetAllChannelState(self,ch_state=[True,False,False,False]):
        if len(ch_state)==0:
            return
        if len(ch_state)>EXTREM_VAL.NBCHAN.value:
            print("Trop de channels dans la liste")
            return
        if not isinstance(ch_state, list):
            print("L'argument n'est pas une liste")
            return
        if not all([isinstance(elm,bool) for elm in ch_state]):
            print("Au moins un des éléments de la liste n'est pas de type bool")
            return
        for i,state in enumerate(ch_state):
            self.SetChannelState(i+1,state)
        


#File
    def GetCurrentWorkingDirectory(self):
        return self.Query("FILESystem:CWD?")
    
    def SetCurrentWorkingDirectory(self,path=".\\"):
        self.Command(f"FILESystem:CWD {path}")
         
    def SaveWaveformAsCSV(self,Channel=1,filepath="",filename="temp"):
        self.Command(f"SAVE:WAVEFORM CH{Channel},\"{filepath}\\{filename}.csv\"")
        
    def SaveAllWaveformsAsCSV(self,filepath="",filename="temp"):
        self.Command(f"SAVE:WAVEFORM ALL,\"{filepath}/{filename}.csv\"")
        

#Measurements
    def GetMeasurementsList(self):
        data=self.Query("MEASUrement:LIST?")
        if (data.strip()).upper()=="NONE":
            return []
        else:
            return (data.strip()).split(",")
        
    def AddNewMeasurement(self,MeasType=MEAS_TYPE.MAXIMUM):
        self.Command(f"MEASUREMENT:ADDMEAS {MeasType.value}")
        
    def AddNewMeasurementAtIndex(self,Channel=1,MeasID=1,MeasType=MEAS_TYPE.MAXIMUM):
        #Création de la mesure
        self.Command(f"MEASUrement:MEAS{MeasID}:TYPe {MeasType.value}")
        #Application au channel
        self.Command(f"MEASUrement:MEAS<x>:SOUrce CH{Channel}")
        
    
    def DeleteMeasurement(self,MeasID=1):
        self.Command(f"MEASUREMENT:DELETE \"MEAS{MeasID}\"")
        
    def GetMeasurementMeanValue(self,MeasID=1):
        data =self.Query(f"MEASUrement:MEAS{MeasID}:RESUlts:CURRentacq:MEAN?")
        return float(data.strip())

#Autoscale

    def VerticalAutoScale(self,Channel=1):
        
        #Réglage de l'oscilloscope sur la bande max, en Highres pour avoir les 12 bits et Scale max
        self.SetChannelState(Channel,True)
        self.SetAcqMode(ACQ_MODE.HIRES)
        self.SetBandwidth(Channel,BW=EXTREM_VAL.MAX_BW.value)
        self.SetScale(Channel,EXTREM_VAL.MAX_SCALE.value)
        self.SetPosition(Channel,0)
        
        #Sauvegarde des paramètres
        old_SR = self.GetSampleRate()
        old_RL = self.GetRecordLength()
        
        #mesure sur une bande de fs durant 1s
        fs=100e6
        self.SetSampleRate(2*fs)
        SR_set =self.GetSampleRate()
        self.SetRecordLength(1/(SR_set))
        
        #Ajout de la mesure
        last_meas_index = int((self.GetMeasurementsList()[-1].strip())[-1])
        self.AddNewMeasurementAtIndex(Channel,last_meas_index+1,MEAS_TYPE.MAXIMUM)
        self.AddNewMeasurementAtIndex(Channel,last_meas_index+2,MEAS_TYPE.MINIMUM)
        
        
        
        print("Attente d'une acquisition pour le clipping et pre-scaling")
        self.WaitForAnAcquisition()
        
        #Si il y a du clipping on ne peut rien faire
        if self.IsClipping(Channel):
            print("Le signal en entrée est trop fort")
            return
                 
        #Pré-réglage
        
        #Recupération mesure
        max_val = self.GetMeasurementMeanValue(last_meas_index+1)
        min_val = self.GetMeasurementMeanValue(last_meas_index+2)
        
        
        amplitude = max_val - min_val
        offset = (max_val + min_val)/2
        
        if amplitude == 0:
            print("Amplitude mesuré égale à zéro")
            self.SetScale(Channel,1e-3)
            self.SetPosition(Channel,-offset/1e-3)
            return
        
        scale = 2.5 * amplitude/EXTREM_VAL.VDIV.value #on prend une marge pour avoir 40% de l'ecran remplit
        self.SetScale(Channel,scale)
        scale = self.GetScale()
        
        position = -offset/scale
        
        self.SetPosition(Channel,position)

        
        #On remet les paramètres d'avant pré-réglage
        self.SetSampleRate(old_SR)
        self.SetRecordLength(old_RL)
        
        
        #on fait le réglage fin
        
        #Attente
        print("Attente d'une acquisition pour scaling")
        self.WaitForAnAcquisition()
        
        #Recupération mesure
        max_val = self.GetMeasurementMeanValue(last_meas_index+1)
        min_val = self.GetMeasurementMeanValue(last_meas_index+2)
        
        
        #delete mesure
        self.DeleteMeasurement(last_meas_index+1)
        self.DeleteMeasurement(last_meas_index+2)
        
        amplitude = max_val - min_val
        offset = (max_val + min_val)/2
        
        print(f"Amplitude: {amplitude}")
        print(f"Offset: {offset}")
        
        if amplitude == 0:
            print("Amplitude mesuré égale à zéro")
            self.SetScale(Channel,1e-3)
            self.SetPosition(Channel,-offset/1e-3)
            return
        
        scale = 1.1 * amplitude/EXTREM_VAL.VDIV.value #on prend une marge pour avoir 90% de l'écran remplit
        
        self.SetScale(Channel,scale)
        scale = self.GetScale()
        
        position = -offset/scale
        
        print(f"Scale: {scale}")
        print(f"Position: {position} division")
 
        self.SetScale(Channel,scale)
        self.SetPosition(Channel,position)

        
        return

#Exemple de gestion de l'oscillo
# from contextlib import closing
# MSO64 = OscClient()
# with closing(MSO64.OpenCom()):
#     print(MSO64.Query("TIME?"))
#     print(MSO64.Query("*IDN?"))
#     print(MSO64.GetAcqMode())
