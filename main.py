import algorithm as al



# Główna funkcja programu
def main():

    # Zmienna z osobami biorącymi udział w grze
    people = ['Karol Dulak',
              'Patryk Nalepka',
              'Jakub Borowiecki',
              'Bajura Kaja',
              'Grzesiek Chmura',
              'Krystian Relidzyński',
              'Łukasz Broś',
              'Jakub Strojewski',
              'Dominik Babiarczyk',
              'Michał Cynarski',
              'Bartosz Młynarski',
              'Mikołaj Wandzel',
              'Karolina Michalik',
              'Kacper Iwicki']

    # Wywołanie algorytmu wybierającego pozycje dla zawodników
    al.select_positions(people)



# Wywołanie funkcji głównej main()
if __name__ == '__main__':
    main()