import csv
import urllib.parse

csv_file = open('ai_index.csv')
ai_index = csv.reader(csv_file)
urls = []
for ind in ai_index:
    ind_url = urllib.parse.quote(ind[0])
    urls.append([ind[0], 'https://ja.wikipedia.org/wiki/' + ind_url])

f = open('result.csv', 'w')

writer = csv.writer(f, lineterminator='\n')
writer.writerows(urls)

f.close()