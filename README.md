# NFCBusinessCard

## Programowanie Elektronicznej Wizytówki

Ten program służy do programowania kart NTAG 215 za pomocą czytnika Ac122u i biblioteki `smartcard` w Pythonie. Aplikacja korzysta ze wzorca projektowego MVC (Model-View-Controller) i posiada interfejs graficzny oparty na bibliotece `tkinter`.

### Wymagania

- Python 3.10.12 ()
- Biblioteka `pyscard` w wersji 2.0.9
- Biblioteka `tkinter` 

### Instalacja

1. Zainstaluj Python 3.10.12
2. Zainstaluj wymagane biblioteki:

```bash
pip install pyscard
```

### Struktura Projektu

- `main.py` - Główny plik uruchamiający aplikację.
- `model.py` - Model zawierający logikę komunikacji z kartą i czytnikiem.
- `view.py` - Widok odpowiedzialny za interfejs użytkownika.
- `controller.py` - Kontroler obsługujący interakcje między widokiem a modelem.

### Uruchomienie Aplikacji

Aby uruchomić aplikację, wykonaj poniższe polecenie:

```bash
python main.py
```

### Opis Plików

#### main.py

Plik `main.py` inicjalizuje aplikację, tworząc instancje modelu, widoku i kontrolera oraz uruchamia główną pętlę aplikacji.

#### view.py

Plik `view.py` zawiera klasę `CardView`, która odpowiada za interfejs użytkownika. Umożliwia połączenie z czytnikiem, programowanie i czyszczenie karty, a także wysyłanie komend APDU. 

Główne elementy interfejsu:
- Przycisk do połączenia z czytnikiem.
- Przycisk do połączenia z kartą.
- Pola tekstowe do wprowadzenia tekstu, numeru telefonu i URL.
- Przycisk do programowania karty.
- Przycisk do czyszczenia karty.
- Pole tekstowe do wprowadzania komend APDU.
- Pole tekstowe do wyświetlania logów.

#### controller.py

Plik `controller.py` zawiera klasę `CardController`, która odpowiada za obsługę logiki aplikacji. Kontroler waliduje dane wprowadzone przez użytkownika i przekazuje je do modelu.

Główne funkcje kontrolera:
- Połączenie z czytnikiem (`connectToReader`).
- Połączenie z kartą (`connectToCard`).
- Czyszczenie karty (`clear_card`).
- Programowanie karty (`write_card`).
- Walidacja danych i wysyłanie komend APDU do modelu (`validate_and_send_command`).
- Zapisywanie danych NDEF na karcie (`save_data`).

#### model.py

Plik `model.py` zawiera klasę `CardModel`, która odpowiada za bezpośrednią komunikację z czytnikiem i kartą. Model obsługuje funkcje związane z wykrywaniem czytnika, połączeniem z kartą, wysyłaniem komend APDU oraz zapisywaniem i czyszczeniem danych NDEF.

Główne funkcje modelu:
- Wykrywanie dostępnych czytników (`detect_reader`).
- Połączenie z czytnikiem (`connectToReader`) (realnie uzywane tylko do testowania, poniewaz program nie utrzymuje połączenia z urządzeniem - zwalnia je po kazdym wyslaniu komendy).
- Połączenie z kartą (`connectToCard`) (realnie uzywane tylko do testowania, poniewaz program nie utrzymuje połączenia z urządzeniem - zwalnia je po kazdym wyslaniu komendy).
- Czyszczenie karty (`clear_card`) (nadpisywanie zerami wszystkich stron).
- Wysyłanie własnych komend APDU (`send_apdu_command`).
- Zapisywanie danych NDEF (`save_ndef_data`) na karcie.
- Przygotowanie komunikatów NDEF dla URL, numeru telefonu i tekstu (`prepare_url_ndef_message`, `prepare_phone_ndef_message`, `prepare_text_ndef_message`).

### Przykład Użycia

1. Uruchom aplikację za pomocą `python main.py`.
2. Kliknij przycisk "Połącz z czytnikiem" aby nawiązać połączenie z czytnikiem.
3. Kliknij przycisk "Połącz z kartą" aby nawiązać połączenie z kartą.
4. Wprowadź dane do odpowiednich pól tekstowych (Tekst, Numer telefonu, URL).
5. Kliknij przycisk "Programuj kartę" aby zapisać dane na karcie.
6. Kliknij przycisk "Czyść kartę" aby wyczyścić dane z karty.
7. Wprowadź komendę APDU do odpowiedniego pola tekstowego i kliknij "Wyślij Komendę" aby wysłać komendę do karty.
