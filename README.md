# DOKUMENTACJA
# 1) Do czego służy program i jaką funkcjonalność oferuje?
Program TRANSFORMACJE służy do przeprowadzenia różnych transformacji współrzędnych geodezyjnych.
Oferuje funkcjonalność transformacji z geocentrycznych na elipsoidalne wspołrzędne geodezyjne(BLH) oraz z współrzędnych BLH na geocentryczne.
Obsługuje również transformacje z geocentrycznych na topocentryczne współrzędne NEU.
Dodatkowo umożliwia transformacje współrzędnych BL między różnymi układami odniesienia(np. PL1992, PL2000).
Obsługiwane elipsoidy to WGS84, GRS80, elipsoida Krasowskiego.
# 2) Jakie wymagania należy spełnić by program działał na danym komputerze?
 Należy posiadać oprogramowanie Pythona w wersji 3.x, bibliotekę Numpy, tkinter, os, ArgumentParser.
# 3) Dla jakiego systemu operacyjnego został napisany program?
Program można uruchomić na dowolnym systemie obslugującym Pythona. 
Środowisko Pythona jest dostępne na wielu platformach np. Windows, 
macOS, Linux.
# 4) Jak używać programu TRANSFORMACJE (w tym opis danych wejściowych i wyjściowych) oraz rezultat tych wywołań?
Chciałbyś korzystać z programu, który umożliwia przekształcanie 
współrzędnych geodezyjnych na ortokartezjańskie oraz odwrotnie? Ten 
program obsługuje różne elipsoidy, w tym WGS84, Krasowskiego i GRS80. 
Możesz wprowadzać dane ręcznie, korzystając z wiersza poleceń, lub 
wczytywać współrzędne z pliku tekstowego. Aby rozpocząć, otwórz terminal 
w folderze, w którym znajduje się plik programu, i wpisz "python 
nazwa_pliku.py".
Jeśli chcesz przekształcić współrzędne XYZ na BLH (szerokość 
geograficzną, długość geograficzną i wysokość), wystarczy podać 
współrzędne XYZ w metrach. Natomiast dla przekształcenia współrzędnych 
BLH na XYZ, wprowadź wartości B i L w stopniach dziesiętnych oraz H w 
metrach.
   
Oto przykłady wykorzystania programu w różnych scenariuszach:
- Przekształcenie współrzędnych XYZ na BLH z wykorzystaniem modelu 
   GRS80:
   *python infa_projekt.py --dane XYZ 3664000.123 1408000.456 5009000.789 --
   model grs80 --uklad BLH --output wyniki.txt*

   WYNIK:
  *fi = 52.0973 [deg]; lam = 21.0315 [deg]; h = 141.399 [m] | BLH | 
  grs80*
 - Przekształcenie współrzędnych z pliku tekstowego z wykorzystaniem 
      modelu GRS80:
   *python infa_projekt.py --input txt --model grs80 -txt wsp_input.txt - 
   txt_out wsp_output.txt*

   Co ważne dane wejściowe w pliku tekstowym powinny przedstawiać się 
   następująco: \
   *3664000.123,1408000.456,5009000.789* \
   *3664000.234,1408000.567,5009000.890* \
   *3664000.345,1408000.678,5009001.001* \
   *3664000.456,1408000.789,5009001.112* \
   *3664000.567,1408000.890,5009001.223*

Jeśli potrzebujesz przekształcić współrzędne XYZ na współrzędne PL-1992 lub PL-2000, bądź na system współrzędnych NEU, także możesz skorzystać z tego programu.
# 5) Znane błędy oraz nietypowe zachowania programu.
   - Błędy związane z modelem elipsoidy lub systemem współrzędnych:
     Program zwraca błąd w przypadku podania niepoprawnego modelu elipsoidy 
     lub systemu współrzędnych.

   - Błąd w przypadku transformacji XYZ -> BLH:
     Program zwraca błąd dla transformacji XYZ -> BLH w przypadku podania 
     współrzędnych X=0 Y=0, dla których nie jest możliwe jednoznaczne 
     określenie współrzędnych w układzie BLH.

   - Nieobsługiwane formaty danych wejściowych:
     Nieobsługiwane są niektóre formaty danych wejściowych, takie jak dane 
     tekstowe.

   - Niepoprawne transformacje XYZ -> PL-1992 oraz XYZ -> PL-2000 dla 
     elipsoidy Krasowskiego:
     Transformacja XYZ -> PL-1992 oraz XYZ -> PL-2000 dla elipsoidy 
     Krasowskiego zwraca błędne wyniki, dlatego też nie powinna być używana.

W przypadku wystąpienia któregokolwiek z powyższych wyjątków, program przerywa działanie i zwraca odpowiedni komunikat błędu.







   
