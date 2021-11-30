import os
import nlpcloud


client = nlpcloud.Client('gpt-j', os.getenv("NLPCLOUD_API_KEY"), True)
sample_text = 'John loves to skate.'


def get_entities(text):
    return client.entities(text)


def generate(text,
             length_no_input=True,
             end_sequence="\n###",
             remove_input=True):
    # return generation based on args
    return client.generation(
        text,
        length_no_input=length_no_input,
        end_sequence=end_sequence,
        remove_input=remove_input
    )
