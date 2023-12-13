import pandas as pd



# Funkcja segregująca plik z danymi osób do gry
def binder():

    # Wczytanie pliku z danymi zawodników
    data = pd.read_csv('data.csv')

    # Utworzenie kopii danych zawodników
    new_data = data.copy()

    # Posortowanie danych zawodników w kolejności alfabetycznej
    new_data = new_data.sort_values(by=['Name', 'Surname'], ascending=True)

    # Ustawienie nowych wartości ID dla zawodników po posortowaniu
    new_data['ID'] = range(1, len(new_data) + 1)

    # Przepisanie nowej posortowanej tabeli do pliku data.csv
    new_data.to_csv('data.csv', index = False)



# Wywołanie funkcji segregującej plik z danymi osób do gry oraz ich pozycjami
if __name__ == "__main__":
    binder()