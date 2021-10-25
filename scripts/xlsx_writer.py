# import xlsxwriter module
import xlsxwriter
import intent_generation as ig

# Workbook() takes one, non-optional, argument
# which is the filename that we want to create.
workbook = xlsxwriter.Workbook('datasets/custom_data.xlsx')

# The workbook object is then used to add new
# worksheet via the add_worksheet() method.
worksheet = workbook.add_worksheet()

# Use the worksheet object to write
# data via the write() method.
worksheet.write('A1', 'text')
worksheet.write('B1', 'label')
row = 1
for intent in range(len(ig.clusters_intents)):
    if ig.clusters_intents[intent] == 'undefined':
        continue
    for sentence in range(len(ig.clusters_sentences[intent])):
        row += 1
        worksheet.write(
            'A' + str(row), ig.clusters_sentences[intent][sentence])
        worksheet.write('B' + str(row), ig.clusters_intents[intent])
# Finally, close the Excel file
# via the close() method.
workbook.close()


# corpus = ig.load_corpus(dataset_path=ig.dataset_path,
#                         max_corpus_size=ig.max_corpus_size)
# clusters_sentences = ig.find_clusters_sentences(corpus)
# clusters_intents = ig.extract_intents(clusters_sentences)
# print('sentences:', len(clusters_sentences))
# print('intents', len(clusters_intents))
# for i in range(len(clusters_intents)):
#     if clusters_intents[i] == 'undefined':
#         continue
#     for sentence in clusters_sentences[i]:
#         print(sentence, '|', clusters_intents[i], '\n')
