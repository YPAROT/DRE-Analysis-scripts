# -*- coding: utf-8 -*-
"""
Created on Tue Aug 27 21:46:17 2024

@author: Yann Parot
"""

import numpy as np
import scipy.signal as signal
from matplotlib import pyplot as plt

def CheckDACLinearity(osc,index,step_size,FS,dT,N,signed=True,**kwargs):
    """
    Permet de comparer un pattern généré par un compteur sur un DAC à sa courbe théorique

    Parameters
    ----------
    osc : Oscilloscope
        contient les données numérisées de l'oscilloscope'
    index : TYPE
        channel a utiliser comme waveform pour l'entrée DAC à analyser.
    step_size : TYPE
        nb de LSB d'un step.
    FS : TYPE
        Fullscale du DAC théorique.
    dT : TYPE
        durée d'un step en temps.
    N : TYPE
        Nombre de bits du DAC.
    signed : TYPE, optional
        Indique si le DAC est signé ou non. The default is True.

    Returns
    -------
    None.

    """
    #Définition de la fonction d'un DAC parfait
    DAC = lambda i : i%int(np.power(2,N)) if not signed else (i%int(np.power(2,N))-np.power(2,N-1))
    
    #Création d'un pattern utilisé pour la cross corrélation
    #pattern = [DAC(int(np.floor(t/dT))*step_size)/np.power(2,N)*FS for t in osc._Time]
    indices = [int(np.floor(t/dT))*step_size for t in osc._Time]
    DAC_ideal = [DAC(val) for val in indices]
    pattern =[val/2**N*FS for val in DAC_ideal]
    
    # fig,axtemp = plt.subplots(figsize=(15, 15))
    # axtemp.plot(osc._Time,DAC_ideal,'+')
    
    if kwargs:
        try:
            fc=kwargs['fc']
            filtre_od1 = signal.butter(1,fc,'low',output='sos',fs=1/osc._Ts)
            DACSignal = signal.sosfilt(filtre_od1,osc._Waveforms[index])
            Title = osc._Labels[index]+' avec filtre ordre 1: fc = '+str(fc/1e6)+' MHz'
        except KeyError:
            print('L\'argument donné n\'existe pas')
    else:
        DACSignal = osc._Waveforms[index]
        Title = osc._Labels[index]
    
    #plot du DAC théorique et du signal avant alignement en echantillons
    # fig, ax1 = plt.subplots(figsize=(15, 15))
    # ax1.plot(DACSignal)
    # ax1.plot(pattern,'-r')
    # ax1.set_title(Title)
    # ax1.set_ylabel('Tension (V)')
    # ax1.set_xlabel('Echantillon')
    # ax1.legend(['Signal','DAC idéal'])
    
    #Correlation
    correlation = signal.correlate(DACSignal, pattern, mode="full")
    lags = signal.correlation_lags(len(DACSignal), len(pattern), mode="full")
    lag = lags[np.argmax(correlation)]
    
    print('Meilleure correlation trouvée pour un retard de '+str(lag)+' échantillons soit dT = '+str(lag*osc._Ts)+' s')
    
    #Alignement des signaux en temporel
    #pattern = pattern[-lag:]+pattern[:-lag]
    pattern = [DAC(int(np.floor((t-lag*osc._Ts)/dT))*step_size)/np.power(2,N)*FS for t in osc._Time]
    
    
    #ci-dessous ça dépend de la courbe!!! à améliorer!!!
    #temps au début du max
    indmax=np.argmax(pattern)
    tmax=osc._Time[indmax]
    print('Début du premier palier de la rampe à '+str(tmax)+' s')
    
    indmin=np.argmin(pattern[indmax:])+indmax
    tmin=osc._Time[indmin]
    print('Début du dernier palier de la rampe à '+str(tmin)+' s')
    
    ramp_duration = tmin-tmax+(dT-osc._Ts)
    nb_steps = int(np.round((ramp_duration)/dT)) #arrondi au plus proche qui sera en général le supérieur car cela se joue à 1 Tsampling en moins
    print('Nombre de paliers dans la rampe: '+str(nb_steps))
    
    #Identification des saut de valeur
    dT_indice = int(np.floor(1.5*dT/osc._Ts)) #on regarde combien dure environ 1.5 pallier
    #On recherche les mins successifs sur la rampe tous les 1.5 dT indice à partir de la dernière transition trouvée
    liste_transition=[indmax]
    for i in range(nb_steps):
        liste_transition.append(np.argmin(pattern[liste_transition[i]:liste_transition[i]+dT_indice])+liste_transition[i])
    
    
    #Calcul du gain à appliquer
    d_indice=100 #permet de ne pas prendre les bords
    DACSignal_ideal=[np.mean(DACSignal[liste_transition[i]+d_indice:liste_transition[i+1]-d_indice]) for i in range(nb_steps-1)]
    
    pattern_reduced = [pattern[i] for i in liste_transition]
    
    
    #On corrige le gain en prenant un indice >0 et <-1 pour éviter les effets de bord
    ind_gain_corr = int(len(DACSignal_ideal)/4) #on prendra à +/-1/4 de la courbe
    
    x0=ind_gain_corr
    x1=3*ind_gain_corr
    # dV0=pattern_reduced[x0]-DACSignal_ideal[x0]
    # print(dV0)
    # dV1=pattern_reduced[x1]-DACSignal_ideal[x1]
    # print(dV1)
    
    # fig,axtemp = plt.subplots(figsize=(15, 15))
    # axtemp.plot([x0,x1],[DACSignal_ideal[i] for i in [x0,x1]],'+r')
    # axtemp.plot([x0,x1],[pattern_reduced[i] for i in [x0,x1]],'+k')
    
    # dA=(dV0-dV1)/(osc._Time[liste_transition[x0]]-osc._Time[liste_transition[x1]])
    # #coeff_correc = 1/(1-(dV0-dV1)/(FS/(2**N)*(x0-x1)))
    
    # print('Coefficient de correction de gain: '+str(dA))
    
    dA1=pattern_reduced[x0]/DACSignal_ideal[x0]
    dA2=pattern_reduced[x0]/DACSignal_ideal[x0]
    dA=(dA1+dA2)/2
    
    print('Coefficient de correction de gain: '+str(dA))
    
    #Calcul de l'Offset
    Offset_DACSignal = (max(DACSignal)+min(DACSignal))/2
    Offset_DACTh = (max(pattern)+min(pattern))/2
    
    Offset= Offset_DACTh - Offset_DACSignal
    
    print('Offset entre les deux courbes d\'environ '+str(Offset)+' V')
    
    
    pattern = [val-Offset for val in pattern]
    
    pattern = [DAC(int(np.floor((t-lag*osc._Ts)/dT))*step_size)*(FS/np.power(2,N))/dA+Offset for t in osc._Time]
    
    
    #plot du DAC théorique et du signal
    fig, ax2 = plt.subplots(figsize=(15, 15))
    ax2.plot(osc._Time,DACSignal)
    ax2.plot(osc._Time,pattern,'-r')
    ax2.plot([osc._Time[i] for i in liste_transition],[pattern[i] for i in liste_transition],'+k')
    ax2.set_title(Title)
    ax2.set_ylabel('Tension (V)')
    ax2.set_xlabel('Temps (s)')
    ax2.legend(['Signal','DAC idéal'])
    
    
    
    

