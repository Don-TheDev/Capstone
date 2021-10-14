from numpy import iterable
import pandas as pd
import json

# data = pd.read_csv("got_scripts_breakdown.csv", sep=';')

# characterName = 'jon'

# filtered_data = data[data.Name == characterName]


# print(filtered_data)

with open("downloads/train.json") as f:
    tweetqa = json.load(f)

lines = ["""version: \"2.0\"

stories:
#tweetqa stories

"""]

for tweet in tweetqa:
    story = tweet["qid"]
    user = tweet["Question"]
    bot = tweet["Answer"][0]
    lines.append(f"""  - story: {story}
    steps:
      - user: '{user}'
      - bot: '{bot}'\n\n""")

f = open("bot/data/core/tweetqa.yml", "w", encoding="utf-8")
f.writelines(lines)

f.close()

# print(lines)
