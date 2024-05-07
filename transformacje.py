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


    def flh2PL92(self, f, l):
     '''
     Konwersja współrzędnych geodezyjnych na układ współrzędnych płaskich 1992 (PL92).

     Parametry
     ----------
     f : FLOAT
         Zmienna ta przedstawia szerokość geodezyjna.
     l : FLOAT
         Zmienna ta przedstawia długośc geodezyjna.

     Returns
     -------
      X1992, Y1992 : FLOAT
                     Zmienna ta przedstawia współrzędne w układzie 1992.

     '''
     
     if l > 25.5 or l < 13.5:
         raise NotImplementedError(f"{Transformacje.dms(self, np.radians(l))} południk nie jest obsługiwany przez układ współrzędnych płaskich PL1992")
         
     if f > 55 or f < 48.9:
         raise NotImplementedError(f"{Transformacje.dms(self, np.radians(f))} równoleżnik nie jest obsługiwany przez układ współrzędnych płaskich PL1992")
         
     f = np.radians(f)
     l = np.radians(l)
     a2 = self.a**2
     b2 = a2 * (1 - self.e2)
     e_2 = (a2 - b2)/b2
     l0 = np.radians(19)
     dl = l - l0
     dl2 = dl**2
     dl4 = dl**4
     t = np.tan(f)
     t2 = t**2
     t4 = t**4
     n2 = e_2 * (np.cos(f)**2)
     n4 = n2 ** 2
     N = Transformacje.get_np(self, f)
     e4 = self.e2**2
     e6 = self.e2**3
     A0 = 1 - (self.e2/4) - ((3*e4)/64) - ((5*e6)/256)
     A2 = (3/8) * (self.e2 + e4/4 + (15*e6)/128)
     A4 = (15/256) * (e4 + (3*e6)/4)
     A6 = (35*e6)/3072
     sigma = self.a * ((A0 * f) - A2 * np.sin(2*f) + A4 * np.sin(4*f) - A6 * np.sin(6*f))
     xgk = sigma + ((dl**2)/2) * N * np.sin(f) * np.cos(f) * (1 + ((dl**2)/12)*(np.cos(f)**2)*(5 - t2 + 9 * n2 + 4 * n4) + (dl4/360) * (np.cos(f)**4)*(61 - (58 * t2) + t4 + (270 * n2) - (330 * n2 * t2)))
     ygk = dl * N * np.cos(f) * (1 + (dl2/6) * (np.cos(f)**2) * (1 - t2 + n2) + (dl4/120) * (np.cos(f)**4) * (5 - (18 * t2) + t4 + (14 * n2) - 58 * n2 * t2))
     x92 = xgk * 0.9993 - 5300000
     y92 = ygk * 0.9993 + 500000
     return(x92,y92)
 
 
    def flh2PL00(self, f, l):
     '''
     Konwersja współrzędnych geodezyjnych na układ współrzędnych płaskich 2000.

     Parametry
     ----------
     f : FLOAT
         Zmienna ta przedstawia szerokość geodezyjna..
     l : FLOAT
         Zmienna ta przedstawia długośc geodezyjna.

     Returns
     -------
      X2000, Y2000 : FLOAT
                     Zmienna ta przedstawia współrzędne w układzie 2000
     '''
       
     if l >= 13.5 and l < 16.5:
         l0 = np.radians(15)
     elif l >= 16.5 and l < 19.5:
         l0 = np.radians(18)
     elif l >= 19.5 and l < 22.5:
         l0 = np.radians(21)
     elif l >= 22.5 and l <= 25.5:
         l0 = np.radians(24)
     else:
         raise NotImplementedError(f"{Transformacje.dms(self, np.radians(l))} południk nie jest obsługiwany przez układ współrzędnych płaskich PL2000")
     
     if f > 55 or f < 48.9:
         raise NotImplementedError(f"{Transformacje.dms(self, np.radians(f))}równoleżnik nie jest obsługiwany przez układ współrzędnych płaskich PL2000")
         
     f = np.radians(f)
     l = np.radians(l)
     a2 = self.a**2
     b2 = a2 * (1 - self.e2)
     e_2 = (a2 - b2)/b2
     dl = l - l0
     dl2 = dl**2
     dl4 = dl**4
     t = np.tan(f)
     t2 = t**2
     t4 = t**4
     n2 = e_2 * (np.cos(f)**2)
     n4 = n2 ** 2
     N = Transformacje.get_np(self, f)
     e4 = self.e2**2
     e6 = self.e2**3
     A0 = 1 - (self.e2/4) - ((3*e4)/64) - ((5*e6)/256)
     A2 = (3/8) * (self.e2 + e4/4 + (15*e6)/128)
     A4 = (15/256) * (e4 + (3*e6)/4)
     A6 = (35*e6)/3072
     sigma = self.a * ((A0 * f) - A2 * np.sin(2*f) + A4 * np.sin(4*f) - A6 * np.sin(6*f))
     xgk = sigma + ((dl**2)/2) * N * np.sin(f) * np.cos(f) * (1 + ((dl**2)/12)*(np.cos(f)**2)*(5 - t2 + 9 * n2 + 4 * n4) + (dl4/360) * (np.cos(f)**4)*(61 - (58 * t2) + t4 + (270 * n2) - (330 * n2 * t2)))
     ygk = dl * N * np.cos(f) * (1 + (dl2/6) * (np.cos(f)**2) * (1 - t2 + n2) + (dl4/120) * (np.cos(f)**4) * (5 - (18 * t2) + t4 + (14 * n2) - 58 * n2 * t2))
     strefa = round(l0 * 180/np.pi)/3
     x00 = xgk * 0.999923
     y00 = ygk * 0.999923 + strefa * 1000000 + 500000
     return(x00,y00)
 
 
    def get_dXYZ(self, xa, ya, za, xb, yb, zb):
     '''
     Funkcja ta jest wykorzystywana do liczenia róznicy wspolrzędnych punktów A i B, a następnie wykorzystywana do liczenia macierzy NEU.
     
     Parametry
     ----------
     XA, YA, ZA, XB, YB, ZB: FLOAT
                             Zmienna ta przedstawia współrzędne w układzie ortokartezjańskim.

     Returns
     -------
     dXYZ : ARRAY
            Zmienna ta przedstawia macierz różnicy współrzędnych.

     '''
     dXYZ = np.array([xb-xa, yb-ya, zb-za])
     return(dXYZ)
 
 
    def rneu(self, f, l):
     '''
     Funkcja tworzy macierz obrotu R na podstawie szerokości i długości geodezyjnej.

     Parametry
     ----------
     f : FLOAT
         Zmienna ta przedstawia szerokość geodezyjna.
     l : FLOAT
         Zmienna ta przedstawia długośc geodezyjna.

     Returns
     -------
     R ARRAY
       Zmienna ta przedstawia macierz obrotu R.
          
     '''
     f=np.radians(f)
     l=np.radians(l)
     R = np.array([[-np.sin(f)*np.cos(l), -np.sin(l), np.cos(f)*np.cos(l)],
                   [-np.sin(f)*np.sin(l),  np.cos(l), np.cos(f)*np.sin(l)],
                   [np.cos(f),             0,         np.sin(f)          ]])
     return(R)
 
 
    def xyz2neu(self, f, l, xa, ya, za, xb, yb, zb):
     '''
    Funkcja konwertuje współrzędne geodezyjne na współrzędne horyzontalne.


     Parametry
     ----------
     f : FLOAT
         Zmienna ta przedstawia szerokość geodezyjna..
     l : FLOAT
         Zmienna ta przedstawia długośc geodezyjna.
     XA, YA, ZA, XB, YB, ZB: FLOAT
                             Zmienna ta przedstawia współrzędne w układzie orto-kartezjańskim, 

     Returns
     -------
     N, E, U : STR
                Zmienna ta przedstawia współrzędne horyzontalne.
         

     '''
     dX = Transformacje.get_dXYZ(self, xa, ya, za, xb, yb, zb)
     R = Transformacje.rneu(self, f,l)
     neu = R.T @ dX
     n = neu[0];   e = neu[1];   u = neu[2]
     n = "%.16f"%n; e = "%.16f"%e; u="%.16f"%u
     dlugosc = []
     xx = len(n); dlugosc.append(xx)
     yy = len(e); dlugosc.append(yy)
     zz = len(u); dlugosc.append(zz)
     P = 50
     
     while xx < P:
         n = str(" ") + n
         xx += 1
     
     while yy < P:
         e = str(" ") + e
         yy += 1
         
     while zz < P:
         u = str(" ") + u
         zz +=1
         
     return(n, e, u)

