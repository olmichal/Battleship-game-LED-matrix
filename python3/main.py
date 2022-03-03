#              IMPORTANT!!!!
# BEFORE RUNNING THE CODE TYPE IN TERMINAL:
#
#      sudo chmod a+rw /dev/ttyUSB0

import serial
import time
import sys
import random
from rgbmatrix import RGBMatrix, RGBMatrixOptions


# Configuration for the matrix
options = RGBMatrixOptions()
options.rows = 16
options.cols = 32
options.chain_length = 1
options.parallel = 1
options.hardware_mapping = 'regular' 
options.brightness = 50
matrix = RGBMatrix(options=options)
    

def stworz_ramki():
    for i in range(0,12):
        matrix.SetPixel(20,i,0,0,255)
        matrix.SetPixel(31,i,0,0,255)
        matrix.SetPixel(0,i,0,0,255)
        matrix.SetPixel(11,i,0,0,255)
    
    for i in range(21,31):
        matrix.SetPixel(i,0,0,0,255)
        matrix.SetPixel(i,11,0,0,255)
        matrix.SetPixel(i-20,0,0,0,255)
        matrix.SetPixel(i-20,11,0,0,255)
    
plansza=[[0 for i in range(10)] for j in range(10)]
pole_komputera=[[0 for i in range(10)] for j in range(10)]
pole_gracza=[[0 for i in range(10)] for j in range(10)]
plansza_strzalow_gracza=[[0 for i in range(10)] for j in range(10)]
plansza_strzalow_komputera=[[0 for i in range(10)] for j in range(10)]
statki_komputera=[]
statki_gracza=[]

def zamien_na_zera(matrix):
    for i in range(10):
        for j in range(10):
            if matrix[i][j]=='#':
                matrix[i][j]=0



def sasiad(macierz, wiersz, kolumna):
    sasiedzi = []
    for i in range(-1, 2):
        wiersz_sasiada = wiersz + i
        if wiersz_sasiada >= 0 and wiersz_sasiada <= len(macierz)-1:
            for j in range(-1, 2):
                kolumna_sasiada = kolumna + j
                if kolumna_sasiada >= 0 and kolumna_sasiada <= len(macierz)-1:
                    if kolumna_sasiada == kolumna and wiersz_sasiada == wiersz:
                        continue
                    sasiedzi.append([wiersz_sasiada,kolumna_sasiada])
    return sasiedzi

def utworz_plansze(macierz,statki):
    #rozstaw 4.
    rozstaw_czworke(macierz,statki)

    for i in range(2):
        flag = 0
        while (flag == 0):
            x = random.randrange(0, 10)
            y = random.randrange(0, 10)
            sasiedzi = sasiad(macierz, x, y)
            z=random.randrange(0,2)
            if macierz[x][y] == 0:
                if z==0:
                    sasiedzi=sasiedzi[::-1]
                for z in sasiedzi:
                    sasiedzi_sasiada = sasiad(macierz, z[0], z[1])
                    if macierz[z[0]][z[1]] == 0 and abs(z[0] - x) + abs((z[1] - y)) != 2:
                        for j in sasiedzi_sasiada:
                            if macierz[j[0]][j[1]] == 0 and abs(z[0] - j[0]) + abs(z[1] - j[1]) != 2 and j != [x, y]:
                                macierz[x][y] = 3
                                macierz[z[0]][z[1]] = 3
                                macierz[j[0]][j[1]] = 3
                                statki.append([[x,y],[z[0],z[1]],[j[0],j[1]]])
                                # print((x,y),(z[0],z[1]),(j[0],j[1]))
                                sasiedzi2 = sasiad(macierz, j[0], j[1])
                                sasiedzi.extend(sasiedzi_sasiada)
                                sasiedzi.extend(sasiedzi2)

                                for k in sasiedzi:
                                    macierz[k[0]][k[1]] = '#'

                                for k in sasiedzi:
                                    if k[0] == x and k[1] == y:
                                        macierz[k[0]][k[1]] = 1
                                    elif k[1] == z[1] and k[0] == z[0]:
                                        macierz[k[0]][k[1]] = 1
                                    elif k[0] == j[0] and k[1] == j[1]:
                                        macierz[k[0]][k[1]] = 1

                                flag = 1
                                break
                    break
    #rozstaw 1
    for i in range(4):
        while(True):
            x=random.randrange(0,10)
            y=random.randrange(0,10)
            if macierz[x][y]==0:
                break

        macierz[x][y]=1
        statki.append([[x,y]])
        pom_zakazane=sasiad(macierz,x,y)
        for i in pom_zakazane:
            macierz[i[0]][i[1]]='#'
    #rozstaw 2.
    for i in range(3):
        sasiedzi=[]
        sasiedzi2=[]
        flag=0
        while (flag==0):
            x = random.randrange(0, 10)
            y = random.randrange(0, 10)
            sasiedzi=sasiad(macierz,x,y)
            if macierz[x][y]==0:
                for z in sasiedzi:
                    if macierz[z[0]][z[1]]==0 and abs(z[0]-x)+abs((z[1]-y))!=2:
                        macierz[x][y]=1
                        macierz[z[0]][z[1]]=1
                        statki.append([[x,y],[z[0],z[1]]])
                        sasiedzi2=sasiad(macierz,z[0],z[1])
                        sasiedzi.extend(sasiedzi2)
                        for k in sasiedzi:
                            if k[0]==x and k[1]==y:
                                pass
                            elif k[1]==z[1] and k[0]==z[0]:
                                pass
                            else:
                                macierz[k[0]][k[1]]='#'
                        flag=1
                        break

    return macierz

