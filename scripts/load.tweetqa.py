import json
dataset_path = "datasets/tweetqa/TweetQA_data/train.json"

questions = []
answers = []
with open(dataset_path) as fileIn:
    data = json.load(fileIn)
    # for qa in data:
    #     questions.append(qa['Question'])
    #     answers.append(qa['Answer'])
    # for i in range(len(questions)):
    #     print(questions[i])
    #     print(answers[i])
