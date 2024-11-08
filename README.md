## Instrukcja uruchomienia aplikacji

Poniżej znajdują się kroki, które należy wykonać, aby uruchomić aplikację na lokalnym serwerze:

### Wymagania wstępne

Upewnij się, że masz zainstalowane:
- **Python 3.7+** – [Pobierz Python](https://www.python.org/downloads/)
- **Git** – [Pobierz Git](https://git-scm.com/downloads)
- **Wirtualne środowisko Python (virtualenv)** – można je zainstalować za pomocą poniższej komendy:
  ```bash
  pip install virtualenv
  ```

### Krok 1: Klonowanie repozytorium

Sklonuj repozytorium projektu za pomocą Gita:
```bash
git clone <URL_REPOZYTORIUM>
cd <NAZWA_FOLDERU_PROJEKTU>
```

### Krok 2: Utworzenie i aktywacja wirtualnego środowiska

Utwórz nowe wirtualne środowisko i aktywuj je:
```bash
python -m venv venv
# Na systemach Windows
venv\Scripts\activate
# Na systemach Unix/MacOS
source venv/bin/activate
```

### Krok 3: Instalacja zależności i dodanie zmiennej 

Zainstaluj wymagane biblioteki Python:
```bash
$env:FLASK_APP = "main.py"
pip install -r requirements.txt
```

### Krok 4: Uruchomienie aplikacji

Uruchom aplikację Flask:
```bash
flask run
```
Aplikacja będzie dostępna pod adresem `http://127.0.0.1:5000`.

### Krok 5: Zatrzymanie aplikacji

Aby zatrzymać aplikację, naciśnij `Ctrl + C` w terminalu.

# Dokumentacja projektu: Aplikacja do śledzenia czasu pracy

## Członkowie zespołu:
- **Aleksandra Adamiak**
- **Maja Chlipała**
- **Paweł Klocek**
- **Kamil Hebda**

---

## 1. Macierz kompetencji zespołu

| Kompetencje             | Ola | Maja | Paweł | Kamil |
|-------------------------|-----|------|-------|-------|
| Znajomość algorytmów    | TAK | TAK  | TAK   | TAK   |
| Znajomość Excela        | TAK | TAK  | NIE   | TAK   |
| Znajomość j. angielskiego| TAK | TAK  | TAK   | TAK   |
| Obsługa GitLab          | TAK | TAK  | TAK   | TAK   |
| Programowanie Python     | TAK | TAK  | TAK   | TAK   |
| Programowanie SQL        | TAK | TAK  | TAK   | TAK   |
| Programowanie C++        | TAK | TAK  | NIE   | NIE   |
| Programowanie Java       | NIE | NIE  | TAK   | TAK   |
| Programowanie Matlab     | NIE | TAK  | NIE   | NIE   |
| Praca w grupie           | TAK | NIE  | TAK   | TAK   |
| Testowanie oprogramowania| TAK | TAK  | TAK   | NIE   |

---

## 2. Pytania i odpowiedzi związane z projektem

| Pytanie                                 | Odpowiedź                                               | Uwagi                          |
|-----------------------------------------|---------------------------------------------------------|--------------------------------|
| W jakim terminie należy oddać aplikację?| 6 listopada 2024 (środa)                                |                                |
| Jak mają być generowane raporty?        | W ciągu 1 sekundy                                       |                                |
| W jakiej formie ma być aplikacja?       | Aplikacja webowa                                        |                                |
| Jak ma się logować admin?               | Za pomocą ID admina i hasła, ID opisane jako „admin”   | ID w bazie danych             |
| Jak przeprowadzana jest weryfikacja?    | Za pomocą ID pracownika, numeru stanowiska i hasła       |                                |
| Zarządzanie bazą pracowników            | Admin zarządza danymi, dodaje/usuwa pracowników i hasła  |                                |
| Jak generowany jest raport?             | Raport generowany w Excelu, zawiera historię czasu pracy | Zawiera ID pracownika i numer stanowiska |
| Czy wszystkie wymagania są spełnione?   | TAK                                                     |                                |

---

## 3. Ustalony format danych wejściowych

| ID | Numer stanowiska | Hasło/Token | Zdjęcie |
|----|------------------|-------------|---------|
| int (unique) | numer stanowiska | Generowane przez admina, wpisywane przez pracownika | .png |

---

## 4. Opis modelowanego systemu

|                              |                                                                                                                                                             |
|------------------------------|-------------------------------------------------------------------------------------------------------------------------------------------------------------|
| **Aktorzy**                  | Admin, pracownicy                                                                                                                                           |
| **Opis**                     | Celem działania jest pełen wgląd w czas pracy pracowników firmy w celu dokładniejszej kontroli ich wydajności w ramach kwartalnej/miesięcznej ewaluacji.    |
| **Dane**                     | Czas rozpoczęcia i zakończenia pracy w danym dniu.                                                                                                          |
| **Wyzwalacz**                | Admin – przycisk „wygeneruj raport”.                                                                                                                         |
| **Odpowiedź**                | Raport: prezentacja czasu pracy pracownika w Excel.                                                                                                          |
| **Uwagi**                    | Czas pracy nie powinien przekraczać maksymalnie 12 godzin danego dnia.                                                                                       |

---

## 5. Diagramy UML:

### Diagram przypadków użycia 
```mermaid
graph TD
    A[Admin] -->|Generuje raport| B[System]
    B -->|Zapisuje dane| C[Baza danych]
    D[Pracownik] -->|Rejestruje czas pracy| B
```
### Diagram przepływu danych
```mermaid
graph LR
    A[Admin] --> B[Logowanie]
    B --> C[Weryfikacja]
    D[Pracownik] --> E[Rejestracja pracy]
    C --> F[Zapis danych do bazy]
    A -->|Pobiera raport| F
    F -->|Generuje raport| G[Excel]
```
### Diagram sekwencyjny UML
```mermaid
sequenceDiagram
    participant Pracownik
    participant System
    participant Admin
    Pracownik->>System: Logowanie
    System->>System: Weryfikacja
    Pracownik->>System: Rejestracja czasu pracy
    System->>BazaDanych: Zapis danych
    Admin->>System: Generowanie raportu
    System->>Admin: Raport w Excelu
```

## 6. Architektura systemu:
System składa się z trzech głównych komponentów:

- **Logowanie i weryfikacja użytkownika** – system umożliwia poprawną autoryzację pracowników.
- **Baza danych** – gromadzi i segreguje informacje o czasie pracy.
- **Generowanie raportów** – admin może wygenerować raport na podstawie danych z bazy.

## 7. Język implementacji: Python

Uzasadnienie: wszyscy członkowie zespołu podali w kompetencjach umiejętność programowania w Pythonie, zatem jest to opcja najwygodniejsza do wprowadzenia – cały zespół będzie mógł współpracować na równym poziomie. Dodatkowo za Pythonem przemawia doświadczenie w tworzeniu stron internetowych po semestralnym kursie, w którym uczestniczył każdy z członków zespołu.

---


