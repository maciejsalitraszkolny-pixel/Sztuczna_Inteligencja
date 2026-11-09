1. 
Przebuduj poniższy skrypt analizy postaci RPG tak, aby całkowicie zrezygnować z list słowników na rzecz tablic NumPy. Zdefiniuj stałe NAZWY (jako np.array ciągów znaków), STATYSTYKI (jako dwuwymiarowa tablica float dla kolumn: HP, atak, obrona, szybkość) oraz WAGI [0.20, 0.40, 0.25, 0.15]. Napisz funkcję walidującą waliduj(nazwy, dane), która sprawdza, czy dane mają 2 wymiary i poprawny kształt (len(nazwy) x 4), czy nazwy są unikatowe, czy liczba postaci $\ge 2$ oraz czy wszystkie wartości są skończone i nieujemne (w razie błędów rzuć ValueError). Zachowaj oryginalne wartości statystyk postaci z wersji bazowej.

Cel promptu: Usunięcie list słowników na rzecz czystych, zoptymalizowanych tablic NumPy oraz zabezpieczenie wejścia.

Działanie:

Zdefiniowano stałe jako tablice NumPy (NAZWY, STATYSTYKI, WAGI).

Napisano funkcję waliduj(nazwy, dane), która sprawdza m.in. czy liczba postaci jest większa lub równa 2, czy macierz ma właściwy kształt, czy nazwy są unikatowe oraz czy w statystykach nie ma wartości ujemnych, NaN lub Inf.
-----------------------------------------------------------------------------------------------------
2. 
Dołącz do stworzonego kodu funkcję normalizuj(dane), która wykonuje normalizację min-max wzdłuż kolumn (axis=0). Zabezpiecz kod przed dzieleniem przez zero dla kolumn o stałej wartości (użyj np.divide z parametrem where=rozpietosc != 0 i out=np.zeros_like). Następnie napisz funkcję oblicz_sile(dane), która wykorzystując znormalizowane dane oraz tablicę WAGI, oblicza siłę postaci w sposób wektorowy (operator mnożenia macierzowego @). Zweryfikuj, czy wynik zwraca jednowymiarową tablicę sił.

Cel promptu: Wprowadzenie skalowania statystyk oraz efektywnego obliczania siły.

Działanie:

Dodano funkcję normalizuj(dane), która skaluje cechy wzdłuż kolumn (axis=0) przy użyciu bezpiecznego dzielenia (np.divide z masek where i out), zapobiegając błędom przy kolumnach o stałej wartości.

Stworzono funkcję oblicz_sile(), która wykonuje szybkie mnożenie macierzowe za pomocą operatora @ z wagami.
-----------------------------------------------------------------------------------------------------
3. 
Rozbuduj analizator o dwie nowe funkcje analityczne działające na tablicach NumPy:
1. okresl_role(dane) – przydzielającą role przy użyciu np.select według kryteriów: Szturmowiec (atak $\ge 35$ i szybkość $\ge 12$), Obrońca (HP $\ge 120$ i obrona $\ge 18$), a w pozostałych przypadkach Wszechstronny.
2. macierz_pojedynkow(sila) – obliczającą macierz prawdopodobieństw wygranej $N \times N$ wzorem sigmoidalnym $1 / (1 + \exp(-8 \cdot różnice))$, gdzie różnice to macierzowe odchyłki siły między postaciami. Przekątna macierzy (pojedynki z samym sobą) musi być sztywno ustawiona na 0.5 za pomocą np.fill_diagonal.

Cel promptu: Rozbudowa warstwy analitycznej o automatyczny przydział ról oraz macierz szans na wygraną.

Działanie:
Dodano funkcję okresl_role(dane), która za pomocą wektorowej funkcji np.select przypisuje postaciam role (Szturmowiec, Obrońca, Wszechstronny).

Stworzono funkcję macierz_pojedynkow(sila), która oblicza macierz prawdopodobieństw wygranej ($N \times N$) przy użyciu funkcji sigmoidalnej i wyrównuje przekątną do 0.5 za pomocą np.fill_diagonal.

-----------------------------------------------------------------------------------------------------
4. 
Dodaj funkcję zapisz_csv(sciezka, nazwy, role, sila, srednie_szanse, ranking), która zapisuje wyniki do pliku CSV z kodowaniem utf-8-sig, separatorem ; oraz nagłówkiem: Miejsce;Postać;Rola;Siła;Średnia szansa wygranej. Wartości siły sformatuj do 4 miejsc po przecinku, a średnią szansę wygranej (wyliczoną ze średniej wierszowej macierzy pojedynków) jako procent z dwoma miejscami po przecinku. Następnie napisz funkcję testy(), która za pomocą np.testing.assert_allclose przetestuje poprawność działania funkcji normalizuj (np. dla małej macierzy testowej) oraz symetrię i przekątną macierzy pojedynków.

Cel promptu: Umożliwienie zapisu wyników do pliku oraz automatyczna weryfikacja poprawności obliczeń.

Działanie:

Napisano funkcję zapisz_csv(), która zapisuje gotowy ranking do pliku z kodowaniem utf-8-sig (poprawne wyświetlanie polskich znaków np. w Excelu), separatorem ; oraz odpowiednim formatowaniem liczb i procentów (:.2%).

Dodano funkcję testy() korzystającą z np.testing.assert_allclose, która testuje poprawność normalizacji na małych danych oraz symetrię i przekątną macierzy pojedynków.
-----------------------------------------------------------------------------------------------------
5. 
Zintegruj wszystkie napotkane komponenty w spójną funkcję główną main(). Wewnątrz niej wykonaj walidację, uruchom testy jednostkowe, oblicz siłę, wyznacz role, stwórz macierz pojedynków i oblicz średnie szanse wygranej dla każdej postaci. Wygeneruj ranking postaci od najsilniejszej do najsłabszej przy użyciu np.argsort(-sila, kind='stable'). Na końcu wywołaj funkcję zapisującą wyniki do pliku CSV pod nazwą ranking_postaci.csv. Kod musi być w pełni uruchomieniowy i odporny na błędy.

Cel promptu: Spięcie wszystkich elementów w jeden spójny, odporny na błędy skrypt z procedurą uruchomieniową.

Działanie:

Utworzono funkcję główną main() zabezpieczoną blokiem try...except.

Wdrożono stabilne sortowanie rankingu postaci za pomocą np.argsort(-sila, kind='stable'), co gwarantuje deterministyczną kolejność przy identycznych wynikach siły.

Zdefiniowano docelowy plik wyjściowy ranking_postaci.csv.

