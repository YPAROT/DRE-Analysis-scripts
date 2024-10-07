# -*- coding: utf-8 -*-
"""
Created on Wed Sep 11 10:18:11 2024

@author: Yann Parot
"""

import TestsDRE as TDRE

moyenne_PSD = 10000

#Mesure de bruit avec sauvegarde sur NAS
#TDRE.Test.MeasureNoise(channel=1,fstart=1e3,fstop=1.5e9,PntsperDec=100,mean=moyenne_PSD,savepath="M:/00_TRANSFERS/00 - Yann codes Python/Captures")

#Exploitation sur NAS
TDRE.Test.ExploitNoiseFiles("Z:/00_TRANSFERS/00 - Yann codes Python/Captures",moyenne_PSD)