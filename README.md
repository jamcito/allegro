Projekt z przedmiotu "Wprowadzenie do semantyki języka naturalnego"

Automatyczna kategoryzacja aukcji allegro na podstawie zrzutu części bazy serwisu.

----

Projekt składa się z dwóch części:

* crawlera który posłużył do stworzenia plików .dat zamieszczonych w repozytorium
* programu korzystającego z pobranych danych, wyszukującego najpodobniejszej do zadanej aukcji oraz jej kategorii

Crawler pozbawiony został prywatnych danych (loginu, hasła, klucza) i nie będzie funkcjonalny bezpośrednio po pobraniu z repozytorium. Należy w tym celu podać własne dane z serwisu allegro.

----

Sposób realizacji zadania:
* Wszystkie aukcje pozbawiane są interpunkcji i sprowadzane do formy podstawowej
* Usuwane są słowa występujące tylko raz
* Aplikowana jest stoplista
* Na tak przetworzonej liście aukcji budowana jest mapa częstości poszczególnych słów
* Zadana aukcja którą chcemy kategoryzować przetwarzana jest analogicznie jak pozostałe
* Zadana aukcja porównywana jest z każdą inną pod kątem wspólnych słow. Za każde takie słowo aukcja dostaje 1 / (ilość wystąpień słowa) punktów. W ten sposób promujemy słowa rzadkie. Aukcja o największej ilości punktów zwracana jest jako najbardziej podobna, a jej kategorie jako najbardziej prawdopodobne kategorie aukcji o którą pytamy

----

Sposób uruchamiania:
* Zadanie zrealizowano w języku Python 2.7
* W celu uruchomienia crawlera należy z katalogu projektu wykonać komendę: "python crawler-public.py". Słowa po których przeglądamy bazę allegro zawarte są w kodzie.
* W celu uruchomienia właściwego zadania, należy z katalogu projektu wykonać komendę: "python reader.py". Przykładowe zapytania do programu zawarte są w kodzie, na dole pliku reader.py
