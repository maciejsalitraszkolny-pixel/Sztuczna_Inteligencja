import csv
import numpy as np

# Definicje stałych
NAZWY = np.array([
    "Wojownik", "Mag", "Łucznik", "Paladyn", 
    "Łotrzyk", "Berserker", "Druid", "Strażnik"
], dtype=str)

# Kolumny: [HP (0), atak (1), obrona (2), szybkość (3)]
STATYSTYKI = np.array([
    [120.0, 28.0, 18.0, 9.0],
    [75.0, 44.0, 6.0, 13.0],
    [95.0, 34.0, 10.0, 17.0],
    [140.0, 25.0, 22.0, 7.0],
    [80.0, 39.0, 8.0, 21.0],
    [110.0, 42.0, 7.0, 12.0],
    [105.0, 26.0, 15.0, 14.0],
    [155.0, 18.0, 26.0, 5.0]
], dtype=float)

WAGI = np.array([0.20, 0.40, 0.25, 0.15], dtype=float)


def waliduj(nazwy, dane):
    """Waliduje poprawność danych wejściowych dla systemu postaci."""
    if len(nazwy) < 2:
        raise ValueError("Liczba postaci w tablicy NAZWY musi wynosić co najmniej 2.")
        
    if dane.ndim != 2:
        raise ValueError("Tablica STATYSTYKI musi mieć dokładnie 2 wymiary.")
        
    expected_shape = (len(nazwy), 4)
    if dane.shape != expected_shape:
        raise ValueError(
            f"Niepoprawny kształt tablicy statystyk: {dane.shape}, oczekiwano {expected_shape}."
        )
        
    if len(np.unique(nazwy)) != len(nazwy):
        raise ValueError("Nazwy postaci w tablicy NAZWY muszą być unikatowe.")
        
    if not np.all(np.isfinite(dane)):
        raise ValueError("Wszystkie wartości w tablicy STATYSTYKI muszą być skończone (brak NaN/Inf).")
        
    if not np.all(dane >= 0):
        raise ValueError("Wszystkie wartości w tablicy STATYSTYKI muszą być nieujemne.")


def normalizuj(dane):
    """Wykonuje normalizację min-max wzdłuż kolumn (axis=0) z zabezpieczeniem przed dzieleniem przez zero."""
    min_val = dane.min(axis=0)
    max_val = dane.max(axis=0)
    rozpietosc = max_val - min_val
    
    licznik = dane - min_val
    wynik = np.zeros_like(dane, dtype=float)
    
    np.divide(licznik, rozpietosc, out=wynik, where=rozpietosc != 0)
    return wynik


def oblicz_sile(dane_znormalizowane):
    """Oblicza siłę postaci w sposób wektorowy przy użyciu operatora @ i weryfikuje wymiar wyniku."""
    sily = dane_znormalizowane @ WAGI
    
    if sily.ndim != 1:
        raise ValueError(f"Wynik obliczeń musi być tablicą 1D, a ma wymiar: {sily.ndim}")
        
    return sily


def okresl_role(dane):
    """Przydziela role postaciom na podstawie statystyk za pomocą np.select."""
    hp = dane[:, 0]
    atak = dane[:, 1]
    obrona = dane[:, 2]
    szybkosc = dane[:, 3]
    
    warunki = [
        (atak >= 35) & (szybkosc >= 12),  # Szturmowiec
        (hp >= 120) & (obrona >= 18)     # Obrońca
    ]
    wybory = ["Szturmowiec", "Obrońca"]
    
    return np.select(warunki, wybory, default="Wszechstronny")


def macierz_pojedynkow(sila):
    """Oblicza macierz prawdopodobieństw wygranej w pojedynkach (N x N) za pomocą formuły sigmoidalnej."""
    roznice = sila[:, None] - sila[None, :]
    prawdopodobienstwa = 1 / (1 + np.exp(-8 * roznice))
    np.fill_diagonal(prawdopodobienstwa, 0.5)
    return prawdopodobienstwa


