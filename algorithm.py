import pandas as pd



# Funkcja znajdująca suboptymalny skład do gry w siatkówke
def select_positions(people = None, option = 'ID', number_players = 14):

    # Załadowanie pliku z danymi o pozycjach i osobach
    data = pd.read_csv('data.csv')

    # Utworzenie nowej zmiennej, pod którą będzie zapisana część pliku data
    # uwzględniająca tylko 14 konkretnych osób do gry
    new_data = pd.DataFrame()

    # Sprawdzenie czy jest odpowiednia liczba osób do rozdzielenia pozycji
    if len(people) != number_players:
        print('ERROR - Nieprawidłowa liczba osób')
        return None

    # Przepisywanie danych ze zmiennej data do zmiennej new_data poprzez ID
    if option == 'ID':
        for player in people:
            new_data = new_data._append(data.loc[data['ID'] == player], ignore_index=True)

    # Przepisywanie danych ze zmiennej data do zmiennej new_data poprzez nazwę zawodnika
    elif option == 'Name':
        for player in people:
            name, surname = player.split(' ')
            new_data = new_data._append(data.loc[(data['Name'] == name) & (data['Surname'] == surname)], ignore_index=True)

            # Sprawdzenie czy dana osoba została zapisana i wyświetlenie komunikatu w wypadku nie wpisania jej do zmiennej new_data
            if len(data.loc[(data['Name'] == name) & (data['Surname'] == surname)]) == 0:
                print('\n\nERROR -', name, surname, 'nie został wpisany\n\n')
    
    # W przypadku wyboru innej opcji funkcja nic nie zwraca i wyświetla błąd
    else:
        print("ERROR - nieprawidłowa opcja")
        return None

    # Sprawdzenie czy do zmiennej new_data przepisało się 14 osób
    if len(new_data) != number_players:
        print('ERROR - Nieprawidłowa liczba osób')
        return None

    # Utworzenie zmiennej, do której będą zapisywane osoby do gry na danych pozycjach
    players = {'R' : [], 'L' : [], 'A' : [], 'S' : [], 'P' : []}

    # Utworzenie zmiennej przechowującej dane o deficycie osób na danych pozycjach
    standard_value = [-2, -2, -2, -4, -4]

    if number_players == 12:
            standard_value[1] = 0

    # Zmienna przechowująca indeksy głównych pozycji
    positions = ['R', 'L', 'A', 'S', 'P']
    positions_12 = ['R', '', 'A', 'S/L', 'P']

    # Zmienna przechowująca indeksy drugich pozycji
    second_positions = ['(R)', '(L)', '(A)', '(S)', '(P)']

    # Utworzenie listy indeksów osób ze zmiennej new_data
    list_of_id = [i for i in range(number_players)]

    # Utworzenie listy przechowującej pełne nazwy pozycji
    names_positions = ['Rozgrywający', 'Libero', 'Atakujący', 'Środkowi', 'Przyjmujący']
    names_positions_12 = ['Rozgrywający', '', 'Atakujący', 'Środkowi/Libero', 'Przyjmujący']

    # Główna pętla wyznaczająca pozycje danych osób
    while len(new_data) > 0:

        # Przepisanie deficytu pozycji do zmiennej tymczasowej
        positions_count = standard_value.copy()

        # Liczenie deficytu i nadmiaru osób na każdą pozycje
        for i in list_of_id:
            pos = new_data['Positions'][i].split(';')
            for j in range(5):
                if positions[j] in pos or second_positions[j] in pos:
                    positions_count[j] += 1

        # W wypadku braku liczby osób na daną pozycje zakończenie działania funkcji
        # oraz wyświetlenie odpowiedniego komunikatu
        if min(positions_count) < 0:
            print(positions_count)
            print(players)
            print("ERROR - nie da się ułożyć teamów")
            return None

        # Utworzenie zmiennych pomocniczych do szukania aktualnej pozycji do przydzielenia
        ID_pos = None
        min_pos_count = float('inf')

        # Pętla szukająca odpowiedniej pozycji do przydzielenia w tej iteracji
        for i in range(len(positions_count)):
            if positions_count[i] < min_pos_count and standard_value[i] != 0:
                min_pos_count = positions_count[i]
                ID_pos = i

        # Utworzenie zmiennej przechowującej kandydatów do grania na wybranej powyżej pozycji
        candidates_ID = []

        # Wyznaczenie kandydatów do gry na wybranej pozycji poprzez główne pozycje
        for i in list_of_id:
            pos = new_data['Positions'][i].split(';')
            if positions[ID_pos] in pos:
                candidates_ID.append(i)
        
        # Jeżeli nie ma żadnego kandydata do gry na wybranej pozycji z ustawioną pozycją główną
        # to wtedy szukamy kandydatów z ustawioną tą pozycją jako drugą
        if len(candidates_ID) == 0:
            for i in list_of_id:
                pos = new_data['Positions'][i].split(';')
                if second_positions[ID_pos] in pos:
                    candidates_ID.append(i)

        # Utworzenie zmiennej pomocniczej przechowującą liczbę ewentualnych pozycji do grania
        # przez danego zawodnika
        other_pos = float('inf')

        # Wybranie z pośród liczby kandydatów osoby, która powinna zostać przydzielona do wybranej
        # pozycji w tej iteracji poprzez minimalizacji zmiennej "other_pos"
        for i in candidates_ID:
            pos = new_data['Positions'][i].split(';')
            number_pos = 0
            for j in range(5):
                if positions[j] in pos and standard_value[j] != 0 and j != ID_pos:
                    number_pos += 1
            if number_pos < other_pos:
                other_pos = number_pos
                candidate = i

        # Zaktualizowania zmiennej new_data, przypisanie kandydata do słownika z pozycjami
        # oraz usunięcie tego gracza ze zmiennej new_data
        name = new_data['Name'][candidate]
        surname = new_data['Surname'][candidate]
        players[positions[ID_pos]].append(name + ' ' + surname)
        new_data = new_data.drop(candidate)
        standard_value[ID_pos] += 1
        list_of_id.remove(candidate)

    # Wyświetlenie graczy na danych pozycjach

    if number_players == 14:

        print()
        for i in range(5):
            print(names_positions[i] + ':')
            for e in players[positions[i]]:
                print('\t(' + str(positions[i]) + ') -', e)
        print()

    elif number_players == 12:

        print()
        for i in range(5):
            if i != 1:
                print(names_positions_12[i] + ':')
                for e in players[positions[i]]:
                    print('\t(' + str(positions_12[i]) + ') -', e)
        print()

    else:
        print("ERROR - nieprawidłowa liczba graczy")
