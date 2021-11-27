import os
import openai

openai.api_key = os.getenv("OPENAI_API_KEY")

start_sequence = "\nAI:"
restart_sequence = "\nHuman: "

# prompt = "The following is a conversation with an AI assistant. The assistant is helpful, creative, clever, and very friendly.\n\nHuman: Hello, who are you?\nAI: I am an AI created by OpenAI. How can I help you today?\n"
prompt = "The AI is named Marilyn Monroe. Marilyn Monroe (/ˈmærəlɪn mʌnˈroʊ/; born Norma Jeane Mortenson; June 1, 1926 – August 4, 1962) was an American actress, model and singer. Famous for playing comedic \"blonde bombshell\" characters, she became one of the most popular sex symbols of the 1950s and early 1960s and was emblematic of the era's sexual revolution. She was a top-billed actress for only a decade, but her films grossed $200 million (equivalent to $2 billion in 2020) by the time of her death in 1962.[3] Long after her death, she continues to be a major icon of pop culture.[4] In 1999, the American Film Institute ranked Monroe sixth on its list of the greatest female screen legends from the Golden Age of Hollywood."
examples = "Human: Hello, who are you?\nAI: I am Marilyn Monroe.\nHuman: What do you do?\nAI: I'm an actor.\n"
additional_text = ""


def create_completion():
    return openai.Completion.create(
        engine="davinci",
        prompt="The following is a conversation with an AI assistant. The assistant is helpful, creative, clever, and very friendly.\n\nHuman: Hello, who are you?\nAI: I am an AI created by OpenAI. How can I help you today?\nHuman: ",
        temperature=0.9,
        max_tokens=150,
        top_p=1,
        frequency_penalty=0,
        presence_penalty=0.6,
        stop=["\n", " Human:", " AI:"]
    )


def create_completion_with_message(text):
    return openai.Completion.create(
        engine="davinci",
        prompt="The following is a conversation with an AI assistant. The assistant is helpful, creative, clever, and very friendly.\n\nHuman: Hello, who are you?\nAI: I am an AI created by OpenAI. How can I help you today?\nHuman: " + text + "\n",
        temperature=0.9,
        max_tokens=150,
        top_p=1,
        frequency_penalty=0,
        presence_penalty=0.6,
        stop=["\n", " Human:", " AI:"]
    )


def create_completion_with_full():
    # print(get_full_text())
    return openai.Completion.create(
        engine="davinci",
        prompt=get_full_text(),
        temperature=0.9,
        max_tokens=150,
        top_p=1,
        frequency_penalty=0,
        presence_penalty=0.6,
        stop=["\n", " Human:", " AI:"]
    )


def create_completion_with_examples():
    # print(get_full_text())
    return openai.Completion.create(
        engine="davinci",
        prompt=prompt + '\n\n' + examples,
        temperature=0.9,
        max_tokens=150,
        top_p=1,
        frequency_penalty=0,
        presence_penalty=0.6,
        stop=["\n", " Human:", " AI:"]
    )


def get_full_text():
    return prompt + '\n\n' + examples + '\n' + additional_text

# print(create_completion())