def zapisz_csv(sciezka, nazwy, role, sila, srednie_szanse, ranking):
    """Zapisuje wyniki analizy do pliku CSV z kodowaniem utf-8-sig i separatorem ;."""
    naglowek = ["Miejsce", "Postać", "Rola", "Siła", "Średnia szansa wygranej"]
    
    with open(sciezka, mode="w", encoding="utf-8-sig", newline="") as plik:
        writer = csv.writer(plik, delimiter=";")
        writer.writerow(naglowek)
        
        for miejsce, idx in enumerate(ranking, start=1):
            nazwa = nazwy[idx]
            rola = role[idx]
            s_val = f"{sila[idx]:.4f}"
            szansa_val = f"{srednie_szanse[idx] * 100:.2f}%"
            
            writer.writerow([miejsce, nazwa, rola, s_val, szansa_val])


def testy():
    """Przeprowadza testy jednostkowe z użyciem np.testing.assert_allclose."""
    dane_testowe = np.array([
        [10.0, 100.0],
        [20.0, 200.0],
        [30.0, 150.0]
    ])
    norm_wynik = normalizuj(dane_testowe)
    norm_oczekiwane = np.array([
        [0.0, 0.0],
        [0.5, 1.0],
        [1.0, 0.5]
    ])
    np.testing.assert_allclose(norm_wynik, norm_oczekiwane, err_msg="Test normalizacji min-max nie powiódł się!")
    
    sila_testowa = np.array([1.5, 2.0, 1.0])
    m_p = macierz_pojedynkow(sila_testowa)
    np.testing.assert_allclose(np.diag(m_p), 0.5, err_msg="Przekątna macierzy pojedynków nie jest równa 0.5!")
    np.testing.assert_allclose(m_p + m_p.T, 1.0, err_msg="Macierz pojedynków nie spełnia warunku symetrii dopełniającej!")


def main():
    print("=== URUCHOMIENIE SYSTEMU ANALIZY POSTACI RPG ===")
    try:
        print("[1/5] Uruchamianie testów jednostkowych...")
        testy()
        print("      -> Wszystkie testy przeszły pomyślnie.")

        print("[2/5] Walidacja danych bazowych...")
        waliduj(NAZWY, STATYSTYKI)
        print("      -> Dane wejściowe są poprawne.")

        print("[3/5] Przetwarzanie danych i obliczanie siły...")
        statystyki_norm = normalizuj(STATYSTYKI)
        sily = oblicz_sile(statystyki_norm)
        role = okresl_role(STATYSTYKI)
        macierz_prawdopodobienstw = macierz_pojedynkow(sily)
        
        srednie_szanse = np.mean(macierz_prawdopodobienstw, axis=1)

        print("[4/5] Generowanie rankingu postaci...")
        ranking = np.argsort(-sily, kind='stable')

        sciezka_pliku = "ranking_postaci.csv"
        print(f"[5/5] Zapisywanie wyników do pliku '{sciezka_pliku}'...")
        zapisz_csv(sciezka_pliku, NAZWY, role, sily, srednie_szanse, ranking)
        
        print("\n=== ANALIZA ZAKONCZONA SUKCESEM ===")
        print(f"Wyniki zapisano w pliku: {sciezka_pliku}\n")
        
        print("Końcowa tabela wyników:")
        for miejsce, idx in enumerate(ranking, start=1):
            print(f" {miejsce}. {NAZWY[idx]:10} | Rola: {role[idx]:13} | Siła: {sily[idx]:.4f} | Szansa wygranej: {srednie_szanse[idx]*100:6.2f}%")

    except Exception as e:
        print(f"\n[BŁĄD KRYTYCZNY] Wystąpił problem podczas wykonywania programu: {e}")
        raise

if __name__ == "__main__":
    main()
