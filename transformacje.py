# -*- coding: utf-8 -*-
"""
Created on Tue May  7 20:44:05 2024

@author: 48514
"""

import numpy as np
import tkinter as tk
import os as os
from argparse import ArgumentParser


class Transformacje:
    
    def __init__(self, model: str="WGS84"):
        """
        Parametry elipsoid:
            a - duża półoś elipsoidy
            e2 - mimośród
        + WGS84: https://pl.wikipedia.org/wiki/System_odniesienia_WGS_84
        + Alternatywne powierzchnie odniesienia: http://uriasz.am.szczecin.pl/naw_bezp/Powierzchnie.html
        """
        
        if model == "elipsoida WGS84":
            self.a = 6378137.000
            self.e2 = 0.00669437999013
        elif model == "elipsoida Krasowskiego":
            self.a = 6378245.000
            self.e2 = 0.00669342162296
        elif model == "elipsoida GRS80":
            self.a = 6378137.000
            self.e2 = 0.00669438002290
        else:
            raise NotImplementedError(f"{model} to nieobsługiwana elipsoida - obsługiwane elipsoidy to WGS84, Krasowskiego, GRS80.")

    def dms(self, x):
        '''
        Funkcję 'dms' wykorzystuje się w celu zamiany radianów na stopnie, minuty i sekundy.   

        Parametry
        ----------
        x : FLOAT
            Zmienna ta będzie zamieniana na stopnie, minuty i sekundy.

        Returns
        x : STR
            Zmienna ta przedstawia wynik w stopniach, minutach i sekundach.
        '''
        sig = ' '
        if x < 0:
            sig = '-'
            x = abs(x)
        x = x * 180/np.pi
        d = int(x)
        m = int(60 * (x - d))
        s = (x - d - m/60)*3600
        if s > 59.999995:
            s = 0
            m = m + 1
        if m == 60:
            m = 0
            d = d + 1
        
        d = str(d)
        if len(d) == 1:
            d = "  " + d
        elif len(d) == 2:
            d = " " + d
        elif len(d) == 3:
            d = d
            
        if m < 10:
            m = str(m)
            m = "0" + m
            
        if s < 10:
            s = "%.5f"%s
            s = str(s)
            s= "0" + s
        else:
            s = ("%.5f"%s)
            
        x1=(f'{d}°{m}′{s}″')  
        return(x1)
        
        
    def get_NP(self, f):
        '''
        Funkcja 'get_NP' zwraca wartosc promienia przekroju w I wertykale.
        
        Parameters
        ----------
        f : FLOAT
            Zmienna ta przedstawia szerokość geodezyjna wyrażona w radianach.

        Returns
        -------
        N : float
            Zmienna ta przedstawia promień przekroju w pierwszym wertykale wyrażony w metrach.
        '''
        N = self.a / np.sqrt(1 - self.e2 * np.sin(f)**2)
        return(N)
    
    
    def hirvonen(self, X, Y, Z, output="dec_degree"):
        '''
        Funkcja Hirvonena wykorzystywana jest do zamiany współrzędnych ortokartezjańskich (X,Y,Z) na współrzędne
        geodezyjne (FI,LAMBDA,H).
        
        Parametry
         ----------
         X, Y, Z : FLOAT
              Zmienna ta przedstawia współrzędne w układzie ortokartezjańskim. 

         Returns
         -------
         fi : FLOAT
              Zmienna ta przedstawia szerokość geodezyjna.
         lam : FLOAT
               Zmienna ta przedstawia dlugośc geodezyjna.
         h : FLOAT
             Zmienna ta przedstawia wysokość elipsoidalna.
         output [STR] - opcjonalnie
             dec_degree - przedstawia stopnie dziesiętne
             radiany - radiany 
             dms - stopnie, minuty, sekundy
         """
        '''

        p = np.sqrt(X**2 + Y**2)
        f = np.arctan(Z/(p * (1 - self.e2)))
        while True:
            N = Transformacje.get_np(self, f)
            h = (p / np.cos(f)) - N
            fp = f
            f = np.arctan(Z / (p * (1 - self.e2 * (N / (N+h)))))
            if np.abs(fp - f) < (0.000001/206265):
                break
        l = np.arctan2(Y, X)
        if output == "dec_degree":
            fi=(f*180/np.pi)
            lam=(l*180/np.pi)
            return (fi, lam, h)
        elif output == "dms":
            fi = Transformacje.dms(self, f)
            lam = Transformacje.dms(self, l)
            return (fi,lam,h) 
        elif output == 'radiany':
            fi=f
            lam=l
            return(f,l,h)
        else:
            raise NotImplementedError(f"{output} - output format not defined")

    
    
    def flh2XYZ(self, f, l, h):
        '''
        Funkcja ta jest odwrotnoscią algorytmu Hirvonena, zamienia wspólrzędne geodezyjne na ortokartezjanskie.
        Parametry
        ----------
        f : FLOAT
            Zmienna ta przedstawia szerokość geodezyjna.
        l : FLOAT
            Zmienna ta przedstawia długośc geodezyjna.
        h : FLOAT
            Zmienna ta przedstawia wysokość elipsoidalna.
        Returns
        -------
         X, Y, Z : FLOAT
                   Zmienna ta przedstawia współrzędne w układzie ortokartezjańskim.

        '''
        f=np.radians(f)
        l=np.radians(l)
        N = Transformacje.get_np(self, f)
        X = (N + h) * np.cos(f) * np.cos(l)
        Y = (N + h) * np.cos(f) * np.sin(l)
        Z = (N * (1 - self.e2) + h) * np.sin(f)
        return(X,Y,Z)

