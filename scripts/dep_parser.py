from spacy.symbols import nsubj, dobj, VERB
import spacy

# nlp = spacy.load("en_core_web_sm")
# doc = nlp("Autonomous cars shift insurance liability toward manufacturers")
# for chunk in doc.noun_chunks:
#     print(chunk.text, chunk.root.text, chunk.root.dep_,
#           chunk.root.head.text)
# for token in doc:
#     print(token.text, token.dep_, token.head.text, token.head.pos_,
#           [child for child in token.children])


nlp = spacy.load("en_core_web_sm")
doc = nlp("Autonomous cars shift insurance liability toward manufacturers")

# Finding a verb with a subject from below — good
# nouns = set()
# verbs = set()
action_object = set()
for possible_subject in doc:
    if possible_subject.dep == dobj and possible_subject.head.pos == VERB:
        # nouns.add(possible_subject.text)
        # verbs.add(possible_subject.head.text)
        action_object.add(possible_subject.head.text +
                          '-' + possible_subject.text)

# print(nouns)
# print(verbs)
print(action_object)
