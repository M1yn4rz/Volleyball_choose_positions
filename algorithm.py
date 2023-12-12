import pandas as pd



# Funkcja znajdująca suboptymalny skład do gry w siatkówke
def select_positions(people = None, number_players = 14, libero = True, fill = False):

    with open('raport.txt', 'w', encoding = 'utf8') as f:

        print("\nOptions:\n")
        print("\tNumber of players:", number_players)
        print("\tLibero:", libero)
        print("\tFill:", fill, "\n")

        f.write("Options:\n")
        f.write("\n\tNumber of players: " + str(number_players))
        f.write("\n\tLibero: " + str(libero))
        f.write("\n\tFill: " + str(fill) + "\n")

        # Załadowanie pliku z danymi o pozycjach i osobach
        data = pd.read_csv('data.csv')

        # Utworzenie nowej zmiennej, pod którą będzie zapisana część pliku data
        # uwzględniająca tylko 14 konkretnych osób do gry
        new_data = pd.DataFrame()

        # Sprawdzenie czy jest odpowiednia liczba osób do rozdzielenia pozycji
        if len(people) != number_players and not fill:
            fill = True
            print('ERROR - Incorrect number of players')
            print("Fill:", fill)
            f.write('\nERROR - Incorrect number of players')
            f.write("\nFill: " + str(fill) + "\n")

        continue_permit = True

        # Przepisywanie danych ze zmiennej data do zmiennej new_data poprzez nazwę zawodnika
        for player in people:
            name, surname = player.split(' ')
            new_data = new_data._append(data.loc[(data['Name'] == name) & (data['Surname'] == surname)], ignore_index=True)

            # Sprawdzenie czy dana osoba została zapisana i wyświetlenie komunikatu w wypadku nie wpisania jej do zmiennej new_data
            if len(data.loc[(data['Name'] == name) & (data['Surname'] == surname)]) == 0:
                print('ERROR -', name, surname, "hasn't been written")
                f.write('\nERROR - ' + str(name) + ' ' + str(surname) + " hasn't been written")
                continue_permit = False
        
        if not continue_permit:
            print('\nERROR - interruption of program operation - not everyone has been written\n')
            f.write('\n\nERROR - interruption of program operation - not everyone has been written')
            return None

        print("\nPeople to add:\n\n", new_data)
        f.write("\nPeople to add:\n\n" + str(new_data))

        # Utworzenie zmiennej, do której będą zapisywane osoby do gry na danych pozycjach
        players = {'R' : [], 'L' : [], 'A' : [], 'S' : [], 'P' : []}

        # Zmienna przechowująca indeksy głównych pozycji
        positions = ['R', 'L', 'A', 'S', 'P']
        positions_not_libero = ['R', '', 'A', 'S/L', 'P']

        # Zmienna przechowująca indeksy drugich pozycji
        second_positions = ['(R)', '(L)', '(A)', '(S)', '(P)']

        # Utworzenie listy indeksów osób ze zmiennej new_data
        list_of_id = [i for i in range(len(new_data))]

        # Utworzenie listy przechowującej pełne nazwy pozycji

        if libero:
            names_positions = ['Setters', 'Liberos', 'Opposite Hitters', 'Middle Blockers', 'Outside Hitters']
            positions_print = positions
        else:
            names_positions = ['Setters', '', 'Opposite Hitters', 'Middle Blockers/Liberos', 'Outside Hitters']
            positions_print = positions_not_libero

        # Utworzenie zmiennej przechowującej dane o deficycie osób na danych pozycjach
        standard_value = [-2, -2, -2, -4, -4]

        if number_players == 12:
                if libero:
                    standard_value[3] = -2
                else:
                    standard_value[1] = 0



        if not fill:

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
                    print("\nERROR - impossible to organize teams")
                    f.write("\n\nERROR - impossible to organize teams")
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

        else:

            # Przepisanie deficytu pozycji do zmiennej tymczasowej
            positions_count = standard_value.copy()

            # Liczenie deficytu i nadmiaru osób na każdą pozycje
            for i in list_of_id:
                pos = new_data['Positions'][i].split(';')
                for j in range(5):
                    if positions[j] in pos:
                        positions_count[j] += 1

            change = True

            while change:

                change = False

                for pos_ID in range(5):
                    if positions_count[pos_ID] <= 0 and standard_value[pos_ID] < 0:
                        list_of_id_copy = list_of_id.copy()
                        for candidate in list_of_id_copy:
                            pos = new_data['Positions'][candidate].split(';')
                            if positions[pos_ID] in pos:
                                name = new_data['Name'][candidate]
                                surname = new_data['Surname'][candidate]
                                players[positions[pos_ID]].append(name + ' ' + surname)
                                new_data = new_data.drop(candidate)
                                standard_value[pos_ID] += 1
                                positions_count[pos_ID] -= 1
                                list_of_id.remove(candidate)
                                change = True

                positions_count = standard_value.copy()

                # Liczenie deficytu i nadmiaru osób na każdą pozycje
                for i in list_of_id:
                    pos = new_data['Positions'][i].split(';')
                    for j in range(5):
                        if positions[j] in pos:
                            positions_count[j] += 1

            while min(standard_value) < 0:
                for pos_ID in range(5):
                    if standard_value[pos_ID] < 0:
                        for _ in range(-standard_value[pos_ID]):
                            players[positions[pos_ID]].append('(Player to add)')
                        standard_value[pos_ID] = 0



        # Wyświetlenie graczy na danych pozycjach
        print("\nPlayers in positions:")
        f.write("\n\nPlayers in positions:")

        for i in range(5):
            print("\n\t" + names_positions[i] + ':')
            f.write("\n\n\t" + str(names_positions[i]) + ":")
            for e in players[positions[i]]:
                print('\t\t(' + str(positions_print[i]) + ') -', e)
                f.write("\n\t\t(" + str(positions_print[i]) + ") - " + str(e))
        print()

        if len(new_data):

            print("Not add players:\n\n", new_data, "\n")
            f.write("\n\nNot add players:\n\n" + str(new_data))

        f.close()