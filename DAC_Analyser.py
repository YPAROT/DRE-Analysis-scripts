# -*- coding: utf-8 -*-
"""
Created on Fri Aug 30 18:05:04 2024

@author: Yann Parot
"""

import numpy as np

class DACAnalyser:
    """
    Calcule la linéarité d'un DAC ou le théorème de superposition peut s'appliquer:
        l'erreur de chaque bit est indépendante des autres. Ainsi la DNL d'un code 101
        est la DNL de 100 additionnée à celle de 001
    """
    def __init__(self,isSigned=True,Nbits=12):
        #Paramètres du DAC idéal à analyser
        self._Nbits=12 #par défaut si le setter rejette le paramètre
        self.Nbits=Nbits
        self._isSigned=True #par défaut si le setter rejette le paramètre
        self.isSigned=isSigned
        
        #Paramètres privés qui seront calculés
        if self.isSigned:
            self.Hlvl=2**(self.Nbits-1)-1
            self.Llvl=-2**(self.Nbits-1)
        else:
            self.Hlvl=2**(self.Nbits)-1
            self.Llvl = 0
            
        self._bias = 0
        
    
    
    
    #Définition des getters et setters
    @property
    def Nbits(self):
        return self._Nbits
    
    @Nbits.setter  
    def Nbits(self,Nbits):
        if not isinstance(Nbits, int):
            print('Le paramètre n\'est pas de type int')
            return
        if Nbits==0:
            print('Le paramètre ne peut être nul')
            return
        self._Nbits = Nbits
      
    
    @property
    def isSigned(self):
        return self._isSigned
    
    @isSigned.setter
    def isSigned(self,isSigned):
        if not isinstance(isSigned,bool):
            print("Le paramètre n'est pas un booléen")
            return
        self._isSigned=isSigned
        if self.isSigned:
            self.Hlvl=2**(self.Nbits-1)-1
            self.Llvl=-2**(self.Nbits-1)
        else:
            self.Hlvl=2**(self.Nbits)-1
            self.Llvl = 0
        
    
    @property
    def Hlvl(self):
        return self._Hlvl
    
    @Hlvl.setter
    def Hlvl(self,Hlvl):
        if not isinstance(Hlvl,(int,float)):
            print("Le paramètre n'est pas un nombre")
            return
        self._Hlvl = Hlvl
    
    @property
    def Llvl(self):
        return self._Llvl
    
    @Llvl.setter
    def Llvl(self,Llvl):
        if not isinstance(Llvl,(int,float)):
            print("Le paramètre n'est pas un nombre")
            return
        self._Llvl = Llvl
    
    @property
    def bias(self):
        return self._bias
    
    
    #Méthodes
    def SetHlvlFromWaveform(self,waveform):
        """
        Calcule et règle le niveau haut du DAC à partir d'une liste de valeurs type int ou float

        Parameters
        ----------
        waveform : list[int/float]
            capture temporelle d'un niveau haut en sortie de DAC.

        Returns
        -------
        None.

        """
        if not isinstance(waveform,list) and not waveform:
            print('waveform n\'est pas de type list ou est vide')
            return
        if not all([isinstance(val,(int,float)) for val in waveform]):
            print('waveform n\'est pas une liste de nombres')
            return
        self._Hlvl = np.mean(waveform)
     
        
    def ResetHlvl(self):
        if self.isSigned:
            self._Hlvl=2**(self._Nbits-1)-1
        else:
            self._Hlvl=2**(self._Nbits)-1
    
    
    def SetLlvlFromWaveform(self,waveform):
        if not isinstance(waveform,list) and not waveform:
            print('waveform n\'est pas de type list ou est vide')
            return
        if not all([isinstance(val,(int,float)) for val in waveform]):
            print('waveform n\'est pas une liste de nombres')
            return
        self._Llvl = np.mean(waveform)
    
    
    def ResetLlvl(self):
        if self.isSigned:
            self._Llvl=-2**(self._Nbits-1)
        else:
            self._Llvl = 0
    
    
    def CalcGain(self):
        return (self.Hlvl - self.Llvl)/(2**self.Nbits-1)
        
    def SetBiasFromWaveform(self,waveform):
        if not isinstance(waveform,list) or not waveform:
            print('waveform n\'est pas de type list ou est vide')
            return
        if not all([isinstance(val,(int,float)) for val in waveform]):
            print('waveform n\'est pas une liste de nombres')
            return
        self._bias = np.mean(waveform)
        
    def ResetBias(self):
        self._bias=0
    
    
    def CalcLinearity(self,bits_waveforms):
        """
        

        Parameters
        ----------
        bits_waveforms : list[list[(int,float)]]
            indice0 = 0 DAC, indice1 = lowvalue = 0 DAC si non signé,waveform du poids fort au faible, indice N+2= max DAC .

        Returns
        -------
        None.

        """
        #vérifications que le nombre de waveform corrspond au nombre de bits du DAC (tous les poids plus valeurs extrêmes pour calculer bias et gain)
        if self.isSigned:
            Nbadditionalwave=3
        else:
            Nbadditionalwave=2
        if len(bits_waveforms) != self.Nbits+Nbadditionalwave:
            print('Le nombre de waveforms ne correspond pas au nombre de bits du DAC')
            return
        #Vérification du typage
        if not isinstance(bits_waveforms,list) and not bits_waveforms:
            print('bits_waveforms n\'est pas de type list ou est vide')
            return
        if not all([isinstance(sslist,list) for sslist in bits_waveforms]):
            print('Au moins un des éléments de bits_waveforms n\'est pas une liste')
            return
        for sslist in bits_waveforms:
            if not sslist or not all([isinstance(number,(int,float)) for number in sslist]):
                print('Au moins un des éléments de bits_waveforms n\'est pas une liste de nombre ou est vide')
                return
            
        
        #correction bias et gain
        if not self.isSigned:
            self.SetLlvlFromWaveform(bits_waveforms[0])
            self._bias=self._Llvl
        else:
            self.SetLlvlFromWaveform(bits_waveforms[1])
            self.SetBiasFromWaveform(bits_waveforms[0])
        self.SetHlvlFromWaveform(bits_waveforms[-1])
        
        #Function linéaire du DAC
        DACLinearFunc = lambda i : self.CalcGain()*i+self.bias
        
        #Calcul de la non linéarité de chaque poids
        DNL_poids=[]
        for i in range(Nbadditionalwave-1,self.Nbits+Nbadditionalwave-1):
            DNL_temp = np.mean(bits_waveforms[i])-DACLinearFunc(2**(i-Nbadditionalwave+1))
            DNL_poids.append(DNL_temp)
            
        DNL_poids.reverse()#On met les poids forts en premier pour coller à la génération de code binaire qui est MSB first
        #Calcul de la non linéarité totale
        DNL_totale = []
        Table_binaire=[f'{i:0{self.Nbits}b}' for i in range(1,2**self.Nbits)]
        for i in range(1,2**self.Nbits):
            DNL_temp = self._ProdScalaireList([ord(c)-ord('0') for c in Table_binaire[i-1]],DNL_poids)
            DNL_totale.append(DNL_temp)
        
        return [0]+DNL_totale,DNL_poids
        
        
    def _ProdScalaireList(self,list1,list2):
        if len(list1) != len(list2) or not list1: #vu que les listes doivent être de même taille il suffit de tester une liste vide seulement
            return
        if not all([isinstance(number, (int,float)) for number in list1]) or not all([isinstance(number, (int,float)) for number in list2]):
            return
        
        return np.sum([val[0]*val[1] for val in zip(list1,list2)])