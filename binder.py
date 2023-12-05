import pandas as pd



def data_binder():

    data = pd.read_csv('data.csv')

    new_data = data.sort_values(by = ['Name', 'Surname'], ascending = True)

    for i in range(len(data)):
        new_data['ID'][i] = i + 1

    new_data.to_csv('data.csv', index=False)



def main():

    data_binder()



main()