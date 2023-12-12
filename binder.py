import pandas as pd



def main():

    data = pd.read_csv('data.csv')
    new_data = data.copy()
    new_data = new_data.sort_values(by=['Name', 'Surname'], ascending=True)
    new_data['ID'] = range(1, len(new_data) + 1)
    new_data.to_csv('data.csv', index = False)



if __name__ == "__main__":

    main()