# -*- coding: utf-8 -*-
"""
Created on Tue Aug 27 13:29:22 2024

Analyse des signaux DRE

@author: Yann Parot
"""

import csv
from tkinter import Tk
from tkinter.filedialog import askopenfilename
from matplotlib import pyplot as plt
import matplotlib.cm as cm
import scipy.signal as signal
from scipy.optimize import curve_fit
import numpy as np
#import statistics

class Oscilloscope:
    
    def __init__(self):
        self._Waveforms=[]
        self._Time=[]
        self._Ts=0
        self._Labels = []
        
    @property
    def Time(self):
        return self._Time

    @property
    def Ts(self):
        return self._Ts
    
    @property
    def Labels(self):
        return self._Labels 
     
    def __len__(self):
        return len(self._Time)
    
    def OpenOscilloscopeFile(self,filename):
    
        #lecture
        with open(filename, newline='') as csvfile:
            
            oscillo_file = csv.reader(csvfile, delimiter=',')               
                
            Start=False
            nbvoies=0
            for oscillo_iter in oscillo_file:
                if not Start and oscillo_iter: #Lecture Header
                    if oscillo_iter[0] == 'Sample Interval':
                        self._Ts=float(oscillo_iter[1])
                    elif oscillo_iter[0] == 'Labels':
                        self._Labels = oscillo_iter[1:]
                        nbvoies=len(self._Labels)
                        self._Waveforms=[ [] for i in range(nbvoies)]
                    elif oscillo_iter[0] == 'TIME':
                        Start=True
                elif Start and nbvoies>0:
                    self._Time.append(float(oscillo_iter[0]))
                    for i in range(nbvoies):
                        self._Waveforms[i].append(float(oscillo_iter[1+i]))
       

                    
    def OpenFile(self):
        #Choix fichier
        root=Tk()
        root.lift()
        root.withdraw()
        filename = askopenfilename(filetypes=[('fichier Oscilloscope','*.csv')],parent=root)
        if filename:
            self.clear() #On fait un clear car c'est le fichier oscilloscope qui défini le Ts. Ainsi des waveforms générées après doivent l'être avec ce même Ts
            self.OpenOscilloscopeFile(filename)
    
    def AddWaveform(self,waveform,label):
        if not isinstance(waveform,list):
            print('Waveform n\'est pas de type List!!!')
            return
        elif not isinstance(label,str):
            print('label n\'est pas de type str!!!')
            return
        else:
            if len(waveform) > len(self):
                print('la waveform contient trop d\'échantillons. les derniers ont étés supprimés')
                waveform = waveform[:len(self)-1]
            elif len(waveform) < len(self):
                print('la waveform ne contient pas assez d\'échantillons. Des zeros ont étés ajoutés')
                waveform = waveform+[0 for i in range(len(self)-len(waveform))]
            
            self._Waveforms.append(waveform)
            self._Labels.append(label)
            
    def clear(self):
      self._Waveforms.clear()
      self._Time.clear()
      self._Ts=0
      self._Labels.clear()
            
      
    def NbWaveforms(self):
        return len(self._Waveforms)

    def GetIndexFromLabel(self,label):
        if isinstance(label,str):
            return self._Labels.index(label)
        
    def GetWaveform(self,index):
        if index<=self.NbWaveforms():
            return self._Waveforms[index]
        else:
            print('La waveform demandé n\'existe pas')
            return []

    def PlotWaveForm(self,index_list,shared=True,**kwargs):
        
        if shared:
            fig, ax1 = plt.subplots(figsize=(15, 15))
        else:
            fig, ax1 = plt.subplots(min(self.NbWaveforms(),len(index_list)),1,figsize=(15, 15),squeeze=False)
        legend=[]
        for index in index_list:
            if index>self.NbWaveforms()-1:
                continue
            else:
                if kwargs:
                    try:
                        fc=kwargs['fc']
                        filtre_od1 = signal.butter(1,fc,'low',output='sos',fs=1/self._Ts)
                        plotted_Voltage = signal.sosfilt(filtre_od1,self._Waveforms[index])
                        Title = 'Oscillogramme avec filtre ordre 1: fc = '+str(fc/1e6)+' MHz'
                    except KeyError:
                        print('L\'argument donné n\'existe pas')
                else:
                    plotted_Voltage = self._Waveforms[index]
                    Title = 'Oscillogramme'
                if shared:
                    ax1.plot(self._Time,plotted_Voltage)
                    ax1.set_title(Title)
                    ax1.set_ylabel('Tension (V)')
                    ax1.set_xlabel('Temps (s)')
                else:
                    ax1[index,0].plot(self._Time,plotted_Voltage)
                    ax1[index,0].set_title(self._Labels[index])
                    ax1[index,0].set_ylabel('Tension (V)')
                    ax1[index,0].set_xlabel('Temps (s)')
                    
                legend.append(self._Labels[index])
        
        if shared:
            ax1.legend(legend)
        
    def PlotAll(self,shared=True):
        self.PlotWaveForm([i for i in range(self.NbWaveforms())],shared)
        
    
    def PlotWaveFormDSP(self,index_list,shared=False,**kwargs):
        
        if shared:
            fig, ax1 = plt.subplots(figsize=(15, 15))
        else:
            fig, ax1 = plt.subplots(min(self.NbWaveforms(),len(index_list)),1,figsize=(15, 15),squeeze=False)
        legend=[]
        for i,index in enumerate(index_list):
            if index>self.NbWaveforms()-1:
                continue
            else:
                if kwargs:
                    try:
                        fc=kwargs['fc']
                        filtre_od1 = signal.butter(1,fc,'low',output='sos',fs=1/self._Ts)
                        plotted_Voltage = signal.sosfilt(filtre_od1,self._Waveforms[index])
                        Title = 'Oscillogramme avec filtre ordre 1: fc = '+str(fc/1e6)+' MHz'
                    except KeyError:
                        print('L\'argument donné n\'existe pas')
                else:
                    plotted_Voltage = self._Waveforms[index]
                    Title = 'Oscillogramme'
                freq, Power = signal.periodogram(plotted_Voltage, 1/self._Ts, 'hann', scaling='density')
                if shared:
                    ax1.semilogy(freq/1e6,np.sqrt(Power))
                    ax1.set_title('DSP: ' + Title)
                    ax1.set_ylabel('Tension ( V / $\sqrt{Hz}$ )')
                    ax1.set_xlabel('Fréquence ( MHz )')
                else:
                    ax1[i,0].semilogy(freq/1e6,np.sqrt(Power))
                    ax1[i,0].set_title('DSP: '+self._Labels[index])
                    ax1[i,0].set_ylabel('Tension ( V / $\sqrt{Hz}$ )')
                    ax1[i,0].set_xlabel('Fréquence ( MHz )')
                    
                legend.append(self._Labels[index])
        
        if shared:
            ax1.legend(legend)
    
    
    
    def PlotAllDSP(self,shared=True):
        self.PlotWaveFormDSP([i for i in range(self.NbWaveforms())],shared)
        
    @staticmethod
    def plot_high_res_csv(**kwargs):
        #Choix fichier
        root=Tk()
        root.lift()
        root.withdraw()
        filename = askopenfilename(filetypes=[('fichier Oscilloscope high res','*.csv')],parent=root)
        
        #lecture
        with open(filename, newline='') as csvfile:
            
            hr_file = csv.reader(csvfile, delimiter=',')               

            param = dict()
            data = []
            for i,csvline in enumerate(hr_file):
                if i < 9:
                    param[csvline[0]] = csvline[1]
                else:
                    for pxl_value in csvline:
                        if pxl_value != '':
                            data.append(int(pxl_value)) 
                            
        #conversion vers numpy array
        data = np.array(data)
    
        #reshape en image
        nb_rows = int(param['Total Rows'])
        nb_cols = int(param['Total Columns'])
        data = data.reshape((nb_rows,nb_cols))
    
        #Affichage des axes
        nb_ticks=10
        t_start = float(param['Left Column'])
        t_stop = t_start + float(param['Sample Interval']) * nb_cols
        x_ticks_labels = [f"{val:.2e}" for val in np.linspace(t_start,t_stop,nb_ticks)]
        x_ticks_locs = np.linspace(0,nb_cols-1,nb_ticks)
        
        y_info = None
        if kwargs:
            try:
                y_info=kwargs['y_info']
            except KeyError:
                print('L\'argument donné n\'existe pas')

        if y_info and len(y_info)==3:
            y_ticks_labels = [f"{val:.2e}" for val in np.linspace(y_info[0],y_info[0]+y_info[1]*y_info[2],nb_ticks)]
        else:
            y_ticks_labels = [f"{val:.2e}" for val in np.linspace(0,nb_rows-1,nb_ticks)]
        y_ticks_locs = np.linspace(nb_rows-1,0,nb_ticks)
    
        #plot image
        y_im_size = 10
        fig, ax = plt.subplots(figsize=(int(y_im_size*nb_cols/nb_rows), y_im_size))
        ax.imshow(np.log10(data+1),cmap=cm.inferno) #log pour augmenter le contraste avec +1 pour éviter le inf
        plt.sca(ax)
        plt.xticks(x_ticks_locs,x_ticks_labels)
        plt.yticks(y_ticks_locs,y_ticks_labels)
        

        return

    @staticmethod
    def plot_hist_measurement(fit=False,fittype='gaussian',**kwargs):
         
        #Choix fichier
        root=Tk()
        root.lift()
        root.withdraw()
        filename = askopenfilename(filetypes=[('fichier Oscilloscope measurement histogramme','*.csv')],parent=root)
        
        #lecture
        x_data = []
        y_data = []
        with open(filename, newline='') as csvfile:           
            histo_file = csv.reader(csvfile, delimiter=',')               
            for i,csvline in enumerate(histo_file):
                if i < 1:
                    next
                else:
                    x_data.append(float(csvline[0]))
                    y_data.append(int(csvline[1]))
  
        #plot histogram
        dx_min = min([x_data[i]-x_data[i-1] for i in range(1,len(x_data))])
        fig, ax = plt.subplots(figsize=(15,15))
        ax.bar(x_data,y_data,width=dx_min*0.8,label='Data')
        ax.set_title('Histogram')
        ax.set_ylabel('Hits')
        ax.set_xlabel('Time / freq / ...')             
        
        #add filt if needed
        txt_cr='\n'
        if fit:
            if fittype == 'gaussian':
                if kwargs:
                    params,cov = fit_gaussian(x_data, y_data,guess = kwargs['guess'])
                else:
                    params,cov = fit_gaussian(x_data, y_data)
                y_fit = gaussian(x_data,*params)
                sigma=np.sqrt(np.diag(cov))
                print(f'µ1 = {params[0]} -- dev = {sigma[0]}{txt_cr}sigma1 = {params[1]} -- dev = {sigma[1]}{txt_cr}A1 = {params[2]} -- dev = {sigma[2]}{txt_cr}')
            elif fittype == 'bimodal_gaussian':
                if kwargs:
                    params,cov = fit_bimodal_gaussian(x_data, y_data,guess = kwargs['guess'])
                else:
                    params,cov = fit_bimodal_gaussian(x_data, y_data)
                y_fit = bimodal_gaussian(x_data,*params)
                sigma=np.sqrt(np.diag(cov))
                print(f'µ1 = {params[0]} -- dev = {sigma[0]}{txt_cr}sigma1 = {params[1]} -- dev = {sigma[1]}{txt_cr}A1 = {params[2]} -- dev = {sigma[2]}{txt_cr}µ2 = {params[3]} -- dev = {sigma[3]}{txt_cr}sigma2 = {params[4]} -- dev = {sigma[4]}{txt_cr}A2 = {params[5]} -- dev = {sigma[5]}{txt_cr}')
            
            if y_fit.any:
                ax.plot(x_data,y_fit,'--r',label='Fit')
                
        
        #add legend
        ax.legend()
        


                    
        return
    
def gaussian(x,mu,sigma,A):
    #return A*1/(sigma*np.sqrt(2*np.pi))*np.exp(-(x-mu)**2/(2*sigma**2))
    return A*np.exp(-(x-mu)**2/(2*sigma**2))
    
def bimodal_gaussian(x,mu1,sigma1,A1,mu2,sigma2,A2):
    return gaussian(x,mu1,sigma1,A1)+gaussian(x,mu2,sigma2,A2)

def fit_gaussian(xdata,ydata,**kwargs):
    if kwargs:
        params,cov = curve_fit(gaussian, xdata, ydata,kwargs['guess'])
    else:
        params,cov = curve_fit(gaussian, xdata, ydata)
    return params,cov

def fit_bimodal_gaussian(xdata,ydata,**kwargs):
    if kwargs:
        params,cov = curve_fit(bimodal_gaussian, xdata, ydata,kwargs['guess'])
    else:
        params,cov = curve_fit(bimodal_gaussian, xdata, ydata)
    return params,cov
    