# -*- coding: utf-8 -*-
"""
Created on Thu Sep  5 19:50:37 2024

@author: Yann Parot
"""

import oscillo

#Ref_Osc = oscillo.Oscilloscope()
#SondeTDP = oscillo.Oscilloscope()
SE2DE_off = oscillo.Oscilloscope()
SE2DE_on = oscillo.Oscilloscope()

#Ref_Osc.OpenFile()
#SondeTDP.OpenFile()
SE2DE_off.OpenFile()
SE2DE_on.OpenFile()


import numpy as np
from matplotlib import pyplot as plt
from scipy import signal



#DSP
print('Calcul DSP oscilloscope')
#fosc, Posc = signal.welch(Ref_Osc._Waveforms[0], 1/Ref_Osc.Ts, nperseg=10000)
print('Calcul DSP sonde TPD1500')
#fsonde, Psonde = signal.welch(SondeTDP._Waveforms[0], 1/SondeTDP.Ts, nperseg=10000)
print('Calcul DSP SE2DE Off')
fse2de_off, Pse2de_off = signal.welch(SE2DE_off._Waveforms[0], 1/SE2DE_off.Ts, nperseg=10000)
print('Calcul DSP SE2DE On')
fse2de_on, Pse2de_on = signal.welch([val*2 for val in SE2DE_on._Waveforms[0]], 1/SE2DE_on.Ts, nperseg=10000) #facteur 2 car sortie 50 Ohms sur entrée 50 Ohms

ref=15e-9

#Plots
fig,ax=plt.subplots(figsize=(15,15))
#ax.loglog(fosc, np.sqrt(Posc),'k')
#ax.loglog(fsonde, np.sqrt(Psonde),'g')
ax.loglog(fse2de_off, np.sqrt(Pse2de_off),'--b') 
ax.loglog(fse2de_on, np.sqrt(Pse2de_on),'-*b') 
ax.loglog([fse2de_off[0],fse2de_off[-1]], [ref,ref],'r')



ax.set_xlabel('frequency [Hz]')
ax.set_title('Bruit des divers moyen de mesure')
ax.set_ylabel('Tension de bruit ( V / $\sqrt{Hz}$ )')
#ax.legend(['Bruit de l\'oscilloscope','Bruit de la sonde TDP1500','Bruit de l\'EGSE DE2SE Off','Bruit de l\'EGSE DE2SE On','Exigence DRE'])
ax.legend(['Bruit de l\'EGSE DE2SE Off','Bruit de l\'EGSE DE2SE On','Exigence DRE'])