import algorithm as al



def main():

    people = [  'Michał Bujak',
                'Patryk Nalepka',
                'Bartosz Miklas',
                'Michał Cynarski',
                'Bartosz Młynarski',
                'Mateusz Wirkijowski',
                'Błażej Czyżycki',
                'Jakub Strojewski',
                'Dominik Babiarczyk',
                'Karol Dulak',
                'Jakub Borowiecki',
                'Grzesiek Chmura',
                'Jakub Świeca',
                'Jakub Sobczyk']

    al.select_positions(people, option = 'Name', number_players = 14)



if __name__ == '__main__':
    main()