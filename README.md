# DOKUMENTACJA
# 1) Do czego służy program i jaką funkcjonalność oferuje?
Program TRANSFORMACJE służy do przeprowadzenia różnych transformacji współrzędnych geodezyjnych.
Oferuje funkcjonalność transformacji z geocentrycznych na elipsoidalne wspołrzędne geodezyjne(BLH) oraz z współrzędnych BLH na geocentryczne.
Obsługuje również transformacje z geocentrycznych na topocentryczne współrzędne NEU.
Dodatkowo umożliwia transformacje współrzędnych BL między różnymi układami odniesienia(np. PL1992, PL2000).
Obsługiwane elipsoidy to WGS84, GRS80, elipsoida Krasowskiego.
# 2) Jakie wymagania należy spełnić by program działał na danym komputerze?
 Należy posiadać oprogramowanie Pythona w wersji 3.x, bibliotekę Numpy, argparse(ArgumentParser).
# 3) Dla jakiego systemu operacyjnego został napisany program?
Program można uruchomić na dowolnym systemie obslugującym Pythona. 
Środowisko Pythona jest dostępne na wielu platformach np. Windows, 
macOS, Linux.
# 4) Jak używać programu TRANSFORMACJE (w tym opis danych wejściowych i wyjściowych) oraz rezultat tych wywołań?
Ten program obsługuje różne elipsoidy, w tym WGS84, Krasowskiego i GRS80. 
Możesz wprowadzać dane ręcznie, korzystając z wiersza poleceń, lub 
wczytywać współrzędne z pliku tekstowego. Aby rozpocząć, otwórz terminal 
w folderze, w którym znajduje się plik programu, i wpisz 
*"python nazwa_pliku.py --input plik.txt --transform funckja --output plik.txt --model "model_elipsoidy"".*
Przykładowe wywołanie dla zamiany współrzędnych XYZ na BLH dla elipsoidy WGS84
*"python transformacje.py --input dane.txt --transform XYZ2BLH --output wyniki.txt --model "elipsoida WGS84"".*
Aby wykonać transformacje xyz2neu należy podać współrzędne orto-kartezjańskie punktu referencyjnego (xa,ya,za) i punktu do przetransformowania(xb,yb,zb). Plik tekstowy powininen wyglądać następująco: 

1234567.890,2345678.910,3456789.920,1234568.891,2345679.911,3456790.921

Współrzędne powinny być podane po przecinku i plik nie może zawierać inncyh danych. Jeżeli chcemy dodać kolejny punkt do liczenia należy to zrobić w nowym wierszu.
Przykładowe wywołanie dla zamiany współrzędnych XYZ na NEU dla elipsoidy krasowskiego
*"python transformacje.py --input dane.txt --transform xyz2neu --output wyniki.txt --model "elipsoida Krasowskiego"".*


Jednostki: 
Współrzędne XYZ należy podać w metrach,
współrzędne elipsoidalne BL w stopniach dziesiętnych i H w metrach,
Po transformacji otrzymamy wyniki:
Współrzędne XYZ w metrach,
współrzędne elipsoidalne BL w stopniach, minutach, sekundach i H w metrach.

  
   Co ważne dane wejściowe w pliku tekstowym powinny przedstawiać się 
   następująco: \
   *3664000.123,1408000.456,5009000.789* \
   *3664000.234,1408000.567,5009000.890* \
   *3664000.345,1408000.678,5009001.001* \
   *3664000.456,1408000.789,5009001.112* \
   *3664000.567,1408000.890,5009001.223*
   W transformacji BLH na PL-2000 lub PL-1992 należy podać tylko wartości B i L.

# 5) Znane błędy oraz nietypowe zachowania programu.
   - Błędy związane z modelem elipsoidy lub systemem współrzędnych:
     Program zwraca błąd w przypadku podania niepoprawnego modelu elipsoidy 
     lub systemu współrzędnych.

   - Błąd w przypadku transformacji XYZ -> BLH:
     Program zwraca błąd dla transformacji XYZ -> BLH w przypadku podania 
     współrzędnych X=0 Y=0, dla których nie jest możliwe jednoznaczne 
     określenie współrzędnych w układzie BLH.

   - Niepoprawne transformacje np. XYZ -> PL-1992 oraz XYZ -> PL-2000 (program nie zwróci wyniku)
  

W przypadku wystąpienia któregokolwiek z powyższych wyjątków, program przerywa działanie i zwraca odpowiedni komunikat błędu.







   
