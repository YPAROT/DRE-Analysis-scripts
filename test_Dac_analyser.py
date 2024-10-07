# -*- coding: utf-8 -*-
"""
Created on Tue Sep  3 09:11:02 2024

Test de la classe DAC_Analyser

@author: Yann Parot
"""

import DAC_Analyser as DA
import random as rd
import numpy as np
from matplotlib import pyplot as plt


dac1 = DA.DACAnalyser()


#Test des getters:
print("Test des Getters:")
print("-----------------\n")
print("Paramètre Nbits: "+str(dac1.Nbits))
print("Paramètre isSigned: "+str(dac1.isSigned))    
#print("Paramètre FS: "+str(dac1.FS))
print("Paramètre Hlvl: "+str(dac1.Hlvl))
print("Paramètre Llvl: "+str(dac1.Llvl))
print("Paramètre bias: "+str(dac1.bias))

#setters simples:
print("\nTest des setters:")
print("------------------\n")
print("passage à 14 bits")
dac1.Nbits=14
print("Paramètre Nbits: "+str(dac1.Nbits))
print("Paramètre Hlvl: "+str(dac1.Hlvl))
print("Paramètre Llvl: "+str(dac1.Llvl))
print("Paramètre bias: "+str(dac1.bias))
print("\npassage en non signé")
dac1.isSigned=False
print("Paramètre isSigned: "+str(dac1.isSigned))
print("Paramètre Hlvl: "+str(dac1.Hlvl))
print("Paramètre Llvl: "+str(dac1.Llvl))
print("Paramètre bias: "+str(dac1.bias))

#Définition du DAC à l'aide de waveforms
Nb_test_bits = 4
FS=2
Bias=1
DNL_add=0.6
LSB=1/2**Nb_test_bits

##Version non signée##

# print("\ntest du calcul à partir de waveforms pour un DAC non signé sur "+str(Nb_test_bits)+" bits")
# print("-----------------------------------------------------------\n")
# dac1.Nbits=Nb_test_bits
# #DNL de +/-1.5 LSB en distribution uniforme
# DNL=[rd.uniform(-DNL_add,DNL_add) for i in range(Nb_test_bits)]
# DAC_wave=[0]+[1+DNL[0]]+[2**i+DNL[i] for i in range(1,Nb_test_bits)]+[float(np.sum(DNL))+2**Nb_test_bits-1]
# DAC_wave_measured  = [[FS*LSB*val+Bias] for val in DAC_wave]


# DNL_th = [0]
# Table_binaire=[f'{i:0{Nb_test_bits}b}' for i in range(1,2**Nb_test_bits)]
# for i in range(1,2**Nb_test_bits):
#     Code_DAC = [ord(c)-ord('0') for c in Table_binaire[i-1]]
#     Code_DAC.reverse() #inversion de la liste pour aligner MSB et LSB
#     DNL_temp = np.sum([val[0]*val[1] for val in zip(Code_DAC,[val*FS*LSB for val in DNL])])    
#     DNL_th.append(DNL_temp)

# DNL_Calc=dac1.CalcLinearity(DAC_wave_measured)




# #INL
# INL_th=[np.sum(DNL_th[0:i]) for i in range(len(DNL_th))]
# INL_Calc=[np.sum(DNL_Calc[0:i]) for i in range(len(DNL_Calc))]

# #Plots
# fig,ax=plt.subplots(3,1,figsize=(15,15))
# fig.suptitle(f'Test de tracé DNL et INL pour un DAC non signé {Nb_test_bits} Bits, FS de {FS} V, Biais de {Bias} V et DNL injecté de +/- {DNL_add} LSB max/Bits')
# ax[0].bar([i for i in range(len(DNL))],DNL,0.2)
# #ax[0].set_xlabel('Poids DAC')
# ax[0].set_ylabel('DNL injectée/Bit en LSB')
# plt.sca(ax[0])
# plt.xticks(range(Nb_test_bits),[f'Bit{i}' for i in range(Nb_test_bits)])
# plt.grid(True)

