# -*- coding: utf-8 -*-
"""
Created on Mon Sep  9 11:02:38 2024

@author: Yann Parot
"""
import os
import numpy as np
import PilotageMSO64 as Tek
from contextlib import closing
import oscillo
from matplotlib import pyplot as plt
from scipy import signal

#Classe statique pour regrouper les tests (wrapper)
class Test:
    
    #Attributs statiques
    #Param MSO64
    OscRLmax = 62.5e6
    OscSRmax = 250e9
    IPaddress = "10.120.1.86"
    Port = 4000
    
    
    @classmethod
    def MeasureNoise(cls,channel=1,fstart=10,fstop=1e9,PntsperDec=100,mean=10,savepath="C:"): 
        
        # #Vérification du dossier de sauvegarde et création au besoin
        # PathExist = os.path.exists(savepath)
        # if not PathExist:
        #     os.makedirs(savepath)
        #     print("Dossier créé car inexistant")
        
        print("------Calcul des intervalles------")   
        #Définition des paramètres de mesure
        dec_exp_min=int(np.floor(np.log10(fstart)))
        dec_exp_max=int(np.floor(np.log10(fstop)))
        
        ParamOsc = []
        for i in range(dec_exp_min,dec_exp_max):
            f_interval = 9*10**i
            fspan = f_interval/PntsperDec
            SR = min(10.0**(i+1)*2,cls.OscSRmax)
            ParamOsc.append((SR,fspan))
            
        #Connection à l'oscilloscope
        print("------Connection à l'oscilloscope------")    
        mso64 = Tek.OscClient(cls.IPaddress,cls.Port)     
        with closing(mso64.OpenCom()):
            print("------Réglage général de l'oscilloscope------") 
            #Affichage du channel d'intérêt seulement pour maximiser le sampling rate
            ch_list = [True if ch==channel else False for ch in range(1,Tek.EXTREM_VAL.NBCHAN.value+1)]
            mso64.SetAllChannelState(ch_list)
            
            #Réglage de la bandwidth au max ainsi que du mode en Highres
            mso64.SetAcqMode(Tek.ACQ_MODE.HIRES)
            mso64.SetBandwidth(channel,Tek.EXTREM_VAL.MAX_BW.value)
            
            #Passage en manuel sur l'échelle horizontale
            mso64.SetManualHorizontalMode(True)
            
            #On ne veut pas que RL bouge quand SR bouge
            mso64.AdjustRLWhenSRMove(False)
            
            for SR,fspan in ParamOsc:
                print("------ACQUISITION------")
                print(f"Sample Rate désiré: {SR} Samples/s")
                #Réglage du SR
                mso64.SetSampleRate(SR)
                #récupération des valeurs réglées
                current_SR=mso64.GetSampleRate()
                print(f"Sample Rate réglé sur: {current_SR} Samples/s")
                #Réglage du RL
                RL = min(np.ceil(SR/fspan*mean),cls.OscRLmax)
                mso64.SetRecordLength(RL)
                #récupération des valeurs réglées
                current_RL=mso64.GetRecordLength()
                print(f"Record Length réglé sur: {current_RL}")
                print(f"Fspan désiré: {fspan} Hz")
                print(f"Fspan réglé: {SR/(RL/mean)} Hz")
                

                #Autoscale Y
                mso64.VerticalAutoScale(channel)

                #Wait 
                mso64.WaitForAnAcquisition()

                #Sauvegarde fichier
                mso64.SaveWaveformAsCSV(channel,filepath=savepath,filename=f"Noise SR-{SR} RL-{RL}")
                
    @staticmethod
    def ExploitNoiseFiles(dirpath="C:",welch_mean=10): #ne marche qu'avec des fichiers de 1 channel comme les mesures de bruits
        
        #Ajout de la figure
        fig,ax=plt.subplots(figsize=(15,15))
        ax.set_title('Mesure de bruit')
        ax.set_xlabel('frequency [Hz]')
        ax.set_ylabel('Tension de bruit ( V / $\sqrt{Hz}$ )')
        
        #ouverture des fichier et plot sur la figure
        osc = oscillo.Oscilloscope()
        CSV_gen = Test.ListCSVFilesGenerator(dirpath)
        for CSV in CSV_gen:
            osc.OpenOscilloscopeFile(CSV)
            welch_length = int(np.floor(len(osc)/welch_mean)) #La longueur des segments pour le calcul est égale au nombre d'échantillons divisé par le nombre de moyennes
            freq,power = signal.welch(osc.GetWaveform(0),fs=1/osc.Ts,nperseg=welch_length)
            ax.loglog(freq[1:], np.sqrt(power)[1:],'+-k') #on enlève le premier point pour un tracé plus propre
            
        
    
    @staticmethod
    def ListCSVFilesGenerator(dirpath="C:"):
        for entry in os.scandir(dirpath):
            if entry.name.endswith(".csv") and entry.is_file():
                yield entry.path
                