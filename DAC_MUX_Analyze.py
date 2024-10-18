# -*- coding: utf-8 -*-
"""
Created on Tue Oct  8 10:53:15 2024

@author: Yann Parot
"""

import DREAnalysisscripts.DAC_Analyser as DA
import DREAnalysisscripts.oscillo as o
from matplotlib import pyplot as plt
import numpy as np
import scipy.signal as signal

def Analyze(n_bits, fc, filelist):
    """
    Important, la liste filelist doitêtre ordonnée de manière croissante vis àvis des codes DAC

    Parameters
    ----------
    n_bits : TYPE
        DESCRIPTION.
    fc : TYPE
        DESCRIPTION.
    filelist : TYPE
        DESCRIPTION.

    Returns
    -------
    None.

    """
    
    #Initialisation DAC MUX
    DAC_MUX = DA.DACAnalyser(isSigned=False,Nbits=n_bits)
    
    
    #Récupération des fichiers oscillo
    osc = o.Oscilloscope()
    
    print("Ouverture des fichiers") 
    DAC_lvls = []
    for i in range(n_bits+2):
        osc.OpenOscilloscopeFile(filelist[i])
        # Ajout d'un filtrage
        filtre_od1 = signal.butter(1,fc,'low',output='sos',fs=1/osc._Ts)
        DAC_signal_filtered = signal.sosfilt(filtre_od1,osc.GetWaveform(0)) #passage d'un premier filtre passe bas avant moyenne
        DAC_lvls.append([np.mean(DAC_signal_filtered)]) #On moyenne tout de suite pour ne pas trop encombre la mémoire
        
    print("Calculs DNL et INL") 
    #DNL
    DNL,DNL_par_poids=DAC_MUX.CalcLinearity(DAC_lvls)
    
    
    #INL
    INL=[np.sum(DNL[0:i]) for i in range(len(DNL))]
    
    print(f"Gain DAC: {DAC_MUX.CalcGain()}") 
    
    #Plots
    bar_width = 0.5
    fig,ax=plt.subplots(3,1,figsize=(15,15))
    fig.suptitle('Linéarité du DAC MUX SQUID')
    ax[0].bar([i for i in range(len(DNL_par_poids))],DNL_par_poids,bar_width)
    #ax[0].set_xlabel('Poids DAC')
    plt.sca(ax[0])
    plt.xticks(range(n_bits),[f'Bit{i}' for i in range(n_bits)])
    plt.grid(True)
    
    ax[1].plot(DNL,'+-k')
    ax[1].set_xlabel('Code DAC')
    ax[1].set_ylabel('DNL (V)') 
    plt.sca(ax[1])
    plt.grid(True)
    
    ax[2].plot(INL,'+-k')
    ax[2].set_xlabel('Code DAC')
    ax[2].set_ylabel('INL (V)') 
    plt.sca(ax[2])
    plt.grid(True)