import pandas as pd


data = pd.read_excel ('G:\Projects\IRODS\REMBI overview+edit3.xlsx')
#Remove the NaN attribute value in column Attribute (empty cell from excel sheet)
data.dropna(subset=['Attribute'], inplace=True)
#Set the column attribute as the index one
data.set_index('Attribute', inplace=True)
#create a dictionnary where key is Attribute (the index) and value is Attribute values
microscopy_dic = data.to_dict()['Attribute values']
#print(microscopy_dic)

for key, value in microscopy_dic.items():
    print(key+':'+str(value))
