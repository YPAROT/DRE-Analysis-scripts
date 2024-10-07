# -*- coding: utf-8 -*-
"""
Created on Wed Aug 28 14:14:17 2024

@author: Yann Parot
"""

import oscillo

osc1 = oscillo.Oscilloscope()

osc1.OpenFile()


#osc1.PlotAll(shared=True)

#Test DSP
#osc1.PlotAllDSP(shared=False)

import numpy as np
from matplotlib import pyplot as plt
from scipy import signal


div_factor = 100
# l_fft=int(2**(np.floor(np.log2(len(osc1)/div_factor))-1))
# Power = np.zeros(l_fft+1)
# for i in range(div_factor):
#     freq, Power_temp = signal.periodogram(osc1._Waveforms[0][i*l_fft*2:(i+1)*l_fft*2], 1/osc1.Ts, 'hann', scaling='density')
#     Power+=Power_temp

fig,ax=plt.subplots(figsize=(15,15))
# ax.loglog(freq,np.sqrt(Power/div_factor))


f, Pxx_den = signal.welch(osc1._Waveforms[0], 1/osc1.Ts, nperseg=int(np.floor(len(osc1)/div_factor)))

ax.loglog(f, np.sqrt(Pxx_den),'r')


ax.set_xlabel('frequency [Hz]')


ax.set_title('Bruit de la sonde TPD1500')
ax.set_ylabel(r'$\frac{V}{\sqrt{Hz}}$')