# ax[1].plot(DNL_th,'+-k')
# ax[1].plot(DNL_Calc,'+-r') 
# ax[1].set_xlabel('Code DAC')
# ax[1].set_ylabel('DNL (V)')
# ax[1].legend(['DNL théorique sans recalculer le gain','DNL calculée par l\'algo'])   
# plt.sca(ax[1])
# plt.grid(True)
# #plt.xticks(range(2**Nb_test_bits),[f'{i:0{Nb_test_bits}b}' for i in range(2**Nb_test_bits)])

# ax[2].plot(INL_th,'+-k')
# ax[2].plot(INL_Calc,'+-r') 
# ax[2].set_xlabel('Code DAC')
# ax[2].set_ylabel('INL (V)')
# ax[2].legend(['INL théorique sans recalculer le gain','INL calculée par l\'algo'])   
# plt.sca(ax[2])
# plt.grid(True)


##Version signée##

dac1.isSigned=True
print("\ntest du calcul à partir de waveforms pour un DAC signé sur "+str(Nb_test_bits)+" bits")
print("-----------------------------------------------------------\n")
dac1.Nbits=Nb_test_bits
#DNL en distribution uniforme
DNL=[rd.uniform(-DNL_add,DNL_add) for i in range(Nb_test_bits)]
code0=0
DAC_wave=[0]+[code0]+[1+DNL[0]]+[2**i+DNL[i] for i in range(1,Nb_test_bits)]+[float(np.sum(DNL))+2**Nb_test_bits-1] #génération pourrave!!! à revoir
DAC_wave_measured  = [[FS*LSB*(val-2**(Nb_test_bits-1))] for val in DAC_wave]


DNL_th = [0]
Table_binaire=[f'{i:0{Nb_test_bits}b}' for i in range(1,2**Nb_test_bits)]
for i in range(1,2**Nb_test_bits):
    Code_DAC = [ord(c)-ord('0') for c in Table_binaire[i-1]]
    Code_DAC.reverse() #inversion de la liste pour aligner MSB et LSB
    DNL_temp = np.sum([val[0]*val[1] for val in zip(Code_DAC,[val*FS*LSB for val in DNL])])    
    DNL_th.append(DNL_temp)

DNL_Calc=dac1.CalcLinearity(DAC_wave_measured)




#INL
INL_th=[np.sum(DNL_th[0:i]) for i in range(len(DNL_th))]
INL_Calc=[np.sum(DNL_Calc[0:i]) for i in range(len(DNL_Calc))]

#Plots
fig,ax=plt.subplots(3,1,figsize=(15,15))
fig.suptitle(f'Test de tracé DNL et INL pour un DAC signé {Nb_test_bits} Bits, FS de {FS} V, Biais de {Bias} V et DNL injecté de +/- {DNL_add} LSB max/Bits')
ax[0].bar([i for i in range(len(DNL))],DNL,0.2)
#ax[0].set_xlabel('Poids DAC')
ax[0].set_ylabel('DNL injectée/Bit en LSB')
plt.sca(ax[0])
plt.xticks(range(Nb_test_bits),[f'Bit{i}' for i in range(Nb_test_bits)])
plt.grid(True)

ax[1].plot(DNL_th,'+-k')
ax[1].plot(DNL_Calc,'+-r') 
ax[1].set_xlabel('Code DAC')
ax[1].set_ylabel('DNL (V)')
ax[1].legend(['DNL théorique sans recalculer le gain','DNL calculée par l\'algo'])   
plt.sca(ax[1])
plt.grid(True)
#plt.xticks(range(2**Nb_test_bits),[f'{i:0{Nb_test_bits}b}' for i in range(2**Nb_test_bits)])

ax[2].plot(INL_th,'+-k')
ax[2].plot(INL_Calc,'+-r') 
ax[2].set_xlabel('Code DAC')
ax[2].set_ylabel('INL (V)')
ax[2].legend(['INL théorique sans recalculer le gain','INL calculée par l\'algo'])   
plt.sca(ax[2])
plt.grid(True)