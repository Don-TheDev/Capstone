import pandas as pd

data = pd.read_csv("got_scripts_breakdown.csv", sep=';')

characterName = 'jon'

filtered_data = data[data.Name == characterName]


print(filtered_data)
