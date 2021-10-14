from io import FileIO
import wikipedia
import pandas
import re

page = wikipedia.page("List of United States cities by population")
html = page.html()
cities_df = pandas.read_html(html)[4]
city_names = cities_df.iloc[:, 1]
pat = "\\[(.+)\\]"
cleaned_names = []
for i, name in enumerate(city_names):
    cleaned_names.append(re.split(pat, name)[0])

# cities_df.to_csv('beautifulsoup_pandas.csv', header=0, index=False)
cities_yml = open("cities.txt", "w")
# cities_yml.write("""version: "2.0"
# nlu:
#   - lookup: products
#     examples: |\n
# """)

for name in cleaned_names:
    cities_yml.write(f"{name}\n")

print(cleaned_names)