def rozstaw_czworke(macierz,statki):
    #rozstaw 4
    kierunki = [0, 1, 2, 3]
    kierunek = random.choice(kierunki)
    flaga=1
    while (flaga==1):
        x = random.randrange(0, 10)
        y = random.randrange(0, 10)
        if kierunek==0: # w gore
            if y+3<=9:
                wsp1=[x,y]
                wsp2=[x,y+1]
                wsp3=[x,y+2]
                wsp4=[x,y+3]
                statki.append([wsp1,wsp2,wsp3,wsp4])
                flaga=0

        elif kierunek==1: #w dol
            if y-3>=0:
                wsp1 = [x, y]
                wsp2 = [x, y - 1]
                wsp3 = [x, y - 2]
                wsp4 = [x, y - 3]
                statki.append([wsp1, wsp2, wsp3, wsp4])
                flaga = 0
        elif kierunek==2: # w lewo
            if x-3>=0:
                wsp1 = [x, y]
                wsp2 = [x-1, y]
                wsp3 = [x-2, y]
                wsp4 = [x-3, y]
                statki.append([wsp1, wsp2, wsp3, wsp4])
                flaga=0
        elif kierunek==3:
            if x+3<=9:
                wsp1 = [x, y]
                wsp2 = [x + 1, y]
                wsp3 = [x + 2, y]
                wsp4 = [x + 3, y]
                statki.append([wsp1, wsp2, wsp3, wsp4])
                flaga=0

    macierz[wsp1[0]][wsp1[1]]=1
    macierz[wsp2[0]][wsp2[1]] = 1
    macierz[wsp3[0]][wsp3[1]] = 1
    macierz[wsp4[0]][wsp4[1]] = 1
    """"""
    sasiad1 = sasiad(macierz, wsp1[0], wsp1[1])
    sasiad2 = sasiad(macierz, wsp2[0], wsp2[1])
    sasiad3 = sasiad(macierz, wsp3[0], wsp3[1])
    sasiad4 = sasiad(macierz, wsp4[0], wsp4[1])
    sasiedzi = sasiad1
    sasiedzi.extend(sasiad2)
    sasiedzi.extend(sasiad3)
    sasiedzi.extend(sasiad4)
    for i in sasiedzi:
        macierz[i[0]][i[1]]='#'
    for i in sasiedzi:
        if i[0]==wsp1[0] and i[1]==wsp1[1]:
            macierz[i[0]][i[1]]=1
        elif i[0]==wsp2[0] and i[1]==wsp2[1]:
            macierz[i[0]][i[1]]=1
        elif i[0]==wsp3[0] and i[1]==wsp3[1]:
            macierz[i[0]][i[1]]=1
        elif i[0]==wsp4[0] and i[1]==wsp4[1]:
            macierz[i[0]][i[1]] = 1


def wypisz_plansze(macierz):
    for i in range(10):
        for j in range(10):
            if macierz[i][j] == 1:
                matrix.SetPixel(j+1,i+1,255,255,255)
            print(macierz[i][j], end = " ")
        print('')
        
def wypisz_plansze_1(macierz):
    for i in range(10):
        for j in range(10):   
            print(macierz[i][j], end = " ")
        print('')
        
