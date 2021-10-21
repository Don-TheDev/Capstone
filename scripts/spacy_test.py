import spacy

spacy.prefer_gpu()
nlp = spacy.load("en_core_web_sm")

print(nlp.component_names)