def czy_zatopiony(statki,ruchy_strzalow):
    for statek in statki:
        sprawdz=all(item in ruchy_strzalow for item in statek)
        if sprawdz==True:
            return True
    return False

def zwroc_wspolrzedne_zatopionego_statku(statki,ruchy_strzalow):
    for statek in statki:
        sprawdz=all(item in ruchy_strzalow for item in statek)
        if sprawdz==True:
            return statek
        
def sasiad_bez_rogow(macierz, wiersz, kolumna):
    sasiedzi = []
    for i in range(-1, 2):
        wiersz_sasiada = wiersz + i
        if wiersz_sasiada >= 0 and wiersz_sasiada <= len(macierz)-1:
            for j in range(-1, 2):
                kolumna_sasiada = kolumna + j
                if kolumna_sasiada >= 0 and kolumna_sasiada <= len(macierz)-1:
                    if kolumna_sasiada == kolumna and wiersz_sasiada == wiersz:
                        continue
                    if abs(kolumna_sasiada-kolumna)+abs(wiersz_sasiada-wiersz)!=2:
                        sasiedzi.append([wiersz_sasiada,kolumna_sasiada])
    return sasiedzi

def rozpocznij_gre():
    ruchy_komputera=[]
    ruchy_gracza=[]
    chwilowe_ruchy_komputera=[]
    dobre_ruchy=[]
    ruch = 'gracz'
    runda_gracza = 1
    zycie_gracza = 20
    zycie_komputera = 20
    pierwszy = 1
    while(zycie_gracza!=0 and zycie_komputera!=0):
        if(ruch=='gracz'):
            if pierwszy == 1:
                dane = ruch_gracza(runda_gracza,plansza_strzalow_gracza,1,21)
                pierwszy = 0
            else:
                dane = ruch_gracza(runda_gracza,plansza_strzalow_gracza,x_dane+1,y_dane+21)
            x=dane[1]-1
            y=dane[0]-21
            #odczytywanie z joysticka
            if plansza_komputera[x][y]!=0:
                zycie_komputera=zycie_komputera-1
                plansza_strzalow_gracza[x][y]=1
                matrix.SetPixel(y+21,x+1,255,0,0)
                ruchy_gracza.append([x,y])
                #print('statki komputera:',statki_komputera)
                #print('ruchy_gracza:',ruchy_gracza)
                if czy_zatopiony(statki_komputera, ruchy_gracza) == True:
                    wspolrzedne_zatopionego = zwroc_wspolrzedne_zatopionego_statku(statki_komputera, ruchy_gracza)
                    sasiedzi_zatopionego = []
                    for wsp in wspolrzedne_zatopionego:
                        sasiedzi_zatopionego.extend(sasiad(plansza_komputera, wsp[0], wsp[1]))
                    for pole in sasiedzi_zatopionego:
                        wsp_x = pole[0]
                        wsp_y = pole[1]
                        if plansza_komputera[wsp_x][wsp_y] == 0:
                            plansza_strzalow_gracza[wsp_x][wsp_y] = 'X'
                            matrix.SetPixel(wsp_y+21,wsp_x+1,0,0,255)
                            
                        else:
                            plansza_strzalow_gracza[wsp_x][wsp_y] = 1
                            matrix.SetPixel(wsp_y+21,wsp_x+1,255,0,0)
                    ruchy_gracza = []
            else:
                plansza_strzalow_gracza[x][y]='X'
                matrix.SetPixel(y+21,x+1,0,0,255)

            ruch= 'komputer'
            print("\n MOJ STRZAL \n")
            wypisz_plansze_1(plansza_strzalow_gracza)
            x_dane = x
            y_dane = y

        if(ruch=='komputer'):
            #print(ruchy_komputera)
            if dobre_ruchy==[]:
                flaga = 0
                while (flaga == 0):
                    x = random.randrange(0, 10)
                    y = random.randrange(0, 10)
                    if [x, y] not in ruchy_komputera:
                        flaga = 1
                ruchy_komputera.append([x, y])
                if plansza_gracza[x][y]!=0:
                    zycie_gracza=zycie_gracza-1
                    dobre_ruchy.extend(sasiad_bez_rogow(plansza_gracza,x,y))
                    chwilowe_ruchy_komputera.append([x,y])
                    plansza_strzalow_komputera[x][y]=1
                    # X,Y - TRAFIONE - TRZEBA ZMIENIC NA CZERWONY
                    matrix.SetPixel(y+1,x+1,255,0,0)
                    if czy_zatopiony(statki_gracza,chwilowe_ruchy_komputera)==True:
                        print('Losowy strzal komputera(trafiony 1. masztowiec) :', x, y)
                        ruchy_komputera.extend(sasiad(plansza_gracza,x,y))
                        sasiedzi_zatopionego=sasiad(plansza_gracza,x,y)
                        for pole in sasiedzi_zatopionego:
                            wsp_x=pole[0]
                            wsp_y=pole[1]
                            if plansza_gracza[wsp_x][wsp_y]!=0:
                                plansza_strzalow_komputera[wsp_x][wsp_y]=1
                                #[WSP_X,WSP_Y] ZMIENIC NA CZERWONE
                                matrix.SetPixel(wsp_y+1,wsp_x+1,255,0,0)
                            else:
                                plansza_strzalow_komputera[wsp_x][wsp_y]='X'
                                #WSP_X,WSP_Y ZMIENIC NA NIEBIESKIE
                                matrix.SetPixel(wsp_y+1,wsp_x+1,0,0,255)
                                ruchy_komputera.append([wsp_x, wsp_y])
                        dobre_ruchy=[]
                        chwilowe_ruchy_komputera=[]
                    else:
                        print('Losowy strzal komputera(trafiony inny niz 1. masztowiec) :', x, y)
                else:
                    print('Nietrafiony losowy strzal')
                    plansza_strzalow_komputera[x][y]='X'
                    #X,Y ZMIENIC NA NIEBIESKIE
                    matrix.SetPixel(y+1,x+1,0,0,255)
            else:
                flaga=0

                while(flaga==0):
                    strzal=random.choice(dobre_ruchy)
                    if strzal not in ruchy_komputera:
                        flaga=1

                ruchy_komputera.append(strzal)
                x,y=strzal[0],strzal[1]
                print('Dobre ruchy:' ,dobre_ruchy)
                dobre_ruchy.remove(strzal)
                if plansza_gracza[x][y]!=0: # jesli komputer trafi
                    print("Trafiony strzal komputera z dobrych",x,y)
                    chwilowe_ruchy_komputera.append([x,y])
                    zycie_gracza=zycie_gracza-1
                    if czy_zatopiony(statki_gracza,chwilowe_ruchy_komputera)==True:
                        print("Zatopiony strzal komputera z dobrych",x,y)
                        #do modyfikacji, trzeba dodac aby wszystkich sasiadow dodawal
                        wspolrzedne_zatopionego=zwroc_wspolrzedne_zatopionego_statku(statki_gracza,chwilowe_ruchy_komputera)
                        sasiedzi_zatopionego=[]
                        for wsp in wspolrzedne_zatopionego:
                            sasiedzi_zatopionego.extend(sasiad(plansza_gracza,wsp[0],wsp[1]))
                        for pole in sasiedzi_zatopionego:
                            wsp_x=pole[0]
                            wsp_y=pole[1]
                            if plansza_gracza[wsp_x][wsp_y]!=0:
                                plansza_strzalow_komputera[wsp_x][wsp_y]=1
                                # WSP_X WSP_Y ZMIENIC NA CZERWONE
                                matrix.SetPixel(wsp_y+1, wsp_x+1,255,0,0)
                            else:
                                ruchy_komputera.append([wsp_x, wsp_y])
                                plansza_strzalow_komputera[wsp_x][wsp_y]='X'
                                # WSP_X WSP_Y ZMIENIC NA NIEBIESKIE
                                matrix.SetPixel(wsp_y+1, wsp_x+1,0,0,255)
                        dobre_ruchy = []
                        print("appendowanie ruchow komputera")
                        ruchy_komputera.extend(sasiad(plansza_gracza,x,y))
                        chwilowe_ruchy_komputera=[]
                    else:
                        print('Strzal trafiony w sasiada, ale nie zatapia:',x,y)
                        plansza_strzalow_komputera[x][y]='1'
                        # X Y ZMIENIC NA CZERWONE
                        matrix.SetPixel(y+1,x+1,255,0,0)
                        dobre_ruchy.extend(sasiad_bez_rogow(plansza_gracza,x,y))
                else:
                    print("Strzal nietrafiony sposrod dobrych rychow:",x,y)
                    plansza_strzalow_komputera[x][y]='X'
                    #X Y ZMIENIC NA NIEBIESKIE
                    matrix.SetPixel(y+1,x+1,0,0,255)
                    #dobre_ruchy.extend(sasiad(plansza_gracza,x,y))
            print("PLANSZA STRZALOW KOMPUTERA\n")
            wypisz_plansze_1(plansza_strzalow_komputera)
            ruch='gracz'
        
    if zycie_gracza == 0:
        print("WYGRAŁ KOMPUTER")
        time.sleep(2)
        sys.exit(0)
    else:
        print("WYGRAŁ GRACZ")
        time.sleep(2)
        sys.exit(0)
        

def ruch_gracza(runda_gracza, plansza_strzalow_gracza,x,y):
    ser = serial.Serial('/dev/ttyUSB0',9600)
    dane_pelne = []
    dane = []
    licznik = 0
    time.sleep(2)
    matrix.SetPixel(y,x,255,255,255)
    while (runda_gracza == 1):
        read0 = ser.readline().strip()
        read = int(read0)
        #print(read)
        if read >= 0 and read <= 1023:
            read_serial = read
        if licznik == 2:
            dane.append(read_serial)
            #sprawdzenie, czy dane są przekazywanie dalej w poprawny sposób
            if dane[0] in [0,1]:
                dane_pelne = dane
            else:
                continue
            dane = []
            licznik = 0
            #po wciśnięciu joysticka oddawany jest strzał i wychodzimy z pętli
            if dane_pelne[0] == 0:
                matrix.SetPixel(y,x,0,0,0)
                matrix.SetPixel(y,x,255,0,255)
                time.sleep(2)
                matrix.SetPixel(y,x,0,0,0)
                runda_gracza = 0
            #ruch góra/dół
            elif dane_pelne[1] < 100:
                if plansza_strzalow_gracza[x-1][y-21] == 'X':
                    matrix.SetPixel(y,x,0,0,255)
                elif plansza_strzalow_gracza[x-1][y-21] == 1:
                    matrix.SetPixel(y,x,255,0,0)
                else:
                    matrix.SetPixel(y,x,0,0,0)
                if x > 1:
                    x = x - 1
                matrix.SetPixel(y,x,255,255,255)
            elif dane_pelne[1] > 900:
                if plansza_strzalow_gracza[x-1][y-21] == 'X':
                    matrix.SetPixel(y,x,0,0,255)
                elif plansza_strzalow_gracza[x-1][y-21] == 1:
                    matrix.SetPixel(y,x,255,0,0)
                else:
                    matrix.SetPixel(y,x,0,0,0)
                if x < 10:
                    x = x + 1
                matrix.SetPixel(y,x,255,255,255)
            #ruch w lewo/prawo
            elif dane_pelne[2] < 100:
                if plansza_strzalow_gracza[x-1][y-21] == 'X':
                    matrix.SetPixel(y,x,0,0,255)
                elif plansza_strzalow_gracza[x-1][y-21] == 1:
                    matrix.SetPixel(y,x,255,0,0)
                else:
                    matrix.SetPixel(y,x,0,0,0)
                if y < 30:
                    y = y + 1
                matrix.SetPixel(y,x,255,255,255)
            elif dane_pelne[2] > 900:
                if plansza_strzalow_gracza[x-1][y-21] == 'X':
                    matrix.SetPixel(y,x,0,0,255)
                elif plansza_strzalow_gracza[x-1][y-21] == 1:
                    matrix.SetPixel(y,x,255,0,0)
                else:
                    matrix.SetPixel(y,x,0,0,0)
                if y > 21:
                    y = y - 1
                matrix.SetPixel(y,x,255,255,255)
        else:
            dane.append(read_serial)
            licznik = licznik + 1
    #zwracamy wspolrzedne joysticka na matrycy        
    return [y,x]


stworz_ramki()
plansza_komputera=utworz_plansze(pole_komputera,statki_komputera)
plansza_gracza=utworz_plansze(pole_gracza,statki_gracza)
zamien_na_zera(plansza_gracza)
zamien_na_zera(plansza_komputera)
wypisz_plansze(plansza_gracza)
print("\n PLANSZA KOMPUTERA \n")
wypisz_plansze_1(plansza_komputera)
rozpocznij_gre()        
x = ruch_gracza(runda_gracza)
print(x)

try:
    print("Press CTRL-C to stop.")
    while True:
        time.sleep(100)
except KeyboardInterrupt:
    sys.exit(0)





        

        